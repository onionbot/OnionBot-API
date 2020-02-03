from __future__ import division
import time
# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout

# Set up pin 11 for PWM
GPIO.setup(18,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(18, 50)     # Sets up pin 11 as a PWM pin
              # Starts running PWM on the pin and sets it to 0

dc = (1100 / 20000)*100
p.start(dc)

p.ChangeDutyCycle(6)

sleep(10)

try:
    # Move the servo back and forth
    while True:
        print dc, (dc/100)*20000
        p.ChangeDutyCycle(dc)     # Changes the pulse width to 3 (so moves the servo)
        sleep(1)
        dc += .05
        #p.ChangeDutyCycle(0)    # Changes the pulse width to 12 (so moves the servo)
        #sleep(2)
except KeyboardInterrupt:
    # Clean up everything
    p.stop()                 # At the end of the program, stop the PWM
    GPIO.cleanup()           # Resets the GPIO pins back to defaults



while True: 
    #speed = float(raw_input("Speed: "))

    #dc = ((speed/100)*1.1)+7.1
    print dc 
    #p.ChangeDutyCycle(dc)     # Changes the pulse width to 3 (so moves the servo)
    sleep(1)