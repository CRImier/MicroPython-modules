import math

sensor_angle = 180 #Angle between center axis of sensors

class IRSensorArray():
    def __init__(self, sensors, sensor_angle):
        self.sensor_angle = sensor_angle
        self.sensors = sensors
        self.sensor_count = len(sensors)
    def read_sensors(self):
        reading = byte("True")*self.sensor_count
        for index, sensor in enumerate(self.sensors):
            reading[index] = sensor.get_state()
        return reading
    def get_angle_from_reading(self, reading):
        int_reading = int() #Converting
        max_int = int(byte"True"*self.sensor_count) #
        offset = self.sensor_angle / 2 #angle between sensor array center axis and any of #### sensor's center axis
        angle = -1*(float(int_reading)/max_int)*self.sensor_angle + offset #is multiplied by -1 because sensor input is inverted
        return angle
    def get_angle(self):
        reading = self.read_sensors()
        angle = self.get_angle_from_reading(reading)
        return angle

