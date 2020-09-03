from machine import Pin
from dht import DHT11 
import network
import urequests

import esp
esp.osdebug(None)

import gc
gc.collect()

#COnectar na rede wifi
ssid = 'SSID'
password = 'Password'

#Chave da aplicação IFTT
api_key = 'Your Key'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

#Sensor de Temperatura e Humidade
sensor = DHT11(Pin(19))
 
try:
  sensor.measure()
  temp = sensor.temperature()
  humidity = sensor.humidity()
  print('Temperature: %2.2f C' %temp)
  print('Humidity: %2.2f %%' %humidity)


  sensor_readings = {'value1':temp, 'value2':humidity}
  print(sensor_readings)

  request_headers = {'Content-Type': 'application/json'}

#Substituir "/Topic/" pelo nome do seu tópico
  request = urequests.post(
    'http://maker.ifttt.com/trigger/topic/with/key/' + api_key,
    json=sensor_readings,
    headers=request_headers)
  print(request.text)
  request.close()

except OSError as e:
  print('Failed to read/publish sensor readings.')