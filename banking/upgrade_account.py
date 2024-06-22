import re
import time

from bank_processes.authentication import Authentication
from banking.main_menu import log_error, go_back, header
from animation.colors import *


def by_tier(auth: Authentication):
    try:
        while True:
            header()

            if auth.account_type == 'savings':
                if auth.account_tier == 'Tier 1':
                    print('hi')
                    time.sleep(3)
                    break
                elif auth.account_tier == 'Tier 2':
                    pass
                elif auth.account_tier == 'Tier 3':
                    print(green, '\n:: You have the highest Savings Account banking Tier already.', end)
            elif auth.account_tier == 'current':
                if auth.account_tier == 'Tier 1':
                    print('hi')
                    time.sleep(3)
                    break
                elif auth.account_tier == 'Tier 2':
                    pass
                elif auth.account_tier == 'Tier 3':
                    print(green, '\n:: You have the highest Current Account banking Tier already.', end)
            else:
                print(green, '\n:: Meet your Account Officer for this inquiry.', end)
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)


def by_account_type(auth: Authentication):
    try:
        while True:
            header()

            if auth.account_type == 'savings':
                print('see')
                time.sleep(3)
                break
            elif auth.account_tier == 'current':
                pass
            else:
                print(green, '\n:: Meet your Account Officer for this inquiry.', end)
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)


def upgrade(auth: Authentication):
    try:
        while True:
            header()

            print('\n+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+')
            print('|   1. by ACCOUNT TYPE   |       2. by TIER       |')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+')

            user_input = input('>>> ')

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                break
            elif re.search('^1$', user_input, re.IGNORECASE):
                by_tier(auth)
                continue
            elif re.search('^2$', user_input, re.IGNORECASE):
                by_account_type(auth)
                continue
            else:
                print('Invalid input. Try again\n')
                time.sleep(2)
                continue
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)
