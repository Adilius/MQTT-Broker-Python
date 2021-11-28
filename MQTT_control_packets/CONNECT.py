def decode(bytes):

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
    if connect_flags_bits[0] == '1':
        decoded_packet['Username flag'] = True
    else:
        decoded_packet['Username flag'] = False

    if connect_flags_bits[1] == '1':
        decoded_packet['Password flag'] = True
    else:
        decoded_packet['Password flag'] = False

    if connect_flags_bits[2] == '1':
        decoded_packet['Retain flag'] = True
    else:
        decoded_packet['Retain flag'] = False

    will_qos = connect_flags_bits[3] + connect_flags_bits[4]
    decoded_packet['Will QoS'] = int(will_qos, 2)

    if connect_flags_bits[4] == '1':
        decoded_packet['QoS 2 flag'] = True
    else:
        decoded_packet['QoS 2 flag'] = False

    if connect_flags_bits[5] == '1':
        decoded_packet['Will flag'] = True
    else:
        decoded_packet['Will flag'] = False

    if connect_flags_bits[6] == '1':
        decoded_packet['Clean Session flag'] = True
    else:
        decoded_packet['Clean Session flag'] = False

    if connect_flags_bits[7] == '1':
        decoded_packet['Reserved flag'] = True
    else:
        decoded_packet['Reserved flag'] = False

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
    payload_length_bits = payload_length_bits_1 + payload_length_bits_2
    payload_length_value = int(payload_length_bits, 2)
    decoded_packet['Payload length'] = payload_length_value

    # Payload
    payload_bytes = bytes[current_byte:current_byte+payload_length_value]
    payload = payload_bytes.decode()
    decoded_packet['Payload'] = payload

    return decoded_packet