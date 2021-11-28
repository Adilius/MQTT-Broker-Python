import MQTT_binary

def encode(session_present : bool = False, return_code: int = 0):

    # Packet type
    packet_type = MQTT_binary.get_bits('CONNACK')

    # Flags
    flags = '0000'

    # Packet length
    packet_length = '00000010'

    # Connect acknowledge flags
    if session_present:
        connect_acknowledge_flags = '00000001'
    else:
        connect_acknowledge_flags = '00000000'

    # Connect return code
    if return_code == 0:
        connect_return_code = '00000000'
    elif return_code == 1:
        connect_return_code = '00000001'
    elif return_code == 2:
        connect_return_code = '00000010'
    elif return_code == 3:
        connect_return_code = '00000011'
    elif return_code == 4:
        connect_return_code = '00000100'
    elif return_code == 5:
        connect_return_code = '00000101'
    else:   # Reserved
        connect_return_code = '11111111'

    packet = packet_type + flags + packet_length + connect_acknowledge_flags + connect_return_code
    encoded_packet = int(packet, 2).to_bytes((len(packet) + 7) // 8, byteorder='big')
    return encoded_packet
    