from core.db_utils import User, Companies, Contacts, Events, Members, Transactions
from datetime import datetime
import requests



#URL = "http://api:9111"
URL = "http://127.0.0.1:8000"



ENTITY_CONFIG = {
    "User": {"path": f"{URL}/users", "class": User},
    "Companies": {"path": f"{URL}/companies", "class": Companies},
    "Contacts": {"path": f"{URL}/contacts", "class": Contacts},
    "Events": {"path": f"{URL}/events", "class" : Events},
    "Members": {"path": f"{URL}/members", "class": Members},
    "Transactions": {"path": f"{URL}/transactions", "class": Transactions}
}



def create_entity(entity_name, details, token):

    credentials = { "Authorization" : f"Bearer {token}" }
    for key, value in details.items():
        if "_id" in key:
            details[key] = int(value)
    print("New row", details)

    config = ENTITY_CONFIG[entity_name]
    # row = config["class"](**details)


    response = requests.post(f"{config['path']}/", json=details, headers=credentials)
    response.raise_for_status()

    return response.json()



def read_all_entities(entity_name, token):

    credentials = { "Authorization" : f"Bearer {token}" }

    config = ENTITY_CONFIG[entity_name]
    response = requests.get(f"{config['path']}/all", headers=credentials)
    response.raise_for_status()


    return response.json()



def read_entity(entity_name, entity_id, token):

    credentials = { "Authorization" : f"Bearer {token}" }

    config = ENTITY_CONFIG[entity_name]
    response = requests.get(f"{config['path']}/{entity_id}", headers=credentials)
    response.raise_for_status()
    row_data = response.json()

    return row_data if row_data else None



def update_entity(entity_name, entity_id, details, token):

    credentials = { "Authorization" : f"Bearer {token}" }

    config = ENTITY_CONFIG[entity_name]
    row_to_update = read_entity(entity_name, entity_id, token)
  #  row_to_update = row_to_update = db.query(Events).get(entity_id)


    if not row_to_update:
        raise ValueError(f"Entity with ID {entity_id} not found.")
    
    for key, value in details.items():
        row_to_update[key] = value  

    response = requests.put(f"{config['path']}/{entity_id}", json=row_to_update, headers=credentials)
    response.raise_for_status()

    return response.json()



def delete_entity(entity_name, entity_id, token):

    credentials = { "Authorization" : f"Bearer {token}" }

    config = ENTITY_CONFIG[entity_name]
    response = requests.delete(f"{config['path']}/{entity_id}", headers=credentials)
    response.raise_for_status()

    return {"status": "success", "id": entity_id}



def delete_table(entity_name, token):

    credentials = { "Authorization" : f"Bearer {token}" }

    response = requests.delete(f"{URL}/delete_table/{entity_name}", headers=credentials)
    response.raise_for_status()

    return {"status": "success", "id": entity_name}



def authenticate(username: str, password: str):
    # Construct the payload as a dictionary
    payload = {
        "username": username,
        "password": password,
    }

    response = requests.post(f"{URL}/token", data=payload)
    if response.status_code == 200:
        print("Access granted")
    
    else:
        print("Not 200")

    
    response.raise_for_status()

    return response.json(), response.status_code



## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 


def get_query(query, token):

    credentials = { "Authorization" : f"Bearer {token}" }

    response = requests.post(f"{URL}/optional_query", json={"query": query}, headers=credentials)
    response.raise_for_status()

    return response.json()



def download_db(token):

    credentials = { "Authorization" : f"Bearer {token}" }

    current_time = datetime.now().strftime("%y%m%d_%H%M%S")
    response = requests.get(f"{URL}/download-db", headers=credentials)
    response.raise_for_status()

    return response, current_time



def get_metadata(token):

    credentials = { "Authorization" : f"Bearer {token}" }

    response = requests.get(f"{URL}/metadata", headers=credentials)
    response.raise_for_status()

    return response.json()



def upload_luma_csv(uploaded_df, token):

    credentials = { "Authorization" : f"Bearer {token}" }

    df_dict = uploaded_df.to_dict(as_series=False)
    response = requests.post(f"{URL}/update_contacts/table", json=df_dict, headers=credentials)
    response.raise_for_status()

    return response.json()
