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

