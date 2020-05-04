from threading import Thread, Event
from knob import Knob
from time import sleep
from collections import deque

from pid import PID

import logging

logger = logging.getLogger(__name__)

knob = Knob()
pid = PID(
    Kp=1.0,
    Ki=0.0,
    Kd=0.0,
    setpoint=0,
    sample_time=0.01,
    output_limits=(0, 100),
    is_enabled=False,
    proportional_on_measurement=False,
)

DEADBAND_THRESHOLD = 5


class Control(object):
    def __init__(self):

        logger.info("Initialising control script")

        self.quit_event = Event()

        self.control_setpoint = 0
        self.servo_setpoint = 0
        self.servo_achieved = 0

        self.setpoint_history = deque([0] * 120)
        self.achieved_history = deque([0] * 120)

        self.data = {
            "servo_setpoint": None,
            "servo_setpoint_history": None,
            "servo_achieved": None,
            "servo_achieved_history": None,
        }

    def _worker(self):

        while True:
            logger.debug(
                "Calling servo update_setpoint with %s " % (self.control_setpoint)
            )

            delta = abs(float(self.control_setpoint) - knob.get_achieved())
            logger.debug("Servo setpoint delta: {:.1f}".format(delta))

            if delta >= DEADBAND_THRESHOLD:
                knob.update_setpoint(self.control_setpoint)

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
        knob.quit()
        self.thread.join(timeout=1)

    def update_setpoint(self, target_setpoint):
        logger.debug("Updating setpoint flag to %s " % (target_setpoint))

        self.control_setpoint = target_setpoint

    def refresh(self):
        """NOTE: Must be called only ONCE per frame for history to stay in sync with thermal"""
        logger.debug("Refresh called")

        setpoint = knob.get_setpoint()
        logger.debug("Servo get_setpoint returned %s " % (setpoint))

        setpoint_history = self.setpoint_history
        setpoint_history.append(setpoint)
        setpoint_history.popleft()
        self.setpoint_history = setpoint_history

        achieved = knob.get_achieved()
        logger.debug("Servo get_achieved returned %s " % (achieved))

        achieved_history = self.achieved_history
        achieved_history.append(achieved)
        achieved_history.popleft()
        self.achieved_history = achieved_history

        self.data = {
            "servo_setpoint": setpoint,
            "servo_setpoint_history": list(setpoint_history),
            "servo_achieved": achieved,
            "servo_achieved_history": list(achieved_history),
        }

    def hob_off(self):
        logger.debug("hob_off called")

        self.control_setpoint = 0

    def set_pid_enabled(self, enabled):

        pid.set_is_enabled(enabled, last_output=self.control_setpoint)

    def set_pid_coefficients(self, coefficients):

        pid.coefficients(coefficients)

    def set_pid_reset(self):

        pid.reset()
