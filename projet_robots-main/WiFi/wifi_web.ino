#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>

//DEFINITION DES PORTS DE L'ESP32

#define enA 19   // On associe la borne "ENA" du L298N à la pin D10 de l'arduino 
#define in1 18
#define in2 5

#define in3 17
#define in4 16
#define enB 4

int motorSpeedA = 70;
int motorSpeedB = 70;


const char *ssid = "Robot1"; //nom choisi pour le réseau
const char *mdp = "ProjetRobot"; //mot de passe choisi
 
WiFiServer server(80);
 
 
void setup() 
{
  //préparation des sorties moteur
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  delay(500);

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

void loop() 
{
  WiFiClient client = server.available();
 
  if (client) 
  {
    Serial.println("Nouveau client");
    String currentLine = "";
    while (client.connected()) 
    {
      if (client.available()) 
      {
        char c = client.read();
        Serial.write(c);
        if (c == '\n') 
        {
          if (currentLine.length() == 0) 
          {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();
            //ajoute la lettre correspondante à la fin de l'adresse web
            client.print("<CENTER>");
            client.print("<h1>PROJET ROBOT</h1>");
            client.print("<h2>Controle en WiFi</h2>");
            client.print("<hr>");
            client.print("<a href=\"/A\">AVANCER</a>");
            client.print("<p>");
            client.print("<a href=\"/G\">GAUCHE  </a>");
            client.print("<a href=\"/S\">  STOP  </a>");
            client.print("<a href=\"/D\">  DROITE  </a>");
            client.print("</p>");
            client.print("<a href=\"/R\">RECULER</a>");
            client.print("</CENTER>");
            client.println();
            break;
          } 
          else 
          {
            currentLine = "";
          }
        } 
        else if (c != '\r') 
        {
          currentLine += c;
        }
 
      //envoi des signaux aux moteurs

        if (currentLine.endsWith("/A")) //avancer
        {
          digitalWrite(in1, HIGH);
          digitalWrite(in2, LOW); 
          digitalWrite(in3, HIGH);
          digitalWrite(in4, LOW);
          analogWrite(enA, motorSpeedA);
          analogWrite(enB, motorSpeedB);
        }

        if (currentLine.endsWith("/R")) //reculer
        {
          digitalWrite(in1, LOW);
          digitalWrite(in2, HIGH); 
          digitalWrite(in3, LOW);
          digitalWrite(in4, HIGH);
          analogWrite(enA, motorSpeedA);
          analogWrite(enB, motorSpeedB);
        }

        if (currentLine.endsWith("/D")) //aller à droite
        {
          digitalWrite(in1, HIGH);
          digitalWrite(in2, LOW); 
          digitalWrite(in3, LOW);
          digitalWrite(in4, HIGH);
          analogWrite(enA, motorSpeedA);
          analogWrite(enB, motorSpeedB);
        }

        if (currentLine.endsWith("/G")) //aller à gauche
        {
          digitalWrite(in1, LOW);
          digitalWrite(in2, HIGH); 
          digitalWrite(in3, HIGH);
          digitalWrite(in4, LOW);
          analogWrite(enA, motorSpeedA);
          analogWrite(enB, motorSpeedB);
        }

        if (currentLine.endsWith("/S")) //STOP
        {
          digitalWrite(in1, LOW);
          digitalWrite(in2, LOW); 
          digitalWrite(in3, LOW);
          digitalWrite(in4, LOW);
        }
      }
    }
    //Deconnexion du client
    client.stop();
    Serial.println("Client déconnecté.");
  }
}