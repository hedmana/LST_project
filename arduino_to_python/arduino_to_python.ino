void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud rate
}

void loop() {
  // Read sensor value (replace this with your sensor reading logic)
  int sensorValue = analogRead(A0);

  // Send sensor value to Python
  Serial.println(sensorValue);

  // Delay for a moment
  delay(1000); // Adjust delay as needed
}
