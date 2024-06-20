from bank_processes.authentication import Authentication
from banking.main_menu import log_error, go_back


def upgrade(auth: Authentication):
    try:
        pass
    except Exception as e:
        log_error(e)
        go_back('signed_in', auth=auth)
