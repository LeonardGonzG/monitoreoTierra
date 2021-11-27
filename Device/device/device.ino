#include <DFRobot_BME280.h>

int SensorPin = A1;
#include "Wire.h"

typedef DFRobot_BME280_IIC    BME;    

BME   bme(&Wire, 0x77);

#define SEA_LEVEL_PRESSURE    1015.0f

// show last sensor operate status
void printLastOperateStatus(BME::eStatus_t eStatus)
{
  switch(eStatus) {
  case BME::eStatusOK:  Serial.println("{\"status\":400,\"msg\":\"everything ok\"}"); break; 
  case BME::eStatusErr:  Serial.println("{\"status\":400,\"msg\":\"unknow error\"}"); break;
  case BME::eStatusErrDeviceNotDetected:  Serial.println("{\"status\":400,\"msg\":\"device not detected\"}"); break;
  case BME::eStatusErrParameter:  Serial.println("{\"status\":400,\"msg\":\"parameter error\"}"); break;
  default:  Serial.println("{\"status\":400,\"msg\":\"unknow status\"}"); break;
  }
} 

void setup()
{
  Serial.begin(230400);
  bme.reset();
  //Serial.println("bme read data test");
  while(bme.begin() != BME::eStatusOK) {
    
   // Serial.println("{\"status\":400,"+ "\"msg\":");
    //Serial.println("bme begin faild");
    printLastOperateStatus(bme.lastOperateStatus);
    delay(2000);
  }
 // Serial.println("bme begin success");
  pinMode(2, OUTPUT);

  delay(100);

  
}

void loop()
{
  float   temp = bme.getTemperature();
  uint32_t    press = bme.getPressure();
  float   alti = bme.calAltitude(SEA_LEVEL_PRESSURE, press);
  float   humi = bme.getHumidity();
  int rain = analogRead(0);
  int humedadSuelo = analogRead(SensorPin);

  String json_data ="{\"status\":200,\"temperature\":"+(String)temp 
                    + ",\"pressure\":"+(String)press+ ",\"altitude\":"+(String)alti
                    + ",\"humidity\":"+(String)humi+",\"rain\":"+ (String)rain+ ",\"humidityFloor\":"+(String)humedadSuelo+"}";


  Serial.println(json_data);
  
  delay(500);
}
