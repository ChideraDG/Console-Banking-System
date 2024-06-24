import re
import time
from bank_processes.authentication import Authentication
from bank_processes.notification import Notification
from bank_processes.user import User
from banking.update_bvn import first_name, last_name, middle_name, address, phone_number, email, date_of_birth
from banking.main_menu import go_back, header, log_error
from banking.register_panel import countdown_timer
from animation.colors import *


notify = Notification()


def update_acct_info(auth: Authentication):
    """
    Updates the account information for the authenticated user.

    Args:
        auth (Authentication): The authentication object containing user details.
    """

    try:
        changed_object = None

        while True:
            user = User()

            header()  # Display the header.

            print(bold, brt_yellow, '\nWhat do you want to Update?')
            print(magenta, '~~~~~~~~~~~~~~~~~~~~~~~~~~~', sep='')

            print(end='\n')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print(f'|   {brt_black_bg}{brt_yellow}1. FIRST NAME{end}   {bold}{magenta}|  {brt_black_bg}{brt_yellow}2. MIDDLE NAME{end}    {bold}{magenta}|   {brt_black_bg}{brt_yellow}3. LAST NAME{end}   {bold}{magenta}|')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print(f'|   {brt_black_bg}{brt_yellow}4. PHONE NUMBER{end} {bold}{magenta}|  {brt_black_bg}{brt_yellow}5. DATE OF BIRTH{end}  {bold}{magenta}|   {brt_black_bg}{brt_yellow}6. ADDRESS{end}     {bold}{magenta}|')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print(f'|                         {brt_black_bg}{brt_yellow}7. EMAIL{end}                          {bold}{magenta}|')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")

            user_input = input(">>> ").strip()  # Get the user's input for the field to update.
            print(end, end='')

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                # If the user types 'back' or 'return', exit the function.
                break

            elif user_input == '1':
                # Update the first name.
                name = first_name()
                if name == 'break':
                    continue
                else:
                    user.update_personal_info(_column_name='first_name', _data=name, _id_number=auth.user_id)
                    changed_object = 'First Name'
                    break

            elif user_input == '2':
                # Update the middle name.
                name = middle_name()
                if name == 'break':
                    continue
                else:
                    user.update_personal_info(_column_name='middle_name', _data=name, _id_number=auth.user_id)
                    changed_object = 'Middle Name'
                    break

            elif user_input == '3':
                # Update the last name.
                name = last_name()
                if name == 'break':
                    continue
                else:
                    user.update_personal_info(_column_name='last_name', _data=name, _id_number=auth.user_id)
                    changed_object = 'Last Name'
                    break

            elif user_input == '4':
                # Update the phone number.
                number = phone_number()
                if number == 'break':
                    continue
                else:
                    user.update_personal_info(_column_name='phone_number', _data=number, _id_number=auth.user_id)
                    changed_object = 'Phone Number'
                    break

            elif user_input == '5':
                # Update the date of birth.
                dob = date_of_birth()
                countdown_timer('New DOB', 'in')

                header()

                print('\nDate of birth successfully changed')
                time.sleep(2)
                if dob == 'break':
                    continue
                else:
                    user.update_personal_info(_column_name='date_of_birth', _data=dob, _id_number=auth.user_id)
                    changed_object = 'Date of Birth'
                    break

            elif user_input == '6':
                # Update the address.
                _address = address()
                countdown_timer('New Address', 'in')

                header()

                print('\nAddress successfully changed')
                time.sleep(2)
                if _address == 'break':
                    continue
                else:
                    user.update_personal_info(_column_name='address', _data=_address, _id_number=auth.user_id)
                    changed_object = 'Address'
                    break

            elif user_input == '7':
                # Update the email.
                mail = email()
                if mail == 'break':
                    continue
                else:
                    user.update_personal_info(_column_name='email', _data=mail, _id_number=auth.user_id)
                    changed_object = 'Email'
                    break

        if changed_object is not None:
            notify.update_notification(
                title='Console Beta Banking',
                message=f'Your {changed_object} has been changed successfully.',
                channel='personal_info'
            )

    except Exception as e:
        # Log any exceptions that occur and return to the script state.
        log_error(e)
        go_back('script')
