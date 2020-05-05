import pigpio
import time
import os
from shutdown import Shutdown

shutdown = Shutdown()
pi = pigpio.pi()

PIN = 21

pi.set_mode(PIN, pigpio.INPUT)  # GPIO  4 as input
pi.set_pull_up_down(PIN, pigpio.PUD_UP)
pi.set_glitch_filter(PIN, 100)


timer = time.time()

print("Running")


def released_callback(gpio, level, tick):
    print("Button released")

    global timer
    time_elapsed = time.time() - timer
    print("Time elapsed:", time_elapsed)

    if 0.1 < time_elapsed <= 3:
        print("Updating shutdown_flag")
        shutdown.set_shutdown("shutdown_flag", True)
    elif 3 < time_elapsed <= 10:
        print("Terminating and restarting")
        os.system("pkill -f API.py; sleep 0.1; ./runonion")  # If all else fails...
    elif 10 < time_elapsed <= 20:
        print("Restarting Pi")
        try:
            shutdown.set_shutdown("shutdown_flag", "Pi Killed")
        except:
            pass
        os.system("sudo reboot now")

    global released
    released.cancel()

    global pressed
    pressed = pi.callback(PIN, pigpio.FALLING_EDGE, pressed_callback)


def pressed_callback(gpio, level, tick):
    print("Button pressed")

    global timer
    timer = time.time()

    global pressed
    pressed.cancel()

    global released
    released = pi.callback(PIN, pigpio.RISING_EDGE, released_callback)


pressed = pi.callback(PIN, pigpio.FALLING_EDGE, pressed_callback)


while True:
    time.sleep(0.1)
