# import paho.mqtt.client as mqtt
# import requests
# import json

# mqtt_server = "192.168.88.190"  # Αντικατέστησε με τη δική σου IP διεύθυνση
# mqtt_port = 1883
# topic = "test/topic"

# fastapi_url = "http://127.0.0.1:8000/sensor-data/"

# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code " + str(rc))
#     client.subscribe(topic)

# def on_message(client, userdata, msg):
#     sensor_value = float(msg.payload.decode())
#     print(f"Received message: {sensor_value}")

#     data = {
#         "value": sensor_value
#     }

#     response = requests.post(fastapi_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
#     print(f"Sent to FastAPI: {response.status_code} - {response.json()}")

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# print(f"Connecting to MQTT broker at {mqtt_server}:{mqtt_port}")
# client.connect(mqtt_server, mqtt_port, 60)

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






