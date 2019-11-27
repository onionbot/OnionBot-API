import collections
import statistics
import time

import pigpio

#https://www.parallax.com/sites/default/files/downloads/900-00360-Feedback-360-HS-Servo-v1.1.pdf
#http://gpiozero.readthedocs.io/en/stable/remote_gpio.html
#https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering

class write_pwm:
    """
    Stears a Parallax Feedback 360° High-Speed Servo `360_data_sheet`_ .

    This class stears a Parallax Feedback 360° High-Speed Servo. Out of the speed range,
    defined by ``min_speed`` and ``max_speed``, and the range of the pulsewidth, defined 
    by ``min_pw`` and ``max_pw``, the class allows setting the servo speed and automatically
    calculates the appropriate pulsewidth for the chosen speed value.

    .. note::
        ``min_pw`` and ``max_pw`` might needed to be interchanged, depending on if ``min_pw`` is 
        moving the servo max_forward/clockwise or max_backwards/counter-clockwise,
        see methods :meth:`max_forward` and  :meth:`max_backward`. 
        :meth:`max_forward` -> ``min_pw`` should let the servo rotate clockwise.

    .. warning::
        Be carefull with setting the min and max pulsewidth! Test carefully ``min_pw`` and ``max_pw``
        before setting them. Wrong values can damage the servo, see set_servo_pulsewidth_ !!!

    :param pigpio.pi pi: 
        Instance of a pigpio.pi() object.
    :param int gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the control wire of the servo has to be connected.
    :param int min_pw:
        Min pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1280, taken from the data sheet `360_data_sheet`_ .
    :param int max_pw:
        Max pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1720, taken from the data sheet `360_data_sheet`_ .
    :param int min_speed:
        Min speed which the servo is able to move. **Default:** -1. 
    :param int max_speed:
        Max speed which the servo is able to move. **Default:** 1. 

    .. _elinux.org: https://elinux.org/RPi_Low-level_peripherals#Model_A.2B.2C_B.2B_and_B2
    .. _set_servo_pulsewidth: http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
    .. _`360_data_sheet`: https://www.parallax.com/sites/default/files/downloads/900-00360-Feedback-360-HS-Servo-v1.1.pdf
    """

    def __init__(self, pi, gpio, min_pw = 1280, max_pw = 1720, min_speed = -1, max_speed = 1):

        self.pi = pi
        self.gpio = gpio
        self.min_pw = min_pw
        self.max_pw = max_pw
        self.min_speed = min_speed
        self.max_speed = max_speed
        #calculate slope for calculating the pulse width
        self.slope = (self.min_pw - ((self.min_pw + self.max_pw)/2)) / self.max_speed
        #calculate y-offset for calculating the pulse width
        self.offset = (self.min_pw + self.max_pw)/2

    def set_pw(self, pulse_width):
        """
        Sets pulsewidth of the PWM.

        This method allows setting the pulsewidth of the PWM directly. This can be used to
        test which ``min_pw`` and ``max_pw`` are appropriate. For this the ``min_pw`` and ``max_pw`` 
        are needed to be set very small and very big, so that they do not limit the set pulsewidth. 
        Normally they are used to protect the servo by limiting the pulsewidth to a certain range.

        .. warning::
            Be carefull with setting the min and max pulsewidth! Test carefully ``min_pw`` and ``max_pw``
            before setting them. Wrong values can damage the servo, see set_servo_pulsewidth_ !!!

        :param int,float pulsewidth:
            Pulsewidth of the PWM signal. Will be limited to ``min_pw`` and ``max_pw``.
        
        .. _set_servo_pulsewidth: http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
        """
        
        pulse_width = max(min(self.max_pw, pulse_width), self.min_pw)

        self.pi.set_servo_pulsewidth(user_gpio = self.gpio, pulsewidth = pulse_width)
        
    def calc_pw(self, speed):

        pulse_width = self.slope * speed + self.offset
        
        return pulse_width

    def set_speed(self, speed):
        """
        Sets speed of the servo.

        This method sets the servos rotation speed. The speed range is defined by 
        by ``min_speed`` and ``max_speed`` .

        :param int,float speed:
            Should be between ``min_speed`` and ``max_speed`` ,
            otherwise the value will be limited to those values.
        """

        speed = max(min(self.max_speed, speed), self.min_speed)

        calculated_pw = self.calc_pw(speed = speed)
        self.set_pw(pulse_width = calculated_pw)

    def stop(self):
        """
        Sets the speed of the servo to 0.
        """

        pulse_width = (self.min_pw+self.max_pw)/2
        self.set_pw(pulse_width = pulse_width)

    def max_backward(self):
        """
        Sets the speed of the servo to -1, so ``min_speed`` (max backwards,
        counter-clockwise)
        """

        self.set_pw(self.max_pw)

    def max_forward(self):
        """
        Sets the speed of the servo to 1, so ``max_speed`` (max forward,
        clockwise)
        """
        
        self.set_pw(self.min_pw)

