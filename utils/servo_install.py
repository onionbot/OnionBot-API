import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from servo import Servo
import time

servo = Servo()

_ = input("Remove servo assembly from hob body. Press enter to continue _")
print("Aligning servo...")
servo.rotate(350)
print("Rotate hob knob anticlockwise to 0, then rotate forward aprrox 10 degrees")
_ = input(" Press enter to continue _")
_ = input("Reattatch servo assembly to hob. Press enter to finish _")
