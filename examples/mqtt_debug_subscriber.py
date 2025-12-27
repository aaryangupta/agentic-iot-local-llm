import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("classroom/agentic/humidity")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"Humidity: {data['Humidity']}%, Temp: {data['Temperature']}°C, Device: {data['device_id']}")
    except Exception as e:
        print("Raw message:", msg.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()
