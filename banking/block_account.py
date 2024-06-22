import re
import time
from banking.main_menu import go_back, log_error, header
from bank_processes.notification import Notification
from bank_processes.authentication import Authentication
from animation.colors import *
from banking.register_panel import countdown_timer

notify = Notification()


def fetch_user_loan_data(auth: Authentication):
    """
    Handles the process of fetching the loan data of a user

    Parameters
    ----------
    auth : Authentication
        An instance of the Authentication class that contains user authentication and transaction details.

   Raises
    ------
    Exception:
        If any unexpected error occurs during the withdrawal process.
    """
    try:
        auth.loan.email = auth.email

        if auth.loan.user_id is not None:
            query = f"""
            SELECT status_id 
            FROM {auth.database.db_tables[7]}
            WHERE user_id = {auth.loan.user_id} 
            """
            user_loan = auth.database.fetch_data(query)
            for value in user_loan:
                for data in value:
                    return data

    except Exception as e:
        # Log the error to a file and notify the user
        log_error(e)
        go_back('signed_in', auth=auth)


def block_user(auth: Authentication):
    """
    Handles the operation of blocking a user account

    Parameters
    ----------
    auth : Authentication
        An instance of the Authentication class that contains user authentication and transaction details.

     Raises
    ------
    Exception:
        If any unexpected error occurs during the withdrawal process.
    """

    try:
        block_user_account = f"""
                            UPDATE {auth.database.db_tables[3]}
                            SET account_status = 'blocked'
                            WHERE account_number = '{auth.account_number}'
                            """
        auth.database.query(block_user_account)

    except Exception as e:
        # Log the error to a file and notify the user
        log_error(e)
        go_back('signed_in', auth=auth)


def block_account(auth: Authentication):
    """
    Initiates the process of blocking a user account and checks if he or she is eligible

    Parameters
    ----------
    auth : Authentication
        An instance of the Authentication class that contains user authentication and transaction details.

    Raises
    ------
    Exception:
        If any unexpected error occurs during the withdrawal process.
    """
    while True:
        try:
            header()

            # Checking if the user has collected a loan before
            if fetch_user_loan_data(auth):
                # Checking if user has any outstanding loan or not. If any, user is prompted to pay before proceeding
                if fetch_user_loan_data(auth) == 1:
                    print('\n:: You have an outstanding loan!!! \n'
                          ':: Pay back before attempting to block your account!!!')
                    time.sleep(3)
                    break

                elif fetch_user_loan_data(auth) == 3:
                    pass

            # Printing blocking confirmation and instructions
            print(f'\n {bold}{auth.account_holder}')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'| {red}This will block your account                                       {end}|')
            print("| You're about to start the process of blocking your bank account.   |")
            print('| You will no longer be able to make transactions.                   |')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'| {red}What else should you know                                          {end}|')
            print('| You can restore your account if it was accidentally or wrongfully  |')
            print('| blocked.                                                           |')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')

            # Prompting user to confirm account blocking
            block = input(f'{red}BLOCK ACCOUNT? y/n \n>>> {end}').lower()

            # Handling user input for cancelling the process
            if re.search('^.*(back|return|n).*$', block.strip(), re.IGNORECASE):
                time.sleep(1)
                break

            elif block == 'y' or block == 'yes':
                # Asking user for reason and proceeding with blocking
                question = input(
                    f'\nDear {auth.first_name}, please share with us why you want to block your account \n>>> ')

                print(f'\n{auth.account_holder}, '
                      f'Console Banking wishes you all the best and we hope you patronize us again')
                time.sleep(5)

                header()

                countdown_timer(_register='\rBlocking Account', _duty='')

                auth.block_account()

                # Sending notification that the user account has been blocked
                notify.send_notification(
                    title='Console Beta Banking',
                    message=f'{auth.account_holder}, you have successfully blocked your account.',
                    channel='block_account'
                )

                header()

                print("\n:: Account blocked successfully, You will be taken to the signup/login page")
                time.sleep(2)

                # Go back to the signup/login page
                go_back('script', auth=auth)

            else:
                print(f"\n:: Wrong Input")
                time.sleep(1.5)
                continue

        except Exception as e:
            # Log the error to a file and notify the user
            log_error(e)
            go_back('signed_in', auth=auth)
