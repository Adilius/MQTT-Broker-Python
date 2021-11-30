import MQTT_binary
import MQTT_database

def encode(packet_identifier: int, topics: list):

    # Packet type
    packet_type = MQTT_binary.get_bits('SUBACK')

    # Flags
    flags = "0000"

    # Packet length
    packet_length_value = len(topics)
    packet_length = format(packet_length_value, "08b")

    # Packet identifier
    packet_identifier_bits = format(packet_identifier, "016b")
    
    # Topics
    return_codes = ""
    for topic in topics:
        
        topic_name = next(iter(topic))
        if not MQTT_database.topic_exists(topic_name):
            return_codes += "10000000"    # Failure
        return_codes += "00000000"        # QoS 0
    
    packet = (
        packet_type +
        flags +
        packet_length +
        packet_identifier_bits +
        return_codes
    )

    decoded_packet = {
        "Packet type": "SUBACK",
        "Flags": flags,
        "Packet length": packet_length_value,
        "Topics": topics
    }
    print(decoded_packet)

    encoded_packet = int(packet, 2).to_bytes((len(packet) + 7) // 8, byteorder="big")
    return encoded_packet
    
    print(topics)