// firmware/esp32c3_simulated.ino
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>

#define RGB_LED_PIN 8       // Built-in RGB LED on ESP32-C3-DevKit-02
#define NUM_PIXELS 1        // Only one LED on the board
#define BRIGHTNESS 50       // Adjust brightness (0–255)

Adafruit_NeoPixel rgb_led(NUM_PIXELS, RGB_LED_PIN, NEO_GRB + NEO_KHZ800);

const char* ssid = "moto";
const char* password = "Hello@1234";

const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* topic_pub = "classroom/agentic/humidity";
const char* topic_sub = "classroom/agentic/control";

WiFiClient espClient;
PubSubClient client(espClient);

const long PUBLISH_INTERVAL = 30000; // publish every 30s
unsigned long lastPublish = 0;

#define LED_PIN 8 // built-in LED on ESP32-C3-DevKit-02

void setup_wifi() {
  Serial.print("\nConnecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  int attempts = 0;
  rgb_led.begin();
  rgb_led.setBrightness(BRIGHTNESS);
  rgb_led.show();  // Initialize all pixels to 'off'

  while (WiFi.status() != WL_CONNECTED && attempts < 40) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi connect failed - rebooting in 5s");
    delay(5000);
    ESP.restart();
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.print("Received ["); Serial.print(topic); Serial.print("] : "); Serial.println(msg);

  if (msg == "LED_ON") {
    rgb_led.setPixelColor(0, rgb_led.Color(0, 255, 0)); // Green ON
    rgb_led.show();
    Serial.println("RGB LED turned ON (Green)");
  } 
  else if (msg == "LED_OFF") {
    rgb_led.clear();  // turn off all colors
    rgb_led.show();
    Serial.println("RGB LED turned OFF");
  } 
  else if (msg == "LED_ALERT") {
    rgb_led.setPixelColor(0, rgb_led.Color(255, 0, 0)); // Red alert
    rgb_led.show();
    Serial.println("RGB LED ALERT (Red)");
  }
}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32C3Client")) {
      Serial.println("connected");
      client.subscribe(topic_sub);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5s");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

float randomFloat(float minVal, float maxVal) {
  return minVal + (random(0, 10001) / 10000.0) * (maxVal - minVal);
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  unsigned long now = millis();
  if (now - lastPublish > PUBLISH_INTERVAL) {
    lastPublish = now;

    float humidity = round(randomFloat(40.0, 95.0));     // simulated humidity
    float temperature = round(randomFloat(20.0, 35.0));  // simulated temperature

    StaticJsonDocument<256> doc;
    doc["Humidity"] = humidity;
    doc["Temperature"] = temperature;
    doc["device_id"] = "ESP32C3_SIM_01";
    doc["timestamp"] = now;

    char buffer[256];
    size_t n = serializeJson(doc, buffer);
    Serial.print("Publishing simulated data: ");
    Serial.println(buffer);
    client.publish(topic_pub, buffer, n);
  }
}
