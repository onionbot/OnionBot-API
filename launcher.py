import pigpio
from time import sleep, time
from os import system
from requests import post
import logging

FORMAT = "       %(levelname)-8s %(name)s %(process)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger("launcher")

pi = pigpio.pi()

PIN = 21

pi.set_mode(PIN, pigpio.INPUT)  # GPIO  4 as input
pi.set_pull_up_down(PIN, pigpio.PUD_UP)
pi.set_glitch_filter(PIN, 100)


timer = time()

logger.info("Onionbot launcher is ready.")


def released_callback(gpio, level, tick):
    logger.debug("Reset button released")

    global timer
    time_elapsed = time() - timer
    logger.debug("Time elapsed: %0.2f" % (time_elapsed))

    if 0.01 < time_elapsed <= 1.5:
        logger.info("Calling shutdown over API")
        try:
            post("http://192.168.0.70:5000/", data={"action": "quit"})
        except:
            logger.info("API is not/no longer alive")

    elif 1.5 < time_elapsed <= 5:
        system("pkill -f API.py;")  # If all else fails...
        sleep(1)
        logger.info("Starting Onionbot Software")
        system(". ~/onionbot/runonion &")

    elif 5 < time_elapsed <= 10:
        logger.info("Restarting Raspberry Pi")
        sleep(1)
        system("sudo reboot now")

    global released
    released.cancel()

    global pressed
    pressed = pi.callback(PIN, pigpio.FALLING_EDGE, pressed_callback)


def pressed_callback(gpio, level, tick):
    logger.debug("Reset button pressed")

    global timer
    timer = time()

    global pressed
    pressed.cancel()

    global released
    released = pi.callback(PIN, pigpio.RISING_EDGE, released_callback)


pressed = pi.callback(PIN, pigpio.FALLING_EDGE, pressed_callback)


while True:
    try:
        sleep(0.1)
    except KeyboardInterrupt:
        logger.info("Launcher quit succesfully")
