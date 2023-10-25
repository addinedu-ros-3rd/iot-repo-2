from datetime import datetime

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

while True:
    connected = False

    while not connected:
        read = ser.readline().decode()
        print(read)
        print(len(read))
        if len(read) == 33:
            connected = True
    
    now_section = int(read.split(":")[0][-1]) + 1
    uid = read.split(":")[-1].strip().upper()
    now = datetime.now()
    now_ts = now.strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        if now_section == 1:
            query = "update rfid set in_time=%s, now_section=%s, section_update_time=%s where uid=%s"
            cursor.execute(query, (now_ts, now_section, now_ts, uid))
            remote.commit()
            
            query = "select category_id from rfid where uid=%s"
            cursor.execute(query, (uid,))
            category_id = cursor.fetchone()[0]
            
            ser.write(category_id.to_bytes())  # 1, 2, 3
            
        else:
            query = "update rfid set now_section=%s, section_update_time=%s where uid=%s"
            cursor.execute(query, (now_section, now_ts, uid))
            remote.commit()
        # ser.write(b'1')  # 성공 알림
    except Exception as e:
        print(e)
        ser.write(b'0')  # 실패 알림

ser.close()
cursor.close()
remote.close()