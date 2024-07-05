// #define LP 35
// #define LM 32
// #define PIN_AN 33

// void setup() {
//   Serial.begin(9600);
//   pinMode(LP, INPUT); // Setup for leads off detection LO +
//   pinMode(LM, INPUT); // Setup for leads off detection LO -

// }

// void loop() {
//   if ((digitalRead(LP) == 1) || (digitalRead(LM) == 1)) {
//     Serial.println('!');
//     return;
//   }
//   // Serial.println(analogRead(PIN_AN));

//   int data = analogRead(PIN_AN);

// if(data == 4095 || data == 0 ){
//   return;
// }
//  Serial.println(data);

//   delay(100);
// }


// Try Connected
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "alifecg";      // Replace with your WiFi SSID
const char* password = "16082003";  // Replace with your WiFi password
const char* serverUrl = "http://192.168.167.149:5000/ecg";  // Replace with your Flask server URL

#define LP 35
#define LM 32
#define PIN_AN 33

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

  // Print ECG data to serial monitor
  Serial.println(data);

  // Send data to Flask server via HTTP POST
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Prepare JSON data
    String jsonData = "{\"value\":" + String(data) + "}";

    // Send POST request
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

  delay(100); // Adjust delay as necessary
}




