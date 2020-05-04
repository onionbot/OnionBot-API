from threading import Thread, Event
from servo import Servo
from time import sleep
from collections import deque


import logging

logger = logging.getLogger(__name__)

servo = Servo()

DEADBAND_THRESHOLD = 5


class Control(object):
    def __init__(self):

        self.quit_event = Event()

        self.control_setpoint = 0
        self.servo_setpoint = 0
        self.servo_actual = 0

        self.setpoint_history = deque([0] * 120)
        self.actual_history = deque([0] * 120)

        self.data = {
            "servo_setpoint": None,
            "servo_setpoint_history": None,
            "servo_actual": None,
            "servo_actual_history": None,
        }

    def _worker(self):

        while True:
            logger.debug("Getting data from servo module")

            logger.debug(
                "Calling servo update_setpoint with %s " % (self.control_setpoint)
            )

            delta = abs(self.control_setpoint - servo.get_actual())
            logger.info("Servo setpoint delta: {:.1f}".format(delta))

            if delta >= DEADBAND_THRESHOLD:
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

    def refresh(self):
        """NOTE: Must be called only ONCE per frame for history to stay in sync with thermal"""
        logger.debug("Refresh called")

        setpoint = servo.get_setpoint()
        logger.debug("Servo get_setpoint returned %s " % (setpoint))

        setpoint_history = self.setpoint_history
        setpoint_history.append(setpoint)
        setpoint_history.popleft()
        self.setpoint_history = setpoint_history

        actual = servo.get_actual()
        logger.debug("Servo get_actual returned %s " % (actual))

        actual_history = self.actual_history
        actual_history.append(actual)
        actual_history.popleft()
        self.actual_history = actual_history

        self.data = {
            "servo_setpoint": setpoint,
            "servo_setpoint_history": list(setpoint_history),
            "servo_actual": actual,
            "servo_actual_history": list(actual_history),
        }

    def hob_off(self):
        logger.debug("hob_off called")

        self.control_setpoint = 0
