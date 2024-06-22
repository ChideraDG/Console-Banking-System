import re
import time

from bank_processes.authentication import Authentication
from bank_processes.user import User
from banking.update_bvn import first_name, last_name, middle_name, address, phone_number, email, date_of_birth
from banking.main_menu import go_back, header, log_error
from banking.register_panel import countdown_timer


def update_acct_info(auth: Authentication):
    try:
        while True:
            user = User()

            header()

            print('\nEnter do you what to Update?')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

            print(end='\n')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print('|   1. FIRST NAME   |  2. MIDDLE NAME    |   3. LAST NAME   |')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print('|   4. PHONE NUMBER |  5. DATE OF BIRTH  |   6. ADDRESS     |')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print('|                      7. EMAIL                             |')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")

            user_input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                break

            elif user_input == '1':
                name = first_name()
                if name == 'break':
                    continue

                else:
                    user.update_personal_info(_column_name='first_name', _data=name, _id_number=auth.user_id)
                    time.sleep(1.5)
                    break

            elif user_input == '2':
                name = middle_name()
                if name == 'break':
                    continue

                else:
                    user.update_personal_info(_column_name='middle_name', _data=name, _id_number=auth.user_id)
                    time.sleep(1.5)
                    break

            elif user_input == '3':
                name = last_name()
                if name == 'break':
                    continue

                else:
                    user.update_personal_info(_column_name='last_name', _data=name, _id_number=auth.user_id)
                    time.sleep(1.5)
                    break

            elif user_input == '4':
                number = phone_number()
                if number == 'break':
                    continue

                else:
                    user.update_personal_info(_column_name='phone_number', _data=number, _id_number=auth.user_id)
                    time.sleep(1.5)
                    break

            elif user_input == '5':
                dob = date_of_birth()
                countdown_timer('New DOB', 'in')
                header()
                print('\nDate of birth successfully changed')
                time.sleep(2)
                if dob == 'break':
                    continue

                else:
                    user.update_personal_info(_column_name='date_of_birth', _data=dob, _id_number=auth.user_id)
                    time.sleep(1.5)
                    break

            elif user_input == '6':
                _address = address()
                countdown_timer('New Address', 'in')
                header()
                print('\nAddress successfully changed')
                time.sleep(2)
                if _address == 'break':
                    continue

                else:
                    user.update_personal_info(_column_name='address', _data=_address, _id_number=auth.user_id)
                    time.sleep(1.5)
                    break

            elif user_input == '7':
                mail = email()
                if mail == 'break':
                    continue

                else:
                    user.update_personal_info(_column_name='email', _data=mail, _id_number=auth.user_id)
                    time.sleep(1.5)
                    break

    except Exception as e:
        log_error(e)
        go_back('script')


# update_acct_info()
