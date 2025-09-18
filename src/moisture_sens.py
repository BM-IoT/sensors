from datetime import datetime
import time
import json
import paho.mqtt.client as mqtt
import random

sens_id = "humidity_sensor_1"
delay = 5
running = False

data_moist = {
    "sensor_id": sens_id,
    "timestamp": 0,
    "value": 0,
    "unit": "g/m3",
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
            data_moist["threshold"] = float(json.loads(payload)["value"])
        case 'd':
            delay = float(json.loads(payload)["value"])



unacked_moist_publish = set()
mqtt_moist = mqtt.Client()
mqtt_moist.user_data_set(unacked_moist_publish)
mqtt_moist.connect("localhost", 1883, 60)

mqtt_main = mqtt.Client()
mqtt_main.on_message = main_on_message
mqtt_main.connect("localhost", 1883, 60)
mqtt_main.subscribe("brain/control")
mqtt_main.loop_start()

while True:
    if running:
        data_moist["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        data_moist["value"] = round(random.uniform(0, 1), 2)
        payload_moist = json.dumps(data_moist)
        mqtt_moist.publish("sensors/moisture", payload_moist)
        time.sleep(delay)
