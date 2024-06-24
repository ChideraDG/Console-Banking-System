import re
import time
from bank_processes.authentication import verify_data, Authentication
from banking.main_menu import log_error, go_back, header
from banking.login_panel import forgot_password, forgot_username
from animation.colors import *
from bank_processes.account import Account
from banking.register_panel import countdown_timer


acc = Account()
auth = Authentication()


def unblock_account():
    """
        Unblocks a user's bank account after verifying the account number and user confirmation.

        This function repeatedly prompts the user for their account number and verifies its validity.
        If the account is found to be blocked, it asks for confirmation from the user to unblock it.
    """

    while True:
        header()  # Display the header information

        # Display the unblocking account section title
        print(bold, brt_yellow, "\nUNBLOCK ACCOUNT", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~", sep='')

        # Prompt the user to enter their account number
        print(bold, brt_yellow, "\nEnter your ACCOUNT NUMBER:", end, sep='')
        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~", sep='')

        user_input = input(">>> ").strip()  # Read and strip any leading/trailing whitespace from user input
        print(end, end='')

        # Check if the user wants to go back to the previous menu
        if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
            time.sleep(0.5)
            break
        elif verify_data('account_number', 3, user_input):
            auth.account_number = user_input  # Assign the validated account number to the auth object
            if auth.account_status == 'blocked':  # Check if the account is currently blocked
                recipient_name = auth.account_holder  # Get the account holder's name
                print(bold, red, f'  :: {recipient_name.upper()} ::', end, sep='')  # Display the account holder's name
                print(bold, brt_yellow, '\nconfirm the NAME?', sep='')  # Confirm the account holder's name
                print(f'1. Yes{end}  {bold}{magenta}|{end}  {bold}{brt_yellow}2. No{end}')  # Present Yes/No options
                print(f'{bold}{magenta}~~~~~~     ~~~~~')

                checking_input = input(">>> ").strip()
                print(end, end='')

                # If the user confirms the account holder's name
                if checking_input == '1' or checking_input.lower() == 'yes':
                    del checking_input  # Clear the variable to free up memory
                    print()

                    # Start a countdown timer for unblocking the account
                    countdown_timer('\rUnblocking', _duty='account', countdown=5)
                    auth.unblock_account(account_number=auth.account_number)  # Call the method to unblock the account

                    header()
                    # Confirm the account has been successfully unblocked
                    print(green, '\n:: Your Account has been successfully Unblocked.', end, sep='')
                    time.sleep(3)

                    go_back('script')
                # Check if the user wants to go back to the previous menu
                elif re.search('^.*(back|return).*$', checking_input, re.IGNORECASE):
                    del checking_input  # Clear the variable to free up memory
                    time.sleep(1.5)
                    break
                # If the user indicates the name is incorrect
                elif checking_input == '2' or checking_input.lower() == 'no':
                    del checking_input  # Clear the variable to free up memory
                    time.sleep(2)
                    continue  # Restart the loop to re-prompt for account number
                else:
                    # Handle invalid responses
                    print(red, "\n:: Invalid response. Try Again.", end, sep='')
                    time.sleep(2)
            else:
                # If the account is not blocked, prompt the user to log in
                print(green, "\n:: This Account is not blocked. Try and Log in for confirmation.", end, sep='')
                time.sleep(3)

                go_back('script')  # Go back to the main script/menu
        else:
            # Handle invalid account numbers
            print(red, "\n:: This is an invalid Account Number.", end, sep='')
            time.sleep(3)


def customer_service():
    try:
        while True:
            header()  # Call the header function to display the header.

            print(bold, brt_yellow, "\nWelcome to CONSOLE BETA BANK Customer Service System", end, sep='')
            print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", end, sep='')

            print(bold, magenta, '\n+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|   {bold}{brt_black_bg}{brt_yellow}1. UNBLOCK ACCOUNT{end}   {bold}{magenta}|   {bold}'
                  f'{brt_black_bg}{brt_yellow}2. CHANGE PASSWORD{end}   {bold}{magenta}|   {bold}{brt_black_bg}'
                  f'{brt_yellow}3. RECOVER USERNAME{end}   {bold}{magenta}|')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+')
            print(f'|    {bold}{brt_black_bg}{brt_yellow}4. BLOCK ACCOUNT{end}    {bold}{magenta}|    {bold}'
                  f'{brt_black_bg}{brt_yellow}3. CLOSE ACCOUNT{end}    {bold}{magenta}|   {bold}{brt_black_bg}'
                  f'{brt_yellow}6. CHANGE USERNAME{end}    {bold}{magenta}|')
            print('+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~+')

            user_input = input(">>> ").strip()
            print(end, end='')

            if re.search('^1$', user_input):
                unblock_account()
                continue
            elif re.search('^2$', user_input):
                header()
                forgot_password()
                break
            elif re.search('^3$', user_input):
                header()
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
