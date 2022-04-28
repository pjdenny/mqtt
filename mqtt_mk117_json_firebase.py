# subscriber.py
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import json
from firebase import firebase  
firebase = firebase.FirebaseApplication('https://mqtt-360be-default-rtdb.asia-southeast1.firebasedatabase.app/', None)  



def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    # client.subscribe("IoTSolutions/#")
    #client.subscribe("MK117-16d0/#")
    client.subscribe("MK117-3e04/04/device_to_app/#")
# the callback function, it will be triggered when receiving messages 
def on_message(client, userdata, msg):
    json_object= str(msg.payload.decode("utf-8"))
    message = json.loads(json_object)
    if message['msg_id'] ==1006:
        print(f"{msg.topic}")
        print("MessageId:",message['msg_id'])
        print("Voltage:",message['data']['voltage'])
        print("Current:",message['data']['current'])
        print("Power:",message['data']['power'])
        print("Pf:",message['data']['power_factor'])
        print("time:", message['data']['timestamp'])
        data =  {message['data']['timestamp']:
            { 
            'voltage': message['data']['voltage'],  
          'current': message['data']['current'],  
          'power': message['data']['power']  
          }  
        }
        time.sleep(3)  
        now = datetime.now()

        result = firebase.post('/python-sample-ed7f7/moko/',data)  
        print(result) 
    elif message['msg_id'] ==1001:  
        print(f"{msg.topic}")
        print("MessageId:",message['msg_id'])
        print("switch_state:",message['data']['switch_state'])
        print("load_state:",message['data']['load_state'])
        print("overload_state:",message['data']['overload_state'])
        print("overcurrent_state:",message['data']['overcurrent_state'])
        print("overvoltage_state:",message['data']['overvoltage_state'])
        print("time:", message['data']['timestamp'])
        
    else:
        print(f"{msg.topic}")
        print("MessageId:",message['msg_id'])
        print("EC:",message['data']['EC'])
        print("all_energy:",message['data']['all_energy'])
        print("thirty_day_energy:",message['data']['thirty_day_energy'])
        print("current_hour_energy:",message['data']['current_hour_energy'])
        print("time:", message['data']['timestamp'])



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
# client.will_set('raspberry/status', b'{"status": "Off"}')

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect("broker.emqx.io", 1883, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()