import paho.mqtt.client as mqtt
import time
import sys
import random
import threading



def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)



mqtt_topic = 'energy_meter/Raju/meter_id_01/voltage'   
value = '230'
mqtt_topic1 = 'energy_meter/Raju/meter_id_01/current'   
value1 = '10'
mqtt_topic2 = 'energy_meter/Raju/meter_id_01/pf'   
value2 = '.8'

        # the four parameters are topic, sending content, QoS and whether retaining the message respectively
#client.publish(mqtt_topic, payload=value, qos=0, retain=False)
def printit():
  threading.Timer(10.0, printit).start()
  
  client.publish(mqtt_topic, payload=value,qos=0, retain=False)
  print(f"send {value} to mqtt topic : {mqtt_topic}")

  time.sleep(3)
  client.publish(mqtt_topic1, payload=value1,qos=0, retain=False)
  print(f"send {value1} to mqtt topic : {mqtt_topic1}")

  time.sleep(3)
  client.publish(mqtt_topic2, payload=value2,qos=0, retain=False)
  print(f"send {value2} to mqtt topic : {mqtt_topic2}")


printit()



time.sleep(3)

client.loop_forever()