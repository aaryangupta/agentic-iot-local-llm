# Agentic IoT with Local LLM

An explainable, local-first IoT control agent using **ESP32**, **MQTT**, and a **local LLM (Ollama)**.

This project demonstrates how an IoT system can **observe, reason, act, remember, and explain its decisions** — without relying on cloud APIs or paid AI services.

---

## What this project does

- Reads humidity and temperature data from an ESP32 (real or simulated)
- Sends data via MQTT
- Uses a **local LLM (Ollama)** to reason about sensor trends
- Decides an action (`LED_ON` / `LED_OFF`)
- Explains *why* the decision was made
- Logs decisions and reasoning
- Visualizes everything in a local dashboard

---

## Why this exists

Most “agentic AI” IoT demos:
- hardcode thresholds
- hide decision logic
- depend on cloud APIs
- are difficult to learn from

This project is designed to be:
- **local-first**
- **explainable**
- **educational**
- **hackable**

---
## Architecture

```markdown

ESP32
↓
MQTT
↓
Python Agent
├─→ LLM (Ollama)
├─→ Memory + Logs
└─→ Dashboard
↓
MQTT Control
↓
ESP32

```
---

## Requirements

- Python 3.10+
- ESP32-C3 (or simulated sensor data)
- Ollama (local LLM runtime)
- MQTT broker (HiveMQ public broker works)

## Quick Start (10 minutes)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Install and run Ollama
```bash
ollama pull mistral
ollama serve
```

### 3. Start the agent
```bash
cd agent
python agent_main.py
```

### 4. Run the dashboard
```bash
python -m streamlit run dashboard.py
```

### 5. Flash ESP32 firmware

Upload the firmware from firmware/ and open Serial Monitor.

## Project Status

v0.1 – Educational foundation  
This project is intended for learning and experimentation.
It is not designed for safety-critical systems.

## License

MIT License
