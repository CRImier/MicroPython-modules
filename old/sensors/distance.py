import pyb

class Sensor():
    def __init__(self, pin):
        self.adc = pyb.ADC(pin)
    def adc_to_distance(self, reading):
        return reading #stub function - to be replaced by child class
    def get_distance(self):
        return self.adc_to_distance(self.adc.read())

class S2D120X(Sensor):
    def adc_to_distance(self, reading):
        try:
            distance = 2076.0/(reading/4 - 11)
        except ZeroDivisionError:
            distance = 2076.0
        return distance


