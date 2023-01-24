from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor
from clcrypto import hash_password
from datetime import datetime



class User:
    def __init__(self, username="", password=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password) VALUES (%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE users SET username=%s, hashed_password=%s WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = """SELECT id, username, hashed_password FROM Users WHERE username=%s"""
        cursor.execute(sql, (id, ))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = """SELECT id, username, hashed_password FROM Users WHERE id=%s"""
        cursor.execute(sql, (id_, ))
        data = cursor.fetchone()
        if data:
            id, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = """SELECT id, username, hashed_password FROM Users"""
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id, ))
        self._id = -1
        return True
    def __str__(self):
        user_info = f'"{self.username}" has id of "{self._id}" and their hashed password is "{self._hashed_password}".'
        return user_info


class Messages:

    def __init__(self, from_id, to_id):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = ""
        self.creation_date = None

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):

        if self._id == -1:
            sql = """INSERT INTO messages(from_id, to_id, creation_date, text) VALUES (%s, %s, %s, %s) RETURNING id"""
            self.creation_date = datetime.now()
            values = (self.from_id, self.to_id, self.creation_date, self.text)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE messages SET from_id=%s, to_id=%s, creation_date=%s, text=%s WHERE id=%s"""
            self.creation_date = datetime.now()
            values = (self.from_id, self.to_id, self.creation_date, self.text)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor):
        sql = """SELECT from_id, to_id, creation_date, text FROM Messages"""
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date, text = row
            loaded_message = Messages()
            loaded_message._id = id_
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message.creation_date = creation_date
            loaded_message.text = text
            messages.append(loaded_message)
        return messages

    def __str__(self):
        message = f'User {self.from_id} to user {self.to_id} at {self.creation_date}: "{self.text}" at {self.creation_date}.'
        return message



cnx = connect(user="postgres",
                password="coderslab",
                host="localhost", database="app")
cnx.autocommit = True
cursor = cnx.cursor()

# m = Messages(3, 4)
# m.text = "KC"
# m.save_to_db(cursor)
# t = m.__str__()
# print(t)






