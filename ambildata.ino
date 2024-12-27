const int ECG_PIN=A1;
const int FSR_PIN=A0;
// const int LOPLUS=1;
// const int LOMIN=13;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  // pinMode(1, INPUT); // LO PLUS
  // pinMode(3, INPUT); // LO MIN
}


void loop() {

  int VMPressure=analogRead(FSR_PIN);
  Serial.print("VM=");
  Serial.println(VMPressure);

  int ECGbla=analogRead(ECG_PIN);
  Serial.print("EG=");
  Serial.println(ECGbla);

//   if((digitalRead(1) == 1)||(digitalRead(3) == 1)){
//    Serial.println('!');
//   }
//  else{
//  }
  delay(10);
}
