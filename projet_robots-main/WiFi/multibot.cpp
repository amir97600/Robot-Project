#include <WiFi.h>
#include <ESPAsyncWebServer.h>

const char* ssid = "Votre_SSID";         // Remplacez par le SSID de votre réseau WiFi
const char* password = "Votre_Mot_De_Passe";  // Remplacez par le mot de passe de votre réseau WiFi

AsyncWebServer server(80);  // Créez un objet de type AsyncWebServer


void setup() {
    // Connexion au réseau WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("");
    Serial.print("WiFi connecté à ");
    Serial.println(ssid);
}



void setup() {
    // ...
    
    // Définissez les routes et les gestionnaires de requêtes
    server.on("/commande", HTTP_GET, [](AsyncWebServerRequest* request){
        String commande = request->getParam("commande")->value();
        // Traitez la commande reçue ici (par exemple, contrôlez le mouvement du robot)
        // ...
        request->send(200, "text/plain", "Commande reçue : " + commande);
    });

    // Démarrez le serveur
    server.begin();
}



