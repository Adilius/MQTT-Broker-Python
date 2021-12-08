from MQTT_control_packets import SUBACK
import MQTT_database
import sys

def handle(incoming_packet: dict, client_ID: str):

    # Get packet identifier
    packet_identifier = incoming_packet.get('Packet identifier')

    # Get topics
    topics = incoming_packet.get('Topics')

    # Get flags
    flags = incoming_packet.get('Flags')
    if flags != "0010": # Malformed packet
        sys.exit()

    # Check that session exists
    if MQTT_database.session_exists(client_ID) == False:
        return_codes = []
        for _ in topics:
            return_codes.append("10000000")    # Failure
        return SUBACK.encode(packet_identifier, return_codes)

    # Evaluate topic requests
    return_codes = []
    for topic in topics:
        topic_name = next(iter(topic))
        if not MQTT_database.topic_exists(topic_name):
            return_codes.append("10000000")    # Failure
        else:
            # Add subscription to client
            MQTT_database.session_add_topic(client_ID, topic_name)
            print(f'Client ID ({client_ID}) subscribed to ({topic_name})')
            return_codes.append("00000000")   # QoS 0

    # Create packet
    outgoing_packet = SUBACK.encode(packet_identifier, return_codes)
    return outgoing_packet