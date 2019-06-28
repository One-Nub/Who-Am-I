import json
import mysql.connector as mariadb
from disco.bot import Plugin

class DB_CREDS:
    name = ""
    password = ""
    address = ""
    database = ""
    port = ""

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
                elif key == "db_port":
                    self.port = value

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

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

class mariadb_funcs(Plugin):
    dbclass = DB_CREDS()
    connection = mariadb.connect(user = dbclass.get_name(), password = dbclass.get_pass(),
        host = dbclass.get_host(), database = dbclass.get_db(), port = dbclass.get_port())

    def confirm_tables_exist(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS user_settings (
                user_id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
                call_me VARCHAR(50),
                usr_desc VARCHAR(1000),
                timezone VARCHAR(25),
                facts VARCHAR(250))""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS server_settings (
                server_id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
                prefix VARCHAR(15) DEFAULT 'wai!')""")

            self.connection.commit()
        except mariadb.Error as error:
            print(error)

        cursor.close()

    def get_server_prefix(self, serverID):
        self.confirm_tables_exist()
        cursor = self.connection.cursor()
        try:
            cursor.execute("""SELECT prefix FROM server_settings WHERE server_id = %s""", (serverID,))
            prefix = cursor.fetchone()
            if prefix:
                for val in prefix:
                    guildPrefix = val
                return guildPrefix
            else:
                self.make_server(serverID)
        except mariadb.Error as error:
            print(error)
            return None
        cursor.close()

    def check_guild_exists(self, serverID):
        self.confirm_tables_exist()
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM server_settings WHERE server_id = %s""", (serverID,))
        existance = cursor.fetchone()
        if existance:
            return True
        else:
            return False


    def make_server(self, serverID):
        self.confirm_tables_exist()
        cursor = self.connection.cursor()

        try:
            cursor.execute("""INSERT INTO server_settings (server_id) VALUES (%s)""", (serverID,))
            self.connection.commit()
        except mariadb.Error as error:
            print("Guild insertion error: {}".format(error))

        cursor.close()

    def update_server_prefix(self, serverID, prefix):
        self.confirm_tables_exist()
        cursor = self.connection.cursor()

        try:
            cursor.execute("""UPDATE server_settings SET prefix = %s
            WHERE server_id = %s""", (prefix, serverID))

            self.connection.commit()
            cursor.close()
            return True
        except mariadb.Error as error:
            print(error)
            cursor.close()
            return error

    def get_user_settings(self, userID):
        userConfig = []
        append = userConfig.append
        self.confirm_tables_exist()
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM user_settings WHERE user_id=%s""", (userID,))
        for value in cursor.fetchone():
            append(value)
        cursor.close()
        return userConfig

    def check_user_exists(self, userID):
        self.confirm_tables_exist()
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM user_settings WHERE user_id = %s""", (userID,))
        existance = cursor.fetchone()
        if existance:
            return True
        else:
            return False

    def make_user(self, userID):
        self.confirm_tables_exist()
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM user_settings WHERE user_id=%s""", (userID,))
        row = cursor.fetchone()
        if row is None:
            try:
                cursor.execute("""INSERT INTO user_settings (user_id) VALUES (%s)""", (userID,))
                self.connection.commit()
            except mariadb.Error as error:
                print("New user insert error: {}".format(error))

            cursor.execute("""SELECT * FROM user_settings WHERE user_id=%s""", (userID,))
            row = cursor.fetchone()

        cursor.close()
        return row

    def update_user_setting(self, userID, option, content):
        self.make_user(userID)
        cursor = self.connection.cursor()

        try:
            if option == 'call_me':
                cursor.execute("""UPDATE user_settings SET call_me = %s
                WHERE user_id = %s""", (content, userID))
            elif option == 'usr_desc':
                cursor.execute("""UPDATE user_settings SET usr_desc = %s
                WHERE user_id = %s""", (content, userID))
            elif option == 'timezone':
                cursor.execute("""UPDATE user_settings SET timezone = %s
                WHERE user_id = %s""", (content, userID))
            elif option == "facts":
                cursor.execute("""UPDATE user_settings SET facts = %s
                WHERE user_id = %s""", (content, userID))

            self.connection.commit()
            cursor.close()
            return True
        except mariadb.Error as error:
            errorStr = "Error: {}".format(error)
            print(errorStr)
            cursor.close()
            return errorStr
        #Option has to be: call_me, usr_desc, timezone, facts (associates to columns in database)
