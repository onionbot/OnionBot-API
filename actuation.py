import pigpio
from parallax_feedback_360 import lib_motion # Manufacturer provided servo contro module
import time

class Servo (object):
    """ Wrapper for servo module to control hob temperature setting """
    def __init__(self):

        pi = pigpio.pi()

        self.servo = lib_motion.control(pi)


    def __init__(
        self, 
        pi, 
        unitsFC = 360,
        dcMin = 30.94, 
        dcMax = 956.41,
        wheel_gpio = 14,
        servo_gpio = 18, 
        min_pw = 1210, 
        max_pw = 1750, 
        min_speed = -1, 
        max_speed = 1,
        sampling_time = 0.01,
        Kp_p = 0.1, #not too big values, otherwise output of position control would slow down too abrupt
        Ki_p = 0.1,
        Kd_p = 0,
        Kp_s = 0.4,
        Ki_s = 0,
        Kd_s = 0):
        
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

        self.wheel = lib_para_360_servo.read_pwm(pi = self.pi, gpio = wheel_gpio)
        self.servo = lib_para_360_servo.write_pwm(pi = self.pi, gpio = servo_gpio, min_pw = min_pw, max_pw = max_pw, min_speed = min_speed, max_speed = max_speed)

        #needed time for initializing the four instances
        time.sleep(1)


    def set_speed(self, speed):

        self.servo.set_speed(speed)

        return None


    #angular position in units full circle
    def get_angle(self):

        #driving forward will increase the angle
        
        angle = (self.wheel.read() - self.dcMin) * self.unitsFC / (self.dcMax - self.dcMin + 1)

        angle = max(min((self.unitsFC - 1), angle), 0)

        return angle



    def rotate(self, target_angle):

        #initial values sum_error_*
        sum_error_p = 0
        sum_error_s = 0
        
        #initial values error_*_old
        error_p_old = 0
        error_s_old = 0

        position_reached = False
        reached_sp_counter = 0
        #position must be reached for one second to allow
        #overshoots/oscillations before stopping control loop
        wait_after_reach_sp = 1/self.sampling_time

        #start time of the control loop
        start_time = time.time()

        list_ticks = []

        #control loop:
        while not position_reached:
            #DEBUGGING OPTION:
            #printing runtime of loop , see end of while true loop
            #start_time_each_loop = time.time()

            angle = self.get_angle()

            #try needed, because:
            #- first iteration of the while loop prev_angle_* is missing

            try:
                #### cascade control

                ## Position Control
                #Er = SP - PV
                error_p = target_angle - angle

                #Deadband-Filter to remove ocillating forwards and backwards after reaching set-point
                if error_p <= 5 and error_p >= -5:
                    error_p = 0

                #I-Part
                sum_error_p += error_p
                #limit I-Part to -1 and 1 
                #try needed, because Ki_p can be zero
                try:
                    sum_error_p = max(min(1/self.Ki_p, sum_error_p), -1/self.Ki_p)
                except ZeroDivisionError:
                    pass

                #POSITION PID-Controller
                output_p = self.Kp_p * error_p + self.Ki_p * self.sampling_time * sum_error_p + self.Kd_p / self.sampling_time * (error_p - error_p_old)
                #limit output of position control to speed range
                output_p = max(min(1, output_p), -1)

                error_p_old = error_p

                ## Speed Control
                #convert range output_p from -1 to 1 to ticks/s
                #full speed of a wheel forward and backward = +-650 ticks/s
                output_p_con = 650 * output_p
                #ticks per second (ticks/s), calculated from a moving median window with 5 values
                ticks = (angle - prev_angle) / self.sampling_time
                list_ticks.append(ticks)
                list_ticks = list_ticks[-5:]
                ticks = statistics.median(list_ticks)
                
                #Er = SP - PV
                error_s = output_p_con - ticks

                #I-Part
                sum_error_s += error_s
                #limit I-Part to -1 and 1
                #try needed, because Ki_s can be zero
                try:
                    sum_error_s = max(min(650/self.Ki_s, sum_error_s), -650/self.Ki_s)
                except ZeroDivisionError:
                    pass

                #SPEED PID-Controller
                output_s = self.Kp_s * error_s + self.Ki_s * self.sampling_time * sum_error_s + self.Kd_s / self.sampling_time * (error_s - error_s_old)

                error_s_old = error_s

                #convert range output_s fom ticks/s to -1 to 1
                output_s_con = output_s / 650

                self.set_speed(output_s_con)


            except NameError:
                pass

            prev_angle = angle

            #try needed, because first iteration of the while loop prev_angle_* is
            #missing and the method self.get_total_angle() will throw an exception,
            #and therefore no total_angle_* gets calculated

            try:
                if error_p == 0:
                    reached_sp_counter += 1

                    if reached_sp_counter >= wait_after_reach_sp:
                        self.set_speed(0.0)
                        position_reached = True
                        print("Position reached!")
                else:
                    pass
            except NameError:
                pass


            #Pause control loop for chosen sample time
            #https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/25251804#25251804
            time.sleep(self.sampling_time - ((time.time() - start_time) % self.sampling_time))
        
        return None






