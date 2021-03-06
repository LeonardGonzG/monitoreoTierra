#include <DFRobot_BME280.h>

/* raed_data_i2c.ino
 *
 * Download this demo to test read data from bme280, connect sensor through IIC interface
 * Data will print on your serial monitor
 *
 * Copyright   [DFRobot](https://www.dfrobot.com), 2016
 * Copyright   GNU Lesser General Public License
 *
 * version  V1.0
 * date  12/03/2019
 */

int SensorPin = A1;
#include "Wire.h"

typedef DFRobot_BME280_IIC    BME;    // ******** use abbreviations instead of full names ********

BME   bme(&Wire, 0x77);   // select TwoWire peripheral and set sensor address

#define SEA_LEVEL_PRESSURE    1015.0f

// show last sensor operate status
void printLastOperateStatus(BME::eStatus_t eStatus)
{
  switch(eStatus) {
  case BME::eStatusOK:    Serial.println("everything ok"); break;
  case BME::eStatusErr:   Serial.println("unknow error"); break;
  case BME::eStatusErrDeviceNotDetected:    Serial.println("device not detected"); break;
  case BME::eStatusErrParameter:    Serial.println("parameter error"); break;
  default: Serial.println("unknow status"); break;
  }
}

void setup()
{
  Serial.begin(115200);
  bme.reset();
  Serial.println("bme read data test");
  while(bme.begin() != BME::eStatusOK) {
    Serial.println("bme begin faild");
    printLastOperateStatus(bme.lastOperateStatus);
    delay(2000);
  }
  Serial.println("bme begin success");
  pinMode(2, OUTPUT);

  delay(100);
}

void loop()
{
  float   temp = bme.getTemperature();
  uint32_t    press = bme.getPressure();
  float   alti = bme.calAltitude(SEA_LEVEL_PRESSURE, press);
  float   humi = bme.getHumidity();

  int humedadSuelo = analogRead(SensorPin);

  Serial.println();
  Serial.println("======== start print ========");
  Serial.print("temperature (unit Celsius): "); Serial.println(temp);
  Serial.print("pressure (unit pa):         "); Serial.println(press);
  Serial.print("altitude (unit meter):      "); Serial.println(alti);
  Serial.print("humidity (unit percent):    "); Serial.println(humi);

  if(analogRead(0)<300) Serial.println("Heavy Rain");
  else if(analogRead(0)<500) Serial.println("Moderate Rain");
  else Serial.println("No Rain");

  Serial.print("Humedad suelo: ");Serial.println(humedadSuelo);

  Serial.println("========  end print  ========");
  
  delay(500);
}
