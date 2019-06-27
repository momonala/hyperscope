// *** Define stepper motor connections, direction and step ***
#define dirPin0 2
#define stepPin0 3

#define dirPin1 4
#define stepPin1 5

// *** Create stepper object. Motor interface type (1st arg) must be set to 1 when using a driver. ***
AccelStepper stepper0(1, stepPin0, dirPin0);
AccelStepper stepper1(1, stepPin1, dirPin1);

void setupMotors(){
  stepper0.setMaxSpeed(500.0);
  stepper1.setMaxSpeed(500.0);
}

void moveSteppers(int xStep, int yStep){
  // move both steppers
  debugArray(STEPPER_SPEED*yStep, STEPPER_SPEED*xStep);
    
  if (xStep != 0){
    stepper0.setSpeed(STEPPER_SPEED*xStep);
    stepper0.runSpeed();
  }

  if (yStep !=0){
    stepper1.setSpeed(STEPPER_SPEED*yStep);
    stepper1.runSpeed();
  }
}
