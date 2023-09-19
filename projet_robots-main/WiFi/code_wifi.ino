#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>

const char *ssid = "Robot1"; //nom choisi pour le réseau
const char *mdp = "ProjetRobot"; //mot de passe choisi
 
WiFiServer server(80);
 
 
void setup() {
  Serial.begin(115200); //correspond au moniteur inclu dans arduino IDE
  Serial.println();
  Serial.println("Configuration du point d'accès...");
 
  //Création du point d'accès -> s'il on veut rajouter un mdp: WiFi.softAP(ssid, mdp);
  WiFi.softAP(ssid);
  IPAddress IP_robot = WiFi.softAPIP();
  Serial.print("Addresse IP: ");
  Serial.println(IP_robot);
  server.begin();
 
  Serial.println("WiFi oppérationnel!");
}
 
void loop() {}