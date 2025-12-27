# agent/mqtt_client.py
import json
import paho.mqtt.client as mqtt

_client = None

def _get_client(broker="broker.hivemq.com", port=1883):
    global _client
    if _client is None:
        _client = mqtt.Client()
        _client.connect(broker, port, 60)
    return _client

def publish_control(topic, payload):
    client = _get_client()
    client.publish(topic, json.dumps(payload))
    print(f"Published to {topic}: {payload}")