#include <SoftwareSerial.h>
#include <TinyGPS.h>
#include <boltiot.h>

float flat,flon;
SoftwareSerial gpsSerial(3,4);
TinyGPS gps;


void setup(){
  Serial.begin(9600);
  gpsSerial.begin(9600);
  boltiot.begin(Serial);
  delay(8000);
}

static void smartdelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (gpsSerial.available())
      gps.encode(gpsSerial.read());
  } while (millis() - start < ms);
}

void loop(){
  smartdelay(1000);

  gps.f_get_position(&flat, &flon);

  Serial.print("Latitude");
  Serial.print("\n");
  delay(1000);
  Serial.print(flat,7);
  delay(1000);
  Serial.print("\n");
  Serial.print("Longitude");
  Serial.print("\n");
  delay(1000);
  Serial.print(flon,7);
  Serial.print("\n");
  delay(1000);
}
