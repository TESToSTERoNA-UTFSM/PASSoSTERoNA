
from cryptography.fernet import Fernet
import base64
import pickle
from os.path import exists
import string
import sys
import secrets
import json

import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DB_NAME = 'password.bin'

def generate_password(lenght, alpha = True, numeric = True, simpleSymbol = True, complexSymbol = True):
    ALPHA = string.ascii_letters
    NUMERIC = string.digits
    SIMPLESYMBOL = "!#$%&"
    COMPLEXSYMBOL = "\'\"()*+,-./:;<=>?@[\\]^_`{|}~"

    password = []
    chars = []

    if alpha:
        chars = chars + list(ALPHA)
    
    if numeric:
        chars = chars + list(NUMERIC)
    
    if simpleSymbol:
        chars = chars + list(SIMPLESYMBOL)
    
    if complexSymbol:
        chars = chars + list(COMPLEXSYMBOL)

    for _ in range(lenght):
        password.append(secrets.choice(chars))

    return ''.join(password)

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
    db = read_db(password, DB_NAME)

    return db

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

def reset(DB_NAME=DB_NAME):
    os.remove(DB_NAME)
    
def update_password(db, password_name, new_psswrd):
    try:
        new_password = read_password(db, password_name)
    except Exception as e:
        raise(e)

    new_password['password'] = new_psswrd

    return db


def update_name(db, password_name, new_name):
    try:
        new_password = read_password(db, password_name)
    except Exception as e:
        raise(e)

    new_password['name'] = new_name

    return db


def update_keyword(db, password_name, new_keyword):
    try:
        new_password = read_password(db, password_name)
    except Exception as e:
        raise(e)

    new_password['keyword'] = new_keyword

    return db

def search_by_name(db, password_name):
    return read_password(db, password_name)

def search_by_keyword(db, password_keyword):
    matching_passwords = []
    for password in db['passwords']:
        if password_keyword in password['keyword']:
            matching_passwords.append(password)
    return matching_passwords


if __name__ == "__main__":
    if should_onboard():
        master_password = input("Ingresa la contraseña maestra: ")
        onboarding(master_password) 
        exit()

    if sys.argv[1] == 'reset':
        reset()
        print("Contraseñas eliminadas")
        print("Vuelve a iniciar el gestor de contraseñas")
        exit()

    master_password = input("Ingresa la contraseña maestra: ")

    try:
        db = login(master_password)
    except:
        print("Contraseña incorrecta")
        exit()

    if (len(sys.argv) == 1):
        print("Debe especificar que acción quiere realizar")
        exit()
    
    args = sys.argv[2:]
    action = sys.argv[1]

    match action:
        case 'generate':
            lenght = int(args[0])
            alpha = '--alpha' in args 
            numeric = '--numeric' in args
            simpleSymbol = '--simple-symbol' in args 
            complexSymbol = '--complex-symbol' in args
             
            print(generate_password(lenght, alpha, numeric, simpleSymbol, complexSymbol))
        
        case 'add':
            name = input("Ingrese el nombre de la contraseña: ")
            passwd = input("Ingrese la contraseña: ")
            n_keywords = int(input("Ingrese la cantidad de keywords que tendrá su contraseña: "))
            keywords = []
            
            for i in range(n_keywords):
                keywords.append(input("Ingrese el keyword " + str(i + 1) + " : "))
            
            password = {
                "name": name,
                "password": passwd,
                "keyword": keywords
            }

            db = add_password(db, password)
        
        case 'remove':
            name = input("Ingrese el nombre de la contraseña que quiere eliminar: ")

            db = remove_password(db, name)     
            
        case 'update':
            method = args[0]
            
            match method:
                case 'name':
                    old_name = input("Ingrese el nombre de la contraseña que quiere modificar: ")
                    new_name = input("Ingrese el nuevo nombre: ")
                    
                    update_name(db, old_name, new_name)
                case 'password':
                    name = input("Ingrese el nombre de la contraseña que quiere modificar: ")
                    new_password = input("Ingrese la nueva contraseña: ")
                    
                    update_password(db, name, new_password)
                
                case 'keyword':
                    name = input("Ingrese el nombre de la contraseña que quiere modificar: ")

                    n_new_keyword = input("Ingrese cuantas keywords quiere añadir: ")
                    new_keywords = []
                    for i in range(n_new_keyword):
                        new_keywords.append(input("Ingrese el keyword ", i, " :"))
                        update_keyword(db, name, new_keywords)
                
                case _:
                    print("Opción del comando update no valido\nPor favor intente con los indicados en la documentación:\nLos comandos disponibles son:")
                    print("name \t\t Este comando actualizara el nombre")
                    print("keyword \t\t Este comando actualizara las palabras clave")
                    print("password \t\t Este comando actualizara la contraseña")
                    
                    exit()

        case 'get':
            method = args[0]

            match method:
                case 'name':
                    name = input("Ingrese el nombre de la contraseña que quiere buscar: ")
                    password = search_by_name(db, name)
                    if password:
                        print("La contraseña encontrada es la siguiente: ")
                        print(json.dumps(password, indent=4))
                    else:
                        print("No se encontró ninguna contraseña")

                case 'keyword':
                    password_keyword = input("Ingrese un keyword de las contraseñas que quiere buscar: ")
                    password = search_by_keyword(db, password_keyword)
                    if password:
                        print("Las contraseñas encontradas son la siguientes: ")
                        print(json.dumps(password, indent=4))
                    else:
                        print("No se encontró ninguna contraseña")
                case _:
                    print("Opción del comando get no valido\nPor favor intente con los indicados en la documentación:\nLos comandos disponibles son:")
                    print("name  Este comando buscará la contraseña por nombre")
                    print("keyword  Este comando buscará las contraseñas que tengan el keyword que se entregue")
                    
                    exit()
        case _:
            print("Comando no valido\nPor favor intente con los indicados en la documentación:\nLos comandos disponibles son:")
            print("generate \t Este comando generará una contraseña con las caracteristicas especificadas")
            print("add \t\t Este comando solicitará los campos necesarios para la creación de una nueva contraseña")
            print("remove \t\t Este comando eliminará una contraseña según el nombre que se le especifique")
            print("update \t\t Este comando permitirá la edición de una contraseña")
            print("reset \t\t Este comando permitirá resetear la contraseña de autenticación CUIDADO, ESTO ELIMINARÁ SUS CONTRASEÑAS")
            print("get \t\t Este comando permitirá buscar contraseñas según la opción adicional que se le entregue")
            exit()

    write_db(master_password, db)
