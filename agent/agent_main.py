# agent/agent_main.py
import json
import paho.mqtt.client as mqtt
from memory_utils import log_reading, log_decision, load_recent_readings
from reasoning import decide_action

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_SUB = "classroom/agentic/humidity"
TOPIC_PUB = "classroom/agentic/control"

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    humidity = data["Humidity"]
    temperature = data["Temperature"]
    device_id = data.get("device_id", "unknown")

    # Normalize once here
    reading = log_reading(humidity, temperature, device_id)

    memory = load_recent_readings()
    action, reason = decide_action(memory)

    client.publish(TOPIC_PUB, json.dumps({"command": action}))

    log_decision(
        action=action,
        reason=reason,
        humidity=humidity,
        temperature=temperature
    )

    print(f"{action} → {reason}")

def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.subscribe(TOPIC_SUB)
    print("Agent started. Waiting for data...")
    client.loop_forever()

if __name__ == "__main__":
    main()
