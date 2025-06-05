from machine import Pin
import time
from neopixel import NeoPixel
import constants
import random

class LEDManager:
    def __init__(self, startupColor):
        self.ledPin = Pin(constants.LED_PIN, Pin.OUT)
        self.ledEnablePin = Pin(constants.LED_ENABLE_PIN, Pin.OUT)
        self.strand = NeoPixel(self.ledPin, constants.LED_COUNT)
        self.startupColor = startupColor
        self.picoLED = Pin("LED", Pin.OUT)

        # LED Sections
        self.eyes = [1, 2]
        self.jacket = [3, 4, 5, 6, 7, 8, 9]

    def apply_brightness(self, color):
        """Scales the RGB color by MAX_BRIGHTNESS (0.0 to 1.0)."""
        scale = constants.MAX_BRIGHTNESS
        return tuple(int(c * scale) for c in color)

    def enable_led_voltage(self):
        self.ledEnablePin.on()

    def disable_led_voltage(self):
        self.ledEnablePin.off()

    def turn_off_leds(self):
        for led in range(constants.LED_COUNT):
            self.strand[led] = self.apply_brightness(constants.LED_COLORS['OFF'])
        self.strand.write()

    def blink_morse(self, number):
        """Blinks the onboard LED in Morse code for a given numeric string."""
        morse_dict = {
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
            '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
        }

        # Validate and convert number to string of Morse patterns
        num_str = str(number)
        if not all(d in morse_dict for d in num_str):
            raise ValueError("Input must be a string of digits 0-9")

        morse_sequence = [morse_dict[d] for d in num_str]

        dot_time = 0.2
        dash_time = dot_time * 3
        intra_char_pause = dot_time       # Between dots/dashes
        inter_char_pause = dot_time * 3   # Between digits

        print("Morse Code:", ' '.join(morse_sequence))

        for pattern in morse_sequence:
            for symbol in pattern:
                self.picoLED.on()
                time.sleep(dash_time if symbol == '-' else dot_time)
                self.picoLED.off()
                time.sleep(intra_char_pause)
            time.sleep(inter_char_pause - intra_char_pause)  # Already paused once at end of last symbol

        self.disable_led_voltage()

    def fade_in_jacket(self, flagDict, duration=3):
        """
        Gradually fades in jacket LEDs. Each LED is tied to a specific flag by index.
        Active flags use reverse rainbow colors; inactive ones use the startup color.
        """
        self.enable_led_voltage()
        self.turn_off_leds()
        steps = 30
        step_delay = duration / steps

        # Mapping of flags to fixed LED jacket positions (must match self.jacket order)
        flag_order = ['Easy', 'Authorized', 'Comms', 'Respond', 'Firmware', 'Secured', 'Credits']
        led_positions = self.jacket[:len(flag_order)]

        # Reverse rainbow color sequence (must be at least 7 colors)
        RAINBOW_ORDER = ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'CYAN', 'BLUE', 'VIOLET']
        rainbow_colors = [constants.LED_COLORS[color] for color in RAINBOW_ORDER]

        # Default color for inactive flags
        default_color = constants.LED_COLORS.get(self.startupColor.upper(), constants.LED_COLORS['OFF'])

        for step in range(steps + 1):
            brightness = step / steps

            for i, flag in enumerate(flag_order):
                led_index = led_positions[i] - 1  # Convert to zero-based index for NeoPixel
                is_active = flagDict.get(flag, False)

                base_color = rainbow_colors[i] if is_active else default_color
                fade_color = tuple(int(c * brightness) for c in base_color)
                self.strand[led_index] = self.apply_brightness(fade_color)

            self.strand.write()
            time.sleep(step_delay)

        time.sleep(2)


    def switch_to_eyes(self):
        """Quickly switches to high intensity on the eyes."""
        eye_color = self.apply_brightness(constants.LED_COLORS['WHITE'])

        #for led in self.jacket:
        #    self.strand[led - 1] = self.apply_brightness(constants.LED_COLORS['OFF'])

        for led in self.eyes:
            self.strand[led - 1] = eye_color

        self.strand.write()
        time.sleep(2)

    def interpolate_color(self, start_color, end_color, steps):
        """Linearly interpolate between two RGB colors."""
        return [
            (
                int(start_color[0] + (end_color[0] - start_color[0]) * i / steps),
                int(start_color[1] + (end_color[1] - start_color[1]) * i / steps),
                int(start_color[2] + (end_color[2] - start_color[2]) * i / steps),
            )
            for i in range(steps + 1)
        ]

    def wink(self, dwell=2):
        """Smoothly winks one eye (fades out then in)."""
        eye_color = constants.LED_COLORS['WHITE']
        off_color = constants.LED_COLORS['OFF']
        steps = 10
        delay = 0.03

        #for led in self.jacket:
        #    self.strand[led - 1] = self.apply_brightness(off_color)

        for led in self.eyes:
            self.strand[led - 1] = self.apply_brightness(eye_color)
        self.strand.write()

        wink_led = self.eyes[0]

        for color in self.interpolate_color(eye_color, off_color, steps):
            self.strand[wink_led - 1] = self.apply_brightness(color)
            self.strand.write()
            time.sleep(delay)

        time.sleep(0.1)

        for color in self.interpolate_color(off_color, eye_color, steps):
            self.strand[wink_led - 1] = self.apply_brightness(color)
            self.strand.write()
            time.sleep(delay)
        time.sleep(dwell)

    def party_blink(self, duration=3, interval=0.1):
        """Randomly blinks all LEDs with bright colors for a fun effect."""
        self.enable_led_voltage()

        bright_colors = [c for name, c in constants.LED_COLORS.items() if name != 'OFF']
        all_leds = self.jacket + self.eyes
        end_time = time.time() + duration

        while time.time() < end_time:
            for led in all_leds:
                color = random.choice(bright_colors)
                self.strand[led - 1] = self.apply_brightness(color)

            self.strand.write()
            time.sleep(interval)

        for led in all_leds:
            self.strand[led - 1] = self.apply_brightness(constants.LED_COLORS['OFF'])
        self.strand.write()

    def boot(self, flagDict=None, dwell=constants.LED_BOOT_TIME_S):
        """Runs the full LED sequence."""
        self.fade_in_jacket(flagDict)
        self.switch_to_eyes()
        self.wink(dwell)
        self.turn_off_leds()

    def maker(self, maker):
        """Runs maker's heartbeat sequence."""
        if( maker == 'Caleb'):
            maker_boot_config = constants.CALEB_LED_BOOT
        elif( maker == 'Kyle'):
            maker_boot_config = constants.KYLE_LED_BOOT
        elif( maker == 'Vee'):
            maker_boot_config = constants.VEE_LED_BOOT
        else:
            print("Unknown maker, defaulting to Caleb's boot sequence.")    
            maker_boot_config = constants.CALEB_LED_BOOT
        self.enable_led_voltage()

        all_leds = self.eyes + self.jacket

        for i in range(3):
            for led in all_leds:
                self.strand[led - 1] = self.apply_brightness(maker_boot_config[led-1])
            self.strand.write()
            time.sleep(0.5)
            self.turn_off_leds()
            time.sleep(0.25)