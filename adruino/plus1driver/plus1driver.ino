#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN_6 6
#define PIN_7 7
#define PIN_8 8
#define PIN_9 9
#define PIN_10 10
#define PIN_11 11
#define NUM_LEDS 15

#define BRIGHTNESS 50
#define BLUE 255
#define WHITE 16777215
#define GREEN 65280
#define RED 16711680
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN_6, NEO_GRBW + NEO_KHZ800);
Adafruit_NeoPixel strip2 = Adafruit_NeoPixel(NUM_LEDS, PIN_7, NEO_GRBW + NEO_KHZ800);
Adafruit_NeoPixel strip3 = Adafruit_NeoPixel(NUM_LEDS, PIN_8, NEO_GRBW + NEO_KHZ800);
Adafruit_NeoPixel strip4 = Adafruit_NeoPixel(NUM_LEDS, PIN_9, NEO_GRBW + NEO_KHZ800);
Adafruit_NeoPixel strip5 = Adafruit_NeoPixel(NUM_LEDS, PIN_10, NEO_GRBW + NEO_KHZ800);
Adafruit_NeoPixel strip6 = Adafruit_NeoPixel(NUM_LEDS, PIN_11, NEO_GRBW + NEO_KHZ800);
byte neopix_gamma[] = {
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 };
String blueToothVal;           //value sent over via bluetooth
char stringIndex;              //stores last state of device (on/off)
char pixelIndex;              //stores which pixel is being adjusted
char colorIndex;              //stores which color is now being set
char brightIndex;              //stores what brightness we are setting the device to

void setup() {
  Serial.begin(9600);  //set Baud rate
  strip.setBrightness(BRIGHTNESS);
  strip2.setBrightness(BRIGHTNESS);
  strip3.setBrightness(BRIGHTNESS);
  strip4.setBrightness(BRIGHTNESS);
  strip5.setBrightness(BRIGHTNESS);
  strip6.setBrightness(BRIGHTNESS);
  strip.begin();
  strip2.begin();
  strip3.begin();
  strip4.begin();
  strip5.begin();
  strip6.begin();
  strip.show(); // Initialize all pixels to 'off'
  strip2.show(); // Initialize all pixels to 'off'
  strip3.show(); // Initialize all pixels to 'off'
  strip4.show(); // Initialize all pixels to 'off'
  strip5.show(); // Initialize all pixels to 'off'
  strip6.show(); // Initialize all pixels to 'off'
}

void loop() {
  while(Serial.available()>0)
  {//while there is data available on the serial monitor
    blueToothVal+=char(Serial.read());//store string from serial command
  }
  if(!Serial.available())
  {
  Serial.println(blueToothVal);
  stringIndex = blueToothVal.charAt(0);
  pixelIndex = blueToothVal.charAt(1);
  colorIndex = blueToothVal.charAt(2);
  brightIndex = blueToothVal.charAt(3);
  // Some example procedures showing how to display to the pixels:
  if (stringIndex=='1')
  {//if value from bluetooth serial is 1 make the LED white
    colorWipe(strip.Color(255, 255, 255), 50); // White
    Serial.println(F("Specific Pixel Function")); //print LED is on
    blueToothVal=""; //clear the data
  }
  else if (stringIndex=='7')
  {//full display
    //so for full display I need colorIndex and brightness Index
    colorFullDisplay(colorIndexGet(colorIndex),brightIndexGet(brightIndex),3);
    Serial.println(F("Full Display On")); //print LED is on
    blueToothVal=""; //clear the data
  }
  else if (stringIndex=='8')
  {//right side of the display
    colorRightDisplay(colorIndexGet(colorIndex),brightIndexGet(brightIndex),3);
    Serial.println(F("Right Side of Display")); //print LED is on
    blueToothVal=""; //clear the data
  }
  else if (stringIndex=='9')
  {//left side of the display
    colorLeftDisplay(colorIndexGet(colorIndex),brightIndexGet(brightIndex),3);
    Serial.println(F("Left Side of Display")); //print LED is on
    blueToothVal=""; //clear the data
  }
  else if (stringIndex=='0')
  {//if value from bluetooth serial is 0 make the LEDs off
    DisplayOff();
    Serial.println(F("Entire Display Off")); //print LED is on
    blueToothVal=""; //clear the data
  }
  }
  blueToothVal=""; //clear the data
  delay(4000);
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
  Serial.println(c);
}

void pulseWhite(uint8_t wait) {
  for(int j = 0; j < 256 ; j++){
      for(uint16_t i=0; i<strip.numPixels(); i++) {
          strip.setPixelColor(i, strip.Color(0,0,0, neopix_gamma[j] ) );
        }
        delay(wait);
        strip.show();
      }

  for(int j = 255; j >= 0 ; j--){
      for(uint16_t i=0; i<strip.numPixels(); i++) {
          strip.setPixelColor(i, strip.Color(0,0,0, neopix_gamma[j] ) );
        }
        delay(wait);
        strip.show();
      }
}


