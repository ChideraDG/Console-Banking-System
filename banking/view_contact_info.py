# username, email, bvn, name, addresses, phone number
from banking.main_menu import go_back, header, log_error
from bank_processes.database import DataBase


def view_info():
    try:
        while True:
            pass

    except Exception as e:
        log_error(e)
        go_back('script')
