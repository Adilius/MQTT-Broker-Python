import MQTT_binary

def decode(bytes):

    #print(f'Packet length: {len(bytes)}')

    # Buffer to hold decoded values from packet
    decoded_packet = {}

    # Control header
    control_header = bytes[0]
    control_header_bits = format(control_header, '08b')

    # Packet type
    packet_type_bits = control_header_bits[:4]
    packet_type = MQTT_binary.get_name(packet_type_bits)
    decoded_packet['Packet type'] = packet_type

    # Flags
    flags_bits = control_header_bits[4:]
    decoded_packet['Flags'] = flags_bits

    # Packet length 1
    packet_length_1 = bytes[1]
    packet_length_1_bits = format(packet_length_1, '08b')

    # Control variables for further packet decoding
    current_byte = 1
    packet_length_continuation = False

    if packet_length_1_bits[0] == '0':
        packet_length_continuation = False
    else:
        packet_length_1_bits = packet_length_1_bits[1:]


    # Packet length 2
    if packet_length_continuation:
        current_byte += 1
        packet_length_2 = bytes[current_byte]
        packet_length_2_bits = format(packet_length_2, '08b')
        if packet_length_2_bits[0] == '0':
            packet_length_continuation = False

        packet_length_2_bits = packet_length_2_bits[1:]
    
    # Packet length 3
    if packet_length_continuation:
        current_byte += 1
        packet_length_3 = bytes[current_byte]
        packet_length_3_bits = format(packet_length_3, '08b')
        if packet_length_3_bits[0] == '0':
            packet_length_continuation = False
        
        packet_length_3_bits = packet_length_3_bits[1:]

    # Packet length 4
    if packet_length_continuation:
        current_byte += 1
        packet_length_4 = bytes[current_byte]
        packet_length_4_bits = format(packet_length_4, '08b')
        packet_length_4_bits = packet_length_4_bits[1:]

    # Packet length value
    if current_byte == 1:   # 1 byte
        packet_length_bits = packet_length_1_bits
        packet_length = int(packet_length_bits, 2)
    elif current_byte == 2: # 2 bytes
        packet_length_bits = packet_length_2_bits + packet_length_1_bits
        packet_length = int(packet_length_bits, 2)
    elif current_byte == 3: # 3 bytes
        packet_length_bits = packet_length_3_bits + packet_length_2_bits + packet_length_1_bits
        packet_length = int(packet_length_bits, 2)
    else: # 4 bytes
        packet_length_bits = packet_length_4_bits + packet_length_3_bits + packet_length_2_bits + packet_length_1_bits
        packet_length = int(packet_length_bits,2)

    decoded_packet['Packet length'] = packet_length

    # Move to next byte
    current_byte += 1

    if packet_type == 'CONNECT':
        connect_message = decode_connect_message(bytes[current_byte:])
        decoded_packet.update(connect_message)

    return decoded_packet

def decode_connect_message(bytes):

    # Buffer to hold decoded values from packet
    decoded_packet = {}

    # Control variable
    current_byte = 0

    # Length of protocol name
    protocol_name_length_bytes_1 = bytes[current_byte]
    protocol_name_length_bits_1 = format(protocol_name_length_bytes_1, '08b')
    current_byte += 1
    protocol_name_length_bytes_2 = bytes[current_byte]
    protocol_name_length_bits_2 = format(protocol_name_length_bytes_2, '08b')
    current_byte += 1
    protocol_name_length_bits = protocol_name_length_bits_1 + protocol_name_length_bits_2
    protocol_name_length_value = int(protocol_name_length_bits, 2)
    decoded_packet['Length of protocol name'] = protocol_name_length_value

    # Protocol name
    protocol_name_bytes = bytes[current_byte:current_byte+protocol_name_length_value+1]
    protocol_name_list = []
    for byte in protocol_name_bytes:
        if byte > 9:
            protocol_name_list.append(chr(byte))
        else:
            protocol_name_list.append(str(byte))
            
    protocol_name = ''.join(protocol_name_list)

    decoded_packet['Protocol name'] = protocol_name
    current_byte += protocol_name_length_value+1

    # Connect flags
    connect_flags_bytes = bytes[current_byte]
    connect_flags_bits = format(connect_flags_bytes, '08b')
    decoded_packet['Connect Flags'] = connect_flags_bits
    current_byte += 1

    # Keep alive
    keep_alive_bytes_1 = bytes[current_byte]
    keep_alive_bits_1 = format(keep_alive_bytes_1, '08b')
    current_byte += 1
    keep_alive_bytes_2 = bytes[current_byte]
    keep_alive_bits_2 = format(keep_alive_bytes_2, '08b')
    current_byte += 1
    keep_alive_bits = keep_alive_bits_1 + keep_alive_bits_2
    keep_alive_value = int(keep_alive_bits, 2)
    decoded_packet['Keep Alive'] = keep_alive_value

    # Payload length
    payload_length_bytes_1 = bytes[current_byte]
    payload_length_bits_1 = format(payload_length_bytes_1, '08b')
    current_byte += 1
    payload_length_bytes_2 = bytes[current_byte]
    payload_length_bits_2 = format(payload_length_bytes_2, '08b')
    current_byte += 1
    payload_length_bits = payload_length_bits_1 + payload_length_bits_
    print(payload_length_bits)
    payload_length_value = int(payload_length_bits, 2)
    decoded_packet['Payload length'] = payload_length_value

    # Payload
    payload_bytes = bytes[current_byte:current_byte+payload_length_value]
    payload = payload_bytes.decode()
    decoded_packet['Payload'] = payload

    return decoded_packet