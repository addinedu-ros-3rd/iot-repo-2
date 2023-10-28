#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN);

Servo myservo1;
Servo myservo2;
Servo myservo3;
int agl = 0;
int mode = 0;

unsigned long previousMillis = 0;
const long interval = 1000;

int tagId[3][4] = {{35, 66, 206, 13},
                   {195, 180, 209, 13},
                   {35, 73, 206, 13}};

bool servoActionDone = false; // Flag to track whether servo action has been performed

void setup() {
  Serial.begin(9600);
  SPI.begin();
  //MFRC522 초기화
  rfid.PCD_Init();
  myservo1.attach(5);
  myservo2.attach(6);
  myservo3.attach(7);
  myservo1.write(90);
  myservo2.write(180);
}

void loop() {
  //태그가 접촉 되지 않았거나 ID가 읽혀지지 않았을 때
  if(!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()){
    myservo1.write(90);
    myservo2.write(180);
    Serial.println("Here!");
    // delay(1000);
    return;
  }

  int same = 0;
  //태그의 ID 출력하기(rfid.uid.uidByte[0] ~ rfid.uid.uidByte[3] 출력)
  Serial.print("Card Tag ID: ");
  for (int j=0; j<3; j++){
    same = 0;
    for(byte i=0; i<4; i++){
      Serial.print(rfid.uid.uidByte[i]);
      Serial.print(" ");
      //인식된 태그와 등록된 태그 번호 일치 여부
      if(rfid.uid.uidByte[i] == tagId[j][i]){
        same++; //모두 맞다면 same 변수는 4가 됨.
      }
      if(same == 4){
        if (j == 0) {
          delay(2000);
          Serial.println("태그 ID가 일치합니다.");
          myservo1.write(0);
          myservo2.write(90);
          Serial.println("0도 돌림");
          delay(2000);
        }
      }
    }
  }
}
    
