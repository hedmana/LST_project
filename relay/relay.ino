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
double Setpoint = 40;
double Output;
// Specify the links and initial tuning parameters
// double Kp=150, Ki=120, Kd=20;
double Kp = 60, Ki = 37, Kd = 32;
PID myPID(&t, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

int menuChoice;
String stringVariable;

int lowerRange;
int upperRange;


void parseTemperatureRange(String inputString) {
  // Ensure the String is not empty
  if (inputString.length() > 0) {
    // Find the index of the comma
    int commaIndex = inputString.indexOf(',');

    // Check if the comma exists in the string
    if (commaIndex != -1) {
      // Extract the lower range substring before the comma
      String lowerRangeString = inputString.substring(0, commaIndex);
      // Extract the upper range substring after the comma
      String upperRangeString = inputString.substring(commaIndex + 1);

      // Convert the substrings to integers
      lowerRange = lowerRangeString.toInt();
      upperRange = upperRangeString.toInt();

      // Print the lower and upper ranges
      Serial.print("Lower Range: ");
      Serial.println(lowerRange);
      Serial.print("Upper Range: ");
      Serial.println(upperRange);
    } else {
      // Handle the case when no comma is found
      Serial.println("Error: No comma found in the input");
    }
  } else {
    // Handle the case when the input string is empty
    Serial.println("Error: Input string is empty");
  }
}

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


  Serial.println("Available modes:");
  Serial.println("1. Temperature cycles between 30-40C");
  Serial.println("2. Manual temp entry");
  Serial.println("3. Ace mode.");
  Serial.println();

  Serial.println("Enter the which mode to execute: ");

  while (Serial.available() == 0) {
  }

  menuChoice = Serial.parseInt();

  // Clear the serial buffer
  while (Serial.available() > 0) {
    char junk = Serial.read();
  }

  switch (menuChoice) {
    case 1:
      // temp sensor code goes here
      Serial.print("This mode runs just temperature temperature cycles.");
      break;

    case 2:
      // humidity sensor code goes here
      Serial.println("2 pressed");

      Serial.println("Enter temperature range (for example 25,30)");

      while (Serial.available() == 0) {
      }
      

      stringVariable = Serial.readString();

      Serial.print("Given range was: ");
      Serial.println(stringVariable);
      Serial.println("Converting the range into integers...");
      Serial.println();

      // parse
      parseTemperatureRange(stringVariable);


      break;

    case 3:
      // pressure sensor code goes here
      Serial.print("3 pressed");

      break;

    default:
      Serial.println("Please choose a valid selection");
  }
}

void loop() {
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

    if (abs(t - Setpoint) < 0.1) {
      if (Setpoint == 40) {
        Setpoint = 30;
      } else {
        Setpoint = 40;
      }
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