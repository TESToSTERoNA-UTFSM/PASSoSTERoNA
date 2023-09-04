import json
from cryptography.fernet import Fernet
import base64, hashlib
from os.path import exists

import os
import ast
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DB_NAME = 'db_schema.json'

PASSWORD = 'admin'

# inicio de 0 del programa
def onboarding():
    PASSWORD = input("Ingresa tu wea: ")

    salt = get_random_salt()

    db = {
        "salt": str(salt),
        "passwords": ""
    }
    
    with open(DB_NAME, 'w') as f:
        return json.dump(db, f, indent=4)

# cada vez que parto
def login():
    PASSWORD = input("Ingresa tu password de autenticación: ")
    return decrypt_passwords(PASSWORD)

# FUNCIONA
def get_salt():
    db = read_db()
    salt = db['salt']
    salt = salt[2:-1].encode()

    return salt

# FUNCIONA
def get_random_salt():
    return os.urandom(16)


def get_key(password):
    password = str.encode(password)
    salt = get_salt()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    return base64.urlsafe_b64encode(kdf.derive(password))


def read_db():
    with open(DB_NAME, 'r') as f:
        return json.load(f)
    

def encrypt_passwords(password, passwords):
    with open(DB_NAME, "r+") as f:
        db = json.load(f)

        key = get_key(password)

        fernet = Fernet(key)

        encrypted_passwords = fernet.encrypt(str(passwords).encode())
        
        db['passwords'] = str(encrypted_passwords)[2:]
        
        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()

def decrypt_passwords(password):
    key = get_key(password)
    
    fernet = Fernet(key)

    #Limita que las contraseñas estén en UTF-8
    passwords = bytes(read_db()['passwords'], "utf-8")

    # try:
    # except:
        # print("WRONG PASSOWRD")
        # exit()
    uncrypted_psswd = fernet.decrypt(passwords)
    
    return ast.literal_eval(uncrypted_psswd.decode())


passwords = [
    {
        "name": "kjshkasjhd",
        "password": "chao",
        "keyword": "uno"
    },
]
s = get_random_salt()

# print(str(s), type(str(s)))
#print(str(s))
#lala = str(s)[2:-1]
#
#print(type(lala))
#print(lala.encode())
#print(type(lala.encode()))
# print(s, type(s))
# print(ast.literal_eval(str(s)), type(ast.literal_eval(str(s))))

# if database is not created

if not exists(DB_NAME):
    onboarding()
    exit()
    
passwords = login()
print(passwords)import json
from cryptography.fernet import Fernet
import base64, hashlib
from os.path import exists

import os
import ast
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DB_NAME = 'db_schema.json'

PASSWORD = 'admin'

# inicio de 0 del programa
def onboarding():
    PASSWORD = input("Ingresa tu wea: ")

    salt = get_random_salt()

    db = {
        "salt": str(salt),
        "passwords": ""
    }
    
    with open(DB_NAME, 'w') as f:
        return json.dump(db, f, indent=4)

# cada vez que parto
def login():
    PASSWORD = input("Ingresa tu password de autenticación: ")
    return decrypt_passwords(PASSWORD)

# FUNCIONA
def get_salt():
    db = read_db()
    salt = db['salt']
    salt = salt[2:-1].encode()

    return salt

# FUNCIONA
def get_random_salt():
    return os.urandom(16)


def get_key(password):
    password = str.encode(password)
    salt = get_salt()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    return base64.urlsafe_b64encode(kdf.derive(password))


def read_db():
    with open(DB_NAME, 'r') as f:
        return json.load(f)
    

def encrypt_passwords(password, passwords):
    with open(DB_NAME, "r+") as f:
        db = json.load(f)

        key = get_key(password)

        fernet = Fernet(key)

        encrypted_passwords = fernet.encrypt(str(passwords).encode())
        
        db['passwords'] = str(encrypted_passwords)[2:]
        
        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()

def decrypt_passwords(password):
    key = get_key(password)
    
    fernet = Fernet(key)

    #Limita que las contraseñas estén en UTF-8
    passwords = bytes(read_db()['passwords'], "utf-8")

    # try:
    # except:
        # print("WRONG PASSOWRD")
        # exit()
    uncrypted_psswd = fernet.decrypt(passwords)
    
    return ast.literal_eval(uncrypted_psswd.decode())


passwords = [
    {
        "name": "kjshkasjhd",
        "password": "chao",
        "keyword": "uno"
    },
]
s = get_random_salt()

# print(str(s), type(str(s)))
#print(str(s))
#lala = str(s)[2:-1]
#
#print(type(lala))
#print(lala.encode())
#print(type(lala.encode()))
# print(s, type(s))
# print(ast.literal_eval(str(s)), type(ast.literal_eval(str(s))))

# if database is not created

if not exists(DB_NAME):
    onboarding()
    exit()
    
passwords = login()
print(passwords)