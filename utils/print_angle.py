from servo import Servo
import time

import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

servo = Servo()

while True:
    print(360 - float(servo.get_angle()))
    time.sleep(.1)
