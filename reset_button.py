import pigpio
import time
import os
from requests import post

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

    if 0.01 < time_elapsed <= 3:
        print("Calling shutdown over API")
        try:
            post("http://192.168.0.70:5000/", data={"action": "quit"})
        except ConnectionRefusedError:
            print("API not running")
    elif 3 < time_elapsed <= 10:
        print("Terminating and restarting")
        os.system("pkill -f API.py;")  # If all else fails...
        time.sleep(1)
        os.system("./runonion &")
    elif 10 < time_elapsed <= 20:
        print("Restarting Pi")
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
