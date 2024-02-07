// ds18b20
#include <OneWire.h>
#include <DallasTemperature.h>
#include <PID_v1_bc.h>


#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
double t;



// relay
const int relay_pin = 11;
int relay_state = LOW;



// Temperature thresholds for duty cycle calculation
const float tempMin = 20.0; // Minimum temperature for 0% duty cycle
const float tempMax = 30.0; // Maximum temperature for 100% duty cycle

// Timing
unsigned long lastTime = 0;
const long interval = 1000; // Interval at which to check/update relay status (in milliseconds)
bool isOn = false;

// PID setup
double Setpoint, Output;
// Specify the links and initial tuning parameters
// double Kp=150, Ki=120, Kd=20;
double Kp=120, Ki=20, Kd=20;
PID myPID(&t, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

void setup() {
  // temp
  Serial.begin(115200);
  

  // relay
  pinMode(relay_pin, OUTPUT);

  Setpoint = 40.0; // Desired temperature
  
  myPID.SetMode(AUTOMATIC); // Turn the PID on
  myPID.SetOutputLimits(0, 100); // Limits output to between 0 and 100%
  myPID.SetSampleTime(500);

}

void loop() {
  
  // read temperature
  sensors.begin();
  sensors.requestTemperatures();
  t = sensors.getTempCByIndex(0);
  Serial.println(t);

  

  unsigned long currentTime = millis();
  unsigned long onTime, offTime;

  myPID.Compute(); // Computes the PID output


  int pwmValue = map(Output, 0, 100, 0, 255);
  
  // Apply PWM to the transistor gate/base
  if (t > -20) {
    analogWrite(relay_pin, pwmValue);
  } else {
    analogWrite(relay_pin, 0);
  }


  Serial.print("Temp: ");
  Serial.print(t);
  Serial.print(" C, PID Output: ");
  Serial.println(Output);

}