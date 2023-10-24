import serial
import mysql.connector
import time
import re

remote = mysql.connector.connect(
	user='test', password='1234',
    port=3306,
	host='database-1.cktq4evzprzg.ap-northeast-2.rds.amazonaws.com',
	database='conveyor')

cursor = remote.cursor()
ser = serial.Serial("/dev/ttyACM0", 9600)

connected = False

while not connected:
	read = ser.readline().decode()
	connected = True
 
insert_query = ("insert into rfid (uid, in_time, tag_info, category_id, now_section, section_update_time) \
            values (%s, %s, %s, %s, %s, %s)")

print(read)
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