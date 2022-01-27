import sys
import json
import time
import requests

from datetime import datetime
from functions import constants

def get_public_key():
    with open("keys.json") as file:
        payload = json.load(file)
        return payload["Public-Key"]

def get_private_key():
    with open("keys.json") as file:
        payload = json.load(file)
        return payload["Private-Key"]

def store_public_key(Public_Key: str):
    with open("keys.json", "w") as file:
        data = {
            "Public-Key": Public_Key
        }
        json.dump(data, file)

def store_private_key(Private_Key: str):
    with open("keys.json", "w") as file:
        data = {
            "Private-Key": Private_Key
        }
        json.dump(data, file)

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
        print("[!] Your Private Key is: " + response.json()['Private-Key'])
        print("[!] Your Public Key is: " + response.json()['Public-Key'])
        store_private_key(response.json()['Private-Key'])
        store_public_key(response.json()['Public-Key'])
    else:
        print("[-] Sympathy-Messenger account not registered successfully.")

def send(Public_Key: str):
    message = input("[?] Enter your message: ")
    Private_Key = input("[?] Enter the recipient's Private Key: ")

    data = {
        "message": message
    }
    headers = {
        "Private-Key": Private_Key,
        "Public-Key": Public_Key
    }

    response = requests.post(constants.API_ENDPOINT + "/send", json=data, headers=headers)

    if response.status_code == 200:
        print("[+] Message sent successfully.")
    else:
        print("[-] Message not sent successfully.")

def option_selector():
    user_input = input("[?] What would you like to do?\n\n[1] Register\n[2] Listen for messages\n[3] Send a message\n[4] Get Public Key\n[5] Get Private Key\n[6] Exit\n\n")
    valid_options = ["1", "2", "3", "4"]
    if user_input not in valid_options:
        print("[-] Invalid option. Abort!")
        sys.exit()

    elif user_input == "1":
        username = input("[?] Enter your username: ")
        register(username)
        print("[!] Function completed! Aborting!")
        sys.exit()

    elif user_input == "2":
        Private_Key = get_private_key()
        start(Private_Key)
        print("[!] Function completed! Aborting!")
        sys.exit()

    elif user_input == "3":
        Public_Key = get_public_key()
        send(Public_Key)
        print("[!] Function completed! Aborting!")
        sys.exit()

    elif user_input == "4":
        Public_Key = get_public_key()
        print("[+] Your Public Key is: " + Public_Key)
        print("[!] Function completed! Aborting!")
        sys.exit()

    elif user_input == "5":
        Private_Key = get_private_key()
        print("[+] Your Private Key is: " + Private_Key)
        print("[!] Function completed! Aborting!")
        sys.exit()

    elif user_input == "6":
        print("[!] Exiting!")
        sys.exit()

    else:
        print("[-] Invalid option. Abort!")
        sys.exit()