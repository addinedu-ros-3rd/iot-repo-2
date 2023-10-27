#include <SoftwareSerial.h>

// 블루투스 모듈 포트 설정 ()
#define BT_RXD 2
#define BT_TXD 3
SoftwareSerial BTSerial(BT_RXD, BT_TXD);

void setup()  {
  Serial.begin(9600); // PC에서 모니터링하기 위한 시리얼 통신 시작
  BTSerial.begin(9600);
  Serial.println("Bluetooth initail");
}

void loop() {
  // 블루투스쪽에서 데이터를 수신한 경우, 시리얼 모니터에  수신한 데이터를 출력한다.
  if (BTSerial.available()) {
    Serial.write(BTSerial.read());
  }
  // 시리얼 모니터에서 데이터를 전송한 경우, 전송한 데이터를 블루투스 모듈을 통해 내보낸다
  if (Serial.available()) {
    BTSerial.write(Serial.read());
  }
}
