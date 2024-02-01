// ds18b20
#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
float t;


// relay
const int relay_pin = 11;
int relay_state = LOW;

unsigned long previous_millis = 0;

const long interval = 10000;

void setup() {
  // temp
  Serial.begin(9600);
  

  // relay
  pinMode(relay_pin, OUTPUT);
}

void loop() {
  sensors.begin();
  // read temperature
  sensors.requestTemperatures();
  t = sensors.getTempCByIndex(0);
  Serial.println(t);
  if (t > 40) { digitalWrite(relay_pin, LOW); }
  if (t < 40) { digitalWrite(relay_pin, HIGH); }
}