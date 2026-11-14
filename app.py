
from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import json
import uuid

app = Flask(__name__)

# HiveMQ public broker settings
BROKER = "broker.hivemq.com"
PORT = 1883

# MQTT topics
SENSOR_TOPIC = "smartlivingcompanion/room1/sensors"

# Latest sensor readings
sensor_data = {
    "temperature": None,
    "humidity": None,
    "motion": "Waiting for ESP32"
}

mqtt_connected = False


# Runs when the website connects to HiveMQ
def on_connect(client, userdata, flags, reason_code, properties):
    global mqtt_connected

    if not reason_code.is_failure:
        mqtt_connected = True
        print("Connected to HiveMQ successfully!")
        client.subscribe(SENSOR_TOPIC)
        print("Subscribed to:", SENSOR_TOPIC)
    else:
        mqtt_connected = False
        print("MQTT connection failed:", reason_code)


# Runs whenever a sensor message arrives
def on_message(client, userdata, message):
    global sensor_data

    try:
        received_data = json.loads(message.payload.decode())

        sensor_data.update(received_data)

        print("Received sensor data:", sensor_data)

    except Exception as error:
        print("Error receiving data:", error)


# Create MQTT client
mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="SLC_" + uuid.uuid4().hex[:8]
)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


# Dashboard page
@app.route("/")
def home():
    return render_template("index.html")


# Send sensor data to the dashboard
@app.route("/api/sensors")
def get_sensors():
    return jsonify({
        "connected": mqtt_connected,
        "data": sensor_data
    })


if __name__ == "__main__":

    try:
        print("Connecting to HiveMQ...")
        mqtt_client.connect(BROKER, PORT, 60)
        mqtt_client.loop_start()

    except Exception as error:
        print("MQTT connection error:", error)

    app.run(debug=True, use_reloader=False)
