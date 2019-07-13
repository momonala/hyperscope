// *** Setup joystick ***
const int joyYPin = A0;
const int joyXPin = A1;
const int joyButtonPin = 12;
int joyXyArray[2];

int transformJoystick(int data){
  // method to fit joystick value to [0-100], then thresh again to [-1, 0, 1]
  int scaled_0_100 = (int)(((float)data) * 100 /1048);
  if (scaled_0_100 > 55){
    return 1;
  }
  else if (scaled_0_100 < 45){
    return -1;
  }
  else {
    return 0;
  }
}

void setupJoyStick(){
  pinMode(joyButtonPin, INPUT_PULLUP); 
}

int getJoyButton(){
  return digitalRead(joyButtonPin);  
}

void updateJoyArray(){
      // Update joystick values
    joyXyArray[0] = transformJoystick(analogRead(joyXPin));
    joyXyArray[1] = transformJoystick(analogRead(joyYPin));
    //debugArray(joyXyArray[0], joyXyArray[1]);
}

void moveSteppersViaJoystick(){
    updateJoyArray();
    moveSteppers(joyXyArray[0], joyXyArray[1]);
}
