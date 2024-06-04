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
    CREATE TABLE `Account` (
      `account_id` int(11) NOT NULL AUTO_INCREMENT,
      `account_number` varchar(10) NOT NULL,
      `account_type` varchar(15) NOT NULL,
      `account_holder` varchar(70) NOT NULL,
      `account_balance` float NOT NULL,
      `minimum_balance` float NOT NULL,
      `maximum_balance` float NOT NULL,
      `account_fee` float NOT NULL,
      `transaction_pin` varchar(4) NOT NULL,
      `account_status` varchar(10) NOT NULL,
      `account_tier` varchar(10) NOT NULL,
      `overdraft_protection` enum('yes','no') NOT NULL,
      `transaction_limit` int(11) NOT NULL,
      `transfer_limit` float NOT NULL,
      `beneficiaries` varchar(100) NOT NULL,
      `fixed_account` varchar(5) NOT NULL DEFAULT 'no',
      PRIMARY KEY (`account_id`),
      UNIQUE KEY `account_number` (`account_number`)
    ) AUTO_INCREMENT=2;
    """,
    """
    CREATE TABLE `Bank_Verification_Number` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `first_name` varchar(50) NOT NULL,
      `middle_name` varchar(50) NOT NULL,
      `last_name` varchar(50) NOT NULL,
      `gender` enum('Male','Female') NOT NULL,
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
    ) AUTO_INCREMENT=6;
    """,
    """
    CREATE TABLE `Transaction` (
      `transaction_id` varchar(20) NOT NULL,
      `transaction_type` varchar(15) NOT NULL,
      `transaction_amount` float NOT NULL,
      `sender_account_number` varchar(10) NOT NULL,
      `sender_name` varchar(50) NOT NULL,
      `receiver_account_number` varchar(10) NOT NULL,
      `receiver_name` varchar(50) NOT NULL,
      `transaction_date_time` datetime NOT NULL,
      `description` varchar(100) NOT NULL,
      `status` enum('successful','failed') NOT NULL,
      `account_type` varchar(15) NOT NULL,
      `account_balance` float NOT NULL,
      `transaction_mode` varchar(10) NOT NULL,
      PRIMARY KEY (`transaction_id`)
    );
    """,
    """
    CREATE TABLE `User` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `username` varchar(20) NOT NULL,
      `password` varchar(20) NOT NULL,
      `first_name` varchar(20) NOT NULL,
      `middle_name` varchar(20) NOT NULL,
      `last_name` varchar(20) NOT NULL,
      `gender` enum('Male','Female') NOT NULL,
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
    ) AUTO_INCREMENT=2;
    """,
    """
    CREATE TABLE `Fixed_Deposit` (
      `deposit_id` varchar(15) NOT NULL,
      `account_number` varchar(11) NOT NULL,
      `deposit_title` varchar(30) DEFAULT NULL,
      `initial_deposit` float NOT NULL,
      `interest_rate` varchar(10) NOT NULL,
      `total_interest_earned` float NOT NULL,
      `start_date` date NOT NULL,
      `payback_date` date NOT NULL,
      `payback_time` time NOT NULL,
      `status` varchar(10) NOT NULL,
      PRIMARY KEY (`deposit_id`)
    );
    """,
    """
    CREATE TABLE `Central_Bank` (
      `account_number` varchar(15) NOT NULL,
      `account_balance` float NOT NULL,
      PRIMARY KEY (`account_number`)
    );
    """
]

for query in queries:
    my_cursor.execute(query)

user_insert = """
INSERT INTO `User` (`id`, `username`, `password`, `first_name`, `middle_name`, `last_name`, `gender`, `email`, `phone_number`, `address`, `date_of_birth`, `linked_accounts`, `last_login_timestamp`, `account_open_date`, `account_close_date`) VALUES
(1, 'CHI', 'chi', 'Chidera', 'Divine-Gift', 'Ohanenye-Ohiaekpete', 'Male', 'chrischidera6@gmail.com', '07033327493', 'Lagos', '2001-09-27', '[]', '2024-05-25 10:39:50', '2024-05-04 19:58:00', NULL),
(2, 'VICTORYAKHERE', '!INternational10', 'Victory', 'Akhere', 'Oboh', 'Male', 'victoryoboh10@gmail.com', '09048786573', '29 Sufianu Street', '2000-03-14', '[]', '2024-05-25 10:41:49', '2024-05-07 14:49:17', NULL),
(3, 'CHIEDOZIEEMMANUEL', 'Dozie12$', 'Chiedozie', 'Emmanuel', 'Ezenwa', 'Male', 'chiedoziee@gmail.com', '09134030147', '8 Lawanson Street Lagos', '2004-09-03', '[]', '2024-05-07 15:07:47', '2024-05-07 15:06:51', NULL),
(4, 'ABDULBYE', 'Password 234', 'Abdul', 'Bye', 'Hello', 'Male', 'abdul@gmail.com', '09065433456', 'Olajide', '1999-10-29', '[]', '2024-05-11 11:19:55', '2024-05-11 11:18:41', NULL),
(5, 'EBUBEGODSON', 'Swaggzgenius12@', 'Ebube', 'Godson', 'Nwa', 'Male', 'nwagodson@gmail.com', '09087876565', 'Festac', '1998-04-11', '[]', '2024-05-16 13:58:49', '2024-05-16 11:01:25', NULL),
(6, 'MEMEMIMI', 'Swert12@', 'Meme', 'Mimi', 'Mmeso', 'Female', 'meme@gmail.com', '07034567893', 'Lagos', '2001-02-03', '[]', '2024-05-21 12:15:30', '2024-05-20 18:20:10', NULL);
"""

bvn_insert = """
INSERT INTO `Bank_Verification_Number` (`id`, `first_name`, `middle_name`, `last_name`, `gender`, `address`, `phone_number`, `date_of_birth`, `nationality`, `email`, `bvn_number`, `created_date`, `last_updated`, `bvn_status`) VALUES
(1, 'Chidera', 'Divine-Gift', 'Ohanenye-Ohiaekpete', 'Male', 'Lagos', '07033327493', '2001-09-27', 'Nigeria', 'chrischidera6@gmail.com', '357455498371', '2024-05-04 19:57:21', '2024-05-04 19:57:21', 'active'),
(2, 'Victory', 'Akhere', 'Oboh', 'Male', '29 Sufianu Street', '09048786573', '2000-03-14', 'Nigeria', 'victoryoboh10@gmail.com', '450986277846', '2024-05-07 14:47:33', '2024-05-07 14:47:33', 'active'),
(3, 'Chiedozie', 'Emmanuel', 'Ezenwa', 'Male', '8 Lawanson Street Lagos', '09134030147', '2004-09-03', 'Nigeria', 'chiedoziee@gmail.com', '583707628558', '2024-05-07 15:05:45', '2024-05-07 15:05:45', 'active'),
(4, 'Abdul', 'Bye', 'Hello', 'Male', 'Olajide', '09065433456', '1999-10-29', 'Nigeria', 'abdul@gmail.com', '966145324014', '2024-05-11 11:17:41', '2024-05-11 11:17:41', 'active'),
(5, 'Ebube', 'Godson', 'Nwa', 'Male', 'Festac', '09087876565', '1998-04-11', 'Nigeria', 'nwagodson@gmail.com', '554115460133', '2024-05-16 11:00:46', '2024-05-16 11:00:46', 'active'),
(6, 'Meme', 'Mimi', 'Mmeso', 'Female', 'Lagos', '07034567893', '2001-02-03', 'Nigeria', 'meme@gmail.com', '816707385819', '2024-05-20 18:19:27', '2024-05-20 18:19:27', 'active');
"""

account_insert = """
INSERT INTO `Account` (`account_id`, `account_number`, `account_type`, `account_holder`, `account_balance`, `minimum_balance`, `maximum_balance`, `account_fee`, `transaction_pin`, `account_status`, `account_tier`, `overdraft_protection`, `transaction_limit`, `transfer_limit`, `beneficiaries`, `fixed_account`) VALUES
(1, '4773494548', 'savings', 'Ohanenye-Ohiaekpete Chidera Divine-Gift', 9704.02, 50, 300000, 100, '1234', 'active', 'Tier 1', 'no', 10, 50000, '{\"1\": [\"1513500889\", \"Oboh Victory Akhere\"], \"2\": [\"5409484424\", \"Ezenwa Chiedozie Emmanuel\"]}', 'yes'),
(2, '1513500889', 'savings', 'Oboh Victory Akhere', 4752.5, 50, 300000, 100, '2000', 'active', 'Tier 1', 'no', 10, 50000, '{\"1\": [\"4773494548\", \"Ohanenye-Ohiaekpete Chidera Divine-Gift\"]}', 'yes'),
(3, '5409484424', 'savings', 'Ezenwa Chiedozie Emmanuel', 2455.5, 50, 300000, 100, '2094', 'active', 'Tier 1', 'no', 10, 50000, '{}', 'no'),
(4, '2936502510', 'savings', 'Hello Abdul Bye', 500.5, 50, 300000, 100, '1234', 'active', 'Tier 1', 'no', 10, 50000, '{}', 'no'),
(5, '2726400190', 'savings', 'Nwa Ebube Godson', 500.5, 50, 300000, 100, '1234', 'active', 'Tier 1', 'no', 10, 50000, '{}', 'no'),
(6, '1927633030', 'current', 'Mmeso Meme Mimi', 1979.44, 500, 300000, 500, '1234', 'active', 'Tier 1', 'no', 50, 500000, '{\"1\": [\"1513500889\", \"Oboh Victory Akhere\"]}', 'no');
"""

fixed_deposit_insert = """
INSERT INTO `Fixed_Deposit` (`deposit_id`, `account_number`, `deposit_title`, `initial_deposit`, `interest_rate`, `total_interest_earned`, `start_date`, `payback_date`, `payback_time`, `status`) VALUES
('cbb176937083', '1513500889', 'babies', 2345, '0.329%', 7.71, '2024-05-24', '2024-06-08', '20:03:59', 'active'),
('cbb242198673', '4773494548', 'save up 2', 2567.88, '2.411%', 61.911, '2024-05-24', '2024-08-12', '20:09:58', 'active'),
('cbb389472366', '4773494548', 'save up', 1234.56, '3.182%', 39.286, '2024-05-24', '2024-09-03', '18:58:40', 'active'),
('cbb437856199', '4773494548', 'queens', 3456.78, '8.174%', 282.556, '2024-05-24', '2025-01-01', '20:16:52', 'active');
"""

transaction_insert = """
INSERT INTO `Transaction` (`transaction_id`, `transaction_type`, `transaction_amount`, `sender_account_number`, `sender_name`, `receiver_account_number`, `receiver_name`, `transaction_date_time`, `description`, `status`, `account_type`, `account_balance`, `transaction_mode`) VALUES
('197162538621716988524706583141', 'fixed_deposit', 1234.56, '4773494548', 'Ohanenye-Ohiaekpete Chidera Divine-Gift', 'NULL', 'NULL', '2024-05-24 18:58:47', 'FIXED_DEPOSIT/CBB/cbb389472366/SAVE UP', 'successful', 'savings', 18340.2, 'debit'),
('124134303291407776001832822156', 'transfer', 133.53, '4773494548', 'Ohanenye-Ohiaekpete Chidera Divine-Gift', '5409484424', 'Ezenwa Chiedozie Emmanuel', '2024-05-24 19:58:36', 'TRF/CBB/FROM OHANENYE-OHIAEKPETE CHIDERA DIVINE-GIFT TO EZENWA CHIEDOZIE EMMANUEL', 'successful', 'savings', 15728.7, 'debit'),
('124134303291407776001832822156', 'transfer', 123, '4773494548', 'Ohanenye-Ohiaekpete Chidera Divine-Gift', '5409484424', 'Ezenwa Chiedozie Emmanuel', '2024-05-24 19:58:36', 'TRF/CBB/FROM OHANENYE-OHIAEKPETE CHIDERA DIVINE-GIFT TO EZENWA CHIEDOZIE EMMANUEL', 'successful', 'savings', 2455.5, 'credit'),
('291172828005142118892462282990', 'fixed_deposit', 2345, '1513500889', 'Oboh Victory Akhere', 'NULL', 'NULL', '2024-05-24 20:04:49', 'FIXED_DEPOSIT/CBB/cbb176937083/BABIES', 'successful', 'savings', 4752.5, 'debit'),
('198960033301626770364810981590', 'fixed_deposit', 2567.88, '4773494548', 'Ohanenye-Ohiaekpete Chidera Divine-Gift', 'NULL', 'NULL', '2024-05-24 20:10:07', 'FIXED_DEPOSIT/CBB/cbb242198673/SAVE UP 2', 'successful', 'savings', 13160.8, 'debit'),
('472755518586157070730320704276', 'fixed_deposit', 3456.78, '4773494548', 'Ohanenye-Ohiaekpete Chidera Divine-Gift', 'NULL', 'NULL', '2024-05-24 20:17:01', 'FIXED_DEPOSIT/CBB/cbb437856199/QUEENS', 'successful', 'savings', 9704.02, 'debit');
"""

queries2 = [
    user_insert, bvn_insert, account_insert, fixed_deposit_insert, transaction_insert
]

for query in queries2:
    my_cursor.execute(query)
    connection.commit()

my_cursor.close()
