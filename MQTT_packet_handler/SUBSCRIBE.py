from MQTT_control_packets import SUBACK
import sys

def handle(incoming_packet: dict):

    print(incoming_packet)

    # Get packet identifier
    packet_identifier = incoming_packet.get('Packet identifier')

    # Get topics
    topics = incoming_packet.get('Topics')

    # Get flags
    flags = incoming_packet.get('Flags')
    if flags != "0010": # Malformed packet
        sys.exit()
    
    # Create packet
    outgoing_packet = SUBACK.encode(packet_identifier, topics)
    return outgoing_packet