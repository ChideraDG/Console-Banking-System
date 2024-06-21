import re
import time
from banking.update_bvn import first_name, last_name, middle_name, address, phone_number, email, date_of_birth
from banking.main_menu import go_back, header, log_error
from banking.register_panel import countdown_timer


def update_acct_info():
    try:
        while True:
            header()

            print('\nEnter do you what to Update?')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

            print(end='\n')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print('|   1. FIRST NAME   |   2. MIDDLE NAME   |   3. LAST NAME   |')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print('|  4. PHONE NUMBER  |  5. DATE OF BIRTH  |   6. ADDRESS     |')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")
            print('|                    7. EMAIL                               |')
            print("+~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~+")

            user_input = input(">>> ").strip()

            if re.search('^.*(back|return).*$', user_input, re.IGNORECASE):
                break

            elif user_input == '1':
                name = first_name()
                if name == 'break':
                    continue

            elif user_input == '2':
                name = middle_name()
                if name == 'break':
                    continue

            elif user_input == '3':
                name = last_name()
                if name == 'break':
                    continue

            elif user_input == '4':
                number = phone_number()
                if number == 'break':
                    continue

            elif user_input == '5':
                dob = date_of_birth()
                countdown_timer('New DOB', 'in')
                header()
                print('\nDate of birth successfully changed')
                time.sleep(2)
                if dob == 'break':
                    continue

            elif user_input == '6':
                _address = address()
                countdown_timer('New Address', 'in')
                header()
                print('\nAddress successfully changed')
                time.sleep(2)
                if _address == 'break':
                    continue

            elif user_input == '7':
                mail = email()
                if mail == 'break':
                    continue

    except Exception as e:
        log_error(e)
        go_back('script')


# update_acct_info()
