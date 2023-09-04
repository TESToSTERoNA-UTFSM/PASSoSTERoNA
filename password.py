import json
from cryptography.fernet import Fernet
import base64, hashlib
import pickle
from os.path import exists

import os
import ast
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DB_NAME = 'password.bin'

PASSWORD = ''

def onboarding():
    PASSWORD = input("Ingresa tu wea: ")

    salt = os.urandom(16)

    print("salt:", salt)

    db = {
        "passwords": [
            {
                "nombre": "hola",
                "asd_": "chao"
            }
        ]
    }
    
    with open(DB_NAME, 'wb') as f:
        passwords = json.dumps(db, indent=4)
        f.write(salt)
        f.write(passwords.encode())

def get_key(password, salt):
    password = str.encode(password)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    return base64.urlsafe_b64encode(kdf.derive(password))

#fernet = Fernet(get_key())


#fernet.decrypt(passwords)

onboarding()

with open(DB_NAME, 'rb') as f:
    salt = f.readLine()
    print(salt)
    db = json.load(f.readLine())
    salt = db["salt"]
    print("salt:", salt)
    passwords = db["passwords"]

print(passwords)

mi_llavesita = get_key(PASSWORD, salt)

print(mi_llavesita)