import datetime
import datetime as dt
import os
import re
import time
from bank_processes.authentication import Authentication


def clear():
    """Helps Clear the Output Console"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def header():
    clear()
    today_date = dt.datetime.now().date()
    time_now = dt.datetime.now().time()

    print(f"BETA BANKING {today_date} {time_now}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def go_back(return_place):
    if return_place == 'script':
        signing_in()


def signing_in():
    from banking.login_panel import login
    from banking.register_panel import register_bvn_account

    while True:
        header()

        print(end='\n')
        print(' ~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~')
        print("|  1. NEW USER  |  2. EXISTING USER  |")
        print(" ~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~")
        print("|         3. UNBLOCK ACCOUNT         |")
        print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        user_input = input(">>> ")

        if re.search('^1$', user_input):
            register_bvn_account()
            time.sleep(5)
            login()
            break
        elif re.search('^2$', user_input):
            login()
            break
        elif re.search('^3$', user_input):
            break
        else:
            del user_input
            continue


def signed_in(username: str, password: str):
    auth = Authentication()

    auth.username = username
    auth.password = password
    auth.user_login()

    if datetime.time(0, 0, 0) < datetime.datetime.now().time() < datetime.time(12, 0, 0):
        time_of_the_day = 'Morning'
    elif datetime.time(12, 0, 0) < datetime.datetime.now().time() < datetime.time(17, 0, 0):
        time_of_the_day = 'Afternoon'
    elif datetime.time(17, 0, 0) < datetime.datetime.now().time() < datetime.time(22, 0, 0):
        time_of_the_day = 'Evening'
    else:
        time_of_the_day = 'Night'

    while True:
        header()

        print(end='\n')
        print(f"Good {time_of_the_day}, {auth.first_name}  N{auth.account_balance}  Session Token: {auth.session_token}")
        print(f"~~~~~~~", "~"*len(time_of_the_day), "~"*len(auth.first_name), "  ~", "~"*len(str(auth.account_balance)),
              "  ~~~~~~~~~~~~~~~", "~"*len(auth.session_token), sep='')

        break
