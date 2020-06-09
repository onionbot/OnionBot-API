from servo import Servo
import time

servo = Servo()

while True:
    x = float(input("Type setpoint: "))
    servo.update_setpoint(x)
    time.sleep(.1)
