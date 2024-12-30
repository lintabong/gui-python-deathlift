#include <Arduino.h>

void setup() {
  Serial.begin(115200); // Inisialisasi komunikasi Serial
  randomSeed(analogRead(0)); // Seed random number generator dengan input analog
}

void loop() {
  String data = "";

  for (int i = 0; i < 100; i++) {
    float randomValue = random(100, 200) / 100.0;
    data += String(randomValue, 2);
    if (i < 99) data += ",";
  }

  // Tentukan label (VM atau Tanpa VM) secara acak
  String label = random(0, 2) == 0 ? "tanpavm" : "vm";
  data += "," + label;

  // Kirim data ke Serial Monitor
  Serial.println(data);

  // Tunggu 2 detik
  delay(2000);
}
