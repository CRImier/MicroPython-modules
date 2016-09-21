from time import sleep

class HBridge():
    def __init__(self, pin_a, pin_b):
        self.a = pin_a
        self.b - pin_b
        self.a.init(self.a.OUT)
        self.b.init(self.b.OUT)
        self.a.low()
        self.b.low()
        
    def forward(self):
        self.stop()
        sleep(0.001)
        self.a.high()
        self.b.low() #Implied to be low, but still useful
        
    def backward(self):
        self.stop()
        sleep(0.001)
        self.a.low() 
        self.b.high()
        
    def stop(self):
        self.a.low()
        self.b.low()
