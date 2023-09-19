

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}

void TurnRight(int Power){
  analogWrite(MotorForward1,Power);
  analogWrite(MotorReverse1,0);
  analogWrite(MotorForward2,0);
  analogWrite(MotorReverse2,Power);
  analogWrite(MotorForward3,Power);
  analogWrite(MotorReverse3,0);
  analogWrite(MotorForward4,0);
  analogWrite(MotorReverse4,Power);
}

void TurnLeft(int Power){
  analogWrite(MotorForward1,0);
  analogWrite(MotorReverse1,Power);
  analogWrite(MotorForward2,Power);
  analogWrite(MotorReverse2,0);
  analogWrite(MotorForward3,0);
  analogWrite(MotorReverse3,Power);
  analogWrite(MotorForward4,Power);
  analogWrite(MotorReverse4,0);
}
