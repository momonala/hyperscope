// *** Setup joystick ***
const int joyYPin = A0;
const int joyXPin = A1;
const int joyButtonPin = 12;
int joyXyArray[2];

int x_zero;
int y_zero;

int transformJoystick(int data){
  if (data > 20){
    return 1;
  }
  else if (data < -20){
    return -1;
  }
  else {
    return 0;
  }
}

void setupJoyStick(){
  pinMode(joyButtonPin, INPUT_PULLUP);
  // set joystick baseline readings
  x_zero = analogRead(joyXPin);
  y_zero = analogRead(joyYPin);
}

int getJoyButton(){
  return digitalRead(joyButtonPin);  
}

void updateJoyArray(){
      // Update joystick values
    joyXyArray[0] = transformJoystick(analogRead(joyXPin)-x_zero);
    joyXyArray[1] = transformJoystick(analogRead(joyYPin)-y_zero);
//    if (DEBUG){debugArray(analogRead(joyXPin)-x_zero, analogRead(joyYPin)-y_zero);}
    if (DEBUG){debugArray(joyXyArray[0], joyXyArray[1]);}
}

void moveSteppersViaJoystick(){
    updateJoyArray();
    moveSteppers(joyXyArray[0], joyXyArray[1]);
}
