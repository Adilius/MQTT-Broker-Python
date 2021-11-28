import os
import json

# Creates database file
def initialize_database():

    # Create database file
    if not os.path.exists("db.json"):
        with open("db.json", "w+") as db:
            db.write(
                "{ \"Clients\" : [], \n" +
                "  \"Topics\" : [] }")

# Read contents of database file
def read_database():
    # Read database file
    with open("db.json", "r") as db:
        database = json.load(db)

    return database

# Write content to database file
def write_database(database):
    with open("db.json", "w") as file:
        json.dump(database, file, indent = 4, sort_keys=True)

def session_exists(client_id: str):
    pass

def session_get(client_id: str):
    pass


def create_session(client_id: str):

    session_state = f""""
    \"{client_id}\" : {{
        \"Subscriptions\" : [],
        \"NEEDACK\" : [],
        \"NEEDSEND12\": [],
        \"SENDACK\" : [],
        \"NEEDSEND0\" : []
    }}
    """

    database = read_database()

    print(database)

    clients_list = database.get('Clients')

    clients_list.append(session_state)

    database.update({'Clients':clients_list})

    write_database(database)


