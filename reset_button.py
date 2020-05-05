import pigpio
import time
import os
from config import Shutdown

config = Shutdown()
pi = pigpio.pi()

PIN = 21

pi.set_mode(PIN, pigpio.INPUT)  # GPIO  4 as input
pi.set_pull_up_down(PIN, pigpio.PUD_UP)
pi.set_glitch_filter(PIN, 100000)


timer = time.time()


def pressed_callback(gpio, level, tick):
    print("Falling edge detected")

    global timer
    timer = time.time()


def unpressed_callback(gpio, level, tick):
    print("Rising edge detected")

    global timer
    time_elapsed = time.time() - timer

    if 0.2 < time_elapsed <= 3:
        config.set_config("shutdown_flag", True)
    elif 3 < time_elapsed <= 10:
        os.system("pkill -f API.py; sleep 0.1; ./runonion")  # If all else fails...
    elif 10 < time_elapsed <= 20:
        try:
            config.set_config("shutdown_flag", "Pi Killed")
        except:
            pass
        os.system("sudo reboot now")


falling = pi.callback(PIN, pigpio.FALLING_EDGE, pressed_callback)

rising = pi.callback(PIN, pigpio.RISING_EDGE, unpressed_callback)


while True:
    time.sleep(0.1)
