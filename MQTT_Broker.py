import socket
import sys
from threading import Thread
import json
import os
from MQTT_control_packets import CONNACK
import MQTT_decoder
import MQTT_database
from MQTT_packet_handler import packet_router
import time

HOST = "127.0.0.1"
PORT = 1883


def main():
    # Initialize database
    MQTT_database.initialize_database()

    # Create dummy session and topic
    MQTT_database.session_create("test1")
    MQTT_database.topic_create('Temperature', 'number')

    # Delete all sessions and topics
    #MQTT_database.topic_delete_all()
    #MQTT_database.session_delete_all()

    start_broker()


def start_broker():

    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to port
    try:
        server_socket.bind((HOST, PORT))
        print(f"Binding server socket to host: {HOST} and port: {PORT}")
    except:
        print(f"Bind failed. \nError: {str(sys.exc_info())}")
        sys.exit()

    # Enable passive listening sockets
    server_socket.listen(5)

    # Periodically jump out of accept waiting process to receive keyboard interrupt commnad
    server_socket.settimeout(0.5)


    while True:

        client_socket = None

        try:
            # Wait and accept incoming connection
            (client_socket, address) = server_socket.accept()
            ip, port = str(address[0]), str(address[1])
            print(f"Connection from {ip}:{port} has been established.")

            try:
                Thread(target=client_thread, args=(client_socket, ip, port)).start()
                print(f"Client thread for {ip}:{port} has been created.")
            except:
                print(f"Client thread for {ip}:{port} did not create")
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            if client_socket:
                client_socket.close()
            break


def client_thread(client_socket, ip, port):

    while True:

        try:
            # Listen to incoming data
            data = client_socket.recv(1024)
            if not data:
                time.sleep(0.5)
                break

            print(f"Incomming packet: {data}")

            incoming_packet = MQTT_decoder.decode(data)
            print(f"Decoded incoming packet:")
            print(json.dumps(incoming_packet, indent=4, sort_keys=False))

            outgoing_packet = packet_router.route_packet(incoming_packet)
            client_socket.send(outgoing_packet)
        except KeyboardInterrupt:
            client_socket.close()
            break

if __name__ == "__main__":
    main()
