from classes import Messages, User

import argparse
import clcrypto
from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor
from flask import Flask

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="to")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-s", "--send", help="message")

args = parser.parse_args()


def list_all_messages(cur, username):
    messages = Messages.load_all_messages(cur, user.id)
    for message in messages:
        from_ = User.load_user_by_id(cur, message.from_id)
        print(f"""Message from {from_.username} sent on {message.creation_date}: {message.text} \n""")


def send_message(cur, from_id, recipient, text):
    recipient = User.load_user_by_username(cur, recipient)
    if recipient:
        if len(text) < 255:
            message = Messages(from_id, recipient.id)
            message.text = text
            message.save_to_db(cur)
            print('Message sent')
        else:
            print('Message has to be shorter than 255 characters.')
    else:
        print('Recipient does not exist in the database')


if __name__ == '__main__':
    try:
        cnx = connect(user="postgres", password="coderslab", host="localhost", database="app")
        cnx.autocommit = True
        cur = cnx.cursor()
        if args.username and args.password:
            sender = User.load_user_by_username(cur, args.username)
            if not clcrypto.check_password(args.password, sender.hashed_password):
                print('Password is not correct')
            elif args.username and args.password and args.list:
                list_all_messages(cur, args.username)
            elif args.username and args.password and args.to and args.send:
                send_message(cur, sender.id, args.to, args.send)
        else:
            parser.print_help()
        cnx.close()
    except OperationalError as error:
        print('Connection error: ', error)
