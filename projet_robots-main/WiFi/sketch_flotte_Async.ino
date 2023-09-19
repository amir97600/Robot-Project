#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>
#include <ESPAsyncWebSrv.h>

// DEFINITION DES PORTS DE L'ESP32
#define enA 19  // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define in1 18
#define in2 5

#define in3 17
#define in4 16
#define enB 4

int motorSpeedA = 70;
int motorSpeedB = 70;

const char *ssid = "serveurrobot";         // Nom choisi pour le réseau
const char *mdp = "ProjetRobot";     // Mot de passe choisi

AsyncWebServer server(80);

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

  Serial.begin(115200); // Correspond au moniteur inclus dans l'Arduino IDE
  Serial.println();
  Serial.println("Configuration du point d'accès...");

  // Création du point d'accès -> si on veut rajouter un mot de passe : WiFi.softAP(ssid, mdp);
  WiFi.softAP(ssid);
  IPAddress IP_robot = WiFi.softAPIP();
  Serial.print("Adresse IP : ");
  Serial.println(IP_robot);

  server.on("/", HTTP_GET, handleRoot);
  server.on("/A", HTTP_GET, handleCommand);
  server.on("/R", HTTP_GET, handleCommand);
  server.on("/D", HTTP_GET, handleCommand);
  server.on("/G", HTTP_GET, handleCommand);
  server.on("/S", HTTP_GET, handleCommand);

  server.begin();

  Serial.println("WiFi opérationnel !");
}

void loop()
{
  // Rien à faire ici, la gestion des requêtes est gérée de manière asynchrone par le serveur
}

void handleRoot(AsyncWebServerRequest *request)
{
  String webpage = "<html><body><center>";
  webpage += "<h1>PROJET ROBOT</h1>";
  webpage += "<h2>Contrôle en WiFi</h2>";
  webpage += "<hr>";
  webpage += "<a href=\"/A\">AVANCER</a>";
  webpage += "<p>";
  webpage += "<a href=\"/G\">GAUCHE</a>";
  webpage += "<a href=\"/S\">STOP</a>";
  webpage += "<a href=\"/D\">DROITE</a>";
  webpage += "</p>";
  webpage += "<a href=\"/R\">RECULER</a>";
  webpage += "</center></body></html>";

  request->send(200, "text/html", webpage);
}

void handleCommand(AsyncWebServerRequest *request)
{
  String command = request->url();

  if (command.endsWith("/A")) // Avancer
  {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    analogWrite(enA, motorSpeedA);
    analogWrite(enB, motorSpeedB);
  }
  else if (command.endsWith("/R")) // Reculer
  {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    analogWrite(enA, motorSpeedA);
    analogWrite(enB, motorSpeedB);
  }
  else if (command.endsWith("/D")) // Aller à droite
  {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    analogWrite(enA, motorSpeedA);
    analogWrite(enB, motorSpeedB);
  }
  else if (command.endsWith("/G")) // Aller à gauche
  {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    analogWrite(enA, motorSpeedA);
    analogWrite(enB, motorSpeedB);
  }
  else if (command.endsWith("/S")) // STOP
  {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
  }

  request->send(200, "text/plain", "OK");
}
