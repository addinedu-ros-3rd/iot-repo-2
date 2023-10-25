
#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define RST_PIN         9          // Configurable, see typical pin layout above
#define SS_1_PIN        10         // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 2
#define SS_2_PIN        7          // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 1
#define SS_3_PIN        8

#define Servo_1_PIN     3
#define Servo_2_PIN     4

#define NR_OF_READERS   3
#define NR_OF_SERVOS    4


int DCin1Pin = 6;
int DCin2Pin = 5;
char state;
unsigned long currentMillis;
unsigned long turnedMillis;
const long interval = 7000;
int targetPos = 45;
int initPos = 0;
int pos = initPos;
int speed = 15;

byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN};

int taggedID[] = {0, 0, 0, 0};
int servoMode[] = {0, 0, 0, 0};

MFRC522 mfrc522[NR_OF_READERS];   // Create MFRC522 instance.

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

void setup() {
  pinMode(DCin1Pin, OUTPUT);
  pinMode(DCin2Pin, OUTPUT);
  Serial.begin(9600); // Initialize serial communications with the PC
  while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

  SPI.begin();        // Init SPI bus

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) 
  {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Init each MFRC522 card
    // Serial.print(F("Reader "));
    // Serial.print(reader);
    // Serial.print(F(": "));
    // mfrc522[reader].PCD_DumpVersionToSerial();
  }

  servo1.attach(Servo_1_PIN);
  servo1.write(initPos);
  servo2.attach(Servo_2_PIN);
  servo2.write(initPos);

}

void loop() {
  currentMillis = millis();
  
  if (Serial.available())
  {
    state = Serial.read();
    while (Serial.available())
    {
      Serial.read();
    }

    if (state == 'q')
    {
      digitalWrite(DCin1Pin, LOW);
      digitalWrite(DCin2Pin, LOW);
      Serial.println("DC Motor Off");
    }
    else if (state == 's')
    {
      digitalWrite(DCin1Pin, LOW);
      digitalWrite(DCin2Pin, HIGH);
      Serial.println("DC Motor On");
    }
    else
    {
      Serial.println(state);
    }
  }
  
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
      
      taggedID[reader] = 1;


      // Halt PICC
      mfrc522[reader].PICC_HaltA();
      // Stop encryption on PCD
      mfrc522[reader].PCD_StopCrypto1();
    } //if (mfrc522[reader].PICC_IsNewC
  } //for(uint8_t reader

  if (taggedID[0] == 1)
  {
    if (servoMode[1] == 0)
    {
      if (pos < targetPos)
      {
        pos += speed;
        servo2.write(pos);
      }
      else
      {
        
        servoMode[1] = 1;
        turnedMillis = millis();
      }
    }
    else
    {
      if (currentMillis - turnedMillis >= interval)
      {  
        if (pos > initPos)
        {
          pos -= speed;
          servo2.write(pos);
        }
        else
        {
          servoMode[1] = 0;
          turnedMillis = millis();
          pos = initPos;
          taggedID[0] = 0;
        }
      }
    }
  }
  else
  {
    servo2.write(initPos);
  }



}

/**
 * Helper routine to dump a byte array as hex values to Serial.
 */
void dump_byte_array(byte *buffer, byte bufferSize) 
{
  for (byte i = 0; i < bufferSize; i++) 
  {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}