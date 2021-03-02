#include <DHT.h>
#include <DHT_U.h> // Sensor Libraries

#include <WiFi.h>
#include <Firebase_ESP_Client.h>//Wifi and Firebase Libararies

#include "time.h"

FirebaseData fbdo;
FirebaseConfig config_data;
FirebaseAuth auth;
// Firebase database and Json Data Objects

#define DHTPIN 15
#define DHTTYPE DHT11 // Define DHT settings

#define FIREBASE_HOST "https://gpbl-team-04-default-rtdb.firebaseio.com/"
#define API_KEY "AIzaSyBbo4ZGJwHpdDMsElUZgstbXET-R3VIkO4"

#define WIFI_SSID "abu@unifi"
#define WIFI_PASSWORD "izdhan.iyaa.abu" //Enter your WIFI SSID and Password, not 5Ghz

char time_stamp[20];


float t, h;
int resp;
DHT dht(DHTPIN, DHTTYPE);

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 28800; //adjust to time of you region
const int   daylightOffset_sec = 0;

int get_time() {
  struct tm timeinfo;
  time_t timeSinceEpoch;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return 10;
  } else {
    
//    strftime(time_stamp, 20, "MAL01/iz/%d", timeSinceEpoch);
    sprintf(time_stamp, "MAL01/iz/%d", time(&timeSinceEpoch));
    Serial.println(time_stamp);
    return 20;
  }
}

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

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  resp = get_time();

  Firebase.begin(&config_data, &auth );
  Firebase.reconnectWiFi(true);
  Firebase.RTDB.setReadTimeout(&fbdo, 60000);
  fbdo.setResponseSize(8192);


}

void loop() {
  resp = get_time();
  switch (resp) {
    case 20:
      {
        t = dht.readTemperature();
        h = dht.readHumidity();
        FirebaseJson json;
        json.set("temp", t);
        json.set("humidity", h);
        Firebase.RTDB.updateNodeSilent(&fbdo, time_stamp, &json);
        delay(5000);
        break;
      }
    case 10:
      {
        Serial.println("Error");
        break;
      }
  }
}
