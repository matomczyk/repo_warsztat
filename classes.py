from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor
from clcrypto import hash_password


class User:
    def __int__(self, username="", password=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password)

    @property
    def id(self):
        return self._id

    @property
    def hashed_pswd(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_pswd.setter
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

