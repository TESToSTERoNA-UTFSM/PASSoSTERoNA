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

def onboarding(password, DB_NAME=DB_NAME):
    salt = os.urandom(16)

    db = {
        "salt": salt,
        "passwords": []
    }

    write_db(password, db, DB_NAME)

def read_db(password, DB_NAME=DB_NAME):
    with open(DB_NAME, 'rb') as handle:
        b = pickle.load(handle)

    key = get_key(password, b['salt'])

    fernet = Fernet(key)
    decrypted_passwords = fernet.decrypt(b['passwords'])
    
    passwords = pickle.loads(decrypted_passwords)

    db = {
        "salt": b['salt'],
        "passwords": passwords
    }

    return db

def write_db(password, db, DB_NAME=DB_NAME):
    salt = db['salt']
    passwords = db['passwords']

    key = get_key(password, salt)
    fernet = Fernet(key)

    b_passwords = pickle.dumps(passwords, protocol=pickle.HIGHEST_PROTOCOL)

    encrypted_passwords = fernet.encrypt(b_passwords)

    db['passwords'] = encrypted_passwords

    with open(DB_NAME, 'wb') as handle:
        pickle.dump(db, handle, protocol=pickle.HIGHEST_PROTOCOL)

def get_key(password, salt):
    password = str.encode(password)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    return base64.urlsafe_b64encode(kdf.derive(password))

def login(password, DB_NAME=DB_NAME):
    passwords = read_db(password, DB_NAME)

    return passwords

def should_onboard(DB_NAME=DB_NAME):
    if not exists(DB_NAME):
        return True
    else:
        return False

def add_password(db, password):
    #Verificacion de que la contraseña no fue añadida previamente
    for password_i in db['passwords']:
        if password_i['name'] == password['name']:
            raise(Exception('Password already exists'))

    db['passwords'].append(password)

    return db
    
def remove_password(db, password_name):
    passwords = db['passwords']

    password_found = False
    for password in passwords:
        if password['name'] == password_name:
            passwords.remove(password)
            password_found = True

    if not password_found:
        raise(Exception('Password does not exists'))
    
    db['passwords'] = passwords
    
    return db

def read_password(db, password_name):
    for password in db['passwords']:
        if password['name'] == password_name:
            return password
    raise(Exception('Password does not exists'))

def reset():
    pass

if __name__ == "__main__":
    if should_onboard():
        password = input("Ingresa la contraseña para autenticarte: ")
        onboarding(password) 
        exit()

    password = input("Ingresa la contraseña: ")

    db_new = add_password()
    write_db(db_new)


    PASSWORDS = login(password)

    print(PASSWORDS)
