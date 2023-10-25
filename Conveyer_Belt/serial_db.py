import serial
import mysql.connector
import time
import re
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')
dev = config['dev']

remote = mysql.connector.connect(
	user = dev['user'],
    password = dev['password'],
    port = dev['port'],
	host = dev['host'],
	database = dev['database'])

cursor = remote.cursor()
ser = serial.Serial("/dev/ttyACM0", 9600)

connected = False

while not connected:
    read = ser.readline().decode()
    print(read)
    print(len(read))
    if len(read) == 33:
        connected = True
 
query = "update rfid set in_time=%s, now_section=1, section_update_time=%s where uid=%s"

# print(read)
uid = read.split(":")[-1].upper()
now_ts = time.time()

try:
    cursor.execute(query, (now_ts, now_ts, uid))
    remote.commit()
    ser.write(b'1')  # 성공 알림
except Exception as e:
    print(e)
    ser.write(b'0')  # 실패 알림

ser.close()
cursor.close()
remote.close()