
#include<Servo.h>

Servo x;
int width = 1280, height = 720;  // total resolution of the video
int xpos = 90;  // initial positions of both Servos
void setup() {

  Serial.begin(9600);
  x.attach(8);

  x.write(xpos);
}
const int angle = 20;   // degree of increment or decrement

void loop() {
  if (Serial.available() > 0)
  {
    int x_mid;
    if (Serial.read() == 'X')
    {
      x_mid = Serial.parseInt();  // read center x-coordinate

    }

      int val= map(x_mid, 80,1100,0,180);
      x.write(val);

  }
}
