from threading import Thread, Event
from servo import Servo
from time import sleep

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

servo = Servo()


class Control(object):

    def __init__(self):

        self.quit_event = Event()

        self.control_setpoint = 0
        self.servo_setpoint = 0
        self.servo_actual = 0 

    def _worker(self):

        while True:
            logger.debug("Getting data from servo module")

            self.servo_setpoint = servo.get_setpoint()
            logger.debug("Servo get_setpoint returned %s " % (self.servo_setpoint))

            self.servo_actual = servo.get_actual()
            logger.debug("Servo get_actual returned %s " % (self.servo_actual))

            logger.debug("Calling servo update_setpoint with %s " % (self.control_setpoint))
            servo.update_setpoint(self.control_setpoint)

            if self.quit_event.is_set():
                logger.debug("Quitting control thread...")
                break

            sleep(0.1)

    def launch(self):
        logger.debug("Initialising worker")
        t = Thread(target=self._worker)
        t.start()

    def quit(self):
        self.quit_event.set()

    def update_setpoint(self, target_setpoint):
        logger.debug("Updating setpoint flag to" % (target_setpoint))

        self.control_setpoint = target_setpoint

    def get_setpoint(self):
        logger.debug("get_setpoint called")

        return self.servo_setpoint

    def get_actual(self):
        logger.debug("get_actual called")

        return self.servo_actual

    def hob_off(self):
        logger.debug("hob_off called")

        return servo.hob_off()
