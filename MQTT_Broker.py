import socket
import sys
from threading import Thread
import json
import os
import MQTT_decoder

HOST = "127.0.0.1"
PORT = 1883

def main():
    start_broker()
    pass

def start_broker():

    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to port
    try:
        server_socket.bind((HOST, PORT))
        print(f'Binding server socket to host: {HOST} and port: {PORT}')
    except:
        print(f'Bind failed. \nError: {str(sys.exc_info())}')
        sys.exit()

    # Ebavle passive listening sockets
    server_socket.listen(5)

    while True:

        # Wait and accept incoming connection
        (client_socket, address) = server_socket.accept()
        ip, port = str(address[0]), str(address[1])
        print(f'Connection from {ip}:{port} has been established.')

        try:
            Thread(target=client_thread, args=(client_socket, ip, port)).start()
            print(f'Client thread for {ip}:{port} has been created.')
        except:
            print(f'Client thread for {ip}:{port} did not create')


def client_thread(client_socket, ip, port):

    # Listen to incoming data
    data = client_socket.recv(1024)
    print(f'Incomming packet: {data}')

    packet_type = MQTT_decoder.decode(data)
    print(f'Decoded packet: \n{packet_type}')





if __name__ == "__main__":
    main()