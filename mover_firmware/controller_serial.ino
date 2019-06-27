// *** Setup serial ***
int incomingInt = 0;
int serialXyArray[2];

void updateSerialArray(){
    if (Serial.available() > 0) {
        incomingInt = Serial.parseInt();
    }
     // TODO parse incomingByte to get x and y vals, one of [-1, 0, 1]
    serialXyArray[0] = incomingInt;
    serialXyArray[1] = incomingInt;
    debugArray(serialXyArray[0], serialXyArray[1]);
}

void moveSteppersViaSerial(){
    updateSerialArray();
    moveSteppers(serialXyArray[0], serialXyArray[1]);
}
