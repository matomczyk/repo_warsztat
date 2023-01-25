from classes import User
import argparse
import clcrypto
from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor
from flask import Flask

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-n", "--new_pass", help="new password")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")
args = parser.parse_args()

def create_user(cur, username, password):
    if len(password) < 8:
        print('Password too short, should be at least 8 characters')
    else:
        try:
            new_user = User(username, password)
            new_user.save_to_db(cur)
            print('User created.')
        except UniqueViolation as e:
            print('User already exists.', e)


def edit_password(cur, username, password, new_pass):
    if User.load_user_by_username(cur, username):
        if len(new_pass) < 8:
            print('Password too short, should be at least 8 characters')
        else:
            updated_password = User(username, password)
            updated_password.save_to_db(cur)
            print('Password updated')
    else:
        print('User does not exist!')


def delete_user(cur, username, password):
    user = User(username, password)
    if not user:
        print('User does not exist!')
    elif clcrypto.check_password(password, user.hashed_password):
        user.delete(cur)
        print('User deleted')
    else:
        print('Incorrect password!')


def list_users(cur):
    users = User.load_all_users(cur)
    for user in users:
        print(user.username)


if __name__ == '__main__':
    try:
        cnx = connect(user="postgres", password="coderslab", host="localhost", database="app")
        cnx.autocommit = True
        cur = cnx.cursor()
        if args.username and args.password:
            create_user(cur, args.username, args.password)
        elif args.username and args.password and args.new_pass and args.edit:
            edit_password(cur, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cur, args.username, args.password)
        elif args.username and args.password and args.list:
            list_users(cur)
        else:
            parser.print_help()
        cnx.close()
    except OperationalError as error:
        print('Connection error: ', error)
        