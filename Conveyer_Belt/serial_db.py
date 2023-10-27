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


# UI에서 오분류를 감지하기 위해 serial read 모듈화
def read_serial():
    return ser.read().decode().strip()


def update_in():
    now_section = int(read.split(":")[0][-1]) + 1
    
    try:
        query = "update rfid set in_time=%s, now_section=%s, section_update_time=%s where uid=%s"
        cursor.execute(query, (now_ts, now_section, now_ts, uid))
        remote.commit()
        
        query = "select category_id from rfid where uid=%s"
        cursor.execute(query, (uid,))
        category_id = cursor.fetchone()[0]
        
        ser.write(bytes(str(category_id), "utf-8"))  # 1, 2, 3
            
    except Exception as e:
        print(e)
        

def update_store():
    now_section = int(read.split(":")[1]) + 1
    
    try:
        query = "update rfid set now_section=%s, section_update_time=%s where uid=%s"
        cursor.execute(query, (now_section, now_ts, uid))
        remote.commit()
    except Exception as e:
        print(e)
        
        
def update_out():
    now_section = 4
    
    try:
        query = "update rfid set now_section=%s, section_update_time=%s, out_time=%s where uid=%s"
        cursor.execute(query, (now_section, now_ts, now_ts, uid))
        remote.commit()
    except Exception as e:
        print(e)


while True:
    inRead = False
    storeRead = False
    outRead = False

    while (not inRead) and (not storeRead) and (not outRead):
        read = ser.readline().decode()
        print(read)
        print(len(read))
        # store:i:uid
        # out:uid
        if len(read) == 33:
            inRead = True
    
    uid = read.split(":")[-1].strip().upper()
    now = datetime.now()
    now_ts = now.strftime('%Y-%m-%d %H:%M:%S')  # 서버의 시간을 보관 = 서버 시간이 UTC이면 UTC로 보관(로컬 테스트 시 한국 시간 저장됨)
    
    # RFID를 읽는 경우와 아닌 경우(출고시각을 받는 경우)를 구분해야 함
    if inRead == True:
        update_in()
            
    elif storeRead == True:
        update_store()
        
    else:
        update_out()

ser.close()
cursor.close()
remote.close()