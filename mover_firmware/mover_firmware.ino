#include <AccelStepper.h>

// ---------------------- GLOBALS --------------------------
bool debug = false; 

// *** Define stepper motor connections, direction and step ***
#define dirPin0 2
#define stepPin0 3

#define dirPin1 4
#define stepPin1 5

// *** Create stepper object. Motor interface type (1st arg) must be set to 1 when using a driver. ***
AccelStepper stepper0(1, stepPin0, dirPin0);
AccelStepper stepper1(1, stepPin1, dirPin1);

int STEPPER_SPEED = 70; // steps per iteration

// *** Setup joystick ***
const int joy_y_pin = A0;                                               
const int joy_x_pin = A1;
const int switchPin = 13;
int joy_xy_array[2]; 


// ---------------------- METHODS --------------------------
int transform_joystick(int data) {
  // method to fit joystick value to [0-100], then thresh again to [-1, 0, 1]
  int scaled_0_100 = (int)(((float)data) * 100 /1048);
  if (scaled_0_100 > 55){return 1;}
  else if (scaled_0_100 < 45){return -1;}
  else {return 0;}
 }

void update_joy_array(){
      // Update joystick values
    joy_xy_array[0] = transform_joystick(analogRead(joy_x_pin));
    joy_xy_array[1] = transform_joystick(analogRead(joy_y_pin));
    if (debug){
      Serial.print("Joystick Reading: X: "); Serial.print(joy_xy_array[0]);
      Serial.print(" Y: "); Serial.print(joy_xy_array[1]); Serial.println();
    }
}


void move_steppers(int x_step, int y_step){
  // move both steppers
  if (x_step != 0){
    stepper0.setSpeed(STEPPER_SPEED*x_step);
    stepper0.runSpeed();
  }

  if (y_step !=0){
    stepper1.setSpeed(STEPPER_SPEED*y_step);
    stepper1.runSpeed();
  }
}


// ---------------------- SETUP --------------------------
void setup()
  {
    stepper0.setCurrentPosition(0);
    stepper0.setMaxSpeed(200.0);
    
    stepper1.setCurrentPosition(0);
    stepper1.setMaxSpeed(200.0);

    Serial.begin(9600);
    pinMode(switchPin, INPUT_PULLUP);
  }

// ---------------------- LOOP --------------------------
void loop()
  {
    update_joy_array();
    move_steppers(joy_array[0], joy_array[1]);    
  }
