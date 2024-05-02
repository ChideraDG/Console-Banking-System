# import datetime as dt
import random
import re
import time
from banking.script import header, go_back
from bank_processes.authentication import Authentication, verify_data, check_account_status, get_username_from_database

auth = Authentication()


def token_auth():
    """Generates token for username and password recovery."""
    token = str(random.randint(100000, 999999))
    with open('token_notification.txt', 'w') as file:
        file.write(f"Your Token Number: {token}. Don't Share it.\nExpires after 30 minutes.")

    return token


def username():
    """Get Username of the User"""
    while True:
        print("ENTER YOUR USERNAME:")
        print("~~~~~~~~~~~~~~~~~~~~")
        _username = input(">>> ")

        if re.search('^1$', _username):
            return _username
        elif re.search('^2$', _username):
            return _username

        if verify_data('username', 1, _username):
            if check_account_status(_username)[1] == 'suspended':
                print("\nAccount is Suspended.\nReset your Password.")
                del _username
                time.sleep(3)
                go_back('script')
            elif check_account_status(_username)[1] == 'blocked':
                print("\nAccount is Blocked.\nMeet the admin to unblock your account.")
                del _username
                time.sleep(3)
                go_back('script')

        if verify_data('username', 1, _username) and check_account_status(_username)[0]:
            auth.username = _username
            # auth.user_login()
            return _username
        else:
            print("\n*ERROR*\nWrong Username.\n")
            time.sleep(3)
            continue


def password():
    while auth.login_attempts < 3:
        print("ENTER YOUR PASSWORD:")
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
                print("\n*ERROR*\nWrong Password.")
                print("Account has being Suspended. Reset your password.")
                time.sleep(3)
                break
            else:
                print("\n*ERROR*\nWrong Password.")
                print(3 - auth.login_attempts,
                      'attempts remaining.\nAccount will be suspended after exhausting attempts\n')
                time.sleep(3)
                continue

    auth.account_lockout()

    time.sleep(1)

    go_back('script')


def forgot_username():
    while True:
        print("ENTER YOUR PHONE NUMBER/E-MAIL:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        _input = input(">>> ")

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
                if elapsed_time < 30.0:
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
                    print("\n*ERROR*\nTime is already over 30 minutes.\n\nRe-Sending Token Number")
                    start_time = time.time()
                    _token = token_auth()
                    time.sleep(3)
                    continue
            break
        else:
            print("\n*ERROR*\nPhone Number doesn't exist.\n")
            time.sleep(3)
            continue


def login():
    header()

    print("Go Back? Press 1")
    print("----------------")
    print("Forgot Username? Press 2")
    print("------------------------\n")

    time.sleep(1)

    _username: str = username()

    time.sleep(1)

    if re.search('^1$', _username):
        del _username
        del auth.username
        go_back('script')
    elif re.search('^2$', _username):
        del _username
        del auth.username
        header()
        forgot_username()
        time.sleep(3)
        header()
        _username = username()

    header()

    print(f"Welcome Back, {_username}")
    print("~~~~~~~~~~~~~~" + '~' * len(_username))
    print("\nGo Back? Press 1")
    print("----------------")
    print("Forgot Username? Press 2")
    print("------------------------\n")

    _password = password()

    if re.search('^1$', _password):
        del _username
        del _password
        del auth.username
        del auth.password
        go_back('script')
    elif re.search('^2$', _password):
        del _username
        del auth.username
        del _password
        del auth.password
    else:
        print("\nLogin Successful")
        print("~~~~~~~~~~~~~~~~")
