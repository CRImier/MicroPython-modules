# vim: set fileencoding=UTF-8 :

# HMC5883L Magnetometer (Digital Compass) wrapper class
# Based on https://github.com/rm-hull/hmc5883l

import math
from array import array

class HMC5883L():
    
    __scales = {
        "0.88": [0, 0.73],
        "1.3": [1, 0.92],
        "1.9": [2, 1.22],
        "2.5": [3, 1.52],
        "4.0": [4, 2.27],
        "4.7": [5, 2.56],
        "5.6": [6, 3.03],
        "8.1": [7, 4.35]}
        
    def __init__(self, i2c=None, address=30, gauss="1.3", declination=(0,0)):
        self.i2c = i2c
        self.address = address
        degrees, minutes = declination
        self.__declDegrees = degrees
        self.__declMinutes = minutes
        self.__declination = (degrees + minutes / 60) * math.pi / 180
        reg, self.__scale = self.__scales[gauss]
        self.i2c_write(0x00, 0x70) # 8 Average, 15 Hz, normal measurement 
        self.i2c_write(0x01, reg << 5) # Scale 
        self.i2c_write(0x02, 0x00) # Continuous measurement 
    
    def i2c_write(self, reg, value):
        self.i2c.writeto_mem(self.address, reg, bytearray([value]))

    def declination(self):
        return (self.__declDegrees, self.__declMinutes)
    
    def twos_complement(self, val, len): # Convert two's complement to integer
        if (val & (1 << len - 1)):
            val = val - (1<<len)
        return val

    def __convert(self, data, offset):
        val = self.twos_complement(data[offset] << 8 | data[offset+1], 16)
        if val == -4096: return None
        return round(val * self.__scale, 4)

    def axes(self):
        data = array('B', [0]*6)
        self.i2c.readfrom_mem_into(self.address, 0x03, data) #Reading just the necessary registers instead of the whole memory as it was in rm-hull's version
        print(data)
        x = self.__convert(data, 0)
        y = self.__convert(data, 4)
        z = self.__convert(data, 2)
        return (x,y,z)

    def heading(self):
        (x, y, z) = self.axes()
        headingRad = math.atan2(y, x)
        headingRad += self.__declination
        # Correct for reversed heading
        if headingRad < 0:
            headingRad += 2 * math.pi
        # Check for wrap and compensate
        elif headingRad > 2 * math.pi:
            headingRad -= 2 * math.pi
        # Convert to degrees from radians
        headingDeg = headingRad * 180 / math.pi
        return headingDeg

    def degrees(self, headingDeg):
        degrees = math.floor(headingDeg)
        minutes = round((headingDeg - degrees) * 60)
        return (degrees, minutes)

    def direction(self):
        (x, y, z) = self.axes()
        heading = self.heading()
        return (x, y, z, heading)

    def print_direction(self):
        (x, y, z, heading) = self.direction()
        print("Axis X: " + str(x) + "\n" \
               "Axis Y: " + str(y) + "\n" \
               "Axis Z: " + str(z) + "\n" \
               "Heading: " + str(heading) + "\n")

