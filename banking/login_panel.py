# import datetime as dt
import re
import time
from banking.script import header, go_back
from bank_processes.authentication import Authentication, verify_data, check_account_status, get_username_from_database


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

        if check_account_status(_username)[1] == 'suspended':
            print("\nAccount is Suspended.\nReset your Password.")
            time.sleep(3)
            go_back('script')

        if check_account_status(_username)[1] == 'blocked':
            print("\nAccount is Blocked.\nMeet the admin to unblock your account.")
            time.sleep(3)
            go_back('script')

        if verify_data('username', 1, _username) and check_account_status(_username)[0]:
            auth.username = _username
            # auth.user_login()
            return _username
        else:
            print("\n*ERROR*\nWrong Username.")
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
                print("\n*ERROR*\nWrong Password.")
                print("Account has being Suspended. Reset your password.")
                time.sleep(3)
                break
            else:
                print("\n*ERROR*\nWrong Password.")
                print(3-auth.login_attempts, 'attempts remaining.\nAccount will be suspended after exhausting attempts')
                time.sleep(3)
                continue

    auth.account_lockout()

    time.sleep(1)

    go_back('script')


def forgot_username():
    while True:
        print("ENTER YOUR PHONE NUMBER:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        _phoneNumber = input(">>> ")

        if verify_data('phone_number', 1, _phoneNumber):
            _username = get_username_from_database(_phoneNumber, phone_number=True)

        else:
            print("\n*ERROR*\nPhone Number doesn't exist.")
            time.sleep(3)
            continue


def login():
    header()

    print("Go Back? Press 1")
    print("----------------")
    print("Forgot Username? Press 2")
    print("------------------------")

    time.sleep(1)

    _username = username()

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
    else:
        header()

        print(f"Welcome Back, {_username}")
        print("~~~~~~~~~~~~~~" + '~'*len(_username))
        print("\nGo Back? Press 1")
        print("----------------")
        print("Forgot Username? Press 2")
        print("------------------------")

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


