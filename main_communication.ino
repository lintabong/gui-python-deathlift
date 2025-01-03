#include <Arduino.h>

#define pinFSR 36
#define pinECG 37

String receivedString = "";

void setup() {
    Serial.begin(115200);

    pinMode(pinFSR, INPUT);
    pinMode(pinECG, INPUT);
}

void loop() {
    while (Serial.available() > 0) {
        char incomingChar = Serial.read();
        if (incomingChar == '\n') {

            processCommand(receivedString);

            receivedString = "";
        } else {
            receivedString += incomingChar;
        }
    }
}

void processCommand(String command) {
    int firstComma = command.indexOf(',');
    int secondComma = command.indexOf(',', firstComma + 1);

    if (firstComma > 0 && secondComma > firstComma) {
        String action = command.substring(0, firstComma);
        String durationStr = command.substring(firstComma + 1, secondComma);
        String countStr = command.substring(secondComma + 1);

        int duration = durationStr.toInt();
        int count = countStr.toInt();

        if (action == "a") {
            String data = "";

            unsigned long startTime = millis();
            for (int i = 0; i < count; i++) {
                if (millis() - startTime >= (duration * 1000)) break;

                // float analogValue = random(100, 200) / 100.0;
                float analogValue = analogRead(pinFSR);
                data += String(analogValue, 2);

                if (i < count - 1) data += ",";
                delay((duration * 1000) / count);
            }

            String label = random(0, 2) == 0 ? "a" : "a";
            data += "," + label;

            Serial.println(data);
        } 

        
        if (action == "b") {
            String data = "";

            unsigned long startTime = millis();
            for (int i = 0; i < count; i++) {
                if (millis() - startTime >= (duration * 1000)) break;

                // float analogValue = random(100, 200) / 100.0;
                float analogValue = analogRead(pinECG);
                data += String(analogValue, 2);

                if (i < count - 1) data += ",";
                delay((duration * 1000) / count);
            }

            String label = random(0, 2) == 0 ? "b" : "b";
            data += "," + label;

            Serial.println(data);
        } 
    } 
}
