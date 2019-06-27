import json
import mysql.connector as mariadb

class DB_CREDS():
    name = ""
    password = ""
    address = ""
    database = ""

    def __init__(self):
        with open("config.json") as config_file:
            data = json.load(config_file)
            for key, value in data["db_creds"].items():
                if key == "db_user":
                    self.name = value
                elif key == "db_pass":
                    self.password = value
                elif key == "db_host":
                    self.address = value
                elif key == "db_database":
                    self.database = value

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_pass(self):
        return self.password

    def set_pass(self, passw):
        self.password = passw

    def get_host(self):
        return self.address

    def set_host(self, add):
        self.address = add

    def get_db(self):
        return self.database

    def set_db(self, db):
        self.database = db