class read_pwm:
    """
    Reads position of a Parallax Feedback 360° High-Speed Servo `360_data_sheet`_ .

    This class reads the position of a Parallax Feedback 360° High-Speed Servo. At the
    moment, the period for a 910 Hz signal is hardcoded.

    :param pigpio.pi pi: 
        Instance of a pigpio.pi() object.
    :param int gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the feedback wire of the servo has to be connected.

    .. todo::
        Enable the class to be able to handle different signals, not just 910 Hz.

    .. _elinux.org: https://elinux.org/RPi_Low-level_peripherals#Model_A.2B.2C_B.2B_and_B2
    .. _`360_data_sheet`: https://www.parallax.com/sites/default/files/downloads/900-00360-Feedback-360-HS-Servo-v1.1.pdf
    """

    def __init__(self, pi, gpio):

        self.pi = pi
        self.gpio = gpio
        self.period = 1/910*1000000
        self.tick_high = None
        self.duty_cycle = None
        self.duty_scale = 1000

        #http://abyz.me.uk/rpi/pigpio/python.html#set_mode
        self.pi.set_mode(gpio=self.gpio, mode=pigpio.INPUT)
        #http://abyz.me.uk/rpi/pigpio/python.html#callback
        self.cb = self.pi.callback(user_gpio=self.gpio, edge=pigpio.EITHER_EDGE, func=self.cbf)

    #calculate the duty cycle
    def cbf(self, gpio, level, tick):

        #change to low (a falling edge)
        if level == 0:
            #if first edge is a falling one the following code will fail
            #a try first time is faster than an if-statement every time 
            try:
                #http://abyz.me.uk/rpi/pigpio/python.html#callback
                # tick        32 bit    The number of microseconds since boot
                #                       WARNING: this wraps around from
                #                       4294967295 to 0 roughly every 72 minutes
                #Tested: This is handled by the tickDiff function internally, if t1 (earlier tick)
                #is smaller than t2 (later tick), which could happen every 72 min. The result will
                #not be a negative value, the real difference will be properly calculated.
                self.duty_cycle = self.duty_scale*pigpio.tickDiff(t1=self.tick_high, t2=tick)/self.period

            except Exception:
                pass

        #change to high (a rising edge)
        elif level == 1:

            self.tick_high = tick

    def read(self):
        """
        Returns the recent measured duty cycle.

        This method returns the recent measured duty cycle.

        :return: Recent measured duty cycle
        :rtype: float
        """

        return self.duty_cycle

    def cancel(self):
        """
        Cancel the started callback function.

        This method cancels the started callback function if initializing an object.
        As written in the pigpio callback_ documentation, the callback function may be cancelled
        by calling the cancel function after the created instance is not needed anymore.

        .. _callback: http://abyz.me.uk/rpi/pigpio/python.html#callback
        """

        self.cb.cancel()

