#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "brewing";      // Replace with your WiFi SSID
const char* password = "manuwalokak";  // Replace with your WiFi password
const char* serverUrl = "http://192.168.0.111:5000/ecg/add";  // Replace with your Flask server URL

#define LP 35
#define LM 32
#define PIN_AN 33

const int BATCH_SIZE = 186;
int ecgData[BATCH_SIZE];
int dataIndex = 0;

void setup() {
  Serial.begin(9600);
  pinMode(LP, INPUT); // Setup for leads off detection LO +
  pinMode(LM, INPUT); // Setup for leads off detection LO -

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Check for leads off detection
  if ((digitalRead(LP) == 1) || (digitalRead(LM) == 1)) {
    Serial.println('!');
    return;
  }

  // Read ECG data
  int data = analogRead(PIN_AN);

  // Skip invalid readings
  if (data == 4095 || data == 0) {
    delay(100); // Adjust delay as necessary
    return;
  }

  // Normalize ECG data to range 0-1
  float normalizedData = data / 4095.0;

  // Store data in array
  ecgData[dataIndex++] = normalizedData;

  // Check if array is full
  if (dataIndex >= BATCH_SIZE) {
    // Prepare JSON data
    String jsonData = "{\"dataValue\":[";

    for (int i = 0; i < BATCH_SIZE; i++) {
      jsonData += String(ecgData[i]);
      if (i < BATCH_SIZE - 1) {
        jsonData += ",";
      }
    }
    jsonData += "]}";

    // Send data to Flask server via HTTP POST
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;

      http.begin(serverUrl);
      http.addHeader("Content-Type", "application/json");
      int httpResponseCode = http.POST(jsonData);

      // Check response
      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        Serial.println(response);
      } else {
        Serial.print("Error on HTTP request: ");
        Serial.println(httpResponseCode);
      }

      http.end(); // Close HTTP connection
    }

    // Reset index for next batch
    dataIndex = 0;
  }

  delay(100); // Adjust delay as necessary
}
