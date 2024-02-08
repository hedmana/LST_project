// for resistance measurements:
#define R_REF 10000.0
#define AVERAGES 10  // range 1-100
float resistance;
uint16_t x;
static float cumulativeResistance = 0;
static uint8_t i = 0;


TaskHandle_t Task1;
TaskHandle_t Task2;

void setup() {
  Serial.begin(115200);

  // setting up multithreading
  //create a task that will be executed in the Task1code() function, with priority 1 and executed on core 0
  xTaskCreatePinnedToCore(
    Task1code, /* Task function. */
    "Task1",   /* name of task. */
    10000,     /* Stack size of task */
    NULL,      /* parameter of the task */
    1,         /* priority of the task */
    &Task1,    /* Task handle to keep track of created task */
    0);        /* pin task to core 0 */
  delay(500);

  //create a task that will be executed in the Task2code() function, with priority 1 and executed on core 1
  xTaskCreatePinnedToCore(
    Task2code, /* Task function. */
    "Task2",   /* name of task. */
    10000,     /* Stack size of task */
    NULL,      /* parameter of the task */
    1,         /* priority of the task */
    &Task2,    /* Task handle to keep track of created task */
    1);        /* pin task to core 1 */
  delay(500);

  // resistance measurement:
  //analogReference(DEFAULT);
}

//Task1code: Read temp and heat peltier
void Task1code(void* pvParameters) {
  Serial.print("Task1 running on core ");
  Serial.println(xPortGetCoreID());

  for (;;) {
    Serial.println("heating :DD");
    delay(1000);
  }
}

//Task2code: read resistance
void Task2code(void* pvParameters) {
  Serial.print("Task2 running on core ");
  Serial.println(xPortGetCoreID());

  for (;;) {
    x = analogRead(15);
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
}

void loop() {
}