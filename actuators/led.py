import pyb

class LED():
    state = False
    def __init__(self, pin, pwm=False):
        self.pin = pyb.Pin(pin, pyb.Pin.OUT_PP)
        if pwm:
            self.pwm_enabled = True
        else:
            self.pwm_enabled = False
    def on(self):
        self.state = True
        self.pin.high()
    def off(self):
        self.state = False
        self.pin.low()
    def set(self, value):
        self.state = value
        self.pin.value(value)
    def toggle(self):
        self.state = not self.state
        self.pin.value(self.state)
    def pwm(self, value):
        if not self.pwm_enabled:
            raise Exception #####
