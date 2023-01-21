import psycopg2.errorcodes
from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor

sql = "CREATE DATABASE app;"
try:
    cnx = connect(user="postgres",
                    password="coderslab",
                    host="localhost")
    cnx.autocommit = True
    cursor = cnx.cursor()
    cursor.execute(sql)
    print("Baza założona")
except OperationalError:
    print("Connection Error")
except psycopg2.errors.DuplicateDatabase:
    print("Database already exists")
else:
    cursor.close()
    cnx.close()


