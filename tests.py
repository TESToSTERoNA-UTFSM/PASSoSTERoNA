from os.path import exists
import unittest
import os

import password as main

def get_db_example():
    return {
        "salt": os.urandom(16),
        "passwords": [
            {
                "name": "nombre",
                "password": "password",
                "keyword": "keyword"
            }
        ]
    }
class TestStringMethods(unittest.TestCase):
    def test_should_onboard_when_file_doesnt_exists(self):
        DB_TEST = "tests/tmp_testing.bin"
        
        try:
            os.remove(DB_TEST)
        except FileNotFoundError:
            pass

        self.assertTrue(main.should_onboard(DB_TEST))

    def test_should_onboard_when_file_exists(self):
        DB_TEST = "tests/tmp_testing.bin"

        with open(DB_TEST, 'w+') as _:
            self.assertFalse(main.should_onboard(DB_TEST))

    def test_login_reads_passwords(self):
        DB_TEST = 'tests/testing.bin'

        db = main.login('password', DB_TEST)

        self.assertEqual(db['passwords'], [])

    def test_add_password_when_is_not_repeated(self):
        db = get_db_example()
        password = {
            "name": "name",
            "password": "password",
            "keyword": "value"
        }

        db = main.add_password(db, password)

        self.assertEqual(db['passwords'][1], password)

    def test_add_password_when_there_is_another_with_same_name(self):
        db = get_db_example()
        
        password = {
            "name": "nombre",
            "password": "password",
            "keyword": "value"
        }

        with self.assertRaises(Exception) as cm:
            main.add_password(db, password)
        
        self.assertEqual(str(cm.exception), 'Password already exists')
    
    def test_remove_password_that_exists(self):
        db = get_db_example()

        password_name = "nombre"

        db = main.remove_password(db, password_name)

        self.assertEqual(db['passwords'], [])

    def test_remove_password_that_doesnt_exists(self):
        db = get_db_example()

        password_name = "nombre_no_existe"

        with self.assertRaises(Exception) as cm:
            main.remove_password(db, password_name)
        
        self.assertEqual(str(cm.exception), 'Password does not exists')
    
    def test_read_password_when_exists(self):
        db = get_db_example()

        password_name = "nombre"

        password = main.read_password(db, password_name)

        self.assertEqual(password, db['passwords'][0])

    def test_read_password_when_doesnt_exists(self):
        db = get_db_example()

        password_name = "nombre_no_existe"

        with self.assertRaises(Exception) as cm:
            main.read_password(db, password_name)
        
        self.assertEqual(str(cm.exception), 'Password does not exists')
    

if __name__ == '__main__':
    unittest.main()