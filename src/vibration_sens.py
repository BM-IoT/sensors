from datetime import datetime
import time
import json
import paho.mqtt.client as mqtt
import random

sens_id = "vibration_sensor_1"
delay = 5
running = False

data_vibrate = {
    "sensor_id": sens_id,
    "timestamp": 0,
    "value": 0,
    "unit": "g",
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
            data_vibrate["threshold"] = float(json.loads(payload)["value"])
        case 'd':
            delay = float(json.loads(payload)["value"])



unacked_vibrate_publish = set()
mqtt_vibrate = mqtt.Client()
mqtt_vibrate.user_data_set(unacked_vibrate_publish)
mqtt_vibrate.connect("localhost", 1883, 60)

mqtt_main = mqtt.Client()
mqtt_main.on_message = main_on_message
mqtt_main.connect("localhost", 1883, 60)
mqtt_main.subscribe("brain/control")
mqtt_main.loop_start()

while True:
    if running:
        data_vibrate["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        data_vibrate["value"] = round(random.uniform(0, 1), 2)
        payload_vibrate = json.dumps(data_vibrate)
        mqtt_vibrate.publish("sensors/vibration", payload_vibrate)
        time.sleep(delay)
