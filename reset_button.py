import pigpio
from datetime import datetime

pi = pigpio.pi()

pi.set_mode(23, pigpio.INPUT)  # GPIO  4 as input

pi.set_glitch_filter(23, 100)


while True:
    pi.wait_for_edge(user_gpio=23, edge=pigpio.FALLING_EDGE, timeout=0)
    print("Rising edge detected")
    timer = datetime.now()

    if pi.wait_for_edge(23, pigpio.RISING_EDGE, 5.0):
        print("Falling edge detected")
        print(datetime.now() - timer)
    else:
        print("wait for falling edge timed out")
