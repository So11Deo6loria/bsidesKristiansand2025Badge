import machine
import uhashlib
import urandom
import ubinascii
import random

class Helpers:
    def __init__(self):
        self.device_name = None
        self.get_device_name()

    def pad_with_zeros(self, number, width):
        number_str = str(number)
        while len(number_str) < width:
            number_str = '0' + number_str
        return number_str

    def get_device_name(self):
        # Get the unique ID as bytes
        unique_id_bytes = machine.unique_id()
    
        # Calculate the hash of the unique ID using uhashlib
        unique_id_hash = uhashlib.sha256(unique_id_bytes).digest()

        # Convert to a formatted device name
        self.device_name = 'DUCK-' + ubinascii.hexlify(unique_id_hash[-3:]).decode().upper()

        print('Device Name:', self.device_name)

    def generate_password(self, device_id):
        hash_bytes = uhashlib.sha256(device_id.encode()).digest()
        num = int.from_bytes(hash_bytes[:4], 'big') % 100_000_000
        return f"{num:08}"