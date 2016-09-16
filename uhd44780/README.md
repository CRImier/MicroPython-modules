Simple lightweight MicroPython library for HD44780 displays. 

```hd44780.py``` contains the base ```HD44780``` class with high-level functions. You need this file no matter which low-level interface you use. Its function naming and arguments are based on LiquidCrystal library interface for compatibility.

```hd44780_gpio``` contains a low-level ```Screen``` interface using MicroPython GPIO and 4-bit interfacing (only 6 pins necessary, R/W pin is to be shorted to ground.)

Sample invocation:
```
import uhd44780_gpio
from machine import Pin
screen = uhd44780_gpio.Screen(pins=[Pin(2), Pin(0), Pin(4), Pin(5)], en_pin=Pin(13), rs_pin=Pin(12))
screen.println("MicroPython!")
```
