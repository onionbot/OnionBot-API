from threading import Thread, Event
from servo import Servo
from time import sleep
from collections import deque


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

        self.setpoint_history = deque([0] * 120)
        self.actual_history = deque([0] * 120)

    def _worker(self):

        while True:
            logger.debug("Getting data from servo module")

            logger.debug("Calling servo update_setpoint with %s " % (self.control_setpoint))
            servo.update_setpoint(self.control_setpoint)

            if self.quit_event.is_set():
                logger.debug("Quitting control thread...")
                break

            sleep(0.1)

    def launch(self):
        logger.debug("Initialising worker")
        self.thread = Thread(target=self._worker)
        self.thread.start()

    def quit(self):
        self.quit_event.set()
        self.thread.join(timeout=1)

    def update_setpoint(self, target_setpoint):
        logger.debug("Updating setpoint flag to %s " % (target_setpoint))

        self.control_setpoint = target_setpoint

    def get_setpoint(self):
        setpoint = servo.get_setpoint()
        logger.debug("Servo get_setpoint returned %s " % (setpoint))

        history = self.setpoint_history
        history.append(setpoint)
        history.popleft()
        self.setpoint_history = history

        return setpoint

    def get_setpoint_history(self):
        """NOTE: Relies on get_setpoint function only being called once per frame"""
        logger.debug("get_setpoint_history called")

        return self.setpoint_history

    def get_actual(self):

        actual = servo.get_actual()
        logger.debug("Servo get_actual returned %s " % (actual))

        history = self.actual_history
        history.append(actual)
        history.popleft()
        self.actual_history = history

        return actual

    def get_actual_history(self):
        """NOTE: Relies on get_actual function only being called once per frame"""

        logger.debug("get_actual_history called")

        return self.actual_history

    def hob_off(self):
        logger.debug("hob_off called")

        self.control_setpoint = 0

