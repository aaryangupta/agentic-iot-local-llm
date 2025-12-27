# agent/memory_utils.py
import json, time
from pathlib import Path

BASE_DIR = Path(__file__).parent
READINGS_FILE = BASE_DIR / "readings.log"
DECISIONS_FILE = BASE_DIR / "decisions.log"

def log_reading(humidity, temperature, device_id):
    record = {
        "humidity": humidity,
        "temperature": temperature,
        "device_id": device_id,
        "timestamp": time.time()
    }
    with open(READINGS_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")
    return record

def log_decision(action, reason, humidity, temperature):
    record = {
        "timestamp": time.time(),
        "action": action,
        "reason": reason,
        "humidity": humidity,
        "temperature": temperature
    }
    with open(DECISIONS_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

def load_recent_readings(maxlen=20):
    if not READINGS_FILE.exists():
        return []
    with open(READINGS_FILE) as f:
        lines = f.readlines()[-maxlen:]
    return [json.loads(l) for l in lines]
