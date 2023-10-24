import serial
import mysql.connector
import time
import re
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')
dev = config['dev']

remote = mysql.connector.connect(
	user = dev['host'],
    password = dev['password'],
    port = dev['port'],
	host = dev['host'],
	database = dev['database'])

cursor = remote.cursor()
ser = serial.Serial("/dev/ttyACM0", 9600)

connected = False

while not connected:
    read = ser.readline().decode()
    # print(read)
    # print(len(read))
    if len(read) == 19:
        connected = True
 
insert_query = ("insert into rfid (uid, in_time, tag_info, category_id, now_section, section_update_time) \
            values (%s, %s, %s, %s, %s, %s)")

# print(read)
uid = read.split(":")[0]
now_ts = time.time()
tag_info_base = read.split(":")[1]
tag_info = re.sub('[^a-z]', '', tag_info_base)
now_section = 1  # receiving
section_update_time = now_ts

select_query = ("select id from category where name = %s")
cursor.execute(select_query, (tag_info,))
category_id = cursor.fetchone()[0]

try:
    cursor.execute(insert_query, (uid, now_ts, tag_info, category_id, now_section, section_update_time))
    remote.commit()
    ser.write(b'1')  # 성공 알림
except Exception as e:
    print(e)
    ser.write(b'0')  # 실패 알림

ser.close()
cursor.close()
remote.close()