#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:01:59 2024

@author: debayanb
"""

import paho.mqtt.client as mqtt
import json
import time
import random

# MQTT broker configuration
broker_address = "173.30.0.100"
port = 1883
topic_planner = "greenhouse/planning"
topic_executor = "greenhouse/execution"
topic_feedback = "greenhouse/feedback"

# Global variable to keep track of message count
feedback_counter = 0

# Function to execute planned actions
def execute_action(actions):
    print("Executor: Executing planned actions...")
    # Perform actual actions based on planned actions
    for action in actions:
        print("Executor: Performing action:", action)
        if action == "Adjust ventilation":
            print("Executor: Adjusting ventilation")
            # Code to adjust ventilation
        elif action == "Close windows":
            print("Executor: Closing windows")
            # Code to close windows
        elif action == "Turn off fans":
            print("Executor: Turning off fans")
            # Code to turn off fans
        elif action == "Turn on fans":
            print("Executor: Turning on fans")
            # Code to turn on fans
        else:
            print("Executor: No action required")
    # After all actions are executed, send feedback
    send_feedback_success(actions)

def send_feedback_success(actions):
    global feedback_counter
    feedback_counter += 1

    # Randomly fail one in every ten messages
    if feedback_counter % 10 == random.randint(1, 10):
        outcome = "Failure"
    else:
        outcome = "Success"

    feedback_message = {
        "outcome": outcome,
        "actions_executed": actions
    }
    client.publish(topic_feedback, json.dumps(feedback_message))
    print(f"Feedback about execution {outcome} published to topic:", topic_feedback)

    # Reset the counter if it reaches 10 to avoid large numbers
    if feedback_counter >= 10:
        feedback_counter = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic_planner)
    print("Subscribed to planner topic:", topic_planner)

def on_message(client, userdata, msg):
    print("Message received on topic:", msg.topic)
    # Parse JSON message
    planned_actions = json.loads(msg.payload)
    print("Planned actions received:", planned_actions)
    
    # Execute planned actions
    execute_action(planned_actions["actions"])

    # Publish execution confirmation to MQTT topic
    execution_confirmation = {
        "actions_executed": planned_actions["actions"]
    }
    client.publish(topic_executor, json.dumps(execution_confirmation))
    print("Execution confirmation published to topic:", topic_executor)

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker_address, port, 60)
print("Connected to MQTT broker:", broker_address, "on port:", port)

# Keep the client running to receive messages
print("Listening for messages...")
client.loop_forever()











































'''
import paho.mqtt.client as mqtt
import json
import time

# MQTT broker configuration
broker_address = "localhost"
port = 1883
topic_planner = "greenhouse/planning"
topic_executor = "greenhouse/execution"
topic_feedback = "greenhouse/feedback"

# Function to execute planned actions
def execute_action(actions):
    print("Executor: Executing planned actions...")
    # Perform actual actions based on planned actions
    for action in actions:
        print("Executor: Performing action:", action)
        if action == "Adjust ventilation":
            print("Executor: Adjusting ventilation")
            # Code to adjust ventilation
        elif action == "Close windows":
            print("Executor: Closing windows")
            # Code to close windows
        elif action == "Turn off fans":
            print("Executor: Turning off fans")
            # Code to turn off fans
        elif action == "Turn on fans":
            print("Executor: Turning on fans")
            # Code to turn on fans
        else:
            print("Executor: No action required")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic_planner)
    print("Subscribed to planner topic:", topic_planner)

def on_message(client, userdata, msg):
    print("Message received on topic:", msg.topic)
    # Parse JSON message
    planned_actions = json.loads(msg.payload)
    print("Planned actions received:", planned_actions)
    
    # Execute planned actions
    execute_action(planned_actions["actions"])

    # Publish execution confirmation to MQTT topic
    execution_confirmation = {
        "actions_executed": planned_actions["actions"]
    }
    client.publish(topic_executor, json.dumps(execution_confirmation))
    print("Execution confirmation published to topic:", topic_executor)

def on_feedback(client, userdata, msg):
    print("Feedback received on topic:", msg.topic)
    # Parse JSON feedback
    feedback_data = json.loads(msg.payload)
    print("Feedback data received:", feedback_data)
    # Process feedback
    process_feedback(feedback_data)

# Process feedback
def process_feedback(feedback):
    print("Processing feedback:", feedback)
    # Add your logic here to process the feedback

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add(topic_feedback, on_feedback)

# Connect to MQTT broker
client.connect(broker_address, port, 60)
print("Connected to MQTT broker:", broker_address, "on port:", port)

# Keep the client running to receive messages
print("Listening for messages...")
client.loop_forever()

'''
