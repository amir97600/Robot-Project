#define enA 10   // On associe la borne "ENA" du L298N à la pin D10 de l'arduino 
#define in1 9
#define in2 8

#define in3 7
#define in4 5
#define enB 6

// penser a changer le nom des fonctions pour lever toute ambiguité 
int motorSpeedA = 70;
int motorSpeedB = 70;

bool forwardsPressed = false;
bool backwardsPressed = false;
bool rightPressed = false;
bool leftPressed = false;

const int FORWARDS_PRESSED = 1;
const int FORWARDS_RELEASED = 2;
const int BACKWARDS_PRESSED = 3;
const int BACKWARDS_RELEASED = 4;

const int RIGHT_PRESSED = 5;
const int RIGHT_RELEASED = 6;
const int LEFT_PRESSED = 7;
const int LEFT_RELEASED = 8;

int incomingByte = 0;

void detectKeyPresses() {
    if (incomingByte == FORWARDS_PRESSED) {
      forwardsPressed = true;
    }
    else if (incomingByte == BACKWARDS_PRESSED) {
      backwardsPressed = true;
    }

    if (incomingByte == FORWARDS_RELEASED) {
      forwardsPressed = false;
    }
    else if (incomingByte == BACKWARDS_RELEASED) {
      backwardsPressed = false;
    }

    if (incomingByte == RIGHT_PRESSED) {
      rightPressed = true;
    }
    else if (incomingByte == LEFT_PRESSED) {
      leftPressed = true;
    }

    if (incomingByte == RIGHT_RELEASED) {
      rightPressed = false;
    }
    else if (incomingByte == LEFT_RELEASED) {
      leftPressed = false;
    }
}




void handlePinOutputs() {
  
  if (forwardsPressed == true) { // w  va en avant 
    forword();
  }
  /*else {
    Stop();
  }*/

  else if (backwardsPressed == true) { // s va en arriere 
    backword();
  }
  /*else {
    Stop();
  }*/

  else if (rightPressed == true) { // d tourne a droite
    turnRight();
  }
  /*else {
    Stop();
  }*/

  else if (leftPressed == true) { // a va a gauche
    turnLeft();
  }
  else {
    Stop();
  }
  
}

void setup() {
pinMode(enA, OUTPUT);
pinMode(enB, OUTPUT);
pinMode(in1, OUTPUT);
pinMode(in2, OUTPUT);
pinMode(in3, OUTPUT);
pinMode(in4, OUTPUT);
Serial1.begin(9600);
Serial.begin(9600); // Default communication rate of the Bluetooth module
delay(500);
}




void backword(){Serial.println("forword");
digitalWrite(in1, HIGH);
digitalWrite(in2, LOW); 
digitalWrite(in3, HIGH);
digitalWrite(in4, LOW);
}

void forword(){Serial.println("backword");
digitalWrite(in1, LOW);
digitalWrite(in2, HIGH); 
digitalWrite(in3, LOW);
digitalWrite(in4, HIGH);
}

void turnLeft(){Serial.println("turnRight");
digitalWrite(in1, HIGH);
digitalWrite(in2, LOW); 
digitalWrite(in3, LOW);
digitalWrite(in4, HIGH);
}

void turnRight(){Serial.println("turnLeft");
digitalWrite(in1, LOW);
digitalWrite(in2, HIGH); 
digitalWrite(in3, HIGH);
digitalWrite(in4, LOW);
}

void Stop(){
digitalWrite(in1, LOW);
digitalWrite(in2, LOW); 
digitalWrite(in3, LOW);
digitalWrite(in4, LOW);
Serial.println("stop");
}





void loop() {
  // Default value - no movement when the Joystick stays in the center
  //xAxis = 140;
  //yAxis = 140;

  // Read the incoming data from the Smartphone Android App
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    detectKeyPresses();
    handlePinOutputs();
    analogWrite(enA, motorSpeedA); // Send PWM signal to motor A
    analogWrite(enB, motorSpeedB); // Send PWM signal to motor B 

  }
  
 
}
