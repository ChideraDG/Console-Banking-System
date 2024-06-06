import pymysql as sql

connection = sql.connect(
    host='localhost',
    user='root',
    password='',
    database=''
)

_cursor = connection.cursor()

query0 = """
CREATE DATABASE IF NOT EXISTS bankApp_db
"""

_cursor.execute(query0)

connection = sql.connect(
    host='localhost',
    user='root',
    password='',
    database='bankApp_db'
)

my_cursor = connection.cursor()

queries = [
    """
    CREATE TABLE IF NOT EXISTS `Account` (
    `account_id` int(11) NOT NULL AUTO_INCREMENT,
    `account_number` varchar(10) NOT NULL,
    `account_type` varchar(15) NOT NULL,
    `account_holder` varchar(70) NOT NULL,
    `account_balance` decimal(30,3) NOT NULL,
    `minimum_balance` decimal(30,3) NOT NULL,
    `maximum_balance` decimal(30,3) NOT NULL,
    `account_fee` decimal(30,3) NOT NULL,
    `transaction_pin` varchar(4) NOT NULL,
    `account_status` varchar(10) NOT NULL,
    `account_tier` varchar(10) NOT NULL,
    `overdraft_protection` enum('yes','no') NOT NULL,
    `transaction_limit` int(11) NOT NULL,
    `transfer_limit` decimal(30,3) NOT NULL,
    `beneficiaries` text NOT NULL DEFAULT '{}',
    `fixed_account` varchar(5) NOT NULL DEFAULT 'no',
    PRIMARY KEY (`account_id`),
    UNIQUE KEY `account_number` (`account_number`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=2;
    """,
    """
    CREATE TABLE IF NOT EXISTS `Bank_Verification_Number` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `first_name` varchar(50) NOT NULL,
    `middle_name` varchar(50) NOT NULL,
    `last_name` varchar(50) NOT NULL,
    `gender` varchar(10) NOT NULL,
    `address` varchar(100) NOT NULL,
    `phone_number` varchar(16) NOT NULL,
    `date_of_birth` date NOT NULL,
    `nationality` varchar(20) NOT NULL,
    `email` varchar(50) NOT NULL,
    `bvn_number` varchar(12) NOT NULL,
    `created_date` datetime NOT NULL,
    `last_updated` datetime NOT NULL,
    `bvn_status` varchar(20) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `phone_number` (`phone_number`),
    UNIQUE KEY `email` (`email`),
    UNIQUE KEY `bvn_number` (`bvn_number`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=2;
    """,
    """
    CREATE TABLE IF NOT EXISTS `Transaction` (
    `transaction_id` varchar(35) NOT NULL,
    `transaction_type` varchar(15) NOT NULL,
    `transaction_amount` decimal(30,3) NOT NULL,
    `sender_account_number` varchar(10) NOT NULL,
    `sender_name` varchar(50) NOT NULL,
    `receiver_account_number` varchar(10) DEFAULT NULL,
    `receiver_name` varchar(50) DEFAULT NULL,
    `transaction_date_time` datetime NOT NULL,
    `description` text NOT NULL,
    `status` enum('successful','failed') NOT NULL,
    `account_type` varchar(15) NOT NULL,
    `account_balance` decimal(30,3) NOT NULL,
    `transaction_mode` varchar(10) NOT NULL,
    PRIMARY KEY (`transaction_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=2;
    """,
    """
    CREATE TABLE IF NOT EXISTS `User` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(20) NOT NULL,
    `password` varchar(20) NOT NULL,
    `first_name` varchar(20) NOT NULL,
    `middle_name` varchar(20) NOT NULL,
    `last_name` varchar(20) NOT NULL,
    `gender` varchar(10) NOT NULL,
    `email` varchar(50) NOT NULL,
    `phone_number` varchar(15) NOT NULL,
    `address` varchar(100) NOT NULL,
    `date_of_birth` date NOT NULL,
    `linked_accounts` varchar(100) NOT NULL,
    `last_login_timestamp` datetime NOT NULL,
    `account_open_date` datetime NOT NULL,
    `account_close_date` datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`),
    UNIQUE KEY `phone_number` (`phone_number`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=2;
    """,
    """
    CREATE TABLE IF NOT EXISTS `Fixed_Deposit` (
    `deposit_id` varchar(15) NOT NULL,
    `account_number` varchar(11) NOT NULL,
    `deposit_title` varchar(30) DEFAULT NULL,
    `initial_deposit` decimal(30,3) NOT NULL,
    `interest_rate` varchar(10) NOT NULL,
    `total_interest_earned` decimal(30,3) NOT NULL,
    `start_date` date NOT NULL,
    `payback_date` date NOT NULL,
    `payback_time` time NOT NULL,
    `status` varchar(10) NOT NULL,
    PRIMARY KEY (`deposit_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=2;
    """,
    """
    CREATE TABLE IF NOT EXISTS `Central_Bank` (
    `account_number` varchar(15) NOT NULL,
    `account_balance` double(30,3) NOT NULL,
    PRIMARY KEY (`account_number`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """
]

