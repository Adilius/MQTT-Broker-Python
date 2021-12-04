from MQTT_control_packets import PINGRESP
import MQTT_database

def handle():
    outgoing_packet = PINGRESP.encode()
    return outgoing_packet