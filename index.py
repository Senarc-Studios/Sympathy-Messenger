import time
import requests

from datetime import datetime
from functions import constants

def start(Private_Key: str):
    print("[+] Sympathy-Messenger is Checking for new messages.")
    headers = {
        "Private-Key": Private_Key
    }
    response = requests.get(constants.API_ENDPOINT + "/fetch", headers=headers)
    if response.status_code == 200:
        for key, value in response.json():
            timestamp = datetime.fromtimestamp(value['timestamp']).strftime("%d-%m-%Y | %H:%M:%S")
            print(f"[{timestamp}] New Message from \"{value['username']}\": \n\n" + value['message'])
            print(f"{value['username']}'s Public Key: {value['public_key']}\n\n")
    time.sleep(5)
    return start(Private_Key)

def register(username: str):
    data = {
        "username": username
    }
    response = requests.post(constants.API_ENDPOINT + "/register", json=data)
    if response.status_code == 200:
        print("[+] Sympathy-Messenger account registered successfully.")
    else:
        print("[-] Sympathy-Messenger account not registered successfully.")
