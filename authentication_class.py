class Authentication:

    def __int__(self, username, password, token_num, auth_attempts, time_stamp, user_identifier, outcome,
                failed_login_attempts, auth_token):

        self.username = username
        self.password = password
        self.token_num = token_num
        self.auth_attempts = auth_attempts
        self.time_stamp = time_stamp
        self.user_identifier = user_identifier
        self.outcome = outcome
        self.failed_login_attempts = failed_login_attempts
        self.auth_token = auth_token
        