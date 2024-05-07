# import datetime as dt
import random
import re
import time
from banking.script import header, go_back, signed_in
from bank_processes.authentication import (Authentication,
                                           verify_data,
                                           check_account_status,
                                           get_username_from_database,
                                           token_auth)

auth = Authentication()


def username():
    """Get Username of the User"""
    while True:
        print("\nENTER YOUR USERNAME:")
        print("~~~~~~~~~~~~~~~~~~~~")
        _username = input(">>> ")

        if re.search('^1$', _username):
            return _username
        elif re.search('^2$', _username):
            return _username
        elif re.search('^go back$', _username.lower()):
            go_back('script')

        if verify_data('username', 1, _username):
            if check_account_status(_username)[1] == 'suspended':
                print("\n:: Account is SUSPENDED.\n:: Reset your Password.")
                del _username
                time.sleep(3)
                go_back('script')
            elif check_account_status(_username)[1] == 'blocked':
                print("\n:: Account is BLOCKED.\n:: Meet the admin to UNBLOCK your account.")
                del _username
                time.sleep(3)
                go_back('script')
            elif check_account_status(_username)[0]:
                auth.username = _username
                return _username
        else:
            print("\n:: Wrong Username.")
            time.sleep(3)
            continue


def password():
    while auth.login_attempts < 3:
        print("\nENTER YOUR PASSWORD:")
        print("~~~~~~~~~~~~~~~~~~~~")
        _password = input(">>> ")

        if re.search('^1$', _password):
            return _password
        elif re.search('^2$', _password):
            return _password

        auth.password = _password
        if auth.password_validation():
            return _password
        else:
            auth.login_attempts = auth.login_attempts + 1
            if auth.login_attempts == 3:
                print("\n:: Wrong Password.")
                print("Account has being Suspended. Reset your password.")
                time.sleep(3)
                break
            else:
                print("\n:: Wrong Password.")
                print(3 - auth.login_attempts,
                      'attempts remaining.\nAccount will be suspended after exhausting attempts')
                time.sleep(3)
                continue

    auth.account_lockout()

    time.sleep(1)

    go_back('script')


def forgot_username():
    while True:
        print("\nENTER YOUR REGISTERED PHONE NUMBER/E-MAIL:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        _input = input(">>> ").lower()

        if re.search(r"^\w+@(\w+\.)?\w+\.(edu|com|gov|ng|org)$", _input, re.IGNORECASE):
            _username: str = get_username_from_database(_input, email=True)
            column = 'email'
        elif re.search(r'^\+?[0-9]{3} ?[0-9-]{8,11}$', _input) and 11 <= len(_input) <= 15:
            _username: str = get_username_from_database(_input, phone_number=True)
            column = 'phone_number'
        else:
            print("\nWrong Input")
            time.sleep(3)
            continue

        if verify_data(column, 1, _input):
            auth.username = _username
            time.sleep(1)
            _password = password()
            time.sleep(1)

            start_time = time.time()
            _token = token_auth()
            while True:
                print("\nENTER YOUR TOKEN NUMBER:")
                print("~~~~~~~~~~~~~~~~~~~~~~~~")
                _tokenNumber = input(">>> ")

                elapsed_time = time.time() - start_time
                if elapsed_time < 300.0:
                    if _token == _tokenNumber:
                        with open('notification.txt', 'w') as file:
                            file.write(f"Your Username: {_username}. Don't Share it.")
                        print("\nUsername Successfully Recovered. \nUsername sent to your notification")
                        break
                    else:
                        print("\n*ERROR*\nWrong Token Number.\n\nTry Again")
                        time.sleep(3)
                        continue
                else:
                    print("\n:: Time is already over 5 minutes.")
                    time.sleep(1)
                    print("\n:: Re-Sending Token Number")
                    start_time = time.time()
                    _token = token_auth()
                    time.sleep(3)
                    continue
            break
        else:
            print(":: Phone Number doesn't exist.")
            time.sleep(3)
            continue


def forgot_password():
    while True:
        print("\nENTER YOUR USERNAME:")
        print("~~~~~~~~~~~~~~~~~~~~")
        _input = input(">>> ")

        if verify_data('username', 1, _input):
            auth.username = _input
            time.sleep(2)
            auth.reset_password()
            auth.change_password()
            break
        else:
            print("\n*ERROR*\nUsername doesn't exist.")
            time.sleep(3)
            continue


def login():
    header()

    print("\nGo Back? Press 1")
    print("----------------")

    print("Forgot Username? Press 2")
    print("------------------------")

    time.sleep(1)

    _username: str = username()

    time.sleep(1)

    if re.search('^1$', _username):
        del _username
        if auth.username is not None:
            del auth.username
        go_back('script')
    elif re.search('^2$', _username):
        del _username
        if auth.username is not None:
            del auth.username
        header()
        forgot_username()
        time.sleep(2)
        header()
        _username = username()

    header()

    print(f"\nWelcome Back, {auth.username}")
    print("~~~~~~~~~~~~~~" + '~' * len(auth.username))

    print("\nGo Back? Press 1")
    print("----------------")

    print("Forgot Password? Press 2")
    print("------------------------")

    _password = password()

    if re.search('^1$', _password):
        del _username
        del _password

        if auth.username is not None:
            del auth.username
        if auth.password is not None:
            del auth.password

        go_back('script')
    elif re.search('^2$', _password):
        del _username
        del _password

        if auth.username is not None:
            del auth.username
        if auth.password is not None:
            del auth.password

        time.sleep(2)
        header()
        forgot_password()

        if auth.username is not None:
            del auth.username
        if auth.password is not None:
            del auth.password

        login()
    else:
        header()
        # auth.user_login()
        print("\n:: Login Successful")
        print("~~~~~~~~~~~~~~~~~~~")
        # time.sleep(2)
        signed_in(username=_username, password=_password)
