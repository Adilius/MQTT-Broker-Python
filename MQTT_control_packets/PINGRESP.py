import MQTT_binary

def encode(client_ID: str):

    # Packet type
    packet_type = MQTT_binary.get_bits("PINGRESP")

    # Flags
    flags = "0000"

    # Packet length
    packet_length = "00000000"

    decoded_packet = {
        "Packet type": "PINGRESP",
        "Flags": flags,
        "Packet length": packet_length
    }
    #print(decoded_packet)

    packet = (
        packet_type
        + flags
        + packet_length
    )

    print(f'Responded to ({client_ID}) ping request.')

    encoded_packet = int(packet, 2).to_bytes((len(packet) + 7) // 8, byteorder="big")
    return encoded_packet