# agent/reasoning.py
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="mistral")

def decide_action(memory):
    if not memory:
        return "LED_OFF", "no data yet"

    context = "\n".join(
        f"humidity={r['humidity']} temperature={r['temperature']}"
        for r in memory
    )

    prompt = f"""
You are an IoT control agent.
Decide LED_ON or LED_OFF.

Rules:
- LED_ON if humidity > 75 and rising
- LED_OFF otherwise

Sensor history:
{context}

Return JSON:
{{"action": "...", "reason": "..."}}
"""

    try:
        response = llm.invoke(prompt)
        result = eval(response.strip())
        return result["action"], result["reason"]
    except Exception:
        return "LED_OFF", "default safe mode"
