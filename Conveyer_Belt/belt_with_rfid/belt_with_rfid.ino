#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <stdio.h>
#include <stdlib.h>

#define RST_PIN         9          // Configurable, see typical pin layout above
#define SS_1_PIN        10         // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 2
#define SS_2_PIN        8          // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 1
#define SS_3_PIN        7
// #define SS_4_PIN        4

#define Servo_1_PIN     A2
#define Servo_2_PIN     A1
#define Servo_3_PIN     A3
#define Servo_4_PIN     A4

#define NR_OF_READERS   3
#define NR_OF_SERVOS    2
#define ARRAYSIZE       20

int DCin1Pin = 6;
int DCin2Pin = 5;
char state;
unsigned long currentMillis;
unsigned long turnedMillis1;
unsigned long turnedMillis2;
const long interval1 = 3500;
const long interval2 = 7000;
int targetPos1 = 135;
int targetPos2 = 30;
int initPos1 = 180;
int initPos2 = 0;
int servoPos1 = initPos1;
int servoPos2 = initPos2;
int speed1 = -10;
int speed2 = 10;

byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN};

int received[] = {0, 0};

int received_1 = 0;
int received_2 = 0;

int servoMode[] = {0, 0, 0, 0};

int servoMode_1 = 0;
int servoMode_2 = 0;

int numTaggedUID1 = 0;
int numTaggedUID2 = 0;
int numTaggedUID3 = 0;

MFRC522 mfrc522[NR_OF_READERS];   // Create MFRC522 instance.

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

typedef struct Node 
{
    String data;
    struct Node *next;
}Node;
 
 
typedef struct Queue 
{
    Node *front;
    Node *rear; 
    int count; // 큐 안의 노드 개수  
};
 
void initQueue(Queue *queue)
{
    queue->front = queue->rear = NULL; 
    queue->count = 0;    // 큐 안의 노드 개수를 0으로 설정
}
 
int isEmpty(Queue *queue)
{
    return queue->count == 0;    // 큐안의 노드 개수가 0이면 빈 상태
}
 
void enqueue(Queue *queue, int data)
{
    Node *newNode = (Node *)malloc(sizeof(Node)); // newNode 생성
    newNode->data = data;
    newNode->next = NULL;
 
    if (isEmpty(queue))    // 큐가 비어있을 때
    {
        queue->front = newNode;       
    }
    else    // 비어있지 않을 때
    {
        queue->rear->next = newNode;    //맨 뒤의 다음을 newNode로 설정
    }
    queue->rear = newNode;    //맨 뒤를 newNode로 설정   
    queue->count++;    //큐안의 노드 개수를 1 증가
}
 
String dequeue(Queue *queue)
{
    String data;
    Node *ptr;
    ptr = queue->front;    //맨 앞의 노드 ptr 설정 
    data = ptr->data;    // return 할 데이터  
    queue->front = ptr->next;    //맨 앞은 ptr의 다음 노드로 설정
    free(ptr);    // ptr 해제 
    queue->count--;    //큐의 노드 개수를 1 감소
    
    return data;
}
 
int main(void)
{
    int i;
    Queue queue;
 
    initQueue(&queue);//큐 초기화
    for (i = 1; i <= 10; i++) 
    {
        enqueue(&queue, i);
    }
    while (!isEmpty(&queue))    // 큐가 빌 때까지 
    {
        printf("%d ", dequeue(&queue));    //큐에서 꺼내온 값 출력
    }
    printf("\n");
    return 0;
}


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
  digitalWrite(DCin1Pin, LOW);
  digitalWrite(DCin2Pin, LOW);
  servo1.attach(Servo_1_PIN);
  servo1.write(initPos1);
  servo2.attach(Servo_2_PIN);
  servo2.write(initPos2);
  // servo3.attach(Servo_3_PIN);
  // servo3.write(180);
  // servo4.attach(Servo_4_PIN);
  // servo4.write(90);
  
}

void loop() {

  currentMillis = millis();
  
  while (Serial.available())
  {
    state = Serial.read();

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
    // if ((int)state >= 1 && (int)state <= 2)
    else if (state == '1')
    {
      received_1 = 1;
      Serial.print("received_1: ");
      Serial.println(received_1);
    }
    else if (state == '2')
    {
      received_2 = 1;
      Serial.print("received_2: ");
      Serial.println(received_2);
    }
  }

  runServo1();
  runServo2();
  
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
    } //if (mfrc522[reader].PICC_IsNewC
  } //for(uint8_t reader

  // while (true)
  // {
  //   servo1.write(90);
  //   servo2.write(90);
  //   delay(500);
  //   servo1. write(0);
  //   servo2. write(0);
  //   delay(500);
  //   break;
  // }
  

}

int runServo1()
{
  if (received_1 == 1)
  {
    if (servoMode_1 == 0)
    {
      if (servoPos1 > targetPos1)
      {
        servoPos1 += speed1;
        servo1.write(servoPos1);
      }
      else
      {
        servoMode_1 = 1;
        turnedMillis1 = millis();
      }
    }
    else
    {
      if (currentMillis - turnedMillis1 >= interval1)
      {  
        if (servoPos1 < initPos1)
        {
          servoPos1 -= speed1;
          servo1.write(servoPos1);
        }
        else
        {
          servoMode_1 = 0;
          turnedMillis1 = millis();
          servoPos1 = initPos1;
          received_1 = 0;
        }
      }
    }
  }
  else
  {
    servo1.write(initPos1);
  }
}


int runServo2()
{
  if (received_2 == 1)
  {
    if (servoMode_2 == 0)
    {
      if (servoPos2 < targetPos2)
      {
        servoPos2 += speed2;
        servo2.write(servoPos2);
      }
      else
      {
        servoMode_2 = 1;
        turnedMillis2 = millis();
      }
    }
    else
    {
      if (currentMillis - turnedMillis2 >= interval2)
      {  
        if (servoPos2 > initPos2)
        {
          servoPos2 -= speed2;
          servo2.write(servoPos2);
        }
        else
        {
          servoMode_2 = 0;
          turnedMillis2 = millis();
          servoPos2 = initPos2;
          received_2 = 0;
        }
      }
    }
  }
  else
  {
    servo2.write(initPos2);
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
    String
    Serial.print(buffer[i], HEX);
  }
}


