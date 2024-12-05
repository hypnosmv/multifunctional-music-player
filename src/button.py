import time
import shared
import logging
import timeouts
import pins
from clock import Clock

from gpiozero import Button

def button(shutdown_event):
    buttons = {'stop': {'device': Button(pins.FIRST_BUTTON_PIN),
                        'clock': Clock(start_elapsed_time=timeouts.BUTTON),
                        'state': 'stop_state',
                        'state_lock': 'stop_state_lock'},
               'mode': {'device': Button(pins.SECOND_BUTTON_PIN),
                        'clock': Clock(start_elapsed_time=timeouts.BUTTON),
                        'state': 'mode_state',
                        'state_lock': 'mode_state_lock'}}

    while not shutdown_event.is_set():
        time.sleep(timeouts.LOOP)

        for (button, values) in buttons.items():
            if values['device'].is_pressed and values['clock'].get_elapsed_time() > timeouts.BUTTON:
                logging.info(f'{button.capitalize()} button pressed')

                with getattr(shared, values['state_lock']):
                    setattr(shared, values['state'], not getattr(shared, values['state']))
                values['clock'].reset()
