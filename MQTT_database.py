import os
import json

# Creates database file
def initialize_database():

    # Create database file
    if not os.path.exists("db.json"):
        with open("db.json", "w+") as db:
            db.write('{ "Clients" : [], \n' + '  "Topics" : [] }')

# Read contents of database file
def read_database():
    # Read database file
    with open("db.json", "r") as db:
        database = json.load(db)

    return database

# Write content to database file
def write_database(database):
    with open("db.json", "w") as file:
        json.dump(database, file, indent=4, sort_keys=True)

# Check if session exists given client ID
def session_exists(client_ID: str):

    database = read_database()
    clients_list = database.get('Clients')
    for client in clients_list:
        if client_ID in client:
            return True
    return False

# Given client ID return session values
def session_get(client_ID: str):

    database = read_database()

    clients_list = database.get('Clients')

    for client in clients_list:
        if client_ID in client:
            return client

# Create blank session given client ID
def session_create(client_ID: str):

    if session_exists(client_ID):
        return False

    session_state = {
        client_ID: {
            "Subscriptions": []
        }
    }

    database = read_database()
    clients_list = database.get("Clients")
    clients_list.append(session_state)
    database.update({"Clients": clients_list})
    write_database(database)
    return True

# Delete session given client ID
def session_delete(client_ID: str):
    
    database = read_database()
    clients_list = database.get('Clients')
    old_clients_list_length = len(clients_list)
    clients_list = [client for client in clients_list if not client_ID in client]
    new_clients_list_length = len(clients_list)
    if old_clients_list_length > new_clients_list_length:
        database.update({"Clients": clients_list})
        write_database(database)
        return True
    return False

# Get topics from session
def session_get_topic(client_ID):

    # Safety check
    if session_exists(client_ID) == False:
        return False

    # Get list of clients
    database = read_database()
    clients_list = database.get("Clients")

    # Find client and get topics from their subscriptions
    for client in clients_list:
        if client_ID in client:
            client_variables = next(iter(client.values()))
            return client_variables['Subscriptions']

# Add topic to session
def session_add_topic(client_ID: str, topic: str):

    # Safety check
    if session_exists(client_ID) == False:
        return False

    # Get list of clients
    database = read_database()
    clients_list = database.get("Clients")

    # Find client and add topics to their subscriptions
    for index, client in enumerate(clients_list):
        if client_ID in client:
            client_variables = next(iter(client.values()))
            client_variables['Subscriptions'] = client_variables['Subscriptions'] + [topic]
            clients_list[index][client_ID] = client_variables

    database.update({"Clients": clients_list})
    write_database(database)

# Remove topic from session
def session_remove_topic(client_ID: str, topic: str):

    # Safety check
    if session_exists(client_ID) == False:
        return False

    # Get list of clients
    database = read_database()
    clients_list = database.get("Clients")

    # Find client and remove topic to their subscriptions
    for index, client in enumerate(clients_list):
        if client_ID in client:
            client_variables = next(iter(client.values()))
            try:
                client_variables['Subscriptions'].remove(topic)
            except:
                print(f'Could not to remove subscription ({topic}) from client ({client_ID})')
            clients_list[index][client_ID] = client_variables

    database.update({"Clients": clients_list})
    write_database(database)

# Delete all sessions
def session_delete_all():
    database = read_database()
    database.update({'Clients':[]})
    write_database(database)
    return True

# Check if topic exists given topic name
def topic_exists(topic_name: str):

    database = read_database()
    topics_list = database.get('Topics')

    for topic in topics_list:
        if topic_name in topic:
            return True
    return False

# Udpate value to topic
def topic_update_value(topic_name: str, payload: str):

    database = read_database()
    topics_list = database.get('Topics')
    for index, topic in enumerate(topics_list):
        if topic_name in topic.keys():
            topic = {topic_name : payload}
            topics_list[index] = topic
            database.update({"Topics":topics_list})
            write_database(database)
            return True
    return False

# Create topic 
def topic_create(topic_name: str):

    topic_new = {topic_name:""}

    # Get existing topics
    database = read_database()
    topics_list = database.get('Topics')

    # If list is empty, we dont need to check duplicates
    if len(topics_list) == 0:
        topics_list.append(topic_new)
        database.update({"Topics":topics_list})
        write_database(database)
        return True

    # Gather all topic names
    topics_keys_list = []
    for topic in topics_list:
        key = next(iter(topic))
        topics_keys_list.append(key)

    # Check if new topic doesn't already exist
    if topic_name not in topics_keys_list:
        topics_list.append(topic_new)
        database.update({"Topics":topics_list})
        write_database(database)
        return True

# Delete topic
def topic_delete(topic_name: str):

    if not topic_exists:
        return False

    database = read_database()
    topics_list = database.get('Topics')
    old_topics_list_length = len(topics_list)
    topics_list = [topic for topic in topics_list if not topic_name in topic]
    new_topics_list_length = len(topics_list)
    if old_topics_list_length > new_topics_list_length:
        database.update({'Topics': topics_list})
        write_database(database)
        return True
    return False

# Delete all topics
def topic_delete_all():

    database = read_database()
    database.update({'Topics':[]})
    write_database(database)
    return True

# Get topic value
def topic_get_value(topic_name: str):

    database = read_database()
    topics_list = database.get('Topics')
    for index, topic in enumerate(topics_list):
        if topic_name in topic.keys():
            value = next(iter(topic.values()))

            return value
    return False