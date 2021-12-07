from MQTT_control_packets import PUBACK, PUBLISH
import MQTT_database
import sys

def handle(incoming_packet: dict, client_ID: str):

    topic = incoming_packet.get('Topic')
    payload = incoming_packet.get('Payload')

    # Update topic
    if MQTT_database.topic_update_value(topic, payload):
        print(f'Topic {topic} updated value to: {payload}')

    # Create publish packet
    outgoing_packet = PUBLISH.encode(topic, payload)
    return outgoing_packet