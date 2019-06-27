import json
import mysql.connector as mariadb
from disco.bot import Plugin

class DB_CREDS:
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

class mariadb_funcs(Plugin):
    dbclass = DB_CREDS()
    connection = mariadb.connect(user = dbclass.get_name(), password = dbclass.get_pass(),
    host = dbclass.get_host(), database = dbclass.get_db())

    def update_server_table(self, serverID, prefix):
        pass

    def get_user(self, userID):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM user_settings WHERE user_id=%s", (userID,))
        row = cursor.fetchone()
        if row is None:
            try:
                cursor.execute("INSERT INTO user_settings (user_id) VALUES (%s)", (userID,))
                self.connection.commit()
                print("new user added: {}".format(userID))
            except mariadb.Error as error:
                print("New user insert error: {}".format(error))

            cursor.execute("SELECT * FROM user_settings WHERE user_id=%s", (userID,))
            row = cursor.fetchone()

        cursor.close()
        return row

    def update_user_setting(self, userID, option):
        row = self.get_user(userID)
        print(row)
        #cursor = self.connection.cursor()
        #Option has to be: call_me, usr_desc, timezone, facts (associates to columns in database)
        #try:
        #    cursor.execute
        #pass
