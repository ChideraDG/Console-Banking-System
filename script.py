import datetime as dt
import os
import re
import time
from banking.register_panel import register_bvn_account
from banking.login_panel import login


def clear():
    """Helps Clear the Output Console"""
    os.system('clear')


def header():
    clear()
    today_date = dt.datetime.now().date()
    time_now = dt.datetime.now().time()

    print(f"BETA BANKING {today_date} {time_now}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


def new_user():
    header()
    print('Message from the CUSTOMER SERVICE OFFICER:::')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print("'You will need to Create your BVN first, then Create your Bank Account'. ")
    time.sleep(3)
    header()
    register_bvn_account()


def main():
    while True:
        header()

        print(' ~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~')
        print("|  1. New User  |  2. Existing User  |")
        print(" ~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~")

        print(">>> ", end="")
        _input = input("")

        if re.search('^1$', _input):
            new_user()
            break
        elif re.search('^2$', _input):
            login()
            break
        else:
            continue


if __name__ == '__main__':
    main()
