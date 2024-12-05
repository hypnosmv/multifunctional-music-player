import time
import shared
import logging
import timeouts

from lib.MFRC522 import MFRC522

def rfid(shutdown_event):
    device = MFRC522()

    while not shutdown_event.is_set():
        time.sleep(timeouts.LOOP)

        (request_status, _) = device.MFRC522_Request(device.PICC_REQIDL)

        if request_status != device.MI_OK:
            logging.debug('No card detected')
            continue

        (anti_collision_status, uid) = device.MFRC522_Anticoll()

        if anti_collision_status != device.MI_OK:
            logging.warning('Card collision detected')
            continue

        device.MFRC522_SelectTag(uid)
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

        if device.MFRC522_Auth(device.PICC_AUTHENT1A, 1, key, uid) != device.MI_OK:
            logging.warning('Card authentication failed')
            continue

        data = device.MFRC522_Read(1)
        device.MFRC522_StopCrypto1()

        if data is None:
            logging.error('Card data corrupt')
            continue
        with shared.current_track_lock:
            with shared.card_data_lock:
                if shared.current_track == None:
                    shared.card_data = data[0]
                    logging.info(f'Card data read: {shared.card_data}')
