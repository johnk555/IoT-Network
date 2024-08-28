#include <Wire.h>
#include <SPI.h>
#include <WiFi101.h>
#include <PubSubClient.h>
#include "arduino_secrets.h"

// FOR WIFI
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
int status = WL_IDLE_STATUS;  // variable for WiFi radio's status

const char* mqtt_server = "192.168.88.220";   //IP of the mqtt broker //if the broker is a pc, IP of the pc

WiFiClient wifiClient;
PubSubClient client(wifiClient);

const int ledPin = 11;  // LED connected to digital pin D5



void setup_wifi() {
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
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }
  Serial.println(messageTemp);

  // Control the LED based on the received message
  if (messageTemp == "ON") {
    digitalWrite(ledPin, HIGH);  // Turn LED on
    Serial.println("LED turned ON");
  } else if (messageTemp == "OFF") {
    digitalWrite(ledPin, LOW);   // Turn LED off
    Serial.println("LED turned OFF");
  } else {
    Serial.println("Unknown message");
  }
}


void setup() {
  Serial.begin(9600);

  pinMode(ledPin, OUTPUT);
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ArduinoClient")) {
      Serial.println("connected");
      client.subscribe("home/room/led");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(5000);
    }
 }
}


void reconnect() {
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (client.connect("ArduinoClient")) {
      Serial.println("connected");
      client.subscribe("home/room/led");  // Subscribe to the topic
    } else {
      Serial.println("failed, rc=");
      Serial.println(client.state());
      delay(5000);
    }
  }
}


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
