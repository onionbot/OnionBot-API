import logging
from threading import Thread, Event
from servo import Servo
from time import sleep

servo = Servo()


class Control(object):

    def __init__(self):

        self.quit_event = Event()

        self.control_setpoint = 0
        self.servo_setpoint = 0
        self.servo_actual = 0 

    def _worker(self):

        while True:

            self.servo_setpoint = servo.get_setpoint()
            self.servo_actual = servo.get_actual()

            servo.update_setpoint(self.control_setpoint)

            if self.quit_event.is_set():
                logging.debug("Quitting control thread...")
                break

            sleep(0.1)

    def launch(self):
        logging.debug("Initialising worker")
        Thread(target=self._worker)

    def quit(self):
        self.quit_event.set()

    def update_setpoint(self, target_setpoint):

        self.control_setpoint = target_setpoint

    def get_setpoint(self):

        return self.servo_setpoint

    def get_actual(self):

        return self.servo_actual

    def hob_off(self):

        return servo.hob_off()
