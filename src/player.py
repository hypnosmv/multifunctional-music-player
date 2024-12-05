import time
import shared
import logging
import timeouts
import path
from adb import AdbController

from mutagen.mp3 import MP3
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

def player(shutdown_event):
    pygame.mixer.init()
    adb_controller = AdbController()

    track_file_name = None
    local_track_path = None
    playback_offset = 0
    prev_current_track = None
    prev_local_mode = True

    while not shutdown_event.is_set():
        time.sleep(timeouts.LOOP)

        with shared.current_track_lock:
            with shared.play_progress_lock:
                with shared.play_duration_lock:
                    with shared.local_mode_lock:

                        if shared.local_mode != prev_local_mode and shared.play_progress != None:
                            if shared.local_mode == False:
                                shared.play_progress = playback_offset + int(pygame.mixer.music.get_pos() / 1000)
                                pygame.mixer.music.stop()
                                adb_controller.play(track_file_name, shared.play_progress)
                            else:
                                shared.play_progress = adb_controller.pause()
                                playback_offset = shared.play_progress
                                pygame.mixer.music.load(local_track_path)
                                pygame.mixer.music.play(start=shared.play_progress)

                            prev_local_mode = shared.local_mode

                        if shared.current_track != prev_current_track:
                            playback_offset = 0

                            if shared.current_track != None:
                                track_file_name = f'track{shared.current_track}.mp3'
                                local_track_path = f'{path.TRACK_DIR}/{track_file_name}'
                                shared.play_progress = 0
                                shared.play_duration = int(MP3(local_track_path).info.length)

                                if shared.local_mode == True:
                                    pygame.mixer.music.load(local_track_path)
                                    pygame.mixer.music.play()
                                else:
                                    adb_controller.play(track_file_name)
                            else:
                                track_file_name = None
                                local_track_path = None
                                shared.play_progress = None
                                shared.play_duration = None

                                if shared.local_mode == True:
                                    pygame.mixer.music.stop()
                                else:
                                    adb_controller.stop()

                            prev_current_track = shared.current_track

                        if pygame.mixer.music.get_busy():
                            shared.play_progress = playback_offset + int(pygame.mixer.music.get_pos() / 1000)
                        elif shared.local_mode == True or adb_controller.is_active() == False:
                            shared.play_progress = None
                            shared.play_duration = None
