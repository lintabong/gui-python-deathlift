#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  randomSeed(analogRead(0));
}

void loop() {
  String data = "";

  for (int i = 0; i < 100; i++) {
    float randomValue = random(100, 200) / 100.0;
    data += String(randomValue, 2);
    if (i < 99) data += ",";
  }

  String label = random(0, 2) == 0 ? "tanpavm" : "vm";
  data += "," + label;

  Serial.println(data);

  delay(2000);
}
