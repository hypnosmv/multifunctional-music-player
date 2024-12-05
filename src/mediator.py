import time
import shared
import logging
import timeouts

def mediator(shutdown_event):
    prev_stop_state = False

    while not shutdown_event.is_set():
        time.sleep(timeouts.LOOP)

        with shared.current_track_lock:
            with shared.card_data_lock:
                with shared.stop_state_lock:
                    with shared.play_progress_lock:

                        if shared.stop_state != prev_stop_state:
                            shared.current_track = None
                            prev_stop_state = shared.stop_state

                        if shared.play_progress == None:
                            shared.current_track = shared.card_data
                        else:
                            shared.card_data = None

                        logging.debug(f'Current track: {shared.current_track}')
