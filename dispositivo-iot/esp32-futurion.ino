#include <WiFi.h>
#include <PubSubClient.h>

// ===============================
// CONFIGURAÇÕES DE WIFI (WOKWI)
// ===============================
const char* ssid = "Wokwi-GUEST";
const char* password = "";


// CONFIGURAÇÕES MQTT (FIWARE)
// ===============================

const char* mqttServer = "9.234.176.2";   // IP
const int mqttPort = 1883;

// TÓPICOS DO IOT AGENT
const char* loginTopic = "/json/loginDevice/attrs";
const char* moodTopic = "/json/moodDevice/attrs";

// CLIENTES
WiFiClient espClient;
PubSubClient client(espClient);

// Controle de tempo
unsigned long lastSend = 0;


// CONEXÃO WIFI
// ===============================
void connectWiFi() {
  Serial.println("🔌 Conectando ao WiFi...");
  WiFi.begin(ssid, password);

  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 10) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n🟢 WiFi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n🟡 WiFi não disponível (simulação continua)");
  }
}


// RECONEXÃO MQTT
// ===============================
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.println("🔄 Conectando ao MQTT Broker FIWARE...");

    if (client.connect("ESP32-FuturionHub")) {
      Serial.println("🟢 Conectado ao MQTT!");
    } else {
      Serial.print("MQTT falhou, rc=");
      Serial.println(client.state());
      Serial.println("Tentando novamente em 5s...");
      delay(5000);
    }
  }
}

// ===============================
// SETUP
// ===============================
void setup() {
  Serial.begin(115200);
  delay(500);

  Serial.println("===================================");
  Serial.println(" 🚀 ESP32 - Futurion Hub (FIWARE) ");
  Serial.println("===================================\n");

  connectWiFi();
  client.setServer(mqttServer, mqttPort);
}

// ===============================
// FUNÇÕES ENVIO DE EVENTOS
// ===============================

// ----- ENVIA EVENTO DE LOGIN -----
void sendLoginEvent() {
  String username = "admin@gmail.com";
  unsigned long ts = millis();

  String payload = "{";
  payload += "\"username\":\"" + username + "\",";
  payload += "\"timestamp\":\"" + String(ts) + "\"";
  payload += "}";

  client.publish(loginTopic, payload.c_str());
  Serial.println("📤 Enviado LoginEvent → " + payload);
}

// ----- ENVIA EVENTO DE HUMOR -----
void sendMoodEvent() {
  String humores[3] = {"bem", "neutro", "mal"};
  String mood = humores[random(0, 3)];

  unsigned long ts = millis();

  String payload = "{";
  payload += "\"mood\":\"" + mood + "\",";
  payload += "\"timestamp\":\"" + String(ts) + "\"";
  payload += "}";

  client.publish(moodTopic, payload.c_str());
  Serial.println("📤 Enviado MoodEvent → " + payload);
}

// ===============================
// LOOP PRINCIPAL
// ===============================
void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();

  unsigned long now = millis();

  if (now - lastSend > 5000) {  // A cada 5 segundos
    lastSend = now;

    // Alternar entre login e humor como se viesse do site
    if (random(0, 2) == 0) {
      sendLoginEvent();
    } else {
      sendMoodEvent();
    }

    Serial.println("-----------------------------------");
  }
}
