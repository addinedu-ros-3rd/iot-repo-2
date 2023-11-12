from datetime import datetime
import DB
import Logger

import serial

db = DB()
log = Logger()
ser = serial.Serial("/dev/ttyACM0", 9600)


# UI에서 오분류를 감지하기 위해 serial read 모듈화
def readSerial():
    return ser.read().decode().strip()


def updateIn():
    now_section = int(read.split(":")[0][-1]) + 1
    
    try:
        query = "update rfid set in_time=%s, now_section=%s, section_update_time=%s where uid=%s"
        db.execute(query, (now_ts, now_section, now_ts, uid))
        
        query = "select category_id from rfid where uid=%s"
        db.execute(query, (uid,))
        category_id = db.fetchOne()
        
        ser.write(bytes(str(category_id), "utf-8"))  # 1, 2, 3
            
    except Exception as e:
        log.error(f" DataManager update_in : {e}")
        

def updateStore():
    now_section = int(read.split(":")[1]) + 1
    
    try:
        query = "update rfid set now_section=%s, section_update_time=%s where uid=%s"
        db.execute(query, (now_section, now_ts, uid))
    except Exception as e:
        log.error(f" DataManager update_store : {e}")
        
        
def updateOut():
    now_section = 4
    
    try:
        query = "update rfid set now_section=%s, section_update_time=%s, out_time=%s where uid=%s"
        db.execute(query, (now_section, now_ts, now_ts, uid))
    except Exception as e:
        log.error(f" DataManager update_out : {e}")

msg_complete = False

while not msg_complete:
    in_read = False
    store_read = False
    out_read = False

    while (not in_read) and (not store_read) and (not out_read):
        read = ser.readline().decode()
        print(read)
        # print(len(read))
        # Reader 0: Card UID: 33 F7 D3 0D
        # store:i:uid
        # out:uid
        if len(read) == 33:
            in_read = True
        elif len(read) == 22:
            store_read = True
        elif len(read) == 18:
            outRead = True
    
    uid = read.split(":")[-1].strip().upper()
    now = datetime.now()
    now_ts = now.strftime('%Y-%m-%d %H:%M:%S')  # 서버의 시간을 보관 = 서버 시간이 UTC이면 UTC로 보관(로컬 테스트 시 한국 시간 저장됨)
    
    # RFID를 읽는 경우와 아닌 경우(출고시각을 받는 경우)를 구분해야 함
    if in_read == True:
        updateIn()
            
    elif store_read == True:
        updateStore()
        
    elif out_read == True:
        updateOut()
        
    else:
        log.warning("DataManager Unknown case occured")