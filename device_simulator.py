# subscriber.py
import time
import math
import random
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import threading
import datetime
from datetime import datetime,timedelta


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    

client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)


mqtt_topic = 'ion/smarthome/energy_meter/pump'


dt = datetime(2023, 2, 1, 6, 0, 0)
def publish_it():
    #call this function every 5 seconds
  threading.Timer(60.0, publish_it).start()
  for d in range(1,30):
   for h in range(1,24):
      for m in range(1,60):
        print(f"Meter value Simulation for day  {d} at time  {h}Hrs:{m:02d}Mins for {mqtt_topic}")
        time.sleep(5)
        v=random.randint(220,242)
        amplitude_random_component =(random.randint(0,200))/100 # random value generation between 0 to 2 amps
        amplitude = (math.sin(m/60 * 2*math.pi) + 1) / 2 * 10 + 4 # sin wave generation between 10 to 14 amps
        total_amplitude =amplitude_random_component + amplitude # combine both amplitude to swing between 0 to 16 amps
        i= round(total_amplitude,2)
        c=(random.randint(800,900))/1000 # random value powerfactor generation between 0.8 to 0.9 to simulate non resistive loads
        p=round(v*i*c/1000,2) 
        kwh= (round((p/1000)*3600/1000,2))
        ade= (round((p/1000)*24*3600/1000,2))
        data =json.dumps({
            'Voltage [Volts]': v,
            'Current [Amps]': i,
#            'Time': str(datetime.datetime.now() + datetime.timedelta(minutes = m,hours=h, days=d)),
             'Timestamp': str(dt + timedelta(minutes = m,hours=h, days=d)),
            'Pf [powerfactor]': c,
            'Power [Watts]': p,
            'Energy consumed in the current hour [KiloWatt-Hour]': kwh,
            'Energy consumed all day (24hrs) [KiloWatt-Hour]': ade
            });
        client.publish(mqtt_topic, data, qos=0, retain=False)
  #print the mqtt topic name and value on the command line console.
        print(f"{data}")
        #print(f"send {data} to mqtt topic : {mqtt_topic}")
       
time.sleep(5)

#run the publish_it function {
publish_it()

client.loop_forever()
  

