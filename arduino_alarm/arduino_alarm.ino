#define ALARMPIN 2
int input;

void setup() {
  pinMode(ALARMPIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    input = Serial.parseInt(); // Read the integer sent over serial

    if (input == 1) {
      // If the input is 1, trigger the alarm
      digitalWrite(ALARMPIN, HIGH);
      delay(100); // Adjust this delay as needed
      digitalWrite(ALARMPIN, LOW);
    }
  }
}
