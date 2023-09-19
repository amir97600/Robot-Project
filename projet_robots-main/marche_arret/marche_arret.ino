//*******************************************************************************//
// Association des entrées du L298N, aux sorties utilisées sur notre Arduino Uno //
//*******************************************************************************//
#define borneENA        10      // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define borneIN1        9       // On associe la borne "IN1" du L298N à la pin D9 de l'arduino
#define borneIN2        8       // On associe la borne "IN2" du L298N à la pin D8 de l'arduino
#define borneIN3        7       // On associe la borne "IN3" du L298N à la pin D7 de l'arduino
#define borneIN4        5      // On associe la borne "IN4" du L298N à la pin D6 de l'arduino
#define borneENB        6      // On associe la borne "ENB" du L298N à la pin D5 de l'arduino
int PWM = 0; // Variable PWM pour la vitesse

//*******//
// SETUP //
//*******//
void setup() {
  Serial.begin(9600);
  // Configuration de toutes les pins de l'Arduino en "sortie" (car elles attaquent les entrées du module L298N)
  pinMode(borneENA, OUTPUT);
  pinMode(borneIN1, OUTPUT);
  pinMode(borneIN2, OUTPUT);
  pinMode(borneIN3, OUTPUT);
  pinMode(borneIN4, OUTPUT);
  pinMode(borneENB, OUTPUT);
//for(int i = 0; i<=3; i++){  
  //Acceleration();
  //Arret_moteur();
//}  
}

//**************************//
// Boucle principale : LOOP //
//**************************//
void loop() {

  // Configuration du L298N en "marche avant", pour le moteur connecté au pont A. Selon sa table de vérité, il faut que :
  digitalWrite(borneIN3, HIGH);                 // L'entrée IN1 doit être au niveau haut
  digitalWrite(borneIN4, LOW);                  // L'entrée IN2 doit être au niveau bas

  // Et on lance le moteur (branché sur le pont A du L298N)
  lancerRotationMoteurPontB();

  // Puis on configure le L298N en "marche arrière", pour le moteur câblé sur le pont A. Selon sa table de vérité, il faut que :
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH);                 // L'entrée IN2 doit être au niveau haut

  // Et on relance le moteur (branché sur le pont A du L298N)
  lancerRotationMoteurPontB();
  
  Acceleration();
  Arret_moteur();
}


//************************************************************************************//
// Fonction : lancerRotationMoteurPontB()                                             //
// But :      Active l'alimentation du moteur branché sur le pont B                   //
//            pendant 2 secondes, puis le met à l'arrêt (au moins 1 seconde)          //
//************************************************************************************//
void lancerRotationMoteurPontB() {
  digitalWrite(borneENB, HIGH);       // Active l'alimentation du moteur 1
  delay(2000);                        // et attend 2 secondes
  
  digitalWrite(borneENB, LOW);        // Désactive l'alimentation du moteur 1
  delay(1000);                        // et attend 1 seconde
}

void Arret_moteur(){
digitalWrite(borneIN3,LOW); // Désactivation de la broche A+ du L293D
digitalWrite(borneIN4,LOW); // Désactivation de la broche A- du L293D
delay( 3000 ); 
}

//************************************************************************************//
// Fonction : AccélérationMoteurPontB()                                               //
// But :      Accélérer                                                               //
//                                                                                    //
//************************************************************************************//
void Acceleration(){
for(PWM;PWM <= 255;PWM++){
delay(10); // on attend 10 ms avant de réincrémenter PWM
digitalWrite(borneIN3,HIGH); // activation du port 3
digitalWrite(borneIN4,LOW); // desactivation du port 4
analogWrite(borneENB,PWM); // envoi du signal PWM sur la borne ENB
Serial.print("Valeur PWM : ");
Serial.print(PWM);
} 
delay(3000); // on attend 3 secondes
Deceleration();
}

////////////////////// Deceleration //////////////////////////////////
void Deceleration(){
for (PWM = 255; PWM >= 0; --PWM){// Boucle pour dminuer PWM de 255 jusqu'à 0
delay( 10 ); // Attendre 10ms avant la prochaine décrémentation du PWM
digitalWrite(borneIN3,HIGH); // Activation de la broche A+ du L293D
digitalWrite(borneIN4,LOW); // Désactivation de la broche A- du L293D
analogWrite(borneENB,PWM); // Envoi du signal PWM sur la sortie analogique 10
Serial.print("Valeur PWM : "); // Affichage sur le moniteur série du texte
Serial.println(PWM); // Affichage sur le moninteur série de la valeur PWM
}
}

