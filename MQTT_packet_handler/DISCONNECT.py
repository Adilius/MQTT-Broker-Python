import sys
import MQTT_database

def handle(client_ID: str):
    print(f'Client ID ({client_ID}) disconnected.')
    sys.exit()