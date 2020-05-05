import pigpio
from datetime import datetime

pi = pigpio.pi()

PIN = 23

pi.set_mode(PIN, pigpio.INPUT)  # GPIO  4 as input
pi.set_pull_up_down(PIN, pigpio.PUD_UP)
pi.set_glitch_filter(PIN, 100)


while True:
    pi.wait_for_edge(user_gpio=PIN, edge=pigpio.FALLING_EDGE, wait_timeout=0)
    print("Rising edge detected")
    timer = datetime.now()

    if pi.wait_for_edge(PIN, pigpio.RISING_EDGE, 5.0):
        print("Falling edge detected")
        print(datetime.now() - timer)
    else:
        print("wait for falling edge timed out")
