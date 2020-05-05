import pigpio
import time


pi = pigpio.pi()

PIN = 21

pi.set_mode(PIN, pigpio.INPUT)  # GPIO  4 as input
pi.set_pull_up_down(PIN, pigpio.PUD_UP)
pi.set_glitch_filter(PIN, 100)


timer = time.time()


def pressed_callback(gpio, level, tick):
    print("Falling edge detected")

    global timer
    timer = time.time()


def unpressed_callback(gpio, level, tick):
    print("Rising edge detected")

    global timer
    print(timer - time.time())


falling = pi.callback(PIN, pigpio.FALLING_EDGE, pressed_callback)

rising = pi.callback(PIN, pigpio.RISING_EDGE, unpressed_callback)


while True:
    time.sleep(0.1)
