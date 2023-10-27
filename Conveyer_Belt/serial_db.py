from datetime import datetime

import serial
import mysql.connector
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
        # print(len(read))
        if len(read) == 33:
            connected = True
    
    now_section = int(read.split(":")[0][-1]) + 1
    uid = read.split(":")[-1].strip().upper()
    now = datetime.now()
    now_ts = now.strftime('%Y-%m-%d %H:%M:%S')  # 서버의 시간을 보관 = 서버 시간이 UTC이면 UTC로 보관(로컬 테스트 시 한국 시간 저장됨)
    
    try:
        if now_section == 1:  # 센터 최초 입고 시 인식
            query = "update rfid set in_time=%s, now_section=%s, section_update_time=%s where uid=%s"
            cursor.execute(query, (now_ts, now_section, now_ts, uid))
            remote.commit()
            
            query = "select category_id from rfid where uid=%s"
            cursor.execute(query, (uid,))
            category_id = cursor.fetchone()[0]
            
            ser.write(bytes(str(category_id), "utf-8"))  # 1, 2, 3
            
        else:  # 각 창고 보관 시 인식
            query = "update rfid set now_section=%s, section_update_time=%s where uid=%s"
            cursor.execute(query, (now_section, now_ts, uid))
            remote.commit()
            
            query = "select category_id from rfid where uid=%s"
            cursor.execute(query, (uid,))
            category_id = cursor.fetchone()[0]
            
            if now_section != (category_id + 1):
                ser.write(b'w')  # 오분류 알림
        # ser.write(b'1')  # 성공 알림
    except Exception as e:
        print(e)
        ser.write(b'0')  # 실패 알림

ser.close()
cursor.close()
remote.close()