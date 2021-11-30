from MQTT_packet_handler import CONNECT
from MQTT_packet_handler import SUBSCRIBE
import sys

def route_packet(incoming_packet: dict):
    packet_type = incoming_packet.get('Packet type')

    if packet_type == "CONNECT":
        outgoing_packet = CONNECT.handle(incoming_packet)
    elif packet_type == "SUBSCRIBE":
        outgoing_packet = SUBSCRIBE.handle(incoming_packet)
    else:
        print(incoming_packet)
        sys.exit()
    return outgoing_packet
    
