#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:30:00 2024

@author: debayanb
"""

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient
import json
import numpy as np
from sklearn.ensemble import IsolationForest
import time 

# MQTT and InfluxDB configuration
broker_address = "173.30.0.100"
port = 1883
influxdb_host = "173.30.0.104"
influxdb_port = 8086
influxdb_token = "b320d3x72fwC6N-E07xD-pa1_B9jm6Wi2cNLH1ZPDqe2qkA3e_VbQNGrHwTfrPnHlUFmuea7PqCSQXFAmxJDPQ=="
influxdb_org = "univaq"
influxdb_bucket = "greenhouse"
influxdb_measurement = "monitoring"
topics = {
    "monitoring": "greenhouse/monitoring",
    "analyzer": "greenhouse/analysis",
    "feedback": "greenhouse/feedback"
}

# Machine Learning Model
model = IsolationForest()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in topics.values():
        client.subscribe(topic)
    print("Subscribed to topics:", topics.values())

def on_message(client, userdata, msg):
    if msg.topic == topics['monitoring']:
        handle_monitoring_data(msg)
    elif msg.topic == topics['feedback']:
        handle_feedback(msg)



def handle_monitoring_data(msg):
    try:
        data = json.loads(msg.payload)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return

    value = data.get('temperature')
    if value is not None:
        print("Waiting for 2 seconds before analyzing data...")
        time.sleep(2)  # Delay of 2 seconds
        anomaly_score = predict_anomaly(value)
        print(f"Data analyzed. Anomaly score: {anomaly_score}")
        publish_analysis_results(anomaly_score)
    else:
        print("No 'temperature' value found in data.")



def train_model():
    print("Waiting for 180 seconds to get data for training the model...")
    time.sleep(180)  # Delay of 180 seconds
    influx_client = InfluxDBClient(url=f"http://{influxdb_host}:{influxdb_port}", token=influxdb_token, org=influxdb_org)
    # Query to get only temperature field values from the specified measurement
    query = f"""
    from(bucket: "{influxdb_bucket}") 
    |> range(start: -365d) 
    |> filter(fn: (r) => r["_measurement"] == "{influxdb_measurement}")
    |> filter(fn: (r) => r["_field"] == "temperature")
    """
    
    # Execute the query
    result = influx_client.query_api().query(query, org=influxdb_org)
    
    # Extract only the temperature values
    values = [record.get_value() for table in result for record in table.records]
    if values:
        X = np.array(values).reshape(-1, 1)
        model.fit(X)
        print(f"Model trained with historical data on {len(values)} data points.")
    else:
        print("No data available to train the model.")



def predict_anomaly(value):
    X = np.array([value]).reshape(-1, 1)
    return model.predict(X)[0]

def publish_analysis_results(anomaly_score):
    analysis_result = {"anomaly_score": int(anomaly_score)}
    client.publish(topics['analyzer'], json.dumps(analysis_result))
    print("Analysis results published to:", topics['analyzer'])

def handle_feedback(msg):
    try:
        feedback = json.loads(msg.payload)
    except json.JSONDecodeError as e:
        print("Error decoding feedback JSON:", e)
        return
    
    print("Feedback received:", feedback)
    process_feedback(feedback)

def process_feedback(feedback):
    if feedback["outcome"] != "Success":
        adjust_threshold(feedback)
        
# function to adjust anomaly detection threshold based on feedback
def adjust_threshold(feedback):
    print("Adjusting anomaly detection threshold...")
    
    # Check if the current contamination is set to 'auto'
    if model.contamination == 'auto':
        current_contamination = 0.1  # Default 'auto' value is typically 0.1
        print("Current contamination is set to 'auto', using default value of 0.1")
    else:
        current_contamination = model.contamination
        print(f"Current contamination: {current_contamination}")
    
    if feedback["outcome"] == "Failure":
        print("Decreasing contamination due to feedback.")
        new_contamination = max(current_contamination - 0.01, 0.01)  # Decrease contamination but ensure it's above 0.01
    else:
        print("No contamination required.")
        
    
    model.contamination = new_contamination  # Set the new contamination value
    print(f"Adjusted contamination to {model.contamination}")

       
        
# Create MQTT client instance

client = mqtt.Client()

# Define callback functions for the client
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port, 60)

# Train the model before starting the loop
# For training on startup
train_model()

# Start the loop to handle incoming messages
client.loop_start()



try:
    # Loop forever for user interrupt to handle MQTT messages
    while True:
        continue
except KeyboardInterrupt:
    print("Script interrupted by user")
finally:
    # Stop the client loop and disconnect
    client.loop_stop()
    print("MQTT client loop stopped")
    client.disconnect()
    print("MQTT client disconnected")
