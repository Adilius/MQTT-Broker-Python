import MQTT_binary

def encode(packet_identifier: int, payload: list):

    # Packet type
    packet_type = MQTT_binary.get_bits('SUBACK')

    # Flags
    flags = "0000"

    # Packet length
    packet_length_value = len(payload) + 2
    packet_length = format(packet_length_value, "08b")

    # Packet identifier
    if packet_identifier > 255:
        pass
    else:
        packet_identifier_bits_1 = "00000000"
        packet_identifier_bits_2 = format(packet_identifier_bits_1, "08b")
    pass