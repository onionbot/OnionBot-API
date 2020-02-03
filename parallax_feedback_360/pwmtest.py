#!/usr/bin/python3
import pigpio, time
from statistics import mean

def unwrap(newtick, oldtick):
    """
    a simple function to account for tick wrapround
    """
    diff=newtick-oldtick
    if diff > 0:
        return diff
    else:
        return diff+4294967296

class pwmreader():
    """
    a simple class to monitor a pwm signal and report relevant values
    """
    def __init__(self, pio, pwmpin):
        """
        set up the instance
        
        pio    : an instance of pigpio.pi
        
        pwmpin : the broadcom pin to monitor. The pin is assumed to be already setup
        """
        self.pwmpin=pwmpin
        self.pio=pio
        self.cb=pio.callback(self.pwmpin, edge=pigpio.EITHER_EDGE, func=self.tellme)
        self.last_level=None
        self.last_rise=None
        self.periods=[]
        self.hightimes=[]
        self.pulsecount=0
        self.arraymax=150

    def tellme(self, GPIO, level, tick):
        lon=level==1   # flip this if the signal is inverted
        if self.last_rise is None:
            if lon:
                self.last_rise=tick
                self.last_level=lon
            else:
                pass # ignore if the first thing we get is an end of pulse
        else:
            if lon==self.last_level:
                print('unexpected callback for level {}, same edge as previous call'.format(lon))
            else:
                if lon:
                    self.periods.append(unwrap(tick, self.last_rise))
                    if len(self.periods) > self.arraymax:
                        self.periods.pop(0)
                    self.last_rise=tick
                else:
                    self.hightimes.append(unwrap(tick, self.last_rise))
                    if len(self.hightimes) > self.arraymax:
                        self.hightimes.pop(0)
                    self.pulsecount+=1
                    if self.pulsecount < 51 and self.pulsecount % 10 == 0:
                        self.report()
                    elif self.pulsecount % 50 == 0:
                        self.report()
                self.last_level=lon

    def report(self):
        print('last {:3d} pulses: period min: {:0.4f}, max: {:0.4f}, mean: {:0.4f}, pulse width min: {:0.4f}, max: {:0.4f}, mean: {:0.4f}'.format(
               len(self.periods), min(self.periods), max(self.periods), mean(self.periods),
                                  min(self.hightimes), max(self.hightimes), mean(self.hightimes)))

    def cancel(self):
        self.cb.cancel()

def runtest(pin):
    pio=pigpio.pi()
    if not pio.connected:
        raise ValueError('pigpio does not appear to be running')
    #pio.set_servo_pulsewidth(pin,1700)
    time.sleep(.1)
    t=pwmreader(pio, pin)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    pio.set_servo_pulsewidth(pin,0)
    pio.stop()
    print('byeeeeee')
    
runtest(14)
