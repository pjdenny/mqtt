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


# the four parameters are topic, sending content, QoS and whether retaining the message respectively
#client.publish(mqtt_topic, payload=value, qos=0, retain=False)
#define the publish_it function as follows.
def publish_it():
  #call this function every 5 seconds
  threading.Timer(5.0, publish_it).start()
  #generate a random number between the range of 220 and 250 representing changing AC voltage.
  a=random.randint(220,250)
  value = a
  #publish mqtt message with topic assigned to "mqtt_topic" and payload = value
  client.publish(mqtt_topic, payload=value,qos=0, retain=False)
  #print the mqtt topic name and value on the command line console.
  print(f"send {value} to mqtt topic : {mqtt_topic}")

#run the publish_it function 
publish_it()



time.sleep(3)

client.loop_forever()