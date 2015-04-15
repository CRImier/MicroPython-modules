import pyb

from sensors import distance, tsop4838
from actuators import l293, led
#from algorithms.positioning import IRSensorArray

from engines.car import Car

distance_sensor_pins = ("Y12",)
ir_sensor_pins = ('Y10', 'Y9', 'X8', 'X7', 'X6')
steer_motor_pins = ('Y6', 'Y7', 'Y8')
forward_motor_pins = ('Y3', 'Y4', 'Y5')
led_pins = ('X9', 'X10', 'X11', 'X12')
light_sensor_pins = None
#servo_pins = ("X1",)

car = Car()

car.sensors = {
"infrared":[tsop4838.TSOP4838(pin_name) for pin_name in ir_sensor_pins],
"distance":[distance.S2D120X(distance_sensor_pins[0])],
"acceleration":[pyb.Accel(), None],
"compass":[None],
"gyro":[None],
"light":[None]
}

car.actuators = {
"motors":[l293.Motor(*pin_set) for pin_set in (forward_motor_pins, steer_motor_pins)],
"leds":[led.LED(pin) for pin in led_pins]
#"servo":[pyb.Servo(pin) for pin in servo_pins]
}

car.front_distance_sensor = car.sensors["distance"][0]
#car.sensor_array = IRSensorArray(car.sensors["infrared"], 60)
car.forward_motor = car.actuators["motors"][0]
car.steer_motor = car.actuators["motors"][1]
 
car.get_front_distance = car.front_distance_sensor.get_distance
car.move_forward = car.forward_motor.move_forward
car.move_backward = car.forward_motor.move_backward
car.stop = car.forward_motor.stop

car.setup_actions = [
(car.forward_motor.enable,),
(car.steer_motor.disable,),
(car.stop,)
]


def print_distance():
    print(car.get_front_distance())

def okay():
    car.stop()
    print("Okay!")

def forward():
    car.move_forward()
    print("Forward!")

def backward():
    car.move_backward()
    print("Backward!")

def while_true():
    return True



car.goals = [
(while_true, print_distance),
(lambda: car.get_front_distance() >= 14.0, forward),
(lambda: car.get_front_distance() <= 7.0, backward),
(lambda: car.get_front_distance() < 14.0 and car.get_front_distance() > 7.0, okay)
]

car.setup()
car.run()

#car.move_forward()
