// ds18b20
#include "DFRobot_BMP280.h"
#include "Wire.h"
#include <PID_v1_bc.h>



typedef DFRobot_BMP280_IIC BMP;  // ******** use abbreviations instead of full names ********
BMP bmp(&Wire, BMP::eSdoLow);

double t;



// relay
const int relay_pin = 11;
int relay_state = LOW;



// Temperature thresholds for duty cycle calculation
const float tempMin = 20.0;  // Minimum temperature for 0% duty cycle
const float tempMax = 30.0;  // Maximum temperature for 100% duty cycle

// Timing
unsigned long lastTime = 0;
const long interval = 1000;  // Interval at which to check/update relay status (in milliseconds)
bool isOn = false;

// PID setup
double Setpoint, Output;
// Specify the links and initial tuning parameters
// double Kp=150, Ki=120, Kd=20;
double Kp = 60, Ki = 37, Kd = 32;
PID myPID(&t, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

void setup() {
  // temp
  Serial.begin(115200);
  bmp.reset();

  while (bmp.begin() != BMP::eStatusOK) {
    //Serial.println("bmp begin faild");
    delay(2000);
  }
  //Serial.println("bmp begin success");
  delay(100);

  // relay
  pinMode(relay_pin, OUTPUT);

  Setpoint = 35.0;  // Desired temperature

  myPID.SetMode(AUTOMATIC);       // Turn the PID on
  myPID.SetOutputLimits(0, 255);  // Limits output to between 0 and 100%
}

void loop() {
  if (Serial.available() > 0) {
    Setpoint = Serial.parseFloat();
    Serial.print("New Setpoint: ");
    Serial.println(Setpoint);
  }

  // #Serial.print(Setpoint - 0.5);
  // Serial.print(",");
  // Serial.print(Setpoint + 0.5);
  // Serial.print(",");
  t = bmp.getTemperature();
  Serial.println(t);


  unsigned long currentTime = millis();
  unsigned long onTime, offTime;

  myPID.Compute();  // Computes the PID output


  // Apply PWM to the transistor gate/base
  if (t > 0) {
    analogWrite(relay_pin, Output);

    if (abs(t-Setpoint) < 0.1) {
      if (Setpoint == 40) {Setpoint = 30;}
      else {Setpoint = 40;}
    }
  } else {
    analogWrite(relay_pin, 0);
  }


  // Serial.print("Temp: ");
  // Serial.print(t);
  // Serial.print(" C, PID Output: ");
  // Serial.println(Output);

  delay(500);
}