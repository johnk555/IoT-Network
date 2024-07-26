#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <WiFi101.h>
#include <PubSubClient.h>
#include "arduino_secrets.h"

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme; // I2C

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
int status = WL_IDLE_STATUS;  // variable for WiFi radio's status

//WiFiSSLClient WiFiclient; // instantiate a secure WiFi client

 
WiFiClient wifiClient;
PubSubClient client(wifiClient);
 
const char* mqtt_server = "192.168.88.250";  // IP address of the receiving PC

void setup(){
  Serial.begin(9600);


    // Feather M0-specific WiFi pins
  WiFi.setPins(8, 7, 4, 2);

    // attempt to connect to WiFi network:
  while ( status != WL_CONNECTED) {
        Serial.print("Attempting to connect to SSID: ");
        Serial.println(ssid);
        // Connect to WiFi:
        if (sizeof(pass) == 1) { // if no password
            status = WiFi.begin(ssid); // connect with SSID alone
        }
        else {
            status = WiFi.begin(ssid, pass); // connect with SSID and password
        }
  }
      // you're connected now, so print out a success message:
  Serial.println("You're connected to the network");

    // print your Feather's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("Device IP Address: ");
  Serial.println(ip);
        // wait 5 seconds for connection:
  delay(5000);
 
  Serial.println(F("BME280 test"));

  bool status;

  // default settings
  // (you can also pass in a Wire library object like &Wire2)
  status = bme.begin();
  if (!status) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }
  Serial.println("-- Default Test --");
  delay(500);

  client.setServer(mqtt_server, 1883);  // Set the MQTT server address and port
}
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F;

  String payload = String("{\"temperature\": ") + temperature +
                   String(", \"humidity\": ") + humidity +
                   String(", \"pressure\": ") + pressure + String("}");

  Serial.print("Publishing message: ");
  Serial.println(payload);
  client.publish("sensor/bme280", payload.c_str());

  delay(5000);  // wait 5 seconds before sending next reading
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("FeatherM0Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
