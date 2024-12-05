import logging

def init(log_level):
    global LOOP
    LOOP = 0.05 if logging.getLevelNamesMapping()[log_level] >= logging.DEBUG else 0.1

    global BUTTON
    BUTTON = 2.0

    global SILCD_INIT
    SILCD_INIT = 2.0

    global SILCD_REFRESH
    SILCD_REFRESH = 0.2

    global SQLCD_REFRESH
    SQLCD_REFRESH = 0.02

    global ADB_PAUSING
    ADB_PAUSING = 0.5

    global ADB_MESSAGE
    ADB_MESSAGE = 2.0