for query in queries:
    my_cursor.execute(query)

queries2 = [
    """
    INSERT INTO `Account` (`account_id`, `account_number`, `account_type`, `account_holder`, `account_balance`, `minimum_balance`, `maximum_balance`, `account_fee`, `transaction_pin`, `account_status`, `account_tier`, `overdraft_protection`, `transaction_limit`, `transfer_limit`, `beneficiaries`, `fixed_account`) VALUES
    (1, '4773494548', 'savings', 'Ohanenye-Ohiaekpete Chidera Divine-Gift', 191272.388, 50.000, 300000.000, 100.000, '1234', 'active', 'Tier 1', 'no', 8, 39000.000, '{"1": ["1513500889", "Oboh Victory Akhere"], "2": ["5409484424", "Ezenwa Chiedozie Emmanuel"]}', 'yes');
    """,
    """
    INSERT INTO `Bank_Verification_Number` (`id`, `first_name`, `middle_name`, `last_name`, `gender`, `address`, `phone_number`, `date_of_birth`, `nationality`, `email`, `bvn_number`, `created_date`, `last_updated`, `bvn_status`) VALUES
    (1, 'Chidera', 'Divine-Gift', 'Ohanenye-Ohiaekpete', 'Male', 'Lagos', '07033327493', '2001-09-27', 'Nigeria', 'chrischidera6@gmail.com', '357455498371', '2024-05-04 19:57:21', '2024-05-04 19:57:21', 'active');
    """,
    """
    INSERT INTO `Central_Bank` (`account_number`, `account_balance`) VALUES
    ('1000000009', 1344556630016.000);
    """,
    """
    INSERT INTO `Fixed_Deposit` (`deposit_id`, `account_number`, `deposit_title`, `initial_deposit`, `interest_rate`, `total_interest_earned`, `start_date`, `payback_date`, `payback_time`, `status`) VALUES
    ('cbb176937083', '1513500889', 'babies', 2345.000, '0.329%', 7.710, '2024-05-24', '2024-06-08', '20:03:59', 'active');
    """,
    """
    INSERT INTO `Transaction` (`transaction_id`, `transaction_type`, `transaction_amount`, `sender_account_number`, `sender_name`, `receiver_account_number`, `receiver_name`, `transaction_date_time`, `description`, `status`, `account_type`, `account_balance`, `transaction_mode`) VALUES
    ('197162538621716988524706583141', 'fixed_deposit', 1234.560, '4773494548', 'Ohanenye-Ohiaekpete Chidera Divine-Gift', NULL, NULL, '2024-05-24 18:58:47', 'FIXED_DEPOSIT/CBB/cbb389472366/SAVE UP', 'successful', 'savings', 18340.199, 'debit');
    """,
    """
    INSERT INTO `User` (`id`, `username`, `password`, `first_name`, `middle_name`, `last_name`, `gender`, `email`, `phone_number`, `address`, `date_of_birth`, `linked_accounts`, `last_login_timestamp`, `account_open_date`, `account_close_date`) VALUES
    (1, 'c', 'c', 'Chidera', 'Divine-Gift', 'Ohanenye-Ohiaekpete', 'Male', 'chrischidera6@gmail.com', '07033327493', 'Lagos', '2001-09-27', '[]', '2024-06-05 09:12:36', '2024-05-04 19:58:00', NULL);
    """
]

for query in queries2:
    my_cursor.execute(query)
    connection.commit()

my_cursor.close()
