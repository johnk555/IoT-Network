# client.loop_forever()
import paho.mqtt.client as mqtt
import requests
import json

# MQTT settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "test_topic"

# FastAPI settings
FASTAPI_URL = "http://localhost:8000/sensor-data/"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()}")
    data = json.loads(msg.payload.decode())
    print(f"Sending data to API: {data}")
    try:
        response = requests.post(FASTAPI_URL, json=data)
        print(f"Data sent to API. Response: {response.status_code}, {response.json()}")
    except Exception as e:
        print(f"Failed to send data to API: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
