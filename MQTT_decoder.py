import MQTT_binary
import MQTT_control_packets
from MQTT_control_packets import CONNECT
from MQTT_control_packets import SUBSCRIBE
from MQTT_control_packets import UNSUBSCRIBE


def decode(bytes):

    # Buffer to hold decoded values from packet
    decoded_packet = {}

    # Control header
    control_header = bytes[0]
    control_header_bits = format(control_header, "08b")

    # Packet type
    packet_type_bits = control_header_bits[:4]
    packet_type = MQTT_binary.get_name(packet_type_bits)
    decoded_packet["Packet type"] = packet_type

    # Flags
    flags_bits = control_header_bits[4:]
    decoded_packet["Flags"] = flags_bits

    # Packet length 1
    packet_length_1 = bytes[1]
    packet_length_1_bits = format(packet_length_1, "08b")

    # Control variables for further packet decoding
    current_byte = 1
    packet_length_continuation = False

    if packet_length_1_bits[0] == "0":
        packet_length_continuation = False
    else:
        packet_length_1_bits = packet_length_1_bits[1:]

    # Packet length 2
    if packet_length_continuation:
        current_byte += 1
        packet_length_2 = bytes[current_byte]
        packet_length_2_bits = format(packet_length_2, "08b")
        if packet_length_2_bits[0] == "0":
            packet_length_continuation = False

        packet_length_2_bits = packet_length_2_bits[1:]

    # Packet length 3
    if packet_length_continuation:
        current_byte += 1
        packet_length_3 = bytes[current_byte]
        packet_length_3_bits = format(packet_length_3, "08b")
        if packet_length_3_bits[0] == "0":
            packet_length_continuation = False

        packet_length_3_bits = packet_length_3_bits[1:]

    # Packet length 4
    if packet_length_continuation:
        current_byte += 1
        packet_length_4 = bytes[current_byte]
        packet_length_4_bits = format(packet_length_4, "08b")
        packet_length_4_bits = packet_length_4_bits[1:]

    # Packet length value
    if current_byte == 1:  # 1 byte
        packet_length_bits = packet_length_1_bits
        packet_length = int(packet_length_bits, 2)
    elif current_byte == 2:  # 2 bytes
        packet_length_bits = packet_length_2_bits + packet_length_1_bits
        packet_length = int(packet_length_bits, 2)
    elif current_byte == 3:  # 3 bytes
        packet_length_bits = (
            packet_length_3_bits + packet_length_2_bits + packet_length_1_bits
        )
        packet_length = int(packet_length_bits, 2)
    else:  # 4 bytes
        packet_length_bits = (
            packet_length_4_bits
            + packet_length_3_bits
            + packet_length_2_bits
            + packet_length_1_bits
        )
        packet_length = int(packet_length_bits, 2)

    decoded_packet["Packet length"] = packet_length

    # Move to next byte
    current_byte += 1

    if packet_type == "CONNECT":
        connect_message = CONNECT.decode(bytes[current_byte:])
        decoded_packet.update(connect_message)
    elif packet_type == "SUBSCRIBE":
        subscribe_message = SUBSCRIBE.decode(bytes[current_byte:])
        decoded_packet.update(subscribe_message)
    elif packet_type == "UNSUBSCRIBE":
        unsubscribe_message = UNSUBSCRIBE.decode(bytes[current_byte:])
        decoded_packet.update(unsubscribe_message)

    return decoded_packet
