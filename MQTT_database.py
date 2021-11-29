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
def session_exists(client_id: str):

    database = read_database()

    clients_list = database.get('Clients')

    for client in clients_list:
        if client_id in client:
            return True
    return False

# Given client ID return session values
def session_get(client_id: str):

    database = read_database()

    clients_lits = database.get('Clients')

    for client in clients_lits:
        if client_id in client:
            print(client[client_id])
            return client

# Create blank session given client ID
def session_create(client_id: str):

    if session_exists(client_id):
        return False

    session_state = {
        client_id: {
            "Subscriptions": [],
            "NEEDACK": [],
            "NEEDSEND12": [],
            "SENDACK": [],
            "NEEDSEND0": []
        }
    }

    database = read_database()
    clients_list = database.get("Clients")
    clients_list.append(session_state)
    database.update({"Clients": clients_list})
    write_database(database)
    return True

# Delete session given client ID
def session_delete(client_id: str):
    
    database = read_database()
    clients_list = database.get('Clients')
    old_clients_list_length = len(clients_list)
    clients_list = [client for client in clients_list if not client_id in client]
    new_clients_list_length = len(clients_list)
    if old_clients_list_length > new_clients_list_length:
        database.update({"Clients": clients_list})
        write_database(database)
        return True
    return False

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

# Create topic 
def topic_create(topic_name: str, data_type: str):

    if topic_exists(topic_name):
        return False

    if data_type == 'string':
        topic = {
            topic_name : ""
        }
    elif data_type == 'number':
        topic = {
            topic_name : 0
        }
    elif data_type == "object":
        topic = {
            topic_name : {}
        }
    elif data_type == "array":
        topic = {
            topic_name : []
        }
    elif data_type == "boolean":
        topic = {
            topic_name : False
        }
    elif data_type == 'null':
        topic = {
            topic_name : None
        }
    else:
        return False

    database = read_database()
    topics_list = database.get('Topics')
    topics_list.append(topic)
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