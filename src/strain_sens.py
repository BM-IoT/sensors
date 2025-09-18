from datetime import datetime
import time
import json
import paho.mqtt.client as mqtt
import random

sens_id = "strain_sensor_1"
delay = 5
running = False

data_strain = {
    "sensor_id": sens_id,
    "timestamp": 0,
    "value": 0,
    "unit": "ue",
    "threshold": 0.8
}

def main_on_message(client, userdata, msg):
    global running, delay

    payload = msg.payload.decode("utf-8")
    id = json.loads(payload)["id"]

    if (id != sens_id):
        return
    
    cmd = json.loads(payload)["cmd"]
    match cmd:
        case 's':
            running = False
        case 'b':
            running = True
        case 't':
            data_strain["threshold"] = float(json.loads(payload)["value"])
        case 'd':
            delay = float(json.loads(payload)["value"])



unacked_strain_publish = set()
mqtt_strain = mqtt.Client()
mqtt_strain.user_data_set(unacked_strain_publish)
mqtt_strain.connect("localhost", 1883, 60)

mqtt_main = mqtt.Client()
mqtt_main.on_message = main_on_message
mqtt_main.connect("localhost", 1883, 60)
mqtt_main.subscribe("brain/control")
mqtt_main.loop_start()

while True:
    if running:
        data_strain["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        data_strain["value"] = round(random.uniform(0, 1), 2)
        payload_strain = json.dumps(data_strain)
        mqtt_strain.publish("sensors/strain", payload_strain)
        time.sleep(delay)
