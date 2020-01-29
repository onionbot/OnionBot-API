import math
import statistics
import time

import pigpio

import lib_para_360_servo

class control:
    """
    Controls the robot movement.

    This class controls the robots movement by controlling the two Parallax Feedback 360° 
    High-Speed Servos `360_data_sheet`_ . The robots local coordinate system is defined in
    the following way. X-axis positive is straight forward, y-axis positive is perpendicular 
    to the x-axis in the direction to the left wheel. The center (0/0) is where the middle
    of the robots chassi is cutting across a imaginary line through both wheels/servos.
    Angle phi is the displacement of the local coordinate system to the real world 
    coordinate system. See :ref:`Used_local_coordinate_system` for a picture of it.

    .. warning::
        Be carefull with setting the min and max pulsewidth! Test carefully ``min_pw`` and ``max_pw``
        before setting them. Wrong values can damage the servo, see set_servo_pulsewidth_ !!!

    :param pigpio.pi pi: 
        Instance of a pigpio.pi() object.
    :param int width_robot:
        Width of the robot in mm, so distance between middle right wheel and middle 
        left wheel. 
        **Default:** 102 mm, measured.
    :param diameter_wheels:
        Diameter of both wheels. 
        **Default:** 66 mm, measured and taken from the products website `wheel_robot`_ .
    :param int unitsFC:
        Units in a full circle, so each wheel is divided into X sections/ticks. 
        This value should not be changed.
        **Default:** 360
    :param float dcMin_l:
        Min duty cycle of the left wheel. 
        **Default:** 27.3, measured with method :meth:`lib_para_360_servo.calibrate_pwm` , 
        see :ref:`Examples` .
    :param float dcMax_l:
        Max duty cycle of the left wheel. 
        **Default:** 969.15,  measured with method :meth:`lib_para_360_servo.calibrate_pwm` , 
        see :ref:`Examples` .
    :param float dcMin_r:
        Min duty cycle of the right wheel. 
        **Default:** 27.3, measured with method :meth:`lib_para_360_servo.calibrate_pwm` , 
        see :ref:`Examples` .
    :param float dcMax_r:
        Max duty cycle of the left wheel. 
        **Default:** 978.25,  measured with method :meth:`lib_para_360_servo.calibrate_pwm` , 
        see :ref:`Examples` .
    :param int l_wheel_gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the feedback wire of the left servo has to be connected.
    :param int r_wheel_gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the feedback wire of the right servo has to be connected.
    :param int servo_l_gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the control wire of the left servo has to be connected.
    :param int min_pw_l:
        Min pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1280, taken from the data sheet `360_data_sheet`_ .
    :param int max_pw_l:
        Max pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1720, taken from the data sheet `360_data_sheet`_ .
    :param int min_speed_l:
        Min speed which the servo is able to move. **Default:** -1, so that 
        the speed range is also scaled between -1 and 1 as the output of 
        the inner control loop.
    :param int max_speed_l:
        Max speed which the servo is able to move. **Default:** 1, so that 
        the speed range is also scaled between -1 and 1 as the output of 
        the inner control loop. 
    :param int servo_r_gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the control wire of the right servo has to be connected.
    :param int min_pw_r:
        Min pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1280, taken from the data sheet `360_data_sheet`_ .
    :param int max_pw_r:
        Max pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1720, taken from the data sheet `360_data_sheet`_ .
    :param int min_speed_r:
        Min speed which the servo is able to move. **Default:** -1, so that 
        the speed range is also scaled between -1 and 1 as the output of 
        the inner control loop. 
    :param int max_speed_r:
        Max speed which the servo is able to move. **Default:** 1, so that 
        the speed range is also scaled between -1 and 1 as the output of 
        the inner control loop. 
    :param float sampling_time:
        Sampling time of the four PID controllers in seconds.
        **Default:** 0.01.
        1. PWM of motor feedback is 910Hz (0,001098901 s), so position changes cannot 
        be recognized faster than 1.1 ms. Therefore, it is not needed to run the outer control 
        loop more often and update the speed values which have a 50 Hz (20ms) PWM.
        2. Tests of the runtime of the code including the controller part have shown that
        writing the pulsewidth (pi.set_servo_pulsewidth()) in :meth:`lib_para_360_servo.write_pwm.set_pw` is 
        the bottleneck which drastically slows down the code by the factor ~400 
        (0,002 seconds vs 0,000005 seconds; runtime with vs without writing pulsewidth).
        3. For recognizing the RPMs of the wheels 10ms is needed to have enough changes in the
        position. This was found out by testing. See method :meth:`move` for more informations.
    :param int,float Kp_p:
        Kp value of the outer PID controllers, see method :meth:`move` 
        for more informations.
        **Default:** 0.1.
    :param int,float Ki_p:
        Ki value of the outer PID controllers, see method :meth:`move` 
        for more informations.
        **Default:** 0.1.
    :param int,float Kd_p:
        Kd value of the outer PID controllers, see method :meth:`move` 
        for more informations.
        **Default:** 0.
    :param int,float Kp_s:
        Kp value of the inner PID controllers, see method :meth:`move` 
        for more informations.
        **Default:** 0.5.
    :param int,float Ki_s:
        Ki value of the inner PID controllers, see method :meth:`move` 
        for more informations.
        **Default:** 0.
    :param int,float Kd_s:
        Kd value of the inner PID controllers, see method :meth:`move` 
        for more informations.
        **Default:** 0.

    .. _`360_data_sheet`: https://www.parallax.com/sites/default/files/downloads/900-00360-Feedback-360-HS-Servo-v1.1.pdf
    .. _`wheel_robot`: https://www.parallax.com/product/28114
    .. _elinux.org: https://elinux.org/RPi_Low-level_peripherals#Model_A.2B.2C_B.2B_and_B2
    """

    def __init__(
        self, pi, width_robot = 102, diameter_wheels = 66, unitsFC = 360,
        dcMin = 30.94, dcMax = 956.41,
        wheel_gpio = 14,
        servo_gpio = 18, min_pw = 1210, max_pw = 1750, min_speed = -1, max_speed = 1,
        sampling_time = 0.01,
        Kp_p = 0.1, #not too big values, otherwise output of position control would slow down too abrupt
        Ki_p = 0.1,
        Kd_p = 0,
        Kp_s = 0.4,
        Ki_s = 0,
        Kd_s = 0):
        
        self.pi = pi
        self.width_robot = width_robot
        self.diameter_wheels = diameter_wheels
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

    #angular position in units full circle
    def get_angle(self):

        #driving forward will increase the angle
        
        angle = (self.wheel.read() - self.dcMin) * self.unitsFC / (self.dcMax - self.dcMin + 1)

        angle = max(min((self.unitsFC - 1), angle), 0)

        return angle
    

    def set_speed(self, speed):

        self.servo.set_speed(speed)

        return None
    

    def get_total_angle(self, angle, unitsFC, prev_angle, turns):
       
        #### counting number of rotations
        #If 4th to 1st quadrant
        if((angle < (0.25*unitsFC)) and (prev_angle > (0.75*unitsFC))):
            turns += 1
        #If in 1st to 4th quadrant
        elif((prev_angle < (0.25*unitsFC)) and (angle > (0.75*unitsFC))):
            turns -= 1

        ####total angle measurement from zero
        if(turns >= 0):
            total_angle = (turns*unitsFC) + angle
        elif(turns < 0):
            total_angle = ((turns + 1)*unitsFC) - (unitsFC - angle)

        return turns, total_angle


    def get_target_angle(self, number_ticks, angle):
        
        #positiv number_ticks will be added, negativ number_ticks substracted
        target_angle = angle + number_ticks

        return target_angle


    def tick_length(self):

        tick_length_mm = math.pi * self.diameter_wheels / self.unitsFC

        return tick_length_mm


    def arc_circle(self, degree):

        arc_circle_mm = degree * math.pi * self.width_robot / 360.0

        return arc_circle_mm


    def straight(self, distance_in_mm):
        """
        Moves the robot about x mm forward or backward.

        This method moves the robot x mm forward or backward. Positive distance 
        values move the robot forward (regarding the local x-axis), negative distance 
        values backward (regarding the local x-axis), see picture in :ref:`Used_local_coordinate_system` , 
        where the local coordinate system of the robot is shown. This method calls 
        :meth:`lib_motion.control.move` which controls the movement of the robot.

        :param int,float distance_in_mm:
            Distance the robot has to move.
        """

        number_ticks = distance_in_mm/self.tick_length()

        self.move(number_ticks = number_ticks, straight = True)

        return None
    
    def simple_rotate(self, target_angle):
        
        position_reached = False
        
        while not position_reached:
            
            angle = self.get_angle()
            
            error = target_angle - angle
            
            if abs(error) < 2:
               position_reached = True
               print ("Reached")
               self.set_speed(0)
            
            elif error < 0:
                self.set_speed(0.5)
            elif error > 0:
                self.set_speed(-0.5)
    
    
    def rotate(self, target_angle):

        turns = 0

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
            #- first iteration of the while loop prev_angle_* is missing and the 
            #method self.get_total_angle() will throw an exception.
            #- second iteration of the while loop prev_total_angle_* is missing, 
            #which will throw another exception
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
                except Exception:
                    pass

                #PID-Controller
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
                except Exception:
                    pass

                #PID-Controller
                output_s = self.Kp_s * error_s + self.Ki_s * self.sampling_time * sum_error_s + self.Kd_s / self.sampling_time * (error_s - error_s_old)

                error_s_old = error_s

                #convert range output_s fom ticks/s to -1 to 1
                output_s_con = output_s / 650

                self.set_speed(output_s_con)


            except Exception:
                pass

            prev_angle = angle

            #try needed, because first iteration of the while loop prev_angle_* is
            #missing and the method self.get_total_angle() will throw an exception,
            #and therefore no total_angle_* gets calculated

            try:
                prev_angle = angle
            except Exception:
                pass

            try:
                if error_p == 0:
                    reached_sp_counter += 1

                    if reached_sp_counter >= wait_after_reach_sp:
                        self.set_speed(0.0)
                        position_reached = True
                        print("Position reached!")
                else:
                    pass

            except Exception:
                pass

            #Pause control loop for chosen sample time
            #https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/25251804#25251804
            time.sleep(self.sampling_time - ((time.time() - start_time) % self.sampling_time))

            #DEBUGGING OPTION: 
            #printing runtime of loop, see beginning of while true loop
            #print('{:.20f}'.format((time.time() - start_time_each_loop)))
        
        return None

    def cancel(self):
        """
        Cancel the started callback function.

        This method cancels the started callback function if initializing an object.
        As written in the pigpio callback_ documentation, the callback function may be cancelled
        by calling the cancel function after the created instance is not needed anymore.

        .. _callback: http://abyz.me.uk/rpi/pigpio/python.html#callback
        """

        self.wheel.cancel()

if __name__ == '__main__':

    #just continue
    pass