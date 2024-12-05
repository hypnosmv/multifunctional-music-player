#!/usr/bin/env python3
from gpiozero import LED

class Chip74HC595:
    def __init__(self, ds: int, stcp: int, shcp: int):
        self._ds = LED(pin=ds)
        self._shcp = LED(pin=shcp)
        self._stcp = LED(pin=stcp)
        self.BITS = 8

    def write(self, data: list[int]):
        self._shcp.on()
        self._stcp.on()
        for i in reversed(range(self.BITS)):
            if data[i] == True:
                self._ds.on()
            else:
                self._ds.off()
            self._shift_bit()
        self._send_data()

    def _shift_bit(self):
        self._shcp.off()
        self._shcp.on()

    def _send_data(self):
        self._stcp.off()
        self._stcp.on()

    def __del__(self):
        self._ds.close()
        self._shcp.close()
        self._stcp.close()
