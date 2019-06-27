
const int cameraPin = 13;

void setupCamera(){
  pinMode(cameraPin, OUTPUT);
  digitalWrite(cameraPin, LOW);
}

void takePhoto(int trigger){
  analogWrite(cameraPin, 0);
  if (trigger==0){
    if (DEBUG){Serial.println("Taking photo");}
    analogWrite(cameraPin, 255);
    delay(1000);
  }
}  
