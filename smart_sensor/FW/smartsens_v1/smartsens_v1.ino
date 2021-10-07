/* SmartSens
 *  
 *  this program senses temperature and express a specific red or blue led light
 * by EMFS - 7/01/21
 */

#include <Wire.h>
#include <Adafruit_BMP085.h>
#define dt 0.2 //portion of time for sampling

Adafruit_BMP085 bmp;
unsigned long t1,t2;
int F_S = 1/dt;       //Sampling frequency in Hz
int T_S = 1000/F_S;   //Sampling period in milliseconds
float temp;
float max_temp = 35.0;

// blue (from 0 to 255) = bw1*temperature + bw0
// red (from 0 to 255) = rw1*temperature + rw0
float bw0 = 987.81;
float bw1 = -987.85;
float rw0 = -723.62;
float rw1 = 975.65;
int blue;
byte red;

byte rlp= 9; //red ligth pin
byte glp = 10;
byte blp = 11;

void setup() 
{
  pinMode(rlp, OUTPUT);
  pinMode(glp, OUTPUT);
  pinMode(blp, OUTPUT);
  Serial.begin(9600);
  Wire.begin();
  //INitiating preassure BMP180 sensor
  if (!bmp.begin(0x76)) {
    Serial.println("Could not find a valid BMP180 sensor, check wiring!");
    while (1){
      delay(250);
    }
  }
}

float get_b_rgbval(float temp){
  float bval = temp*bw1 + bw0;
  if (bval >= 255.0) bval = 255.0;
  if (bval <= 0.0) bval = 0.0;
  return bval;
}

float get_r_rgbval(float temp){
  float rval = temp*rw1 + rw0;
  if (rval >= 255.0) rval = 255.0;
  if (rval <= 0.0) rval = 0.0;
  return rval;
}

float read_bmp180_temp(){
  float temp = (float)bmp.readTemperature()/max_temp;
  return temp;
}

void set_rgbled_colors(byte blue, byte red){
  analogWrite(rlp,red);
  analogWrite(glp,0);
  analogWrite(blp,blue);
}

void rgb_vals_debug(float temp,byte blue,byte red){
  Serial.println("Temperature: " + String(temp*max_temp));
  Serial.println("Blue: " + String(blue));
  Serial.println("Red: " + String(red));
}

void loop() 
{
  t1 = millis();

  temp = read_bmp180_temp();
  blue = (byte)get_b_rgbval(temp);
  red = (byte)get_r_rgbval(temp);
  set_rgbled_colors(blue,red);
  //rgb_vals_debug(temp,blue,red);
  
  t2 = millis() - t1;
  if(t2 < T_S) delay(T_S - t2);
}
