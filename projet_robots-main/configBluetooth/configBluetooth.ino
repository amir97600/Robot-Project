char message;

void setup() {
  // put your setup code here, to run once:
  Serial1.begin(9600);
  Serial.begin(9600);
}

void loop() {
  // Module Bluetooth --> PC
  if (Serial1.available())
  {
    message = Serial1.read();
    Serial.print(message);
  }

  // PC --> Module Bluetooth
  if (Serial.available()) {
    message = Serial.read();
    Serial1.print(message);
  }
}