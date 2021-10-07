#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <ArduinoJson.hpp>
#include <ArduinoJson.h>

#define dt 1.0 //portion of time for sampling

Adafruit_BMP085 bmp;
int F_S = 1/dt;       //Sampling frequency in Hz
int T_S = 1000/F_S;   //Sampling period in milliseconds
int sample_max_num=10, time_of_sampling=10;
int scounter = 1;
float temp, pres;
boolean inisam = false;
unsigned long t1,t2;

void setup(){
  Serial.begin(9600);
  Wire.begin();
  //Initiating preassure BMP180 sensor
  if (!bmp.begin(0x76)) {
    Serial.println("Could not find a valid BMP180 sensor, check wiring!");
    while (1){
      delay(250);
    }
  }
}

void send_bmp180_temp(float temp, float pres){
  //Json template
  StaticJsonDocument<150> doc;
  String json_msg;
  JsonObject temp_val_obj = doc.createNestedObject("bmp180");
  temp_val_obj["temp"] = temp;
  temp_val_obj["pres"] = pres;
  serializeJson(doc, json_msg);
  Serial.println(json_msg);
}

float read_bmp180_pres(){
  float pres = bmp.readPressure();
  return pres;
}

float read_bmp180_temp(){
  float temp = bmp.readTemperature();
  return temp;
}

void check_status_of_sampling(){
  if(scounter < sample_max_num){
    scounter++;
  }
  else{
    scounter = 1;
    inisam = false;
  }
}

void get_command(){
  if(Serial.available()>0){
    char cmd = Serial.read();
    switch(cmd){
      case 'i':
        inisam = true; //start sampling process flag
        break;
      case 'c':
        Serial.println(cmd); //send c character to confirm communication 
        break;
      case 's':
        while(Serial.available()<1){}
        time_of_sampling = int(Serial.parseInt());
        sample_max_num = time_of_sampling/dt;
        break;
    }
  }
}
 
void loop(){
  if(inisam){
    t1 = millis();

    temp = read_bmp180_temp();
    pres = read_bmp180_pres();
    send_bmp180_temp(temp,pres);
    check_status_of_sampling();
    
    t2 = millis() - t1;
    if(t2 < T_S) delay(T_S - t2);
  }
  get_command();
}
