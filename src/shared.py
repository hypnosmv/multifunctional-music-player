import threading

def init():
    global current_track
    current_track = None
    global current_track_lock
    current_track_lock = threading.Lock()

    global card_data
    card_data = None
    global card_data_lock
    card_data_lock = threading.Lock()

    global stop_state
    stop_state = False
    global stop_state_lock
    stop_state_lock = threading.Lock()

    global mode_state
    mode_state = False
    global mode_state_lock
    mode_state_lock = threading.Lock()

    global play_progress
    play_progress = None
    global play_progress_lock
    play_progress_lock = threading.Lock()

    global play_duration
    play_duration = None
    global play_duration_lock
    play_duration_lock = threading.Lock()

    global local_volume
    local_volume = 0
    global local_volume_lock
    local_volume_lock = threading.Lock()

    global local_mode
    local_mode = True
    global local_mode_lock
    local_mode_lock = threading.Lock()

    global adb_message
    adb_message = None
    global adb_message_lock
    adb_message_lock = threading.Lock()
