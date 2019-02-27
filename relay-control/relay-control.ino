#include<Wire.h>

String label;
void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN,OUTPUT);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    label=Serial.readString();
    Serial.println(label);
    if (label =="Both Arms Up")
      digitalWrite(LED_BUILTIN,HIGH);
   else
      digitalWrite(LED_BUILTIN,LOW); 
  }
  
}
