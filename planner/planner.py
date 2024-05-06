#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 22:53:58 2024

@author: debayanb
"""
import paho.mqtt.client as mqtt
import json

# MQTT broker configuration
broker_address = "173.30.0.100"
port = 1883
topic_analyzer = "greenhouse/analysis"
topic_weather_forecast = "greenhouse/weather_forecast"
topic_planner = "greenhouse/planning"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic_analyzer)
    print(f"Subscribed to {topic_analyzer}")
    client.subscribe(topic_weather_forecast)
    print(f"Subscribed to {topic_weather_forecast}")

def on_message(client, userdata, msg):
    global anomaly_score
    global rain_forecast

    # Parse JSON message
    data = json.loads(msg.payload)
    print(f"Received message on {msg.topic}: {data}")

    # Update anomaly score or rain forecast based on topic
    if msg.topic == topic_analyzer:
        anomaly_score = data["anomaly_score"]
        print(f"Updated anomaly score: {anomaly_score}")
    elif msg.topic == topic_weather_forecast:
        rain_forecast = data["rain"]
        print(f"Updated rain forecast: {rain_forecast}")

    # Plan actions based on analysis result and weather forecast
    if anomaly_score == -1:
        if rain_forecast == "yes":
            planned_actions = "Close windows, Turn off fans"
        else:
            planned_actions = "Adjust ventilation, Turn on fans"
    else:
        planned_actions = "No action required"
    print(f"Determined planned actions: {planned_actions}")

    # Publish planned actions to MQTT topic
    planned_actions = {
        "actions": planned_actions.split(", ")
    }
    client.publish(topic_planner, json.dumps(planned_actions))
    print(f"Published planned actions to {topic_planner}")

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker_address, port, 60)
print(f"Connected to MQTT broker at {broker_address}:{port}")

# Global variables to store anomaly score and rain forecast
anomaly_score = 0
rain_forecast = ""

# Keep the client running to receive messages
client.loop_forever()


