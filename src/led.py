import time
import shared
import logging
import timeouts
import pins

from lib.Chip74HC595 import Chip74HC595

def clear_registers(chip1, chip2):
    chip1.write([0, 0, 0, 0, 0, 0, 0, 0])
    chip2.write([0, 0, 0, 0, 0, 0, 0, 0])

def led(shutdown_event):
    chip1 = Chip74HC595(ds=pins.FIRST_74HC595_DS, stcp=pins.FIRST_74HC595_STCP, shcp=pins.FIRST_74HC595_SHCP)
    chip2 = Chip74HC595(ds=pins.SECOND_74HC595_DS, stcp=pins.SECOND_74HC595_STCP, shcp=pins.SECOND_74HC595_SHCP)

    clear_registers(chip1, chip2)

    while not shutdown_event.is_set():
        time.sleep(timeouts.LOOP)

        data1 = [0, 0, 0, 0, 0, 0, 0, 0]
        data2 = [0, 0, 0, 0, 0, 0, 0, 0]

        with shared.local_mode_lock:
            if shared.local_mode == False:
                data1[3] = 1
            else:
                data1[4] = 1

        local_volume = 0
        with shared.local_volume_lock:
            local_volume = shared.local_volume

        if local_volume > 5:
            data1[5] = 1
        if local_volume > 15:
            data1[6] = 1
        if local_volume > 25:
            data1[7] = 1
        if local_volume > 35:
            data2[1] = 1
        if local_volume > 45:
            data2[2] = 1
        if local_volume > 55:
            data2[3] = 1
        if local_volume > 65:
            data2[4] = 1
        if local_volume > 75:
            data2[5] = 1
        if local_volume > 85:
            data2[6] = 1
        if local_volume > 95:
            data2[7] = 1

        chip1.write(data1)
        chip2.write(data2)

    clear_registers(chip1, chip2)
