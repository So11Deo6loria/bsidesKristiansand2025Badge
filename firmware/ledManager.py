from machine import Pin
import time
from neopixel import NeoPixel
import constants

class LEDManager:
    def __init__(self, startupColor):
        self.ledPin = Pin(constants.LED_PIN, Pin.OUT)
        self.ledEnablePin = Pin(constants.LED_ENABLE_PIN, Pin.OUT)
        self.strand = NeoPixel(self.ledPin, constants.LED_COUNT)
        self.startupColor = startupColor
        
        # LED Sections
        self.eyes = [1, 2]
        self.jacket = [3, 4, 5, 6, 7, 8, 9]
        
    def enable_led_voltage(self):
        self.ledEnablePin.on()
    
    def disable_led_voltage(self):
        self.ledEnablePin.off()

    def turn_off_leds(self):
        for led in range(constants.LED_COUNT):
            self.strand[led] = tuple(constants.LED_COLORS['OFF'])
        self.strand.write()

    def blink_morse(self, number):
        """Blinks all LEDs in Morse code based on the given number."""
        morse_dict = {
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
            '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
        }
        morse_code = ''.join(morse_dict[digit] for digit in str(number) if digit in morse_dict)
        
        self.enable_led_voltage()
        self.turn_off_leds()
        
        dot_time = 0.2  # Duration of a dot
        dash_time = dot_time * 3
        pause_time = dot_time
        
        for symbol in morse_code:
            color = constants.LED_COLORS['PURPLE']
            for led in range(constants.LED_COUNT):
                self.strand[led] = color
            self.strand.write()
            
            time.sleep(dash_time if symbol == '-' else dot_time)
            
            self.turn_off_leds()
            time.sleep(pause_time)
        
        self.disable_led_voltage()

    def fade_in_jacket(self, duration=3):
        """Gradually brightens the jacket LEDs over the specified duration."""
        self.enable_led_voltage()
        self.turn_off_leds()
        steps = 30  # Number of steps in the fade-in effect
        step_delay = duration / steps
        
        # Retrieve target color
        target_color = constants.LED_COLORS[self.startupColor.upper()]  # Adjust as needed
        
        for step in range(steps + 1):
            brightness = step / steps
            new_color = tuple(int(target_color[i] * brightness) for i in range(3))
            
            for led in self.jacket:
                self.strand[led - 1] = new_color
            
            self.strand.write()
            time.sleep(step_delay)
        
        time.sleep(0.5)  # Hold at full brightness for 0.5 seconds
    
    def switch_to_eyes(self):
        """Quickly switches to high intensity on the eyes."""
        eye_color = constants.LED_COLORS['WHITE']  # Adjust as needed
        
        for led in self.jacket:
            self.strand[led - 1] = constants.LED_COLORS['OFF']  # Turn off jacket
        
        for led in self.eyes:
            self.strand[led - 1] = eye_color
        
        self.strand.write()
    
    def boot(self):
        """Runs the full LED sequence."""
        self.fade_in_jacket()
        self.switch_to_eyes()