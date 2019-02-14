int analogDevices[6];//10 bits each (up to 1024) --> 10 * 6 = 60 bits / 8 = 8 bytes rather than 10
byte sliderBytes[4];
byte sliderExtraByte;
byte knobBytes[2];
byte knobExtraByte;

bool switches[12];
byte switch1;
byte switch2;

void setup() {
  for (int i = 2; i <= 13; i++){
    pinMode(i, INPUT);  
  }
  Serial1.begin(9600);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  switch1 = 0;
  switch2 = 0;

  for (int i = 0; i <= 11; i++){
    switches[i] = digitalRead(i+2);
    if(switches[i] == 1){
      if ( i <= 7 )
        switch1 += 1 << i;
      else
        switch2 += 1 << (i-8);
    }
  }

  for (int i = 0; i < 6; i++){
    analogDevices[i] = analogRead(i);
//    Serial.print(analogDevices[i]);
//    Serial.print("\t");
  }

  sliderExtraByte = 0;  
  for (int i = 0; i < 4; i++){  
    sliderBytes[i] = analogDevices[i];
    sliderExtraByte += (analogDevices[i] >> 8) << i*2;
  }

  knobExtraByte = 0;  
  for (int i = 4; i < 6; i++){  
    knobBytes[i-4] = analogDevices[i];
    knobExtraByte += (analogDevices[i] >> 8) << ((i-4)*2);
//    Serial.print(knobBytes[i-4]);
//    Serial.print("\t");
  }
//  Serial.println(knobExtraByte);
  
  Serial1.write(sliderBytes,4);
  Serial1.write(sliderExtraByte);
  
  Serial1.write(knobBytes, 2);
  Serial1.write(knobExtraByte);
  
  Serial1.write(switch1);
  Serial1.write(switch2);

//  Serial.print(switch1);
//  Serial.print("\t");
//  Serial.println(switch2);
  
  delay(30); //allows all serial sent to be received together

}
