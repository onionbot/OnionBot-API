import pigpio
from datetime import datetime

pi = pigpio.pi()

PIN = 21

pi.set_mode(PIN, pigpio.INPUT)  # GPIO  4 as input
pi.set_pull_up_down(PIN, pigpio.PUD_UP)
pi.set_glitch_filter(PIN, 100)


timer = datetime.now()


def pressed_callback(gpio, level, tick):
    print("Falling edge detected")

    global timer
    timer = datetime.now()


def unpressed_callback(gpio, level, tick):
    print("Rising edge detected")

    global timer
    print(timer - datetime.now())


falling = pi.callback(PIN, pigpio.FALLING_EDGE, pressed_callback)

rising = pi.callback(PIN, pigpio.RISING_EDGE, unpressed_callback)
