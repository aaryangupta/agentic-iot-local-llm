import sys, json, time
import pandas as pd
import streamlit as st
from pathlib import Path

# --- absolute paths ---
BASE_DIR = Path(__file__).resolve().parents[1]
AGENT_DIR = BASE_DIR / "agent"
LOG_FILE = AGENT_DIR / "readings.log"
DECISION_FILE = AGENT_DIR / "decisions.log"

# make agent utilities importable (optional for later)
sys.path.append(str(AGENT_DIR))

st.set_page_config(page_title="Agentic IoT Dashboard", layout="wide")

# --- Sidebar info ---
st.sidebar.header("Reading files from:")
st.sidebar.markdown(f"📄 `{LOG_FILE}`")
st.sidebar.markdown(f"📄 `{DECISION_FILE}`")
refresh_rate = st.sidebar.slider("Auto-refresh every (seconds)", 2, 30, 5)

# --- Helpers ---------------------------------------------------------------
def load_readings():
    if not LOG_FILE.exists():
        return pd.DataFrame(columns=["ts", "humidity", "temperature", "device_id"])
    records = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                records.append(json.loads(line.strip()))
            except:
                continue
    if not records:
        return pd.DataFrame(columns=["ts", "humidity", "temperature", "device_id"])
    df = pd.DataFrame(records)
    df.rename(columns={"timestamp": "time"}, inplace=True)

    return df

def load_decisions():
    """Directly read decisions.log without relying on external import."""
    if not DECISION_FILE.exists():
        return []
    with open(DECISION_FILE, "r") as f:
        lines = [json.loads(line.strip()) for line in f if line.strip()]
    return lines

# ---------------------------------------------------------------------------
st.title("📡 Agentic IoT Dashboard — ESP32-C3 + Python Agent")
st.markdown(
    "Visualizes live humidity & temperature data from your ESP32-C3, "
    "along with the agent’s decision reasoning and LED control actions."
)

placeholder = st.empty()

while True:
    df = load_readings()
    if len(df) == 0:
        st.warning("Waiting for readings... Make sure your agent and ESP32 are running.")
    else:
        latest = df.iloc[-1]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌡️ Temperature (°C)", f"{latest['temperature']:.1f}")
        col2.metric("💧 Humidity (%)", f"{latest['humidity']:.1f}")
        col3.metric("📦 Total Readings", len(df))

        # --- Load decisions & LED state ---
        decisions = load_decisions()
        if decisions:
            last_decision = decisions[-1]
            led_state = "🟢 ON" if last_decision["action"] == "LED_ON" else "⚫ OFF"
            reason = last_decision["reason"]

            # colored indicator
            color_box = (
                f"<div style='width:30px;height:30px;border-radius:50%;"
                f"background-color:{'lime' if led_state=='🟢 ON' else 'gray'}'></div>"
            )
            col4.markdown(f"<center>{color_box}<br><b>{led_state}</b></center>", unsafe_allow_html=True)
            st.caption(f"💡 **Reason:** {reason}")
        else:
            col4.metric("💡 LED State", "Unknown")

        st.line_chart(
            df.set_index("time")[["humidity", "temperature"]],
            use_container_width=True,
            height=300
        )

        high_hum = df["humidity"] > 75
        st.caption(
            f"High humidity readings: {high_hum.sum()} / {len(df)} "
            f"({(high_hum.mean()*100):.1f}% of all readings)"
        )

        # --- Agent decisions log ---
        st.subheader("🧠 Agent Decisions Log")
        if decisions:
            for d in reversed(decisions[-10:]):  # last 10
                t = time.strftime("%H:%M:%S", time.localtime(d["timestamp"]))
                st.write(
                    f"**{t}** → Action: `{d['action']}` | "
                    f"Humidity: {d['humidity']}% | Reason: {d['reason']}"
                )
        else:
            st.info("No decisions logged yet.")

    time.sleep(refresh_rate)
    st.rerun()
