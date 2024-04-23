class Authentication:

    def __int__(self, username: str = None, password: str = None, token_num: str = None, auth_attempts: int = None,
                time_stamp: str = None, user_identifier: str = None , outcome: str = None,
                failed_login_attempts: int = None, auth_token: str = None):

        self.username = username
        self.password = password
        self.token_num = token_num
        self.auth_attempts = auth_attempts
        self.time_stamp = time_stamp
        self.user_identifier = user_identifier
        self.outcome = outcome
        self.failed_login_attempts = failed_login_attempts
        self.auth_token = auth_token
        