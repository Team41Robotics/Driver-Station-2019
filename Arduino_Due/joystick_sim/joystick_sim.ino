#include "HID.h"  //uncomment for arduino due
#include "Joystick.h"

#define NUM_BUTTONS 10
#define TIME_TO_CHANGE_COLOR 1500

int redPin = 22;   // LED connected to digital pin 13
int greenPin = 32;   // LED connected to digital pin 13
int bluePin = 42;   // LED connected to digital pin 13
int inPin = 2;     // pushbutton connected to digital pin 7
bool values[NUM_BUTTONS];       // variable to store the read value
bool previous[NUM_BUTTONS];
long millis_held[NUM_BUTTONS];
unsigned long firstTime[NUM_BUTTONS];

union bytestoint
{
   int value;
   byte bytes[4] = {0,0,0,0};
};

byte data[10];
uint8_t buttons1;
uint8_t buttons2;

bytestoint sliders[4];
bytestoint knobs[2];

int POV1 = 0;
int POV2 = 0;

void setup() {
  Serial1.begin(9600); // Right side Raspberry Pi Zero
  Serial3.begin(9600); // Left side Raspberry Pi Zero
  Joystick.clearState();
  for (int i = 0; i < NUM_BUTTONS; i++){
    pinMode(greenPin+i, OUTPUT);      // sets the digital pin 13 as output
    pinMode(bluePin+i, OUTPUT);      // sets the digital pin 13 as output
    pinMode(redPin+i, OUTPUT);      // sets the digital pin 13 as output
    pinMode(inPin+i, INPUT_PULLUP);        // sets the digital pin 7 as input
  }
  
  Serial2.begin(9600); // Arduino Leonardo
}

void loop() {
  
  buttons1 = 0;
  buttons2 = 0;
  
  for (int i = 0; i < NUM_BUTTONS; i++){
 
    values[i] = digitalRead(inPin+i);     // read the input pin
    
    if (values[i] == 0 && previous[i] == 1 && (millis() - firstTime[i]) > 200) {//IF IT IS TURNED ON
      firstTime[i] = millis();
    }

    millis_held[i] = (millis() - firstTime[i]);

    if(values[i] == false && millis_held[i] > TIME_TO_CHANGE_COLOR){
      digitalWrite(redPin+i,HIGH);
      digitalWrite(greenPin+i,HIGH);
      digitalWrite(bluePin+i, LOW);    
    }
    else if(values[i] == false ){
      digitalWrite(redPin+i,HIGH);
      digitalWrite(greenPin+i,LOW);
      digitalWrite(bluePin+i, HIGH);    
    }
    else{
      digitalWrite(redPin+i,LOW);
      digitalWrite(greenPin+i,HIGH);
      digitalWrite(bluePin+i, HIGH);    
    }
    
    previous[i] = values[i];

    if(!values[i]){ // set a byte with each bit containig a button value (on or off)
      if( i < 8 )
        buttons1 += 1 << i;
      else
        buttons2 += 1 << (i-8);
    }
   }

  int q=0;

  if (Serial2.available()) {
    delay(20);
    while(Serial2.available() && q<10) {
      data[q++] = Serial2.read();
    }
  }

  if (Serial3.available()){
    POV1 = (int) Serial3.read();
  }

  if (Serial1.available()){
    POV2 = (int) Serial1.read();
  }

  if(q>0) {
    for (int i =0; i < 4; i++){
      sliders[i].bytes[0] = data[i];
      sliders[i].bytes[1] = (data[4] >> (i*2)) & 3;    
    }
    for (int i =5; i < 7; i++){
      knobs[i-5].bytes[0] = data[i];
      knobs[i-5].bytes[1] = (data[7] >> ((i-5)*2)) & 3;    
    }
    
/*    for(int w = 0; w < q; w++){
      Serial.print(data[w]);
      Serial.print('\t');
    }
    Serial.print('\n');*/
  }

  //clear
  Joystick.clearState();
  //tweak the joystick state (see joystick.h for all possible fields)
  Joystick.state.x.axis = (sliders[0].value - 512) * 64;
  Joystick.state.y.axis = (sliders[1].value - 512) * 64;

  Joystick.state.xRot.axis = (sliders[2].value - 512) * 64;
  Joystick.state.yRot.axis = (sliders[3].value - 512) * 64;

  Joystick.state.z.axis = (knobs[0].value - 512) * 64;
  Joystick.state.zRot.axis = (knobs[1].value - 512) * 64;

  Joystick.state.buttons.data1 = buttons1; // first set of 8 buttons push buttons are set here
  Joystick.state.buttons.data2 = buttons2; // last two buttons push buttons set here
  Joystick.state.buttons.data3 = data[8]; // this byte contains one set of switch data
  Joystick.state.buttons.data4 = data[9]; // last byte contains last set of switch data
  
  Joystick.state.hats.switch1 = POV1;
  Joystick.state.hats.switch2 = POV2;
  //call send state to pack and send the current state over usb
  Joystick.sendState();
//  delay(50);
} 
