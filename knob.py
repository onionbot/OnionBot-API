from threading import Thread, Event
import pigpio
import time
import lib_para_360_servo
import statistics

import logging

logger = logging.getLogger(__name__)

MIN_SAFE_ANGLE = 20
MAX_SAFE_ANGLE = 310

# OFF_ANGLE = 25
MIN_SET_POINT_ANGLE = 50
MAX_SET_POINT_ANGLE = 310

TIMEOUT_PERIOD = 2.5


class Knob(object):
    """ Wrapper for servo module to control hob temperature setting """

    def __init__(
        self,
        unitsFC=360,
        dcMin=31.85,
        dcMax=956.41,
        feedback_gpio=5,
        servo_gpio=13,
        min_pw=1280,  # 1210
        max_pw=1750,  # 1750
        min_speed=-1,
        max_speed=1,
        sampling_time=0.01,
        Kp_p=0.1,  # not too big values, otherwise output of position control would slow down too abrupt
        Ki_p=0.05,
        Kd_p=0.0,
        Kp_s=0.3,
        Ki_s=0,
        Kd_s=0,
    ):

        logger.info("Initialising servo motor")

        self.stop_event = Event()

        pi = pigpio.pi()

        self.pi = pi
        self.unitsFC = unitsFC
        self.dcMin = dcMin
        self.dcMax = dcMax
        self.sampling_time = sampling_time
        self.Kp_p = Kp_p
        self.Ki_p = Ki_p
        self.Kd_p = Kd_p
        self.Kp_s = Kp_s
        self.Ki_s = Ki_s
        self.Kd_s = Kd_s

        self.feedback = lib_para_360_servo.read_pwm(pi=self.pi, gpio=feedback_gpio)
        self.servo = lib_para_360_servo.write_pwm(
            pi=self.pi,
            gpio=servo_gpio,
            min_pw=min_pw,
            max_pw=max_pw,
            min_speed=min_speed,
            max_speed=max_speed,
        )

        self.target_setpoint = 0

    def _set_speed(self, speed):

        self.servo.set_speed(speed)

        return None

    def _worker(self, target_angle):

        #logger.debug("Starting thread")

        target_angle = float(target_angle)

        safe_target = max(min(target_angle, MAX_SAFE_ANGLE), MIN_SAFE_ANGLE)

        #logger.debug("Worker called with target %s " % (safe_target))

        target_angle = float(360 - target_angle)

        #  initial values sum_error_*
        sum_error_p = 0
        sum_error_s = 0

        #  initial values error_*_old
        error_p_old = 0
        error_s_old = 0

        reached_sp_counter = 0
        #  position must be reached for one second to allow
        #  overshoots/oscillations before stopping control loop
        wait_after_reach_sp = 1 / self.sampling_time

        #  start time of the control loop
        start_time = time.time()

        list_ticks = []

        #logger.debug("Starting while loop")

        while True:
            #  DEBUGGING OPTION:
            #  printing runtime of loop , see end of while true loop
            #  start_time_each_loop = time.time()

            angle = self.get_angle()

            #  #   Position Control
            #  Er = SP - PV
            error_p = target_angle - angle

            #  Deadband-Filter to remove ocillating forwards and backwards after reaching set-point
            if error_p <= 5 and error_p >= -5:
                error_p = 0

            #  I-Part
            sum_error_p += error_p
            #  try needed, because Ki_p can be zero
            try:
                #  limit I-Part to -1 and 1
                sum_error_p = max(min(1 / self.Ki_p, sum_error_p), -1 / self.Ki_p)
            except ZeroDivisionError:
                pass

            #  POSITION PID-Controller
            output_p = (
                self.Kp_p * error_p
                + self.Ki_p * self.sampling_time * sum_error_p
                + self.Kd_p / self.sampling_time * (error_p - error_p_old)
            )
            #  limit output of position control to speed range
            output_p = max(min(1, output_p), -1)

            error_p_old = error_p

            #  #   Speed Control
            #  full speed forward and backward = +-650 ticks/s
            output_p_con = 650 * output_p

            try:
                #  convert range output_p from -1 to 1 to ticks/s
                ticks = (angle - prev_angle) / self.sampling_time
            except NameError:
                prev_angle = angle
                continue

            #  ticks per second (ticks/s), calculated from a moving median window with 5 values
            list_ticks.append(ticks)
            list_ticks = list_ticks[-5:]
            ticks = statistics.median(list_ticks)

            #  Er = SP - PV
            error_s = output_p_con - ticks

            #  I-Part
            sum_error_s += error_s
            #  limit I-Part to -1 and 1

            #  try needed, because Ki_s can be zero
            try:
                sum_error_s = max(min(650 / self.Ki_s, sum_error_s), -650 / self.Ki_s)
            except ZeroDivisionError:
                pass

            #  SPEED PID-Controller
            output_s = (
                self.Kp_s * error_s
                + self.Ki_s * self.sampling_time * sum_error_s
                + self.Kd_s / self.sampling_time * (error_s - error_s_old)
            )

            error_s_old = error_s

            #  convert range output_s fom ticks/s to -1 to 1
            output_s_con = output_s / 650
            self._set_speed(output_s_con)

            prev_angle = angle

            if error_p == 0:
                reached_sp_counter += 1

                if reached_sp_counter >= wait_after_reach_sp:
                    self._set_speed(0.0)
                    self.stop_event.set()
                    #logger.debug("At position")
                elif time.time() - start_time >= TIMEOUT_PERIOD:
                    self._set_speed(0.0)
                    self.stop_event.set()
                    #logger.debug("Timed out, position not reached")

            if self.stop_event.is_set():
                #logger.debug("Thread closing")
                break

            #  Pause control loop for chosen sample time
            time.sleep(
                self.sampling_time - ((time.time() - start_time) % self.sampling_time)
            )

    #  angular position in units full circle
    def get_angle(self):

        try:
            angle = (
                (self.feedback.read() - self.dcMin)
                * self.unitsFC
                / (self.dcMax - self.dcMin + 1)
            )
        except TypeError:
            raise TypeError("Could not calculate angle. Servo may not be connected.")

        angle = max(min((self.unitsFC - 1), angle), 0)

        return angle

    def update_setpoint(self, target_setpoint):
        self.stop_event.set()

        target_setpoint = float(target_setpoint)
        target_setpoint = max(min(target_setpoint, 100), 0)
        self.target_setpoint = target_setpoint
        angle_range = MAX_SET_POINT_ANGLE - MIN_SET_POINT_ANGLE
        target_angle = (target_setpoint * 0.01 * angle_range) + MIN_SET_POINT_ANGLE

        try:  # Handle no thread running
            self.thread.join(timeout=1)
            if self.thread.is_alive():
                raise RuntimeError("Knob thread failed to quit")
        except AttributeError:
            logger.debug("No thread to join")

        #logger.debug("Initialising worker with target_angle %s " % (target_angle))
        self.stop_event.clear()
        self.thread = Thread(target=self._worker, args=(target_angle,), daemon=True)
        self.thread.start()

    def get_setpoint(self):

        return self.target_setpoint

    def get_achieved(self):

        window = []

        for _ in range(5):
            achieved_angle = self.get_angle()
            time.sleep(0.001)
            window.append(achieved_angle)

        # Calculate centered average to eliminate noise spikes
        achieved_angle = (sum(window) - max(window) - min(window)) / (len(window) - 2)
        angle_range = MAX_SET_POINT_ANGLE - MIN_SET_POINT_ANGLE
        normalised = (100 * (achieved_angle - MIN_SET_POINT_ANGLE)) / angle_range

        return 100 - round(normalised)

    def quit(self):
        self.update_setpoint(0)
        time.sleep(1)
        self._set_speed(0)
        self.stop_event.set()
        self.thread.join(timeout=1)
        if self.thread.is_alive():
            logger.error("Knob thread failed to quit")
