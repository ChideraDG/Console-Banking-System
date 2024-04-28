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
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


def login():
    pass
