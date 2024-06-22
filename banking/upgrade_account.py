import re
import time
from bank_processes.authentication import Authentication
from banking.main_menu import log_error, go_back, header
from animation.colors import *
from banking.register_panel import countdown_timer


def verify_address(auth: Authentication):
    """
    Verify the user's address.

    Parameters
    ----------
    auth : Authentication
        An instance of the Authentication class used to authenticate the user.

    Returns
    -------
    bool
        True if the address is verified successfully, False if the user decides to return.

    Notes
    -----
    This function prompts the user to input their address and checks if it matches the account address.
    """
    try:
        while True:
            header()  # Display the header.
            print(bold, brt_yellow, '\nVERIFY YOUR ADDRESS', end, sep='')
            print(bold, magenta, '~~~~~~~~~~~~~~~~~~~', end, sep='')
            print('# must match your account address')
            time.sleep(2)

            print(bold, brt_yellow, "\nInput your Address:", end, sep='')
            print(bold, magenta, "~~~~~~~~~~~~~~~~~~~", end, sep='')

            print(bold, brt_yellow, end='')
            _address = input(">>> ").strip()  # Get the user's address input.
            print(end, end='')

            if re.search('^.*(back|return).*$', _address, re.IGNORECASE):
                # If the user types 'back' or 'return', exit the function and return False.
                return False
            else:
                if auth.address.lower() == _address.lower():
                    # If the input address matches the account address, return True.
                    return True
                else:
                    # If the address does not match, notify the user and prompt again.
                    print(red, "\n:: The address doesn't match. Try Again", end)
                    time.sleep(3)
                    continue
    except Exception as e:
        log_error(e)  # Log any exceptions that occur.
        go_back('signed_in', auth=auth)  # Return to the signed-in state.


def verify_bvn(auth: Authentication):
    """
    Verify the user's BVN (Bank Verification Number).

    Parameters
    ----------
    auth : Authentication
        An instance of the Authentication class used to authenticate the user.

    Returns
    -------
    bool
        True if the BVN is verified successfully, False if the user decides to return.

    Notes
    -----
    This function prompts the user to input their BVN and checks if it matches the account BVN.
    """
    try:
        while True:
            header()  # Display the header.
            print(bold, brt_yellow, '\nVERIFY YOUR BVN', end, sep='')
            print(bold, magenta, '~~~~~~~~~~~~~~~', end, sep='')
            print('# must match your BVN detail')
            time.sleep(2)

            print(bold, brt_yellow, "\nInput your BVN:", end, sep='')
            print(bold, magenta, "~~~~~~~~~~~~~~~", end, sep='')

            print(bold, brt_yellow, end='')
            bvn = input(">>> ").strip()  # Get the user's BVN input.
            print(end, end='')

            if re.search('^.*(back|return).*$', bvn, re.IGNORECASE):
                # If the user types 'back' or 'return', exit the function and return False.
                return False
            else:
                auth.get_bvn_verification(auth.user_id)  # Verify the BVN from the authentication system.
                if auth.bvn_number.lower() == bvn.lower():
                    # If the input BVN matches the account BVN, return True.
                    return True
                else:
                    # If the BVN does not match, notify the user and prompt again.
                    print(red, "\n:: The BVN doesn't match. Try Again", end)
                    time.sleep(3)
                    continue
    except Exception as e:
        log_error(e)  # Log any exceptions that occur.
        go_back('signed_in', auth=auth)  # Return to the signed-in state.


