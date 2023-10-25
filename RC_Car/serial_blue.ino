#include <SoftwareSerial.h>

// 블루투스 모듈 포트 설정 (HM10)
#define BT_RXD 2
#define BT_TXD 3
SoftwareSerial BTSerial(BT_RXD, BT_TXD);

void setup() {
  Serial.begin(9600);  // PC에서 모니터링하기 위한 시리얼 통신 시작
  BTSerial.begin(9600);
  Serial.println("Bluetooth initial");
}

void loop() {
  if (BTSerial.available()) {
    Serial.write(BTSerial.read());
  }
  if (Serial.available()) {
    BTSerial.write(Serial.read());
  }
}