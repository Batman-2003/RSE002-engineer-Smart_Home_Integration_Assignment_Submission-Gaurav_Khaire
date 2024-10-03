import os
import paho.mqtt.client as paho
from time import sleep
from datetime import datetime
from numpy import random

from Task2_CentralControlSystem import MQTT_ADDR, MQTT_PORT, MQTT_TOPIC

motionPublisher = paho.Client()
if motionPublisher.connect(MQTT_ADDR, MQTT_PORT) != 0:
    print("Error Connecting to Broker make sure mosquitto is running")
    os._exit(-1)
for _ in range(10_000):
    motionPublisher.publish(MQTT_TOPIC, f"{datetime.now()} | {random.randint(0, 1024)}")
    print(f"motionCounter: {_}")
    sleep(0.01)
motionPublisher.disconnect()