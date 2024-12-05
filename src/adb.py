import time
import shared
import logging
import timeouts
import path
from clock import Clock

import os

class AdbController:
    def __init__(self):
        self.__push_destination = '/storage/emulated/0/Music/mmp'
        self.__ignore_all_output = '>/dev/null 2>&1'
        self.__ignore_stderr = '2>/dev/null'

    def is_connected(self):
        devices = os.popen(f'adb devices {self.__ignore_stderr} | tail -n +2').read()
        return devices.count('device') == 1

    def is_unlocked(self):
        state_string = 'mDreamingLockscreen='
        state = os.popen(f'adb shell dumpsys window {self.__ignore_stderr} | grep {state_string}').read()
        key_index = state.find(state_string)
        value_index = key_index + len(state_string)
        return key_index != - 1 and value_index < len(state) and state[value_index] == 'f'

    def push_files(self):
        os.system(f'adb shell "mkdir -p {self.__push_destination}"')
        for i in range(1, path.NUMBER_OF_TRACKS + 1):
            os.system(f'adb push {path.TRACK_DIR}/track{i}.mp3 {self.__push_destination} {self.__ignore_all_output}')
        os.system(f'adb push {path.ASSET_DIR}/adb_monitor.sh {self.__push_destination} {self.__ignore_all_output}')
        os.system(f'adb shell "nohup sh {self.__push_destination}/adb_monitor.sh {self.__ignore_all_output} &"')

    def notify(self):
        os.system(f'adb shell touch {self.__push_destination}/adb_notif {self.__ignore_all_output}')

    def play(self, file_name, start=0):
        start *= 1000
        os.system(f'adb shell am start -S -n org.videolan.vlc/.gui.video.VideoPlayerActivity\
                  -d "file://{self.__push_destination}/{file_name}" --ei position {start} {self.__ignore_all_output}')

    def is_active(self):
        state = os.popen(f'adb shell dumpsys media_session {self.__ignore_stderr}').read()
        state_string = 'state=PlaybackState {state='
        key_index = state.find(state_string, state.find('org.videolan.vlc/VLC'))
        value_index = key_index + len(state_string)
        return key_index == -1 or state[value_index] != '1'

    def pause(self):
        os.system(f'adb shell input keyevent 127 {self.__ignore_all_output}')
        time.sleep(timeouts.ADB_PAUSING)
        state = os.popen(f'adb shell dumpsys media_session {self.__ignore_stderr}').read()
        state_string = ', position='
        key_index = state.find(state_string, state.find('org.videolan.vlc/VLC'))
        value_index_begin = key_index + len(state_string)
        value_index_end = state.find(',', value_index_begin)
        try: return round(float(state[value_index_begin:value_index_end]) / 1000)
        except ValueError: logging.warning('Fetched incorrect media session information')
        return 0

    def stop(self):
        os.system(f'adb shell am force-stop org.videolan.vlc {self.__ignore_all_output}')

    def __del__(self):
        self.stop()

def adb(shutdown_event):
    adb_controller = AdbController()
    message_clock = Clock(start_elapsed_time=timeouts.ADB_MESSAGE)

    prev_connected_state = False
    prev_availability = False
    prev_mode_state = False

    while not shutdown_event.is_set():
        time.sleep(timeouts.LOOP)

        if adb_controller.is_connected() == True and prev_connected_state == False:
            adb_controller.push_files()
            logging.debug('Adb pushed files')
        prev_connected_state = adb_controller.is_connected()

        adb_available = adb_controller.is_connected() and adb_controller.is_unlocked()
        if adb_available: adb_controller.notify()

        message = None

        if adb_available == True and prev_availability == False:
            message = 'ADB AVAILABLE'
            logging.info('Adb device available')
        elif adb_available == False and prev_availability == True:
            message = 'ADB UNAVAILABLE'
            logging.info('Adb device unavailable')
        prev_availability = adb_available

        with shared.current_track_lock:
            with shared.mode_state_lock:
                with shared.local_mode_lock:
                    with shared.adb_message_lock:

                        if message_clock.get_elapsed_time() >= timeouts.ADB_MESSAGE:
                            shared.adb_message = None

                        if shared.mode_state != prev_mode_state:
                            if adb_available == True: shared.local_mode = not shared.local_mode
                            else: message = 'NO CONNECTION'
                            prev_mode_state = shared.mode_state

                        if adb_available == False and shared.local_mode == False:
                            shared.current_track = None
                            shared.local_mode = True
                            message = 'CONNECTION LOST'

                        if message != None:
                            shared.adb_message = message
                            message_clock.reset()
