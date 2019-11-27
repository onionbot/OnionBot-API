import pigpio
import time
import lib_motion
import random

pi = pigpio.pi()

s = lib_motion.control(pi)

try:
    while True:
        #x =random.randint(0,360)
        #x = 0
        x = input("Type angle")
        time.sleep(2)
        s.rotate(float(x))
        

    
    s.cancel()
except KeyboardInterrupt:
    s.cancel()
