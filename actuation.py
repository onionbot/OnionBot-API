import pigpio
from parallax_feedback_360 import lib_motion # Manufacturer provided servo contro module

class Servo (object):
    """ Wrapper for servo module to control hob temperature setting """
    def __init__(self):

        pi = pigpio.pi()

        self.servo = lib_motion.control(pi)


    def move(self, angle):
        self.servo.rotate(float(angle))