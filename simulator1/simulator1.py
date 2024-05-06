#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:29:47 2024

@author: debayanb
"""
import paho.mqtt.client as mqtt
import json
import random
import time

# MQTT broker configuration
broker_address = "173.30.0.100"
port = 1883
topic_monitoring = "greenhouse/monitoring"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Data published")

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to MQTT broker
client.connect(broker_address, port, 60)

# Simulation loop
while True:
    # Simulate monitoring data
    data = {
        "temperature": round(random.uniform(15, 30), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "soil_moisture": round(random.uniform(0, 100), 2),
        "light_intensity": round(random.uniform(0, 1000), 2)
    }

    # Publish data to MQTT topic
    client.publish(topic_monitoring, json.dumps(data))

    # Wait for some time before publishing next data
    time.sleep(5)