class calibrate_pwm:
    """
    Calibrates a Parallax Feedback 360° High-Speed Servo with the help of the :class:`read_pwm` class.

    This class helps to find out the min and max duty cycle of the feedback signal of a 
    servo. This values ( ``dcMin`` / ``dcMax`` ) are then needed in :ref:`lib_motion` 
    to have a more precise measurement of the position. The experience has shown that each
    servo has slightly different min/max duty cycle values, different than the once 
    provided in the data sheet 360_data_sheet_ . Values smaller and bigger than the 
    printed out once as "duty_cycle_min/duty_cycle_max" are outliers and should 
    therefore not be considered. This can be seen in the printouts of smallest/biggest 
    250 values. There are sometimes a few outliers. Compare the printouts of different
    runs to get a feeling for it.

    .. note::
        The robot wheels must be able to rotate free in the air for calibration.
        Rotating forward or backward might sometimes give slightly 
        different results for min/max duty cycle. Choose the smallest value and the 
        biggest value out of the forward and backward runs. Do both directions three 
        times for each wheel, with speed = 0.2 and -0.2. Then 
        chose the values. The speed has to be set manually, see :ref:`Examples`.

    :param pigpio.pi pi: 
        Instance of a pigpio.pi() object.
    :param int gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the feedback wire of the servo has to be connected.
    :param int,float measurement_time:
        Time in seconds for how long duty cycle values will be collected, so for how long the
        measurement will be made. **Default:** 120.
    :returns: Printouts of different measurements

    At the moment, the period for a 910 Hz signal is hardcoded, as in :meth:`read_pwm` .

    .. todo::
        Enable the class to be able to handle different signals, not just 910 Hz.

    .. _elinux.org: https://elinux.org/RPi_Low-level_peripherals#Model_A.2B.2C_B.2B_and_B2
    .. _`360_data_sheet`: https://www.parallax.com/sites/default/files/downloads/900-00360-Feedback-360-HS-Servo-v1.1.pdf
    """

    def __init__(self, pi, gpio, measurement_time = 120):
         
        self.pi = pi
        self.gpio = gpio
        self.period = 1/910*1000000
        self.tick_high = None
        self.duty_cycle = None
        self.duty_scale = 1000
        self.list_duty_cycles = []
        self.duty_cycle_min = None
        self.duty_cycle_max = None

        #http://abyz.me.uk/rpi/pigpio/python.html#set_mode
        self.pi.set_mode(gpio=self.gpio, mode=pigpio.INPUT)

        #http://abyz.me.uk/rpi/pigpio/python.html#callback
        self.cb = self.pi.callback(user_gpio=self.gpio, edge=pigpio.EITHER_EDGE, func=self.cbf)
        
        print('{}{}{}'.format('Starting measurements for: ', measurement_time, ' seconds.'))
        print('----------------------------------------------------------')
        time.sleep(measurement_time)

        #stop callback before sorting list to avoid getting added new elements unintended
        #http://abyz.me.uk/rpi/pigpio/python.html#callback
        self.cb.cancel()
        time.sleep(1)
        
        self.list_duty_cycles = sorted(self.list_duty_cycles)

        #some analyzis of the dc values
        sorted_set = list(sorted(set(self.list_duty_cycles)))
        print('{} {}'.format('Ascending sorted distinct duty cycle values:', sorted_set))
        print('----------------------------------------------------------')
        differences_list = [sorted_set[i+1]-sorted_set[i] for i in range(len(sorted_set)-1)]
        rounded_differences_list = [round(differences_list[i],2) for i in range(len(differences_list)-1)]
        counted_sorted_list = collections.Counter(rounded_differences_list)
        print('{} {}'.format('Ascending counted, sorted and rounded distinct differences between duty cycle values:',counted_sorted_list))
        print('----------------------------------------------------------')

        #Median and median_high/median_low are chosen, because the biggest 
        #and smallest values are needed, and not an avarage of the smallest 
        #and biggest values of the selection. 
        #https://docs.python.org/3/library/statistics.html#statistics.median
        print('{} {}'.format('Smallest 250 values:', self.list_duty_cycles[:250]))
        self.duty_cycle_min = statistics.median_high(self.list_duty_cycles[:20])
        print('----------------------------------------------------------')
        print('{} {}'.format('Biggest 250 values:',self.list_duty_cycles[-250:]))
        self.duty_cycle_max = statistics.median_low(self.list_duty_cycles[-20:])
        print('----------------------------------------------------------')

        print('duty_cycle_min:', round(self.duty_cycle_min,2))

        print('duty_cycle_max:', round(self.duty_cycle_max,2))
        
    def cbf(self, gpio, level, tick):

        #change to low (a falling edge)
        if level == 0:
            #if first edge is a falling one the following code will not work
            #a try first time is faster than an if-statement every time 
            try:
                self.duty_cycle = self.duty_scale*pigpio.tickDiff(t1=self.tick_high, t2=tick)/self.period
                self.list_duty_cycles.append(self.duty_cycle)

            except Exception:
                pass

        #change to high (a rising edge)
        elif level == 1:

            self.tick_high = tick
            
    def cancel(self):

        self.cb.cancel()

if __name__ == "__main__":

    #just continue
    
    pass
    '''
    pi = pigpio.pi()
    gpio = 14
    #obj = read_pwm(pi, gpio)   
    
    x = calibrate_pwm(pi, gpio)
    
    
    while True: 

    
        time.sleep(0.1)
    
        print(obj.read())
    '''
    
    
    
    
    
    
    
    
    
    
    
    