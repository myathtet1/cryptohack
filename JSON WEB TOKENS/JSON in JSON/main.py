import requests
import json


def create_session(username):
    r = requests.get(f"https://web.cryptohack.org/json-in-json/create_session/{username}/")
    return r.text


def authorise(token):
    r = requests.get(f"https://web.cryptohack.org/json-in-json/authorise/{token}/")
    return r.text


username = "admin\", \"admin\": \"True"
session = create_session(username)
session = json.loads(session)["session"]
print(authorise(session))
