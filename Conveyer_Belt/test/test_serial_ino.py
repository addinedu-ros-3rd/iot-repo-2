import serial
import random

list = [b'1', b'2']

serial.write(random.choice(list))