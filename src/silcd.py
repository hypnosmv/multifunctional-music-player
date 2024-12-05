import time
import shared
import logging
import timeouts
import path
from clock import Clock

from lib.LCD1602 import CharLCD1602

def extract_16(text, index):
    result = text[index:index+16]
    return (result + text[:16-len(result)])[:16]

def silcd(shutdown_event):
    device = CharLCD1602()
    device.init_lcd()
    device.clear()

    prev_track = None
    description = None
    play_duration = None

    init_clock = Clock()
    refresh_clock = Clock()
    top_text = ''
    bottom_text = ''
    iteration = 0
    iteration_count = None

    while not shutdown_event.is_set():
        time.sleep(timeouts.LOOP)

        with shared.current_track_lock:
            with shared.play_duration_lock:

                if shared.current_track != prev_track:
                    view_changed = False
                    if shared.current_track != None:
                        if shared.play_duration != None:
                            with open(f'{path.DESCS_DIR}/track_desc{shared.current_track}.txt') as f:
                                description = f.readline().strip('\n') + ' ' * 5
                            play_duration = shared.play_duration
                            init_clock.reset()
                            view_changed = True
                    else:
                        description = None
                        view_changed = True

                    if view_changed == True:
                        prev_track = shared.current_track
                        iteration = 0

        if description != None:
            top_text = extract_16(description, iteration)

            progress_str = '00:00'
            with shared.play_progress_lock:
                if shared.play_progress != None:
                    progress_str = time.strftime('%M:%S', time.gmtime(shared.play_progress))
            duration_str = time.strftime('%M:%S', time.gmtime(play_duration))
            bottom_text = f'{progress_str}/{duration_str}'.rjust(16)

            if init_clock.get_elapsed_time() <= timeouts.SILCD_INIT: iteration_count = 1
            else: iteration_count = len(description)
        else:
            top_text = f"Waiting{'.' * (iteration + 1)}".ljust(16)
            bottom_text = ' ' * 16
            iteration_count = 3

        with shared.adb_message_lock:
            if shared.adb_message != None:
                bottom_text = shared.adb_message.ljust(16)

        if refresh_clock.get_elapsed_time() >= timeouts.SILCD_REFRESH:
            device.write(0, 0, top_text)
            device.write(0, 1, bottom_text)
            iteration = (iteration + 1) % iteration_count
            refresh_clock.reset()

    device.clear()
