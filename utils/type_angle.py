import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from servo import Servo
import time

servo = Servo()

while True:
    x = float(input("Type angle: "))
    servo.safe_rotate(x)
    time.sleep(.1)
