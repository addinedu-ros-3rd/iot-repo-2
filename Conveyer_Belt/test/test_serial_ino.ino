void setup()
{
	Serial.begin(9600);
}

void loop()
{
	while (Serial.available())
    {
      char state = Serial.read();
      if (state == '1')
      {
        Serial.println("move servo1");
      }
      if (state == '2')
      {
        Serial.println("move servo2");
      }
    }
}