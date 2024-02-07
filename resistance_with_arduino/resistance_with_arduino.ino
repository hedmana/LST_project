#define R_REF 10000.0
#define AVERAGES 10  // range 1-100

void setup() {
  analogReference(DEFAULT);
  Serial.begin(9600);
}

void loop() {
  float resistance;
  uint16_t x;
  static float cumulativeResistance = 0;
  static uint8_t i = 0;
  x = analogRead(A0);
  resistance = R_REF * x / (1024.0 - x);
  cumulativeResistance = cumulativeResistance + resistance;
  i++;
  if (i == AVERAGES) {
    Serial.println(cumulativeResistance / AVERAGES);
    cumulativeResistance = 0;
    i = 0;
  }
  delay(500 / AVERAGES);  // about two measurements per second
}
