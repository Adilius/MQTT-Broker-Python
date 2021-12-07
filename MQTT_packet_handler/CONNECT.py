from MQTT_control_packets import CONNACK
import MQTT_database

def handle(incoming_packet: dict, client_ID: str):

    # Get protocol name
    protocol_name = incoming_packet.get('Protocol name')
    if protocol_name != 'MQTT4':
        outgoing_packet = CONNACK.encode(session_present=False, return_code=1)
        return outgoing_packet

    # Get client ID
    client_id = incoming_packet.get('Payload').split(' ',1)[0]

    # Get clean session
    clean_session = incoming_packet.get('Clean Session flag')

    # Clean session == True
    if clean_session:

        # If we have old session
        if MQTT_database.session_exists(client_id):
            MQTT_database.session_delete(client_id) # Delete any old session
        MQTT_database.session_create(client_id) # Create new session

        outgoing_packet = CONNACK.encode(session_present=False, return_code=0)

    # Clean session == False
    if not clean_session:
        if MQTT_database.session_exists(client_id):
            outgoing_packet = CONNACK.encode(session_present=True, return_code=0)
        else:
            outgoing_packet = CONNACK.encode(session_present=False, return_code=0)
    
    print(f'Client ID ({client_ID}) connected.')

    return outgoing_packet