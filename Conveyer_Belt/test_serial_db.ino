const int G_LED = 8;
const int R_LED = 9;
const int LED_ON = 255;

char state;
int sent;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (sent == 0)
  {
    Serial.println("23 42 CE 0D:seoul");  // uid 보내기
    sent = 1;
  }

  while (Serial.available())
  {
    state = Serial.read();

    if (state == '1')
    {
      analogWrite(G_LED, LED_ON);
      analogWrite(R_LED, 0);
    }
    else
    {
      analogWrite(R_LED, LED_ON);
      analogWrite(G_LED, 0);
    }
  }
}