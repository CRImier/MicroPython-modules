#
# based on code from Adafruit, lrvick, LiquidCrystal and pyLCI
# lrvick - https://github.com/lrvick/raspi-hd44780/blob/master/hd44780.py
# LiquidCrystal - https://github.com/arduino/Arduino/blob/master/libraries/LiquidCrystal/LiquidCrystal.cpp
# Adafruit - https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code
# pyLCI - https://github.com/CRImier/pyLCI/
#

# commands
LCD_CLEARDISPLAY        = const(0x01)
LCD_RETURNHOME          = const(0x02)
LCD_ENTRYMODESET        = const(0x04)
LCD_DISPLAYCONTROL      = const(0x08)
LCD_CURSORSHIFT         = const(0x10)
LCD_FUNCTIONSET         = const(0x20)
LCD_SETCGRAMADDR        = const(0x40)
LCD_SETDDRAMADDR        = const(0x80)

# flags for display entry mode
LCD_ENTRYRIGHT          = const(0x00)
LCD_ENTRYLEFT           = const(0x02)
LCD_ENTRYSHIFTINCREMENT = const(0x01)
LCD_ENTRYSHIFTDECREMENT = const(0x00)

# flags for display on/off control
LCD_DISPLAYON           = const(0x04)
LCD_DISPLAYOFF          = const(0x00)
LCD_CURSORON            = const(0x02)
LCD_CURSOROFF           = const(0x00)
LCD_BLINKON             = const(0x01)
LCD_BLINKOFF            = const(0x00)

# flags for display/cursor shift
LCD_DISPLAYMOVE         = const(0x08)
LCD_CURSORMOVE          = const(0x00)
LCD_MOVERIGHT           = const(0x04)
LCD_MOVELEFT            = const(0x00)

# flags for function set
LCD_8BITMODE            = const(0x10)
LCD_4BITMODE            = const(0x00)
LCD_2LINE               = const(0x08)
LCD_1LINE               = const(0x00)
LCD_5x10DOTS            = const(0x04)
LCD_5x8DOTS             = const(0x00)


from time import sleep

class HD44780(object):
    """An object that provides high-level functions for interaction with display. It contains all the high-level logic and exposes an interface for system and applications to use."""

    #row_offsets = [const(0x00), const(0x40), const(0x14), const(0x54)]
    row_offsets = [0x00, 0x40, 0x14, 0x54]

    display_function = LCD_FUNCTIONSET | LCD_4BITMODE | LCD_2LINE | LCD_5x8DOTS
    displaycontrol = 0x0c
    displaymode = 0x07

    def __init__(self, cols=16, rows=2):
        """ Sets variables for high-level functions.
        
        Kwargs:
           * ``rows`` (default=2): rows of the connected display
           * ``cols`` (default=16): columns of the connected display"""
        self.cols = cols
        self.rows = rows
        self.init_display()

    def init_display(self):
        """Initializes HD44780 controller."""
        self.write_byte(0x33)
        sleep(0.02)
        self.write_byte(0x33)
        sleep(0.02)
        self.write_byte(0x33)
        sleep(0.02)
        self.home()
        self.write_byte(self.display_function)
        self.noDisplay()
        self.noAutoscroll()
        self.clear()
        self.display()

    def println(self, line):
        """Prints a line on the screen (assumes position is set as intended)"""
        for char in line:
            self.write_byte(ord(char), char_mode=True)     

    def home(self):
        """Returns cursor to home position. If the display is being scrolled, reverts scrolled data to initial position.."""
        self.write_byte(LCD_RETURNHOME)  # set cursor position to zero
        sleep(0.005)  # this command takes a long time!

    def clear(self):
        """Clears the display."""
        self.write_byte(LCD_CLEARDISPLAY)  # command to clear display
        sleep(0.005)  # 5000 microsecond sleep, clearing the display takes a long time

    def setCursor(self, row, col):
        """ Set current input cursor to ``row`` and ``column`` specified """
        self.write_byte(LCD_SETDDRAMADDR | (col + self.row_offsets[row]))

    def createChar(self, char_num, char_contents):
        """Stores a character in the LCD memory so that it can be used later.
        char_num has to be between 0 and 7 (including)
        char_contents is a list of 8 bytes (only 5 LSBs are used)"""
        if type(char_num) != int or not char_num in range(8):
            raise ValueError("Invalid char_num!")
        self.write_byte(LCD_SETCGRAMADDR | (char_num << 3))
        try:
            for i in range(8):
                self.write_byte(char_contents[i], char_mode=True)
        except IndexError:
            raise ValueError("Invalid char_contents!")
        finally:
            self.setCursor(0, 0) #Need to issue a command after writing a char. Otherwise, it gets stuck or something.

    def noDisplay(self):
        """ Turn the display off (quickly) """
        self.displaycontrol &= ~LCD_DISPLAYON
        self.write_byte(LCD_DISPLAYCONTROL | self.displaycontrol)

    def display(self):
        """ Turn the display on (quickly) """
        self.displaycontrol |= LCD_DISPLAYON
        self.write_byte(LCD_DISPLAYCONTROL | self.displaycontrol)

    def noCursor(self):
        """ Turns the underline cursor off """
        self.displaycontrol &= ~LCD_CURSORON
        self.write_byte(LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor(self):
        """ Turns the underline cursor on """
        self.displaycontrol |= LCD_CURSORON
        self.write_byte(LCD_DISPLAYCONTROL | self.displaycontrol)

    def noBlink(self):
        """ Turn the blinking cursor off """
        self.displaycontrol &= ~LCD_BLINKON
        self.write_byte(LCD_DISPLAYCONTROL | self.displaycontrol)

    def blink(self):
        """ Turn the blinking cursor on """
        self.displaycontrol |= LCD_BLINKON
        self.write_byte(LCD_DISPLAYCONTROL | self.displaycontrol)

    def scrollDisplayLeft(self):
        """ These commands scroll the display without changing the RAM """
        self.write_byte(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)

    def scrollDisplayRight(self):
        """ These commands scroll the display without changing the RAM """
        self.write_byte(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)

    def leftToRight(self):
        """ This is for text that flows Left to Right """
        self.displaymode |= LCD_ENTRYLEFT
        self.write_byte(LCD_ENTRYMODESET | self.displaymode)

    def rightToLeft(self):
        """ This is for text that flows Right to Left """
        self.displaymode &= ~LCD_ENTRYLEFT
        self.write_byte(LCD_ENTRYMODESET | self.displaymode)

    def autoscroll(self):
        """ This will 'right justify' text from the cursor """
        self.displaymode |= LCD_ENTRYSHIFTINCREMENT
        self.write_byte(LCD_ENTRYMODESET | self.displaymode)

    def noAutoscroll(self):
        """ This will 'left justify' text from the cursor """
        self.displaymode &= ~LCD_ENTRYSHIFTINCREMENT
        self.write_byte(LCD_ENTRYMODESET | self.displaymode)
