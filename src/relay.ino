// ds18b20
#include "DFRobot_BMP280.h"
#include "Wire.h"
#include <PID_v1_bc.h>
#include <time.h>


// temperature sensor
typedef DFRobot_BMP280_IIC BMP;  // ******** use abbreviations instead of full names ********
BMP bmp(&Wire, BMP::eSdoLow);
double t;

// Transistor
const int relay_pin = 11;



// PID setup
double Setpoint;
double Output;
double Kp = 60, Ki = 37, Kd = 32;
PID myPID(&t, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

// Parameters for temperature control logic
int menuChoice;
String stringVariable;
int lowerRange;
int upperRange;

// mode 2 logic
unsigned long current_time = 0;
unsigned long last_transition_time = 0;
unsigned long transition_interval = 60000; //60s
static int direction = 1; // increase of decrease temperature?

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
  //
  Setpoint = 35.0;  // Desired temperature

  myPID.SetMode(AUTOMATIC);       // Turn the PID on
  myPID.SetOutputLimits(0, 255);  // Limits output to between 0 and 100%


  // select which mode to execute and get temperature range
  Serial.println("Select mode");

  while (Serial.available() == 0) {
  }

  menuChoice = Serial.parseInt();

  // Clear the serial buffer
  while (Serial.available() > 0) {
    char junk = Serial.read();
  }

  switch (menuChoice) {
    case 1:
      Serial.println("Mode 1 selected.");
      break;

    case 2:
      Serial.println("Mode 2 selected.");
      break;

    case 3:
      Serial.println("Mode 3 selected.");
      break;

    default:
      Serial.println("invalid choice, selecting 3");
      menuChoice = 3;
  }

  while (Serial.available() == 0) {
  }


  stringVariable = Serial.readString();

  Serial.print("Given range was: ");
  Serial.println(stringVariable);
  Serial.println();

  // parse
  parseTemperatureRange(stringVariable);
  Setpoint = lowerRange;

}

void loop() {
  // read temperature
  t = bmp.getTemperature();
  // send temperature to python
  Serial.println(t);



  // select what to do based on which mode is running
  switch (menuChoice) {
    case 1:
      // cycle between the upper and and lower range limits
      if (abs(t - Setpoint) < 0.1) {
        if (Setpoint == upperRange) {
          Setpoint = lowerRange;
        } else {
          Setpoint = upperRange;
        }
      }
      break;

    case 2:
      // Transition temperature in steps with a pause between each step
        current_time = millis();

        // Check if it's time to transition to the next setpoint
        if (current_time - last_transition_time >= transition_interval) {
            // Move to the next setpoint
            Setpoint += direction; // increase or decrease the setpoint by a degree
            last_transition_time = current_time;

            // Reverse direction if reaching upplower or er range
            if (Setpoint >= upperRange){
                direction = -1;
            }
            if (Setpoint <= lowerRange){
              direction = 1;
            }
        }

      break;

    case 3:
      Setpoint = lowerRange;
      break;
  }

  // PID: compute Output based on Setpoint and t
  myPID.Compute();


  // Apply PWM to the transistor gate/base
  if (t > 0) {
    analogWrite(relay_pin, Output);
  } else {
    analogWrite(relay_pin, 0);
  }

  delay(100);
}