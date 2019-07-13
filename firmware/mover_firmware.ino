#include <AccelStepper.h>

bool DEBUG = true;
signed int STEPPER_SPEED = 300; // steps per iteration
unsigned int BAUDRATE = 9600;
unsigned int INPUT_TYPE = 0; // 0 joystick, 1 Serial

void setup(){
  setupJoyStick();
  setupMotors();
  Serial.begin(BAUDRATE);
  Serial.setTimeout(10);
  while (!Serial){};
}

void loop(){
  if (INPUT_TYPE==0){
    moveSteppersViaJoystick();
    takePhoto(getJoyButton());
  }
  if (INPUT_TYPE==1){
    moveSteppersViaSerial();
  }  
}
