from threading import Thread, Event
from knob import Knob
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

        self.fixed_setpoint = 0
        self.temperature_target = None
        self.servo_setpoint = 0
        self.servo_achieved = 0

        self.setpoint_history = deque([0] * 120)
        self.achieved_history = deque([0] * 120)

        self.data = {
            "servo_setpoint": None,
            "servo_setpoint_history": None,
            "servo_achieved": None,
            "servo_achieved_history": None,
            "temperature_target": None,
            "p_coefficient": None,
            "i_coefficient": None,
            "d_coefficient": None,
        }

    def _worker(self):

        while True:

            current_setpoint = knob.get_achieved()

            if pid.is_enabled:
                pid.setpoint = self.temperature_target
                target_setpoint = pid(current_setpoint)
            else:
                target_setpoint = self.fixed_setpoint

            delta = abs(target_setpoint - current_setpoint)
            logger.debug("Servo setpoint delta: {:.1f}".format(delta))

            if delta >= DEADBAND_THRESHOLD:
                knob.update_setpoint(target_setpoint)

            if self.quit_event.is_set():
                logger.debug("Quitting control thread...")
                break

    def launch(self):
        logger.debug("Initialising worker")
        self.thread = Thread(target=self._worker)
        self.thread.start()

    def update_fixed_setpoint(self, setpoint):
        logger.debug("Updating fixed setpoint to %s/100 " % (setpoint))
        self.fixed_setpoint = float(setpoint)
        self.set_pid_enabled(False)
        self.temperature_target = None

    def hob_off(self):
        logger.debug("hob_off called")
        self.update_fixed_setpoint(0)

    def update_temperature_target(self, setpoint):
        logger.debug("Updating self.temperature_target to %s degrees " % (setpoint))
        self.temperature_target = float(setpoint)
        self.set_pid_enabled(True)
        self.fixed_setpoint = None

    def set_pid_enabled(self, enabled):
        pid.set_is_enabled(enabled, last_output=knob.get_setpoint())

    def set_pid_coefficients(self, coefficients):
        pid.coefficients(coefficients)

    def set_pid_reset(self):
        pid.reset()

    # Create update_angle_setpoint separate to temp setpoint

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

        coefficients = pid.coefficients
        logger.info(coefficients)

        self.data = {
            "servo_setpoint": setpoint,
            "servo_setpoint_history": list(setpoint_history),
            "servo_achieved": achieved,
            "servo_achieved_history": list(achieved_history),
            "temperature_target": self.temperature_target,
            "p_coefficient": coefficients[0],
            "i_coefficient": coefficients[1],
            "d_coefficient": coefficients[2],
        }

    def quit(self):
        self.quit_event.set()
        knob.quit()
        self.thread.join(timeout=1)
