// *** Setup joystick ***
const int joyYPin = A0;
const int joyXPin = A1;
const int joyButtonPin = 12;
int joyXyArray[2];

int x_baseline;
int y_baseline;

int transformJoystick(int j_reading){
    //tranform the joystick value from 10 bit to [-1, 0, 1] for motor control
    if (j_reading > 20){return 1;}
    else if (j_reading < -20){return -1;}
    else {return 0;}
}

void setupJoyStick(){
    // set joystick baseline readings
    pinMode(joyButtonPin, INPUT_PULLUP);
    x_baseline = analogRead(joyXPin);
    y_baseline = analogRead(joyYPin);
}

int getJoyButton(){
  return digitalRead(joyButtonPin);  
}

void updateJoyArray(){
    // Update joystick values
    joyXyArray[0] = transformJoystick(analogRead(joyXPin)-x_baseline);
    joyXyArray[1] = transformJoystick(analogRead(joyYPin)-y_baseline);
    if (DEBUG){debugArray(joyXyArray[0], joyXyArray[1]);}
}

void moveSteppersViaJoystick(){
    updateJoyArray();
    moveSteppers(joyXyArray[0], joyXyArray[1]);
}
