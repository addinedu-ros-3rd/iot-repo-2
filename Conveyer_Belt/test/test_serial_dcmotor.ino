#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

char state;
#define SS_PIN 10
#define RST_PIN 9
MFRC522 rfid(SS_PIN, RST_PIN);
int in1Pin = 4;
int in2Pin = 3;

Servo servo;
//등록할 태그 ID 배열
int tagId[4] = {35, 66, 206, 13};
//핀번호 및 각도 변수 선언
int servoPin = 7, agl = 0;

void setup() {
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  Serial.begin(9600);
  Serial.println("Arduino ready.");
  SPI.begin();
  //MFRC522 초기화
  rfid.PCD_Init();
  //서보모터 연결 핀 설정 및 각도 초기화
  servo.attach(servoPin);
  servo.write(agl);
}

void loop() {
  if (Serial.available())
  {
    state = Serial.read();
    while (Serial.available())
    {
      Serial.read();
    }

    if (state == '0')
    {
      digitalWrite(in1Pin, LOW);
      digitalWrite(in2Pin, LOW);
      Serial.println("DC Motor Off");
    }
    else
    {
      digitalWrite(in1Pin, LOW);
      digitalWrite(in2Pin, HIGH);
      Serial.println("DC Motor On");
    }
  }
  delay(100);
  
  //태그가 접촉 되지 않았거나 ID가 읽혀지지 않았을 때
  if(!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()){
    agl = 0;
    servo.write(agl);
    delay(300);
    return;
  }
  int same = 0;
  //태그의 ID 출력하기(rfid.uid.uidByte[0] ~ rfid.uid.uidByte[3] 출력)
  Serial.print("Card Tag ID: ");
  for(byte i=0; i<4; i++){
    Serial.print(rfid.uid.uidByte[i]);
    Serial.print(" ");
    //인식된 태그와 등록된 태그 번호 일치 여부
    if(rfid.uid.uidByte[i] == tagId[i]){
      same++; //모두 맞다면 same 변수는 4가 됨.
    }
  }
  Serial.println();
  if(same == 4){
    Serial.println("태그 ID가 일치합니다.");
    agl = 90;
    servo.write(agl);
    delay(1000);
  }
  else{
    Serial.println("등록된 태그 ID가 아닙니다.");
  }
}