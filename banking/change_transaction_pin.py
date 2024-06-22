import re
import time
from animation.colors import *
from banking.main_menu import go_back, log_error, header
from bank_processes.notification import Notification
from banking.register_panel import countdown_timer
from bank_processes.authentication import Authentication

notify = Notification()


def change_transaction_pin(auth: Authentication):
    """  Function to change a user transaction pin """
    try:
        while True:
            header()
            print(bold, brt_yellow, "\nEnter your old Transaction Pin: ", end, sep='')
            print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "~", end, sep="")
            print(bold, brt_yellow, "\nEnter old Transaction Pin:", end, sep='')

            print(bold, brt_yellow, end='')

            user_input = input(">>> ").strip()
            time.sleep(1)
            if re.search('^.*(back|return|n).*$', user_input, re.IGNORECASE):
                time.sleep(1)
                break
            else:
                if user_input == auth.transaction_pin:
                    while True:
                        header()
                        print(bold, brt_yellow, "\nEnter your new Transaction Pin: ", end, sep='')
                        print(bold, magenta, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "~", end, sep="")
                        print(bold, brt_yellow, "\nEnter new Transaction Pin:", end, sep='')

                        print(bold, brt_yellow, end='')
                        new_pin = input(">>> ").strip()
                        time.sleep(1)
                        if re.search('^.*(back|return|n).*$', new_pin, re.IGNORECASE):
                            time.sleep(1)
                            break

                        if re.search(r"^\d{4}$", new_pin):

                            print(bold, brt_yellow, "\nConfirm new Transaction Pin:", end, sep='')
                            print(bold, brt_yellow, end='')
                            confirm_pin = input(">>> ")
                            time.sleep(1)
                            print(end, end='')
                            if confirm_pin == new_pin:
                                header()
                                countdown_timer(_register='\rChanging Transaction Pin', _duty='')
                                query = f""" UPDATE   {auth.database.db_tables[3]}
                                        SET transaction_pin = '{confirm_pin}'
                                        WHERE account_number = '{auth.account_number}' 
                                        """
                                auth.database.query(query)

                                notify.send_notification(
                                    title='Console Beta Banking',
                                    message=f'{auth.account_holder}, you have successfully changed your transaction pin.',
                                    channel='changed transaction pin'
                                )

                                header()
                                print("\n:: Transaction Pin changed successfully")
                                time.sleep(2)
                                go_back('signed_in', auth=auth)

                            else:
                                print("\n:: Transaction Pin does not match!!!")
                                time.sleep(2)
                                continue
                        else:
                            print(red, "\n:: Transaction Pin must be only 4 digits.", end, sep='')
                            time.sleep(2)
                            continue
                else:
                    print(f'\n:: Wrong Transaction Pin!!! Try again!!!')
                    time.sleep(2)
                    continue

    except Exception as e:
        # Log the error to a file and notify the user
        log_error(e)
        go_back('signed_in', auth=auth)
