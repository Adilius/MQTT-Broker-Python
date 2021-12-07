import MQTT_binary
import MQTT_database

def encode(packet_identifier: int, return_codes: list):

    # Packet type
    packet_type = MQTT_binary.get_bits('SUBACK')

    # Flags
    flags = "0000"

    # Packet length
    packet_length_value = len(return_codes) + 2
    packet_length = format(packet_length_value, "08b")

    # Packet identifier
    packet_identifier_bits = format(packet_identifier, "016b")
    
    # Return codes
    return_codes = "".join(return_codes)
    
    packet = (
        packet_type +
        flags +
        packet_length +
        packet_identifier_bits +
        return_codes
    )

    encoded_packet = int(packet, 2).to_bytes((len(packet) + 7) // 8, byteorder="big")
    return encoded_packet
    
    print(topics)