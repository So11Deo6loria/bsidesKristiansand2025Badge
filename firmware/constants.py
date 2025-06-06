# Make sure you don't put sensitive information in comments like this...
# STRING_FLAG = 'DUCK_FIRMW4R3_4_56789'

# LEDS
LED_PIN = 16
LED_ENABLE_PIN = 22
LED_COUNT = 9
LED_BOOT_TIME_S = 7
LED_FRAME_RATE = 60
LED_MAX_INTENSITY = 0.25
LED_COLORS = {
    'OFF':      [  0,   0,   0],
    'RED':      [255,   0,   0],
    'WHITE':    [255, 255, 255],
    'BLUE':     [  0,   0, 255],
    'PINK':     [255, 192, 203],
    'ORANGE':   [255,  30,   0],
    'GOLD':     [255, 180,   0],
    'YELLOW':   [255, 255,   0],
    'TAN':      [255, 105,  50],
    'GREEN':    [  0, 255,   0],
    'MINT':     [  0, 255,  60],
    'CYAN':     [  0, 255, 140],
    'LIGHTBLUE':[  0, 140, 255],
    'PURPLE':   [115,   0, 255],
    'MAGENTA':  [220,   0, 255],
    'VIOLET':    [148,   0, 211],
    'INDIGO':    [ 75,   0, 130]    
}
MAX_BRIGHTNESS = 0.25  # Range from 0.0 (off) to 1.0 (full brightness)
LED_BOOT_TIME_S = 7

CALEB_LED_BOOT = [
    [255, 0, 0],   # RED
    [255, 0, 0],   # RED
    [255, 255, 255], # WHITE
    [255, 255, 255], # WHITE    
    [255, 255, 255], # WHITE    
    [255, 255, 255], # WHITE    
    [255, 255, 255], # WHITE    
    [255, 255, 255], # WHITE    
    [255, 255, 255] # WHITE        
]

KYLE_LED_BOOT = [
    [0, 45, 98],    # BLUE
    [255, 185, 0],  # PACERS GOLD
    [0, 45, 98],    # BLUE
    [255, 185, 0],  # PACERS GOLD
    [0, 45, 98],    # BLUE
    [255, 185, 0],  # PACERS GOLD
    [0, 45, 98],    # BLUE
    [255, 185, 0],  # PACERS GOLD
    [0, 45, 98]     # BLUE
]

VEE_LED_BOOT = [
    [255, 0, 0],   # RED
    [255, 30, 0],  # ORANGE
    [255, 255, 0], # YELLOW
    [0, 255, 0],   # GREEN
    [0, 255, 140], # CYAN
    [0, 140, 255], # LIGHTBLUE
    [115, 0, 255],  # PURPLE
    [220, 0, 255],  # MAGENTA
    [148, 0, 211]   # VIOLET
]

# SCAN 
SCAN_COUNT = 3

# SERIAL
SERIAL_TX_PIN = 12
SERIAL_RX_PIN = 13
BAUD_RATE = 38400
UART_INSTANCE = 0
COMMS_TRANSMISSION_COUNT = 5

# DETECT
V_BATT_DETECT_PIN = 27
V_USB_DETECT_PIN = 28

# INTERRUPT
INTERRUPT_PIN = 1

# FLAGS
TOTAL_FLAGS = 7