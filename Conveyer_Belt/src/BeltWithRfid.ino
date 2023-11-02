#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define RST_PIN         9          
#define SS_1_PIN        10
#define SS_2_PIN        8
#define SS_3_PIN        7

#define Servo_1_PIN     A2
#define Servo_2_PIN     A1
#define Servo_3_PIN     A3
#define Servo_4_PIN     A4

#define NR_OF_READERS   3
#define NR_OF_SERVOS    2
#define NR_OF_CATE      3


const int DC_PIN_1 = 6;
const int DC_PIN_2 = 5;
const long INTERVAL_1 = 3500;
const long INTERVAL_2 = 7000;
const long INTERVAL_3 = 10000;
const int TARGET_POS_1 = 135;
const int TARGET_POS_2 = 30;
const int INIT_POS_1 = 180;
const int INIT_POS_2 = 0;
const int SPEED_1 = -10;
const int SPEED_2 = 10;

char state;
unsigned long currentMillis;
unsigned long turnedMillis1;
unsigned long turnedMillis2;
unsigned long checkedMillis;
int servoPos1 = INIT_POS_1;
int servoPos2 = INIT_POS_2;

byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN};

int received1 = 0;
int received2 = 0;
int received3 = 0;
int servoMode1 = 0;
int servoMode2 = 0;

MFRC522 mfrc522[NR_OF_READERS];   // Create MFRC522 instance.

Servo servo1;
Servo servo2;

// to update time when stor
const int QUEUE_SIZE = 10;
String uidQueue[QUEUE_SIZE];
int itemCount = 0;
int front = 0;
int rear = -1;


void setup() {
  pinMode(DC_PIN_1, OUTPUT);
  pinMode(DC_PIN_2, OUTPUT);
  Serial.begin(9600); // Initialize serial communications with the PC
  while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

  SPI.begin();        // Init SPI bus

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) 
  {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Init each MFRC522 card
  }

  digitalWrite(DC_PIN_1, LOW);
  digitalWrite(DC_PIN_2, LOW);
  servo1.attach(Servo_1_PIN);
  servo1.write(INIT_POS_1);
  servo2.attach(Servo_2_PIN);
  servo2.write(INIT_POS_2);
  
}

void loop() {

  currentMillis = millis();
  
  while (Serial.available())
  {
    state = Serial.read();

    if (state == 'q')
    {
      digitalWrite(DC_PIN_1, LOW);
      digitalWrite(DC_PIN_2, LOW);
      Serial.println("DC Motor Off");
    }
    else if (state == 's')
    {
      digitalWrite(DC_PIN_1, LOW);
      digitalWrite(DC_PIN_2, HIGH);
      Serial.println("DC Motor On");
    }
    else if (state == '1')
    {
      received1 = 1;
      // Serial.print("received1: ");
      // Serial.println(received1);
    }
    else if (state == '2')
    {
      received2 = 1;
      // Serial.print("received2: ");
      // Serial.println(received2);
    }
    else if (state == '3')
    {
      received3 = 1;
      checkedMillis = millis();
    }
  }

  runServo1();
  runServo2();
  printOutTime();
  
  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) 
  {
    // Look for new cards

    if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial()) 
    {
      Serial.print(F("Reader "));
      Serial.print(reader);
      // Show some details of the PICC (that is: the tag/card)
      Serial.print(F(": Card UID:"));
      dump_byte_array(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size);
      Serial.println("");

      // Halt PICC
      mfrc522[reader].PICC_HaltA();
      // Stop encryption on PCD
      mfrc522[reader].PCD_StopCrypto1();
    }
  }

}

void runServo1()
{
  if (received1 == 1)
  {
    if (servoMode1 == 0)
    {
      if (servoPos1 > TARGET_POS_1)
      {
        servoPos1 += SPEED_1;
        servo1.write(servoPos1);
      }
      else
      {
        servoMode1 = 1;
        turnedMillis1 = millis();
      }
    }
    else
    {
      if (currentMillis - turnedMillis1 >= INTERVAL_1)
      {  
        if (servoPos1 < INIT_POS_1)
        {
          servoPos1 -= SPEED_1;
          servo1.write(servoPos1);
          if (servoPos1 == INIT_POS_1)
          {
            Serial.println("store:1:" + dequeue());
          }
        }
        else
        {
          servoMode1 = 0;
          turnedMillis1 = millis();
          servoPos1 = INIT_POS_1;
          received1 = 0;
        }
      }
    }
  }
  else
  {
    servo1.write(INIT_POS_1);
  }
}


void runServo2()
{
  if (received2 == 1)
  {
    if (servoMode2 == 0)
    {
      if (servoPos2 < TARGET_POS_2)
      {
        servoPos2 += SPEED_2;
        servo2.write(servoPos2);
      }
      else
      {
        servoMode2 = 1;
        turnedMillis2 = millis();
      }
    }
    else
    {
      if (currentMillis - turnedMillis2 >= INTERVAL_2)
      {  
        if (servoPos2 > INIT_POS_2)
        {
          servoPos2 -= SPEED_2;
          servo2.write(servoPos2);
          if (servoPos2 == INIT_POS_2)
          {
            Serial.println("store:2:" + dequeue());
          }
        }
        else
        {
          servoMode2 = 0;
          turnedMillis2 = millis();
          servoPos2 = INIT_POS_2;
          received2 = 0;
        }
      }
    }
  }
  else
  {
    servo2.write(INIT_POS_2);
  }
}


void printOutTime()
{
  if (received3 == 1)
  {
    if (currentMillis - checkedMillis >= INTERVAL_3)
    {
      Serial.println("out:" + dequeue());
      received3 = 0;
    }
  }
}


/**
 * Helper routine to dump a byte array as hex values to Serial.
 */
void dump_byte_array(byte *buffer, byte bufferSize) 
{
  String uid = "";

  for (byte i = 0; i < bufferSize; i++) 
  {
    uid += String(buffer[i] < 0x10 ? " 0" : " ");
    uid += String(buffer[i], HEX);
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }

  // Serial.println();
  // Serial.println(uid);
  // Serial.println(String(uid.length()));
  enqueue(uid);
}

void enqueue(String data) {
  if (itemCount < QUEUE_SIZE) {
    rear = (rear + 1) % QUEUE_SIZE;
    uidQueue[rear] = data;
    itemCount++;
  } else {
    // Serial.println("Queue is full. Cannot enqueue.");
  }
}

String dequeue() {
  if (itemCount > 0) {
    String data = uidQueue[front];
    front = (front + 1) % QUEUE_SIZE;
    itemCount--;
    return data;
  } else {
    // Serial.println("Queue is empty. Cannot dequeue.");
    return "";
  }
}