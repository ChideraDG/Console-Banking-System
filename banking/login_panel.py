# import datetime as dt
# import os
import re
import time
from banking.script import header, go_back
from bank_processes.authentication import Authentication as auth


def username():
    print("\nENTER YOUR USERNAME:")
    print("~~~~~~~~~~~~~~~~~~~~")
    _username = input(">>> ")

    if re.search('^1$', _username):
        return _username
    elif re.search('^2$', _username):
        return _username

    if auth.user_login():
        print('hi')

    return _username


def password():
    print("\nENTER YOUR PASSWORD:")
    print("~~~~~~~~~~~~~~~~~~~~")


def login():
    header()

    print("\nGo Back? Press 1")
    print("----------------")
    print("Forgot Username? Press 2")
    print("------------------------")
    time.sleep(1)
    _username = username()
    if re.search('^1$', _username):
        del _username
        go_back('script')
    elif re.search('^2$', _username):
        print()


