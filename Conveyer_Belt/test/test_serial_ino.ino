
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

void setup()
{
	Serial.begin(9600);

  servo1.attach(Servo_1_PIN);
  servo1.write(initPos);
  servo2.attach(Servo_2_PIN);
  servo2.write(initPos);
}

void loop()
{
  while (Serial.available())
  {
    char state = Serial.read();

    if (state == '0')
    {
      Serial.println("servo back to initial state");
      servo1.write(0);
    }

    if (state == '1')
    {
      Serial.println("move servo1");
      for (pos = 10; pos <= 130; pos += 1) {
        servo1.write(pos);
        delay(15);
      }
      delay(1000);
      for (pos = 130; pos >= 0; pos -= 1) {
        servo1.write(pos);
        delay(15);
      }
    }

    if (state == '2')
    {
      Serial.println("move servo2");
      servo2.write(130);
    }
  }
}