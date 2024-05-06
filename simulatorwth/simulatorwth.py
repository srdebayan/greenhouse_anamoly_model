#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:44:08 2024

@author: debayanb
"""

import paho.mqtt.client as mqtt
import json
import random
import time

# MQTT broker configuration
broker_address = "173.30.0.100"
port = 1883
topic_weather_forecast = "greenhouse/weather_forecast"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Weather forecast data published")

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to MQTT broker
client.connect(broker_address, port, 60)

# Simulation loop
while True:
    # Simulate weather forecast data
    forecast_data = {
        "temperature": round(random.uniform(15, 30), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "rain": random.choice(["yes", "no"])
    }

    # Publish data to MQTT topic
    client.publish(topic_weather_forecast, json.dumps(forecast_data))

    # Wait for some time before publishing next data
    time.sleep(10)
