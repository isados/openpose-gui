#define RELAY 8

String label;

void setup() {
  // put your setup code here, to run once:
  pinMode(RELAY,OUTPUT);
  pinMode(LED_BUILTIN,OUTPUT);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    label=Serial.readString();
    Serial.println(label);
    if (label =="Left Arm's Up"){
      digitalWrite(RELAY,HIGH);
      digitalWrite(LED_BUILTIN,HIGH);
  }
   else{
       digitalWrite(RELAY,LOW); 
      digitalWrite(LED_BUILTIN,LOW);
      }
  }
  
  
}
