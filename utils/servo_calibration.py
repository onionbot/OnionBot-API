import time

import pigpio

import lib_para_360_servo

#define GPIO for each servo to read from
gpio_r_r = 14

#define GPIO for each servo to write to
gpio_r_w = 18

pi = pigpio.pi()

#### Calibrate servos, speed = 0.2 and -0.2
#choose gpio_l_w/gpio_l_r (left wheel), or gpio_r_w/gpio_r_r
#(right wheel) accordingly

servo = lib_para_360_servo.write_pwm(pi = pi, gpio = gpio_r_w)

#buffer time for initializing everything
time.sleep(1)
servo.set_speed(0.2)
wheel = lib_para_360_servo.calibrate_pwm(pi = pi, gpio = gpio_r_r)
servo.set_speed(0)
#http://abyz.me.uk/rpi/pigpio/python.html#stop
pi.stop()