from servo import Servo

servo = Servo()

_ = input("Remove servo assembly from hob body. Press enter to continue _")
print("Aligning servo...")
servo.rotate(350)
print("Rotate hob knob anticlockwise to 0, then rotate forward aprrox 10 degrees")
_ = input(" Press enter to continue _")
_ = input("Reattatch servo assembly to hob. Press enter to finish _")
