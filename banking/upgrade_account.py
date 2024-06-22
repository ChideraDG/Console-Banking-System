import re
import time
from bank_processes.authentication import Authentication
from banking.main_menu import log_error, go_back, header
from animation.colors import *
from banking.register_panel import countdown_timer


def verify_address(auth: Authentication):
    try:
        while True:
            header()
            print(bold, brt_yellow, '\nVERIFY YOUR ADDRESS', end, sep='')
            print(bold, magenta, '~~~~~~~~~~~~~~~~~~~', end, sep='')
            print('# must match your account address')
            time.sleep(2)

            print(bold, brt_yellow, "\nInput your Address:", end, sep='')
            print(bold, magenta, "~~~~~~~~~~~~~~~~~~~", end, sep='')

            print(bold, brt_yellow, end='')
            _address = input(">>> ").strip()
            print(end, end='')

            if re.search('^.*(back|return).*$', _address, re.IGNORECASE):
                return False
            else:
                if auth.address.lower() == _address.lower():
                    return True
                else:
                    print(red, "\n:: The address doesn't match. Try Again", end)
                    time.sleep(3)
                    continue
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)


def by_tier(auth: Authentication):
    try:
        while True:
            header()

            if auth.account_type == 'savings':
                if auth.account_tier == 'Tier 1':

                    print('\n+~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+')
                    print('|   1. to TIER 2   |   2. to TIER 3   |')
                    print('+~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+')
                    user_input = input('>>> ')

                    if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                        break
                    elif re.search('^1$', user_input, re.IGNORECASE):
                        if verify_address(auth):
                            auth.upgrade_tier_limits(
                                account_tier='Tier 2',
                                maximum_balance=5000000,
                                transaction_limit=50,
                                transfer_limit=200000,
                            )

                            countdown_timer(_register='\rUpgrading to', _duty='Tier 2', countdown=5)

                            header()

                            print(green, '\nSuccessfully Upgraded.', end)
                            time.sleep(2)
                            break
                        else:
                            break
                elif auth.account_tier == 'Tier 2':
                    pass
                elif auth.account_tier == 'Tier 3':
                    print(green, '\n:: You have the highest Savings Account banking Tier already.', end)
            elif auth.account_tier == 'current':
                if auth.account_tier == 'Tier 1':

                    break
                elif auth.account_tier == 'Tier 2':
                    pass
                elif auth.account_tier == 'Tier 3':
                    print(green, '\n:: You have the highest Current Account banking Tier already.', end)
            else:
                print(green, '\n:: Meet your Account Officer for this inquiry.', end)
                time.sleep(3)
                break
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)


def by_account_type(auth: Authentication):
    try:
        while True:
            header()

            if auth.account_type == 'saving':

                break
            elif auth.account_tier == 'current':
                pass
            else:
                print(green, '\n:: Meet your Account Officer for this inquiry.', end)
                time.sleep(3)
                break
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
                by_account_type(auth)
                continue
            elif re.search('^2$', user_input, re.IGNORECASE):
                by_tier(auth)
                continue
            else:
                print(red, '\nInvalid input. Try again', end, sep='')
                time.sleep(2)
                continue
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)