#include <Wire.h>
#include <SPI.h>
#include <WiFi101.h>
#include <PubSubClient.h>
#include "arduino_secrets.h"
#include "Adafruit_TCS34725.h"
#include <Adafruit_BME280.h>

#define SEALEVELPRESSURE_HPA (1013.25)

// For TCS LED
#define redpin 13
#define greenpin 11
#define bluepin 9
#define commonAnode true
const int ledPin = 6;  // LED connected to digital pin D5
byte gammatable[256];
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);

//FOR BME
Adafruit_BME280 bme; // I2C

// FOR PIR
int led = 10;                // the pin that the LED is atteched to
int sensor = 12;              // the pin that the sensor is atteched to
int state = LOW;             // by default, no motion detected
int val = 0;                 // variable to store the sensor status (value)



// FOR WIFI
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
int status = WL_IDLE_STATUS;  // variable for WiFi radio's status

const char* mqtt_server = "192.168.88.220";   //IP of the mqtt broker //if the broker is a pc, IP of the pc

WiFiClient wifiClient;
PubSubClient client(wifiClient);



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

 // FOR BME

  
 
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

  // FOR PIR
  pinMode(led, OUTPUT);      // initalize LED as an output
  pinMode(sensor, INPUT);    // initialize sensor as an input



  // FOR TCS
  if (tcs.begin()) {
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1);
  }
  pinMode(redpin, OUTPUT);
  pinMode(greenpin, OUTPUT);
  pinMode(bluepin, OUTPUT);

  for (int i=0; i<256; i++) {
    float x = i;
    x /= 255;
    x = pow(x, 2.5);
    x *= 255;

    if (commonAnode) {
      gammatable[i] = 255 - x;
    } else {
      gammatable[i] = x;
    }
  }
  delay(500);
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

  //FOR TCS
  float red, green, blue;

  tcs.setInterrupt(false);
  delay(60);
  tcs.getRGB(&red, &green, &blue);
  tcs.setInterrupt(true);

  analogWrite(redpin, gammatable[(int)red]);
  analogWrite(greenpin, gammatable[(int)green]);
  analogWrite(bluepin, gammatable[(int)blue]);


// FOR BME
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F;
  String namee = "Feather M0";
  String brand = "Adafruit";
  String model = "BME280";
  String firmware_version = "1.0.0";
  String manufacturer = "Bosch";

  // FOR PIR
  val = digitalRead(sensor);   // read sensor value
  
      
    String payload = String("{\"temperature\": ") + temperature +
                     String(", \"humidity\": ") + humidity +
                     String(", \"pressure\": ") + pressure +
                     String(", \"name\": \"") + namee + 
                     String("\", \"brand\": \"") + brand + 
                     String("\", \"model\": \"") + model + 
                     String("\", \"firmware_version\": \"") + firmware_version + 
                     String("\", \"manufacturer\": \"") + manufacturer +
                     String("\", \"R\": \"") + red +
                     String("\", \"G\": \"") + green +
                     String("\", \"B\": \"") + blue +
                     String("\"}");

  Serial.print("Publishing message: ");
  Serial.println(payload);
  client.publish("test_topic", payload.c_str());

  delay(5000);  // wait 5 seconds before sending next reading

}


// ETC FOR SUB AND PUB
//mosquitto_pub -h 192.168.88.220 -t home/room/led -m "ON"
//mosquitto_pub -h 192.168.88.220 -t home/room/led -m "OFF"
//mosquitto_sub -h 192.168.88.220 -t test_topic
