import MQTT_binary

def encode(packet_identifier: int):

    # Packet type
    packet_type = MQTT_binary.get_bits('UNSUBACK')

    # Flags
    flags = "0000"

    # Packet length
    packet_length = "00000010"

    # Packet identifier
    packet_identifier_bits = format(packet_identifier, "016b")

    packet = (
        packet_type +
        flags +
        packet_length +
        packet_identifier_bits
    )

    encoded_packet = int(packet, 2).to_bytes((len(packet) + 7) // 8, byteorder="big")
    return encoded_packet