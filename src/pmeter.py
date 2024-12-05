import time
import shared
import logging
import timeouts

from lib.ADCDevice import ADCDevice, ADS7830
import subprocess
import sys

def pmeter(shutdown_event):
    device = ADCDevice()

    if device.detectI2C(0x4b):
        device = ADS7830()
        logging.debug('Device detected')

    prev_local_volume = sys.maxsize

    while not shutdown_event.is_set():
        time.sleep(timeouts.LOOP)

        local_volume = 100 - round(device.analogRead(0) / 2.54)

        if 0 <= local_volume <= 100 and abs(local_volume - prev_local_volume) > 1:
            logging.debug(f'Setting local volume to: {local_volume}%')

            try:
                subprocess.run(['amixer', 'set', 'Master', f'{local_volume}%'],
                               check=True,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)

                prev_local_volume = local_volume
            except FileNotFoundError:
                logging.critical('Amixer not found')
                break

        with shared.local_volume_lock:
            shared.local_volume = local_volume

    device.close()
