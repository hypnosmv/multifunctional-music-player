import time
import shared
import logging
import timeouts
import pins
import path
from clock import Clock

import spidev as SPI
from PIL import Image
from lib.LCD_1inch54 import LCD_1inch54

def sqlcd(shutdown_event):
    sqlcd = LCD_1inch54(
        spi=SPI.SpiDev(0, 1),
        rst=pins.LCD1INCH54_RST,
        dc=pins.LCD1INCH54_DC,
        bl=pins.LCD1INCH54_BL)

    sqlcd.Init()
    sqlcd.bl_DutyCycle(100)

    prev_track = None

    claim_clock = Clock(start_elapsed_time=timeouts.LOOP)
    iteration = 0
    iteration_count = 118

    while not shutdown_event.is_set():
        time.sleep(timeouts.SQLCD_REFRESH)

        if claim_clock.get_elapsed_time() >= timeouts.LOOP:
            with shared.current_track_lock:
                if shared.current_track != None and shared.current_track != prev_track:
                    image = Image.open(f'{path.IMAGE_DIR}/track_image{shared.current_track}.jpg')
                    sqlcd.ShowImage(image)
                prev_track = shared.current_track
            claim_clock.reset()

        if prev_track == None:
            image = Image.open(f'{path.IMAGE_DIR}/waiting/waiting_image{iteration + 1}.jpg')
            sqlcd.ShowImage(image)
            iteration = (iteration + 1) % iteration_count

    sqlcd.reset()
