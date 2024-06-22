import time
from banking.main_menu import go_back, header, log_error
from bank_processes.authentication import Authentication
from banking.register_panel import countdown_timer


def view_info(auth: Authentication):
    try:
        while True:
            countdown_timer('User contact info', 'in')
            header()

            auth.get_bvn_verification(auth.user_id)
            f_name = auth.first_name
            m_name = auth.middle_name
            l_name = auth.last_name
            bvn = auth.bvn_number
            username = auth.username
            email = auth.email
            phone_number = auth.phone_number
            address = auth.address

            print(end='\n')
            print(f'First Name              {f_name}\n')
            print(f'Middle Name             {m_name}\n')
            print(f'Last Name               {l_name}\n')
            print(f'Bvn                     {bvn}\n')
            print(f'Username                {username}\n')
            print(f'Email                   {email}\n')
            print(f'Phone Number            {phone_number}\n')
            print(f'Address                 {address}')

    except Exception as e:
        log_error(e)
        go_back('script')

