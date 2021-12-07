from MQTT_packet_handler import CONNECT
from MQTT_packet_handler import SUBSCRIBE
from MQTT_packet_handler import PINGREQ
from MQTT_packet_handler import DISCONNECT
import sys

def route_packet(incoming_packet: dict, client_ID: str):
    packet_type = incoming_packet.get('Packet type')

    if packet_type == "CONNECT":
        outgoing_packet = CONNECT.handle(incoming_packet, client_ID)
    elif packet_type == "DISCONNECT":
        DISCONNECT.handle(incoming_packet, client_ID)
    elif packet_type == "SUBSCRIBE":
        outgoing_packet = SUBSCRIBE.handle(incoming_packet, client_ID)
    elif packet_type == "PINGQREQ":
        outgoing_packet = PINGREQ.handle(client_ID)
    else:
        print(incoming_packet)
        sys.exit()
    return outgoing_packet
    
