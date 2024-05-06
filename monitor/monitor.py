#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:45:16 2024

@author: debayanb
"""

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import json

# MQTT broker configuration
broker_address = "173.30.0.100"
port = 1883
topic_monitoring = "greenhouse/monitoring"

# InfluxDB configuration
influxdb_host = "173.30.0.104"
influxdb_port = 8086
influxdb_token = "b320d3x72fwC6N-E07xD-pa1_B9jm6Wi2cNLH1ZPDqe2qkA3e_VbQNGrHwTfrPnHlUFmuea7PqCSQXFAmxJDPQ=="
influxdb_org = "univaq"
influxdb_bucket = "greenhouse"
influxdb_measurement = "monitoring"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic_monitoring)

def on_message(client, userdata, msg):
    # Parse JSON message
    data = json.loads(msg.payload)
    
    # Store data in InfluxDB
    influx_client = InfluxDBClient(url=f"http://{influxdb_host}:{influxdb_port}", token=influxdb_token, org=influxdb_org)
    write_api = influx_client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000, jitter_interval=2_000, retry_interval=5_000))
    
    point = Point(influxdb_measurement).field("temperature", data["temperature"]).field("humidity", data["humidity"]).field("soil_moisture", data["soil_moisture"]).field("light_intensity", data["light_intensity"])
    
    write_api.write(influxdb_bucket, influxdb_org, point)

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker_address, port, 60)

# Keep the client running to receive messages
client.loop_forever()
