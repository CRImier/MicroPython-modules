import pyb

#Implement PWM!

class Motor():
    def __init__(self, *args, pwm=False):
        if len(args) == 2:
            self.in1_pinnum, self.in2_pinnum = args
            self.en_pin = None
        elif len(args) == 3:
            self.in1_pinnum, self.in2_pinnum, self.en_pinnum = args
            self.en_pin = pyb.Pin(self.en_pinnum, pyb.Pin.OUT_PP)
        else:
            raise(Exception)
        self.in1_pin = pyb.Pin(self.in1_pinnum, pyb.Pin.OUT_PP)
        self.in2_pin = pyb.Pin(self.in2_pinnum, pyb.Pin.OUT_PP)
        if pwm:
            self.pwm_enabled = True
            #setup pwm on in1 and in2
        else:    
            self.pwm_enabled = False

    def enable(self):
        try:
            self.en_pin.high()
        except Exception as e: ###########
            return e

    def disable(self):
        try:
            self.en_pin.low()
        except Exception as e: ###########
            return e

    def move_forward(self, pwm=None):
        if pwm:
            if not self.pwm_enabled:
                raise Exception #######Re
            self.in1_pin_pwm=pwm
            self.in2_pin.low()
        else:
            self.in1_pin.high()
            self.in2_pin.low()

    def move_backward(self, pwm=None):
        if pwm:
            if not self.pwm_enabled:
                raise Exception #######Re
            self.in2_pin_pwm=pwm
            self.in1_pin.low()
        else:
            self.in2_pin.high()
            self.in1_pin.low()

    def stop(self):
        self.in1_pin.low()
        self.in2_pin.low()

