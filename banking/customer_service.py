import re
import time
from banking.main_menu import log_error, go_back, header
from banking.login_panel import forgot_password, forgot_username
from animation.colors import *
from bank_processes.account import Account
from banking.register_panel import countdown_timer


acc = Account()


def unblock_account():
    while True:
        header()

        print("\nUNBLOCK ACCOUNT")
        print("~~~~~~~~~~~~~~~")

        print("Enter your ACCOUNT NUMBER:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")

        user_input = input(">>> ").strip()
        print(end, end='')


def customer_service():
    try:
        while True:
            header()  # Call the header function to display the header.

            print(bold, magenta, '\n+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|   1. UNBLOCK ACCOUNT   |   2. CHANGE PASSWORD   |   3. RECOVER USERNAME   |')
            print(bold, magenta, '+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print('|    4. BLOCK ACCOUNT    |    3. CLOSE ACCOUNT    |   6. CHANGE USERNAME    |')
            print(bold, magenta, '+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+')

            user_input = input(">>> ").strip()
            print(end, end='')

            if re.search('^1$', user_input):
                unblock_account()
                continue
            elif re.search('^2$', user_input):
                forgot_password()
                break
            elif re.search('^3$', user_input):
                forgot_username()
                break
            elif re.search('^4$', user_input):
                print(green, '\n:: Log into your Account to Block your Account.')
                time.sleep(3)
                break
            elif re.search('^5$', user_input):
                print(green, '\n:: Log into your Account to Close your Account.')
                time.sleep(3)
                break
            elif re.search('^6$', user_input):
                print(green, "\n:: You can't change your USERNAME after registration.")
                time.sleep(3)
                break
            elif re.search('^.*(back|return).*$', user_input):
                time.sleep(0.5)
                break
            else:
                del user_input
                continue

    except Exception as e:
        # Handle any exceptions by logging the error and navigating back
        log_error(e)
        go_back('script')
