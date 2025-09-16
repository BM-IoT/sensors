from datetime import datetime
import time
import json
import paho.mqtt.client as mqtt
import random

unacked_moist_publish = set()
unacked_vibrate_publish = set()
unacked_strain_publish = set()

mqtt_moist = mqtt.Client()
mqtt_moist.user_data_set(unacked_moist_publish)
mqtt_moist.connect("localhost", 1883, 60)

mqtt_vibrate = mqtt.Client()
mqtt_vibrate.user_data_set(unacked_vibrate_publish)
mqtt_vibrate.connect("localhost", 1883, 60)

mqtt_strain = mqtt.Client()
mqtt_strain.user_data_set(unacked_strain_publish)
mqtt_strain.connect("localhost", 1883, 60)

data_moist = {
    "sensor_id": "humidity_sensor_1",
    "timestamp": 0,
    "value": 0,
    "unit": "g/m3",
    "threshold": 0.8
}

data_vibrate = {
    "sensor_id": "vibration_sensor_1",
    "timestamp": 0,
    "value": 0,
    "unit": "g",
    "threshold": 0.8
}

data_strain = {
    "sensor_id": "strain_sensor_1",
    "timestamp": 0,
    "value": 0,
    "unit": "ue",
    "threshold": 0.8
}

while True:
    data_moist["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    data_moist["value"] = round(random.uniform(0, 1), 2)
    payload_moist = json.dumps(data_moist)
    mqtt_moist.publish("sensors/moisture", payload_moist)
    
    data_vibrate["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    data_vibrate["value"] = round(random.uniform(0, 1), 2)
    payload_vibrate = json.dumps(data_vibrate)
    mqtt_vibrate.publish("sensors/vibration", payload_vibrate)
    
    data_strain["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    data_strain["value"] = round(random.uniform(0, 1), 2)
    payload_strain = json.dumps(data_strain)
    mqtt_strain.publish("sensors/strain", payload_strain)
    
    time.sleep(3)
    
mqtt_moist.loop_forever()
mqtt_vibrate.loop_forever()
mqtt_strain.loop_forever()	
