import serial
import random

ser = serial.Serial("/dev/ttyACM0", 9600)

list = [b'1', b'2']

ser.write(random.choice(list))