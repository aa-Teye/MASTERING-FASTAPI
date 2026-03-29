import json
import os

# The name of the file that will act as your database
DB_FILE = "inventory.json"

def load_data():
    """Reads the JSON file. If it doesn't exist, returns an empty dictionary."""
    if not os.path.exists(DB_FILE):
        # Create the file with an empty dictionary if it's the first time running
        with open(DB_FILE, "w") as file:
            json.dump({}, file)
        return {}
    
    with open(DB_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    """Saves the current state of the vault into the JSON file."""
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4) # indent=4 makes the file readable for humans