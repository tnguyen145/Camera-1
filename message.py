import os
import paho.mqtt.client as mqtt
from twilio.rest import Client

# MQTT Configuration
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_TOPIC = "robot/fall_detection"

# Twilio API Configuration
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
EMERGENCY_PHONE_NUMBER = os.getenv("EMERGENCY_PHONE_NUMBER")
# Initialize Twilio client
twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, 1883, 60)

def send_mqtt_alert():
    """ Publish a fall detection alert via MQTT """
    mqtt_client.publish(MQTT_TOPIC, "FALL DETECTED! Assist needed.")
    print("MQTT Alert Sent!")

def send_sms_alert():
    """ Send an SMS alert via Twilio """
    message = twilio_client.messages.create(
        body="Fall detected! call 911 or please check on the person.",
        from_=TWILIO_PHONE_NUMBER,
        to=EMERGENCY_PHONE_NUMBER
    )
    print(f"SMS Alert Sent! Message SID: {message.sid}")