import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from servo import Servo
import time

servo = Servo()

while True:
    print(360 - float(servo.get_angle()))
    time.sleep(.1)
