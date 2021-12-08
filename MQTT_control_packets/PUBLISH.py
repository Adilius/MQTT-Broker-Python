import MQTT_binary

def decode(bytes: bytes, packet_length: int, flags: str):

    # Buffer to hold decoded values from packet
    decoded_packet = {}

    # Control variable
    current_byte = 0

    # Topic filter length
    topic_length_bytes_1 = bytes[current_byte]
    topic_length_bits_1 = format(topic_length_bytes_1, "08b")
    current_byte += 1
    topic_length_bytes_2 = bytes[current_byte]
    topic_length_bits_2 = format(topic_length_bytes_2, "08b")
    current_byte += 1
    topic_filter_length_bits = (
        topic_length_bits_1 + topic_length_bits_2
    )
    topic_length_value = int(topic_filter_length_bits, 2)

    # Topic filter
    topic_bytes = bytes[current_byte:current_byte+topic_length_value]
    topic = topic_bytes.decode()
    decoded_packet['Topic'] = topic
    current_byte += topic_length_value

    # QoS level over 0, then we have packet identifier
    if flags[1] == '1' or flags[2] == '1':

        # Packet identifier
        packet_identifier_bytes_1 = bytes[current_byte]
        packet_identifier_bits_1 = format(packet_identifier_bytes_1, "08b")
        current_byte += 1
        packet_identifier_bytes_2 = bytes[current_byte]
        packet_identifier_bits_2 = format(packet_identifier_bytes_2, "08b")
        current_byte += 1
        packet_identifier_bits = (
            packet_identifier_bits_1 + packet_identifier_bits_2
        )
        packet_identifier_value = int(packet_identifier_bits, 2)
        decoded_packet['Packet identifier'] = packet_identifier_value

    # Payload
    payload_bytes = bytes[current_byte : packet_length]
    payload = payload_bytes.decode()
    decoded_packet["Payload"] = payload

    return decoded_packet

def encode(topic: str, payload:str):

    # Packet type
    packet_type = MQTT_binary.get_bits('PUBLISH')

    # Flags
    flags = "0000"

    # Packet length
    packet_length = len(topic) + len(payload) + 2
    packet_length_bits = format(packet_length, "08b")

    # Topic length
    topic_length = format(len(topic), "016b")

    # Topic
    topic_bits = ''.join(format(ord(i), '08b') for i in topic)

    # Payload
    payload_bits = ''.join(format(ord(i), '08b') for i in payload)

    packet = (
        packet_type +
        flags +
        packet_length_bits +
        topic_length +
        topic_bits +
        payload_bits
    )

    encoded_packet = int(packet, 2).to_bytes((len(packet) + 7) // 8, byteorder="big")
    return encoded_packet