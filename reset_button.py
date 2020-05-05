import pigpio
from time import sleep, time
from os import system
from requests import post
import logging

spacer = "      "
FORMAT = "%(spacer)6d %(levelname)-8s %(name)s %(process)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

pi = pigpio.pi()

PIN = 21

pi.set_mode(PIN, pigpio.INPUT)  # GPIO  4 as input
pi.set_pull_up_down(PIN, pigpio.PUD_UP)
pi.set_glitch_filter(PIN, 100)


timer = time.time()

logger.info("Preparing Onionbot big red button listener...")


def released_callback(gpio, level, tick):
    logger.info("Reset button released")

    global timer
    time_elapsed = time.time() - timer
    logger.info("Time elapsed:", time_elapsed)

    if 0.01 < time_elapsed <= 3:
        logger.info("Calling shutdown over API")
        try:
            post("http://192.168.0.70:5000/", data={"action": "quit"})
            sleep(1)
        except ConnectionRefusedError:
            logger.info("API is not currently alive")

    elif 3 < time_elapsed <= 10:
        logger.info("Forcing termination...")
        system("pkill -f API.py;")  # If all else fails...
        sleep(1)
        logger.info("Restarting...")
        system("./runonion &")

    elif 10 < time_elapsed <= 20:
        logger.info("Restarting Raspberry Pi")
        sleep(1)
        system("sudo reboot now")

    global released
    released.cancel()

    global pressed
    pressed = pi.callback(PIN, pigpio.FALLING_EDGE, pressed_callback)


def pressed_callback(gpio, level, tick):
    logger.info("Reset button pressed")

    global timer
    timer = time.time()

    global pressed
    pressed.cancel()

    global released
    released = pi.callback(PIN, pigpio.RISING_EDGE, released_callback)


pressed = pi.callback(PIN, pigpio.FALLING_EDGE, pressed_callback)


while True:
    sleep(0.1)
