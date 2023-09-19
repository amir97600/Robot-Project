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

    // Spécifiez l'adresse IP statique pour cet ESP32
    IPAddress ip(192, 168, 1, 100);   // Remplacez par l'adresse IP souhaitée
    IPAddress gateway(192, 168, 1, 1);   // Remplacez par l'adresse IP de votre passerelle
    IPAddress subnet(255, 255, 255, 0);  // Remplacez par votre masque de sous-réseau
    WiFi.config(ip, gateway, subnet);
}




