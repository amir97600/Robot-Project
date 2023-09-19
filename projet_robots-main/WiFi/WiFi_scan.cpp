#include "WiFi.h"

void setup()
{
	Serial.begin(115200);
	
	//Déconnection des réseaux précédents pour partir de 0

	WiFi.mode(WIFI_STA);
	WiFi.disconnect();
	delay(100);

	Serial.println("Initialisation: OK");
}

void loop()
{
	Serial.println("Recherche en cours...");
	int n = WiFi.scanNetworks();//retourne le nombre de network trouvés
	Serial.println("Recherche terminée.");
	if (n==0)
	{
		Serial.println("Aucun réseau n'a été trouvé");
	}
	else
	{
		Serial.println("Nombre de réseaux trouvés:");
        Serial.println(n);
		Serial.println("Réseaux disponibles : ");
		//Affichage des différents réseaux
		for (int i=0; i<n; n++)
		{
			Serial.println(i + 1);
			Serial.println(": ");
			Serial.println(WiFi.SSID(i));
			Serial.println(" (");
			Serial.println(WiFi.RSSI(i)); //force du signal (chiffre negatif)
			Serial.println(")"); 
			Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*"); //si il est ouvert ou avec un mdp (affiche *)
			delay(10);
		}
	}
	Serial.println("");
	//refait un scan après 5sec
	delay(5000);
}