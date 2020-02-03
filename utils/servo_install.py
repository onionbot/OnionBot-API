import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from actuation import Servo
import time

servo = Servo()

_ = input("Remove servo assembly from hob body. Press enter to continue ")
print("Aligning servo...")
servo.rotate(350)
_ = input("Rotate hob knob anticlockwise to extreme point. Press enter to continue ")
_ = input("Reattatch servo assembly to hob. Press enter to finish ")
