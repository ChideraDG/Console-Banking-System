import re
import time
from banking.main_menu import go_back, log_error, header
from bank_processes.notification import Notification
from bank_processes.authentication import Authentication
from animation.colors import *
from banking.register_panel import countdown_timer
from banking.block_account import fetch_user_loan_data

notify = Notification()


def delete_records(table, criteria, criteria_value, auth: Authentication, data_filter=''):
    try:
        query = f"""DELETE FROM {auth.database.db_tables[table]}
                WHERE {criteria} = '{criteria_value}'
                {data_filter}
        """
        auth.database.query(query)

    except Exception as e:
        # Log the error to a file and notify the user
        log_error(e)
        go_back('script')


def delete_beneficiary(auth: Authentication):
    import json
    query = f"""SELECT account_id, beneficiaries from {auth.database.db_tables[3]}"""
    beneficiary_list = []
    new_beneficiary_list = []
    total_query = auth.database.fetch_data(query)
    account_id = tuple(val[0] for val in total_query)
    beneficiaries_query = tuple(val[1] for val in total_query)

    for beneficiary in beneficiaries_query:
        bene = json.loads(beneficiary)
        beneficiary_list.append(bene)

    for beneficiary in beneficiary_list:
        for val in list(beneficiary):
            if beneficiary.get(val)[0] == auth.account_number:
                del beneficiary[val]
        beneficiary = str(beneficiary).replace("'", '"')
        new_beneficiary_list.append(beneficiary)

    row_no = 0
    while row_no < len(account_id):
        update_query = f"""UPDATE {auth.database.db_tables[3]}
                        SET beneficiaries = '{new_beneficiary_list[row_no]}'
                        WHERE account_id = {account_id[row_no]}
                    """
        auth.database.query(update_query)
        row_no += 1


def delete_account_and_fixed_deposit_record(auth: Authentication):
    tables = [3, 4]
    for value in tables:
        delete_records(table=value,
                       criteria='account_number',
                       criteria_value=auth.account_number,
                       auth=auth
                       )


def delete_bvn_and_user_record(auth: Authentication):
    tables = [0, 1]
    for value in tables:
        delete_records(table=value,
                       criteria='phone_number',
                       criteria_value=auth.phone_number,
                       auth=auth
                       )


def delete_loan_records(auth: Authentication):
    loan_tables = [7, 6]
    auth.loan.email = auth.email
    for loan in loan_tables:
        delete_records(table=loan,
                       criteria='user_id',
                       criteria_value=auth.loan.user_id,
                       auth=auth
                       )


def delete_transaction_table(auth: Authentication):
    data_filter = f"AND transaction_mode = 'debit'"
    delete_records(table=2,
                   criteria='sender_account_number',
                   criteria_value=auth.account_number,
                   auth=auth,
                   data_filter=data_filter
                   )

    data_filter = f"AND transaction_mode = 'credit' "
    delete_records(table=2,
                   criteria='receiver_account_number',
                   criteria_value=auth.account_number,
                   auth=auth,
                   data_filter=data_filter
                   )


def delete_all_records(auth: Authentication):
    delete_account_and_fixed_deposit_record(auth)
    delete_beneficiary(auth)
    delete_bvn_and_user_record(auth)
    delete_loan_records(auth)
    delete_transaction_table(auth)


def close_account(auth: Authentication):
    while True:
        try:
            header()
            # Checking if the user has collected a loan before
            if fetch_user_loan_data(auth):
                # Checking if user has any outstanding loan or not. If any, user is prompted to pay before proceeding
                if fetch_user_loan_data(auth) == 1:
                    print('\n:: You have an outstanding loan!!! \n'
                          ':: Pay back before attempting to close your account!!!')
                    time.sleep(3)
                    break

                elif fetch_user_loan_data(auth) == 3:
                    pass

            # Printing closing account confirmation and instructions
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'| {red}{bold}You are about to close your account permanently                    {end}|')
            print("| You're about to start the process of closing your bank account.    |")
            print('| You will no longer be able to make transactions of any form        |')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'| {red}{bold}What else should you know                                          {end}|')
            print('| Once your account is closed, you will not be able to access it     |')
            print('| again, as all your records will be permanently deleted.            |')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+')
            close = input(f'{red}{bold}CLOSE ACCOUNT? y/n \n>>> {end}').lower()

            # Handling user input for cancelling the process
            if re.search('^.*(back|return|n).*$', close.strip(), re.IGNORECASE):
                time.sleep(1)
                break

            elif close == 'y' or 'yes':
                # Asking user for reason and proceeding with closing of account
                question = input(
                    f'\nDear {auth.first_name}, please share with us why you want to close your account \n>>> ')

                print(f'\n{auth.account_holder}, '
                      f'Console Banking wishes you all the best and we hope you open an account with us again')

                time.sleep(5)

                header()

                countdown_timer(_register='\rClosing Account', _duty='')

                delete_all_records(auth)

                # Sending notification that the user account has been closed
                notify.send_notification(
                    title='Console Beta Banking',
                    message=f'{auth.account_holder}, you have successfully closed your account.',
                    channel='close_account'
                )

                header()

                print("\n:: Account closed successfully, You will be taken to the signup/login page")
                time.sleep(2)

                # Go back to the signup/login page
                go_back('script')

        except Exception as e:
            # Log the error to a file and notify the user
            log_error(e)
            go_back('script')
