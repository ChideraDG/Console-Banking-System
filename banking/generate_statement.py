from banking.script import header, log_error, go_back


def generate_statement():
    try:
        while True:
            header()
    except Exception as e:
        log_error(e)
        go_back('script')
