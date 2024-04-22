import datetime as dt
import os
from banking import register_bvn_account as rba


def clear():
    """Helps Clear the Output Console"""
    os.system('clear')


def header():
    clear()
    today_date = dt.datetime.now().date()
    time_now = dt.datetime.now().time()

    print(f"BETA BANKING {today_date} {time_now}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


def __main__():
    header()

    print(' ~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~')
    print("|  1. New User  |  2. Existing User  |")
    print(" ~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~")

    print(">>> ", end='')
    input_1 = input("")

    if input_1 == '1':
        header()
        print('\t\t\tMessage from the CUSTOMER SERVICE OFFICER:::')
        print('\t\t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print("'You will need to Create your BVN first, then Create your Bank Account'. \nLet's Create your BVN first")
        header()
        rba.register_bvn()


__main__()
