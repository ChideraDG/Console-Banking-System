import re
import time
from banking.main_menu import go_back, log_error, header
from bank_processes.notification import Notification
from bank_processes.authentication import Authentication
from animation.colors import *
from banking.register_panel import countdown_timer
from banking.block_account import fetch_user_loan_data

notify = Notification()


def delete_records(table, column, column_value, auth: Authentication, data_filter=''):
    """ Deletes records from a table based on a criteria and value

     Parameters
    ----------
    auth : Authentication
        An instance of the Authentication class that contains user authentication and transaction details.

    table: The table which one wants to delete a record from

    column:  The column which the user wants the use as a criteria  to delete records

    column_value: The value in a particular column that the user wants to use as a reference point to delete from

    data_filter :  This serves as an optional query in case the user wants to add another condition to the query
    """

    try:
        query = f"""DELETE FROM {auth.database.db_tables[table]}
                WHERE {column} = '{column_value}'
                {data_filter}
        """
        auth.database.query(query)

    except Exception as e:
        # Log the error to a file and notify the user
        log_error(e)
        go_back('script')


def delete_beneficiary(auth: Authentication):
    """ Function to delete users from any beneficiaries they may be in"""

    import json
    # Query to get all the account ids and beneficiaries from the account table
    query = f"""SELECT account_id, beneficiaries from {auth.database.db_tables[3]}"""
    # Initialize two empty lists
    beneficiary_list = []
    new_beneficiary_list = []
    # Fetch the query
    total_query = auth.database.fetch_data(query)

    # Store the account id in a separate tuple
    account_id = tuple(val[0] for val in total_query)
    # Store the beneficiaries in a separate tuple
    beneficiaries_query = tuple(val[1] for val in total_query)

    for beneficiary in beneficiaries_query:
        # Converting the obtained beneficiaries from string type to dictionary type
        bene = json.loads(beneficiary)
        # Appending the converted beneficiaries to the empty beneficiary list
        beneficiary_list.append(bene)

    for beneficiary in beneficiary_list:
        # A list is used to ensure that the size of the dictionary is maintained to prevent errors due to size change
        for val in list(beneficiary):
            # Check if a user account number is found within any of the beneficiaries and then deleting it if present
            if beneficiary.get(val)[0] == auth.account_number:
                del beneficiary[val]
        # Each beneficiary is then converted back to string type
        beneficiary = str(beneficiary).replace("'", '"')
        new_beneficiary_list.append(beneficiary)

    # Updating the beneficiaries column
    row_no = 0
    while row_no < len(account_id):
        update_query = f"""UPDATE {auth.database.db_tables[3]}
                        SET beneficiaries = '{new_beneficiary_list[row_no]}'
                        WHERE account_id = {account_id[row_no]}
                    """
        auth.database.query(update_query)
        row_no += 1


def delete_all_records(auth: Authentication):
    """ Function to delete user records from all the tables """

    # Delete user record from the account and fixed deposit table
    tables = [3, 4]
    for value in tables:
        delete_records(table=value,
                       column='account_number',
                       column_value=auth.account_number,
                       auth=auth
                       )

    # Delete from the beneficiary column in the account table where user is a beneficiary
    delete_beneficiary(auth)

    # Delete user record from the bvn and user table
    tables = [0, 1]
    for value in tables:
        delete_records(table=value,
                       column='phone_number',
                       column_value=auth.phone_number,
                       auth=auth
                       )

    # Delete user records from the transaction table where user is on the sending end
    data_filter = f"AND transaction_mode = 'debit'"
    delete_records(table=2,
                   column='sender_account_number',
                   column_value=auth.account_number,
                   auth=auth,
                   data_filter=data_filter
                   )
    # Delete user records from the transaction table where user is on the receiving end
    data_filter = f"AND transaction_mode = 'credit' "
    delete_records(table=2,
                   column='receiver_account_number',
                   column_value=auth.account_number,
                   auth=auth,
                   data_filter=data_filter
                   )

    # Delete user records from the loan tables
    loan_tables = [7, 6]
    auth.loan.email = auth.email
    for loan in loan_tables:
        delete_records(table=loan,
                       column='user_id',
                       column_value=auth.loan.user_id,
                       auth=auth
                       )


def close_account(auth: Authentication):
    """ Function that initiates the process of closing a user account """

    while True:
        try:
            header()
            # Checking if the user has collected a loan before
            if fetch_user_loan_data(auth):
                # Checking if user has any outstanding loan or not. If any, user is prompted to pay before proceeding
                if fetch_user_loan_data(auth) == 1:
                    print(red, '\n:: You have an outstanding loan!!! \n'
                          ':: Pay back before attempting to close your account!!!', end)
                    time.sleep(3)
                    break

                elif fetch_user_loan_data(auth) == 3:
                    pass

            # Printing closing account confirmation and instructions
            top_borders = f'{bold}{magenta}+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+{end}'
            print(f'\n{top_borders}')
            print(f'{bold}{magenta}| {red}{bold}You are about to close your account permanently{end}                    {bold}{magenta}|')
            print(f"| {bold}{brt_black_bg}{brt_yellow}You're about to start the process of closing your bank account.{end}    {bold}{magenta}|")
            print(f'| {bold}{brt_black_bg}{brt_yellow}You will no longer be able to make transactions of any form{end}        {bold}{magenta}|')
            print(top_borders)
            print(f'{bold}{magenta}| {red}{bold}What else should you know{end}                                          {bold}{magenta}|')
            print(f'| {bold}{brt_black_bg}{brt_yellow}Once your account is closed, you will not be able to access it{end}     {bold}{magenta}|')
            print(f'| {bold}{brt_black_bg}{brt_yellow}again, as all your records will be permanently deleted.{end}            {bold}{magenta}|')
            print(top_borders)
            close = input(f'{red}{bold}CLOSE ACCOUNT? y/n \n>>> {end}').lower().strip()

            # Handling user input for cancelling the process
            if re.search('^.*(back|return|n|no).*$', close, re.IGNORECASE):
                time.sleep(1)
                break

            elif close == 'y' or close == 'yes':
                # Asking user for reason and proceeding with closing of account
                question = input(
                    f'{bold}{brt_yellow}\nDear {auth.first_name}, please share with us why you want to close your account{bold}{brt_yellow} \n{magenta}>>> ')

                print(f'{end}{bold}{brt_yellow}\n{auth.account_holder}, '
                      f'Console Banking wishes you all the best and we hope you open an account with us again{end}')

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

                print(green, "\n:: Account closed successfully, You will be taken to the signup/login page", end)
                time.sleep(2)

                # Go back to the signup/login page
                go_back('script', auth=auth)

            else:
                print(red, f"\n:: Wrong Input", end)
                time.sleep(1.5)
                continue

        except Exception as e:
            # Log the error to a file and notify the user
            log_error(e)
            go_back('signed_in', auth=auth)
