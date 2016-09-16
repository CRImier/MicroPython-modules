from time import sleep

from uhd44780 import HD44780

class Screen(HD44780):
    """Driver for using HD44780 displays connected to GPIO. Presumes the R/W line is tied to ground. Also, doesn't yet control backlight. """

    def __init__(self, pins = [], rs_pin = None, en_pin = None, rows=2, cols=16):
        """ Initializes the GPIO-driven HD44780 display      
        Kwargs:
           * ``pins``: list of GPIO pins for driving display data bits in format [DB4, DB5, DB6, DB7]
           * ``en_pin``: EN pin GPIO number. Please, make sure it's pulled down to GND (10K is OK). Otherwise, blocks might start filling up the screen unexpectedly.
           * ``rs_pin``: RS pin GPIO number,
           * ``cols``: number of display columns,
           * ``rows``: number of display rows.
        """
        self.rs_pin = rs_pin
        self.en_pin = en_pin
        self.pins = pins
        pin_out = self.en_pin.OUT
        self.en_pin.init(pin_out)
        self.rs_pin.init(pin_out)
        for pin in self.pins:
            pin.init(pin_out)
        HD44780.__init__(self, rows=rows, cols=cols)
        
    def write_byte(self, byte, char_mode=False):
        """Takes a byte and sends the high nibble, then the low nibble (as per HD44780 doc). Passes ``char_mode`` to ``self.write4bits``."""
        self.write4bits(byte >> 4, char_mode)   
        self.write4bits(byte & 0x0F, char_mode) 

    def write4bits(self, bits, char_mode=False):
        """Writes a nibble to the display. If ``char_mode`` is set, holds the RS line high."""
        self.rs_pin.value(char_mode)
        self.pins[0].value(bits&0x1==0x1)
        self.pins[1].value(bits&0x2==0x2)
        self.pins[2].value(bits&0x4==0x4)
        self.pins[3].value(bits&0x8==0x8)
        self.en_pin.high()
        sleep(0.00001) 
        self.en_pin.low()
        sleep(0.00001)
