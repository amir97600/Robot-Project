char message;

#define borneIN4 7
#define borneIN3 5
#define borneENB 6 

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
    switch(message){

      case '1' :
              digitalWrite(borneIN3, HIGH);                 // L'entrée IN1 doit être au niveau haut
              digitalWrite(borneIN4, LOW);
              lancerRotationMoteurPontB();
              break; 
              
      case '2' :
            digitalWrite(borneIN3, LOW);                 // L'entrée IN1 doit être au niveau haut
            digitalWrite(borneIN4, HIGH);
            lancerRotationMoteurPontB();
            break;   
              }
  }

  // PC --> Module Bluetooth
  if (Serial.available()) {
    message = Serial.read();
    Serial1.print(message);
  }
}

void lancerRotationMoteurPontB() {
  digitalWrite(borneENB, HIGH);       // Active l'alimentation du moteur 1
  delay(2000);                        // et attend 2 secondes
  
  digitalWrite(borneENB, LOW);        // Désactive l'alimentation du moteur 1
  delay(1000);                        // et attend 1 seconde
}