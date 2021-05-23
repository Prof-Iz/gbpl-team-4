#include <DHT.h>
#include <DHT_U.h> // Sensor Libraries

#include <WiFi.h>
#include <FirebaseESP32.h> //Wifi and Firebase Libararies
#include "cred.h"

FirebaseData fbdo;
FirebaseConfig config_data;
FirebaseAuth auth;
FirebaseJson json; // Firebase database and Json Data Objects

#define DHTPIN 15
#define DHTTYPE DHT11 // Define DHT settings

#define FIREBASE_HOST "https://gpbl-team-04-default-rtdb.firebaseio.com/"
#define API_KEY "AIzaSyBbo4ZGJwHpdDMsElUZgstbXET-R3VIkO4"

 //Enter your WIFI SSID and Password, not 5Ghz



float t, h;

DHT dht(DHTPIN, DHTTYPE);


void setup() {
  Serial.begin(115200);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  dht.begin();
  config_data.host = FIREBASE_HOST;
  config_data.api_key = API_KEY;

  auth.user.email = "iz@test.com";
  auth.user.password = "password";
  Firebase.begin(&config_data, &auth );
  Firebase.reconnectWiFi(true);
  Firebase.setReadTimeout(fbdo, 60000);


}

void loop() {
  t = dht.readTemperature();
  h = dht.readHumidity();
  json.set("temp", t);
  json.set("humidity", h);
  delay(5000);
  Firebase.pushJSON(fbdo,"/MAL01/iz/data/", json);


}
