#include <Servo.h>

Servo motor_horizontal;  // create servo object to control a servo
Servo motor_vertical;
String motor = "";
int current_horizontal_position = 90;
int current_vertical_position = 90;
// twelve servo objects can be created on most boards

int pos = 90;    // variable to store the servo position

void setup() {
  Serial.begin(9600);
  while (! Serial); // Wait untilSerial is ready - Leonardo
  Serial.println("servo encendido");
  motor_horizontal.attach(9);// x
  motor_vertical.attach(10);//y
  motor_horizontal.write(pos);
  motor_vertical.write(pos);
  delay(5000);
  
}

void loop() {
  
  while(!Serial.available());
  motor = Serial.readString();
  motor.trim();
  while(!Serial.available());
  pos = Serial.readString().toInt();
  if(motor == "x"){
    while (current_horizontal_position != pos){
      if(current_horizontal_position < pos){
        motor_horizontal.write(current_horizontal_position++);
      }else{
        motor_horizontal.write(current_horizontal_position--);
      }
        delay(10);
    }

  }else if(motor == "y"){
    while (current_vertical_position != pos){
      if(current_vertical_position < pos){
        motor_vertical.write(current_vertical_position++);
      }else{
        motor_vertical.write(current_vertical_position--);
      }
        delay(10);
    }
  }
  
  delay(100);
  
}
