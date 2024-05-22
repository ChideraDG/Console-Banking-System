import datetime
import calendar
import os
import re
import time
from bank_processes.authentication import Authentication
from animation.colors import *


def clear():
    """Helps Clear the Output Console"""
    os.system('cls') if os.name == 'nt' else os.system('clear')


def findDate(date):
    year, month, day = (int(i) for i in date.split('-'))
    dayNumber = calendar.weekday(year, month, day)
    monthNumber = datetime.datetime.now().month

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    return days[dayNumber], str(day), months[monthNumber - 1], str(year)


def header():
    clear()
    time_now = datetime.datetime.now().time()
    date = datetime.datetime.today().date()
    day_in_words, day, month, year = findDate(str(date))

    print(bold, end='')
    print(yellow, end='')
    print(f"CONSOLE BETA BANKING   :: {day_in_words}, {day} {month} {year} ::   :: {time_now} ::")
    print(f"{magenta}{bold}~~~~~~~~~~~~~~~~~~~~   ~~~~~~~~~~",
          "~" * (len(day_in_words) + len(day) + len(month) + len(year)),
          "   ~~~~~~", "~" * len(str(time_now)), sep='')
    print(end, end='')


def go_back(return_place, auth: Authentication = None):
    if return_place == 'script':
        signing_in()
    if return_place == 'signed_in':
        signed_in(auth)


def signing_in():
    from banking.login_panel import login
    from banking.register_panel import register_bvn_account

    while True:
        header()

        print(end='\n')

        print(f'{magenta}+~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+')
        print(f"|  {yellow}1. NEW USER  {magenta}|  {yellow}2. EXISTING USER  {magenta}|")
        print(f"+~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+")
        print(f"|         {yellow}3. UNBLOCK ACCOUNT         {magenta}|")
        print(f"+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")

        print(magenta, bold, end='')
        user_input = input(">>> ")
        print(end, end='')

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


def signed_in_header(auth: Authentication, account_balance_display: bool = True):
    try:
        if datetime.time(0, 0, 0) < datetime.datetime.now().time() < datetime.time(12, 0, 0):
            time_of_the_day = 'Morning'
        elif datetime.time(12, 0, 0) < datetime.datetime.now().time() < datetime.time(17, 0, 0):
            time_of_the_day = 'Afternoon'
        elif datetime.time(17, 0, 0) < datetime.datetime.now().time() < datetime.time(22, 0, 0):
            time_of_the_day = 'Evening'
        else:
            time_of_the_day = 'Night'

        header()
        if account_balance_display:
            display_name = 'HIDE'
            print(end='\n')
            print(f"Good {time_of_the_day}, {auth.first_name}"
                  f"{' '*(28-len(auth.first_name+time_of_the_day))}"
                  f"{auth.account_balance} Naira"
                  f"{' '*(24-len(str(auth.account_balance)))}"
                  f"Session Token: {auth.session_token}")
            print(f"~"*7, "~"*len(time_of_the_day), "~"*len(auth.first_name),
                  " "*(28-len(auth.first_name+time_of_the_day)), "~"*6,
                  "~" * len(str(auth.account_balance)), " "*(24-len(str(auth.account_balance))), "~~~~~~~~~~~~~~~",
                  "~" * len(auth.session_token), sep='')
        else:
            display_name = 'SHOW'
            print(end='\n')
            print(f"Good {time_of_the_day}, {auth.first_name}"
                  f"{' '*(58-len(auth.first_name+time_of_the_day))}"
                  f"Session Token: {auth.session_token}")
            print(f"~~~~~~~", "~" * len(time_of_the_day), "~" * len(auth.first_name),
                  ' '*(58-len(auth.first_name+time_of_the_day)),
                  "~~~~~~~~~~~~~~~", "~" * len(auth.session_token), sep='')

        return display_name
    except Exception as e:
        with open('error.txt', 'w') as file:
            file.write(f'Module: script.py \nFunction: signed_in_header \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')


def signed_in(auth: Authentication):
    """Function to sign in Users with a Savings or Current account"""
    from banking import transfer_money
    from banking import fixed_deposit

    try:
        if auth.account_type == 'savings' or auth.account_type == 'current':
            account_balance_display = None
            while True:
                display_name = signed_in_header(auth, account_balance_display)

                print(end='\n')
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print(f"|  1. {display_name} ACCOUNT BALANCE  |    2. TRANSFER MONEY    |   3. CARD-LESS WITHDRAWAL    |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|      4. DEPOSIT MONEY     |     5. COLLECT LOAN     |        6. UPDATE BVN         |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|  7. TRANSACTION HISTORY   |  8. GENERATE STATEMENT  |       9. BENEFICIARIES       |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|    10. UPGRADE ACCOUNT    |    11. OPEN ACCOUNT     |       12. CLOSE ACCOUNT      |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|     13. BLOCK ACCOUNT     |  14. VIEW CONTACT INFO  |  15. CHANGE TRANSACTION PIN  |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|  16. UPDATE ACCOUNT INFO  |  17. BANK INFORMATION   |      18. FIXED DEPOSIT       |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
                print("|                                     19. LOGOUT                                     |")
                print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")

                user_input = input(">>> ")

                if re.search('^1$', user_input):
                    if display_name == 'SHOW':
                        account_balance_display = True
                    else:
                        account_balance_display = False

                    continue
                elif re.search('^2$', user_input):
                    transfer_money.process_transfer(auth)
                    continue
                elif re.search('^3$', user_input):
                    continue
                elif re.search('^4$', user_input):
                    continue
                elif re.search('^5$', user_input):
                    continue
                elif re.search('^6$', user_input):
                    continue
                elif re.search('^7$', user_input):
                    continue
                elif re.search('^8$', user_input):
                    continue
                elif re.search('^9$', user_input):
                    continue
                elif re.search('^10$', user_input):
                    continue
                elif re.search('^11$', user_input):
                    continue
                elif re.search('^12$', user_input):
                    continue
                elif re.search('^13$', user_input):
                    continue
                elif re.search('^14$', user_input):
                    continue
                elif re.search('^15$', user_input):
                    continue
                elif re.search('^16$', user_input):
                    continue
                elif re.search('^17$', user_input):
                    continue
                elif re.search('^18$', user_input):
                    if auth.fixed_account == 'yes':
                        pass
                    if auth.fixed_account == 'no':
                        fixed_deposit.fixed_deposit(auth)
                elif re.search('^19$', user_input):
                    auth.user_logout()
                    del user_input
                    go_back('script')
                    break
                elif re.search('^(go back|goback)$', user_input.strip().lower()):
                    auth.user_logout()
                    del user_input
                    go_back('script')
                    break
                else:
                    del user_input
                    continue
    except Exception as e:
        with open('error.txt', 'w') as file:
            file.write(f'Module: script.py \nFunction: signed_in_ \nError: {repr(e)}')
        print(f'\nError: {repr(e)}')
        time.sleep(3)
        go_back('script')
