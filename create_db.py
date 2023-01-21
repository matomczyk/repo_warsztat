import psycopg2.errorcodes
from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor
def create_database():
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

def execute_sql(sql):
    try:
        cnx = connect(user="postgres",
                        password="coderslab",
                        host="localhost", database="app")
        cnx.autocommit = True
        cursor = cnx.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql)
    except OperationalError:
        print("Connection Error")
    except psycopg2.errors.DuplicateTable:
        print("Table already exists")
    else:
        cursor.close()
        cnx.close()
def create_users_table():
    sql = execute_sql("""CREATE TABLE Users(
                id SERIAL PRIMARY KEY,
                username VARCHAR(225),
                hashed_password VARCHAR(225)        
              );""")
    return sql

def create_messages_table():
    sql = execute_sql("""CREATE TABLE messages(
                id SERIAL PRIMARY KEY,
                from_id INT,
                to_id INT,
                creation_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT current_timestamp,
                text VARCHAR(225),
                FOREIGN KEY (from_id) REFERENCES Users(id) ON DELETE CASCADE,
                FOREIGN KEY (to_id) REFERENCES Users(id) ON DELETE CASCADE
              );""")
    return sql

create_database()
create_users_table()
create_messages_table()




