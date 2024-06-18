import re
import time

from banking.script import go_back, log_error, header
from bank_processes.notification import Notification
from bank_processes.authentication import Authentication
from animation.colors import *
from banking.register_panel import countdown_timer

notify = Notification()


def fetch_user_loan_data(auth: Authentication):
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
        go_back('script')


def block_user(auth: Authentication):
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
        go_back('script')


def block_account(auth: Authentication):
    while True:
        try:
            header()
            if fetch_user_loan_data(auth):
                if fetch_user_loan_data(auth) == 1:
                    print('You have an outstanding loan!!! Pay back before attempting to block your account!!!')
                    time.sleep(3)
                    break

                elif fetch_user_loan_data(auth) == 3:
                    pass

            else:
                pass
            print(f' {bold}{auth.first_name}')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(f'| {red}This will block your account                                       {end}|')
            print("| You're about to start the process of blocking your bank account.   |")
            print('| You will no longer be able to make transactions.                   |')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(f'| {red}What else should you know                                          {end}|')
            print(f'| You can restore your account if it was accidentally or wrongfully  |')
            print('| blocked.                                                           |')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            block = input(f'{" " * int((70 - 18) / 2)}{red}BLOCK ACCOUNT? y/n>>> {end}').lower()

            if re.search('^.*(back|return|n).*$', block.strip(), re.IGNORECASE):
                break

            elif block == 'y':
                question = input(
                    f'Dear {auth.first_name}, please share with us why you want to block your account>>> ')
                print(f'{auth.first_name}, Console Banking wishes you all the best and we hope you patronize us again')
                time.sleep(3)
                header()
                countdown_timer(_register='\rBlocking Account', _duty='')
                block_user(auth)
                notify.send_notification(
                    title='Account Blocked',
                    message=f'{auth.first_name}, you have successfully blocked your account',
                    channel='block_account'
                )
                header()
                print("\n:: Account blocked successfully, You will be taken to the signup/login page")
                time.sleep(2)
                go_back('script')

        except Exception as e:
            # Log the error to a file and notify the user
            log_error(e)
            go_back('script')
