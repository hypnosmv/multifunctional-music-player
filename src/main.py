import time
import shared
import logging
import timeouts
import argparse
import threading
import coloredlogs

from adb import adb
from led import led
from rfid import rfid
from sqlcd import sqlcd
from silcd import silcd
from button import button
from pmeter import pmeter
from player import player
from mediator import mediator

def main(log_level):
    logging.getLogger('PIL').setLevel(logging.WARNING)
    coloredlogs.install(level=log_level,
                        fmt='[%(asctime)s-%(levelname)s-%(funcName)s] %(message)s',
                        datefmt='%H:%M:%S',
                        level_styles={'debug': {'color': 'blue'},
                                      'info': {'color': 'green'},
                                      'warning': {'color': 'yellow'},
                                      'error': {'color': 'magenta'},
                                      'critical': {'color': 'red'}},
                        field_styles={'asctime': {'color': 'white'},
                                      'levelname': {'color': 'white'},
                                      'funcName': {'color': 'white'}})

    shared.init()
    timeouts.init(log_level)

    shutdown_event = threading.Event()

    workers = [adb, led, rfid, sqlcd, silcd, button, pmeter, player, mediator]
    threads = []

    for worker in workers:
        threads.append(threading.Thread(target=worker, args=(shutdown_event,)))
        threads[-1].start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info('Shutting down')
        shutdown_event.set()

        for thread in threads:
            thread.join()

        logging.info('All threads terminated')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multifunctional Music Player')
    parser.add_argument('--log-level', default='INFO', help='set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    args = parser.parse_args()
    main(args.log_level.upper())
