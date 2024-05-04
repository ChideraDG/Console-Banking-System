import datetime as dt
import os
import re
import time


def clear():
    """Helps Clear the Output Console"""
    os.system('clear')


def header():
    clear()
    today_date = dt.datetime.now().date()
    time_now = dt.datetime.now().time()

    print(f"BETA BANKING {today_date} {time_now}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def go_back(return_place):
    if return_place == 'script':
        script()


def script():
    from banking.login_panel import login
    from banking.register_panel import register_bvn_account

    while True:
        header()

        print(end='\n')
        print(' ~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~')
        print("|  1. New User  |  2. Existing User  |")
        print(" ~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~")

        user_input = input(">>> ")

        if re.search('^1$', user_input):
            register_bvn_account()
            time.sleep(5)
            login()
            break
        elif re.search('^2$', user_input):
            login()
            break
        else:
            del user_input
            continue
