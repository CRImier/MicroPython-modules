import pyb

class TSOP4838():
    def __init__(self, pin):
        self.sensor = pyb.Pin(pin, pyb.Pin.IN)
    def read(self):
        return self.sensor.value()


