#include <WiFi.h>
#include <HTTPClient.h>

// DEFINITION DES PORTS DE L'ESP32
#define enA 19  // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define in1 18
#define in2 5

#define in3 17
#define in4 16
#define enB 4

int motorSpeedA = 70;
int motorSpeedB = 70;

const char* ssid = "Csar";
const char* password = "Danse";

const String IPROBOT1 = "192.168.4.1";
const int serverPort = 80;

char* URL_recu ="http://192.168.4.1/";


void setup()
{
    // Préparation des sorties moteur
    pinMode(enA, OUTPUT);
    pinMode(enB, OUTPUT);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    pinMode(in3, OUTPUT);
    pinMode(in4, OUTPUT);
    delay(500);

    Serial.begin(115200);
    delay(1000);

    WiFi.mode(WIFI_STA); //Optional
    WiFi.begin(ssid);
    Serial.println("\nConnection");

    while(WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(100);
    }

    Serial.println("\nConnecté à ");
    Serial.println(ssid);
    Serial.print("Addresse IP:");
    Serial.println(WiFi.localIP());

}

void loop() 
{
  if (Serial.available()) {
    // Lecture de la ligne reçue depuis la communication série
    String line = Serial.readStringUntil('\n');

    // Vérification si la ligne contient l'adresse HTTP
    if (line.startsWith("Adresse HTTP")) {
      // Récupération de l'adresse HTTP
      String address = line.substring(line.indexOf("http://"));

      // Utilisation de l'adresse HTTP récupérée
      // Faites ce que vous souhaitez avec l'adresse
      Serial.print("Adresse HTTP récupérée : ");
      Serial.println(address);
    }

}
}
