def get_name(bits):
    name = [k for k, v in packet_type.items() if v == bits]

    if len(name) > 0:
        name = name[0]
    else:
        name = "Unknown packet type"

    return name


def get_bits(name):
    bits = packet_type.get(name)

    return bits


packet_type = {
    "CONNECT": "0001",
    "CONNACK": "0010",
    "PUBLISH": "0011",
    "PUBACK": "0100",
    "SUBSCRIBE": "1000",
    "SUBACK": "1001",
    "UNSUBSCRIBE": "1010",
    "UNSUBACK": "1011",
    "PINGQREQ": "1100",
    "PINGRESP": "1101",
    "DISCONNECT": "1110",
}