void rainbowFade2White(uint8_t wait, int rainbowLoops, int whiteLoops) {
  float fadeMax = 100.0;
  int fadeVal = 0;
  uint32_t wheelVal;
  int redVal, greenVal, blueVal;

  for(int k = 0 ; k < rainbowLoops ; k ++){
    
    for(int j=0; j<256; j++) { // 5 cycles of all colors on wheel

      for(int i=0; i< strip.numPixels(); i++) {

        wheelVal = Wheel(((i * 256 / strip.numPixels()) + j) & 255);

        redVal = red(wheelVal) * float(fadeVal/fadeMax);
        greenVal = green(wheelVal) * float(fadeVal/fadeMax);
        blueVal = blue(wheelVal) * float(fadeVal/fadeMax);

        strip.setPixelColor( i, strip.Color( redVal, greenVal, blueVal ) );

      }

      //First loop, fade in!
      if(k == 0 && fadeVal < fadeMax-1) {
          fadeVal++;
      }

      //Last loop, fade out!
      else if(k == rainbowLoops - 1 && j > 255 - fadeMax ){
          fadeVal--;
      }

        strip.show();
        delay(wait);
    }
  
  }



  delay(500);


  for(int k = 0 ; k < whiteLoops ; k ++){

    for(int j = 0; j < 256 ; j++){

        for(uint16_t i=0; i < strip.numPixels(); i++) {
            strip.setPixelColor(i, strip.Color(0,0,0, neopix_gamma[j] ) );
          }
          strip.show();
        }

        delay(2000);
    for(int j = 255; j >= 0 ; j--){

        for(uint16_t i=0; i < strip.numPixels(); i++) {
            strip.setPixelColor(i, strip.Color(0,0,0, neopix_gamma[j] ) );
          }
          strip.show();
        }
  }

  delay(500);


}

void whiteOverRainbow(uint8_t wait, uint8_t whiteSpeed, uint8_t whiteLength ) {
  
  if(whiteLength >= strip.numPixels()) whiteLength = strip.numPixels() - 1;

  int head = whiteLength - 1;
  int tail = 0;

  int loops = 3;
  int loopNum = 0;

  static unsigned long lastTime = 0;


  while(true){
    for(int j=0; j<256; j++) {
      for(uint16_t i=0; i<strip.numPixels(); i++) {
        if((i >= tail && i <= head) || (tail > head && i >= tail) || (tail > head && i <= head) ){
          strip.setPixelColor(i, strip.Color(0,0,0, 255 ) );
        }
        else{
          strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
        }
        
      }

      if(millis() - lastTime > whiteSpeed) {
        head++;
        tail++;
        if(head == strip.numPixels()){
          loopNum++;
        }
        lastTime = millis();
      }

      if(loopNum == loops) return;
    
      head%=strip.numPixels();
      tail%=strip.numPixels();
        strip.show();
        delay(wait);
    }
  }
  
}
void fullWhite() {
  
    for(uint16_t i=0; i<strip.numPixels(); i++) {
        strip.setPixelColor(i, strip.Color(0,0,0, 255 ) );
    }
      strip.show();
}


// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256 * 5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3,0);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3,0);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0,0);
}

uint8_t red(uint32_t c) {
  return (c >> 16);
}
uint8_t green(uint32_t c) {
  return (c >> 8);
}
uint8_t blue(uint32_t c) {
  return (c);
}
uint32_t brightIndexGet(char bI){
  //uint32_t j =  (bI << 3) + (bI << 1);
  int inbetween = bI - '0';
  uint32_t j = inbetween*10;
  return (j);
}
uint32_t colorIndexGet(char cI){
  uint32_t j = 0;
  if(cI == 'r'){
    j = 16711680;
  }
  else if(cI == 'g'){
    j = 65280;
  }
  else if(cI == 'b'){
    j = 255;
  }
  else if(cI == 'w'){
    j = 16777215;
  }
  return (j);
}
// Entire Display
void colorFullDisplay(uint32_t c, uint32_t bright, uint8_t wait) {
    for(uint16_t i=0; i<strip.numPixels(); i++) {
        strip.setPixelColor(i,c);
        strip2.setPixelColor(i,c);
        strip3.setPixelColor(i,c);
        strip4.setPixelColor(i,c);
        strip5.setPixelColor(i,c);
        strip6.setPixelColor(i,c);
    }    
    strip.setBrightness(bright); 
    strip.show();
    strip2.setBrightness(bright); 
    strip2.show();
    strip3.setBrightness(bright); 
    strip3.show();
    strip4.setBrightness(bright); 
    strip4.show();
    strip5.setBrightness(bright); 
    strip5.show();
    strip6.setBrightness(bright); 
    strip6.show();
    delay(wait);
}
// Right Side of the Display
void colorRightDisplay(uint32_t c, uint32_t bright, uint8_t wait) {
    for(uint16_t i=0; i<strip.numPixels(); i++) {
        strip.setPixelColor(i,c);
        strip2.setPixelColor(i,c);
        strip3.setPixelColor(i,c);
    }    
    strip.setBrightness(bright); 
    strip.show();
    strip2.setBrightness(bright); 
    strip2.show();
    strip3.setBrightness(bright); 
    strip3.show();
    delay(wait);
}
// Left Side of the Display
void colorLeftDisplay(uint32_t c, uint32_t bright, uint8_t wait) {
    for(uint16_t i=0; i<strip.numPixels(); i++) {
        strip4.setPixelColor(i,c);
        strip5.setPixelColor(i,c);
        strip6.setPixelColor(i,c);
    }    
    strip4.setBrightness(bright); 
    strip4.show();
    strip5.setBrightness(bright); 
    strip5.show();
    strip6.setBrightness(bright); 
    strip6.show();
    delay(wait);
}
// Entire Display Off
void DisplayOff() {
    for(uint16_t i=0; i<strip.numPixels(); i++) {
        strip.setPixelColor(i,0);
        strip2.setPixelColor(i,0);
        strip3.setPixelColor(i,0);
        strip4.setPixelColor(i,0);
        strip5.setPixelColor(i,0);
        strip6.setPixelColor(i,0);
    }    
    strip.setBrightness(0); 
    strip.show();
    strip2.setBrightness(0); 
    strip2.show();
    strip3.setBrightness(0); 
    strip3.show();
    strip4.setBrightness(0); 
    strip4.show();
    strip5.setBrightness(0); 
    strip5.show();
    strip6.setBrightness(0); 
    strip6.show();
}
