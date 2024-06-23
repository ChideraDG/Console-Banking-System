import time
from banking.main_menu import go_back, header, log_error
from bank_processes.authentication import Authentication
from banking.register_panel import countdown_timer
from animation.colors import *


def view_info(auth: Authentication):
    try:
        while True:
            header()
            print()

            countdown_timer('\rGetting your Contact Informations', 'in', countdown=5)

            header()

            auth.get_bvn_verification(auth.user_id)

            print(end='\n\n')
            print(bold, brt_yellow, f'Username         {end}{magenta}::{end}       {green}{auth.username}', end, sep='')
            print(bold, magenta, '~' * len(f'Username         ::       {auth.username}'), sep='', end='\n\n')
            print(bold, brt_yellow, f'Name             {end}{magenta}::{end}       {green}{auth.account_holder}', end, sep='')
            print(bold, magenta, '~' * len(f'Name             ::       {auth.account_holder}'), sep='', end='\n\n')
            print(bold, brt_yellow, f'Bvn              {end}{magenta}::{end}       {green}{auth.bvn_number}', end, sep='')
            print(bold, magenta, '~' * len(f'Bvn              ::       {auth.bvn_number}'), sep='', end='\n\n')
            print(bold, brt_yellow, f'Email            {end}{magenta}::{end}       {green}{auth.email}', end, sep='')
            print(bold, magenta, '~' * len(f'Email            ::       {auth.email}'), sep='', end='\n\n')
            print(bold, brt_yellow, f'Phone Number     {end}{magenta}::{end}       {green}{auth.phone_number}', end, sep='')
            print(bold, magenta, '~' * len(f'Phone Number     ::       {auth.phone_number}'), sep='', end='\n\n')
            print(bold, brt_yellow, f'Address          {end}{magenta}::{end}       {green}{auth.address}', end, sep='')
            print(bold, magenta, '~' * len(f'Address          ::       {auth.address}'), sep='', end='\n\n')

            time.sleep(3)  # Wait for 3 seconds before continuing.

            input("\nTO RETURN -+- PRESS ENTER  ")  # Prompt the user to press Enter to return.
            break

    except Exception as e:
        log_error(e)
        go_back('script')

