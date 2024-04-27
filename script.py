import datetime as dt
import os
import re
import time
from banking import register_users


def clear():
    """Helps Clear the Output Console"""
    os.system('clear')


def header():
    clear()
    today_date = dt.datetime.now().date()
    time_now = dt.datetime.now().time()

    print(f"BETA BANKING {today_date} {time_now}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


def main():
    while True:
        header()

        print(' ~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~')
        print("|  1. New User  |  2. Existing User  |")
        print(" ~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~")

        print(">>> ", end="")
        _input = input("")

        if re.search('^1$', _input):
            header()
            print('Message from the CUSTOMER SERVICE OFFICER:::')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print("'You will need to Create your BVN first, then Create your Bank Account'. ")
            print("\n---Let's Create your BVN---")
            time.sleep(3)
            header()
            register_users.register_bvn()
            time.sleep(5)
            header()
            register_users.register_account()
            break
        elif re.search('^2$', _input):
            print('hi')
            break
        else:
            print('Error')
            continue


if __name__ == '__main__':
    main()