def by_tier(auth: Authentication):
    """
    Upgrade the user's account tier.

    Parameters
    ----------
    auth : Authentication
        An instance of the Authentication class used to authenticate the user.

    Notes
    -----
    This function allows the user to upgrade their account tier based on the current tier.
    """
    try:
        while True:
            header()  # Display the header.

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
                    elif re.search('^2$', user_input, re.IGNORECASE):
                        if verify_address(auth):
                            if verify_bvn(auth):
                                auth.upgrade_tier_limits(
                                    account_tier='Tier 3',
                                    maximum_balance=25000000,
                                    transaction_limit=100,
                                    transfer_limit=5000000,
                                )

                            countdown_timer(_register='\rUpgrading to', _duty='Tier 3', countdown=5)

                            header()

                            print(green, '\nSuccessfully Upgraded.', end)
                            time.sleep(2)
                            break
                        else:
                            break
                    else:
                        print(red, '\nInvalid input. Try again', end, sep='')
                        time.sleep(2)
                        continue
                elif auth.account_tier == 'Tier 2':
                    print('\n+~~~~~~~~~~~~~~~~~~+')
                    print('|   1. to TIER 3   |')
                    print('+~~~~~~~~~~~~~~~~~~+')

                    user_input = input('>>> ')

                    if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                        break
                    elif re.search('^1$', user_input, re.IGNORECASE):
                        if verify_address(auth):
                            if verify_bvn(auth):
                                auth.upgrade_tier_limits(
                                    account_tier='Tier 3',
                                    maximum_balance=25000000,
                                    transaction_limit=100,
                                    transfer_limit=5000000,
                                )

                            countdown_timer(_register='\rUpgrading to', _duty='Tier 3', countdown=5)

                            header()

                            print(green, '\nSuccessfully Upgraded.', end)
                            time.sleep(2)
                            break
                        else:
                            break
                    else:
                        print(red, '\nInvalid input. Try again', end, sep='')
                        time.sleep(2)
                        continue
                elif auth.account_tier == 'Tier 3':
                    print(green, '\n:: You have the highest Savings Account banking Tier already.', end)
                    time.sleep(3)
                    break
            elif auth.account_tier == 'current':
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
                                maximum_balance=30000000,
                                transaction_limit=80,
                                transfer_limit=5000000,
                            )

                            countdown_timer(_register='\rUpgrading to', _duty='Tier 2', countdown=5)

                            header()

                            print(green, '\nSuccessfully Upgraded.', end)
                            time.sleep(2)
                            break
                        else:
                            break
                    elif re.search('^2$', user_input, re.IGNORECASE):
                        if verify_address(auth):
                            if verify_bvn(auth):
                                auth.upgrade_tier_limits(
                                    account_tier='Tier 3',
                                    maximum_balance=500000000,
                                    transaction_limit=140,
                                    transfer_limit=80000000,
                                )

                            countdown_timer(_register='\rUpgrading to', _duty='Tier 3', countdown=5)

                            header()

                            print(green, '\nSuccessfully Upgraded.', end)
                            time.sleep(2)
                            break
                        else:
                            break
                    else:
                        print(red, '\nInvalid input. Try again', end, sep='')
                        time.sleep(2)
                        continue
                elif auth.account_tier == 'Tier 2':
                    print('\n+~~~~~~~~~~~~~~~~~~+')
                    print('|   1. to TIER 3   |')
                    print('+~~~~~~~~~~~~~~~~~~+')

                    user_input = input('>>> ')

                    if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                        break
                    elif re.search('^1$', user_input, re.IGNORECASE):
                        if verify_address(auth):
                            if verify_bvn(auth):
                                auth.upgrade_tier_limits(
                                    account_tier='Tier 3',
                                    maximum_balance=500000000,
                                    transaction_limit=140,
                                    transfer_limit=80000000,
                                )

                            countdown_timer(_register='\rUpgrading to', _duty='Tier 3', countdown=5)

                            header()

                            print(green, '\nSuccessfully Upgraded.', end)
                            time.sleep(2)
                            break
                        else:
                            break
                    else:
                        print(red, '\nInvalid input. Try again', end, sep='')
                        time.sleep(2)
                        continue
                elif auth.account_tier == 'Tier 3':
                    print(green, '\n:: You have the highest Current Account banking Tier already.', end)
                    time.sleep(3)
                    break
            else:
                print(green, '\n:: Meet your Account Officer for this inquiry.', end)
                time.sleep(3)
                break
    except Exception as e:
        log_error(e)  # Log any exceptions that occur.
        go_back('signed_in', auth=auth)  # Return to the signed-in state.


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
