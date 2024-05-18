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

query1 = """
CREATE TABLE `Account` (
  `account_id` int(11) NOT NULL,
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
  `beneficiaries` varchar(100) NOT NULL
) 
"""

query2 = """
CREATE TABLE `Bank_Verification_Number` (
  `id` int(11) NOT NULL,
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
  `bvn_status` varchar(20) NOT NULL
) 
"""

query3 = """
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
  `account_type` varchar(15) NOT NULL
) 
"""

query4 = """
CREATE TABLE `User` (
  `id` int(11) NOT NULL,
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
  `account_close_date` datetime DEFAULT NULL
) 
"""

query5 = """
ALTER TABLE `Account`
  ADD PRIMARY KEY (`account_id`),
  ADD UNIQUE KEY `account_number` (`account_number`);
"""

query6 = """
ALTER TABLE `Bank_Verification_Number`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `phone_number` (`phone_number`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `bvn_number` (`bvn_number`);
"""

query8 = """
ALTER TABLE `User`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `phone_number` (`phone_number`);
"""

query9 = """
ALTER TABLE `Account`
  MODIFY `account_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
"""

query10 = """
ALTER TABLE `Bank_Verification_Number`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
"""

query11 = """
ALTER TABLE `User`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
"""

queries = [query1, query2, query3, query4, query5, query6, query8, query9, query10, query11]

for query in queries:
    my_cursor.execute(query)

query12 = """
INSERT INTO `User` (`id`, `username`, `password`, `first_name`, `middle_name`, `last_name`, `gender`, `email`, `phone_number`, `address`, `date_of_birth`, `linked_accounts`, `last_login_timestamp`, `account_open_date`, `account_close_date`) VALUES
(1, 'CHI', 'chi', 'Chidera', 'Divine-Gift', 'Ohanenye-Ohiaekpete', 'Male', 'chrischidera6@gmail.com', '07033327493', 'Lagos', '2001-09-27', '[]', '2024-05-10 10:42:18', '2024-05-04 19:58:00', NULL),
(2, 'VICTORYAKHERE', '!INternational10', 'Victory', 'Akhere', 'Oboh', 'Male', 'victoryoboh10@gmail.com', '09048786573', '29 Sufianu Street', '2000-03-14', '[]', '2024-05-09 13:15:23', '2024-05-07 14:49:17', NULL),
(3, 'CHIEDOZIEEMMANUEL', 'Dozie12$', 'Chiedozie', 'Emmanuel', 'Ezenwa', 'Male', 'chiedoziee@gmail.com', '09134030147', '8 Lawanson Street Lagos', '2004-09-03', '[]', '2024-05-07 15:07:47', '2024-05-07 15:06:51', NULL);
"""

query13 = """
INSERT INTO `Bank_Verification_Number` (`id`, `first_name`, `middle_name`, `last_name`, `gender`, `address`, `phone_number`, `date_of_birth`, `nationality`, `email`, `bvn_number`, `created_date`, `last_updated`, `bvn_status`) VALUES
(1, 'Chidera', 'Divine-Gift', 'Ohanenye-Ohiaekpete', 'Male', 'Lagos', '07033327493', '2001-09-27', 'Nigeria', 'chrischidera6@gmail.com', '357455498371', '2024-05-04 19:57:21', '2024-05-04 19:57:21', 'active'),
(2, 'Victory', 'Akhere', 'Oboh', 'Male', '29 Sufianu Street', '09048786573', '2000-03-14', 'Nigeria', 'victoryoboh10@gmail.com', '450986277846', '2024-05-07 14:47:33', '2024-05-07 14:47:33', 'active'),
(3, 'Chiedozie', 'Emmanuel', 'Ezenwa', 'Male', '8 Lawanson Street Lagos', '09134030147', '2004-09-03', 'Nigeria', 'chiedoziee@gmail.com', '583707628558', '2024-05-07 15:05:45', '2024-05-07 15:05:45', 'active');
"""

query14 = """
INSERT INTO `Account` (`account_id`, `account_number`, `account_type`, `account_holder`, `account_balance`, `minimum_balance`, `maximum_balance`, `account_fee`, `transaction_pin`, `account_status`, `account_tier`, `overdraft_protection`, `transaction_limit`, `transfer_limit`, `beneficiaries`) VALUES
(1, '4773494548', 'savings', 'Ohanenye-Ohiaekpete Chidera Divine-Gift', 500.5, 50, 300000, 100, '1234', 'active', 'Tier 1', 'no', 10, 49960, '{\"1\": [\"1513500889\", \"Oboh Victory Akhere\"]}'),
(2, '1513500889', 'savings', 'Oboh Victory Akhere', 500.5, 50, 300000, 100, '2000', 'active', 'Tier 1', 'no', 9, 49800, '{\"1\": [\"4773494548\", \"Ohanenye-Ohiaekpete Chidera Divine-Gift\"]}'),
(3, '5409484424', 'savings', 'Ezenwa Chiedozie Emmanuel', 500.5, 50, 300000, 100, '2094', 'active', 'Tier 1', 'no', 10, 50000, '{}'),
(4, '2936502510', 'savings', 'Hello Abdul Bye', 500.5, 50, 300000, 100, '1234', 'active', 'Tier 1', 'no', 10, 50000, '{}'),
(5, '2726400190', 'savings', 'Nwa Ebube Godson', 500.5, 50, 300000, 100, '1234', 'active', 'Tier 1', 'no', 10, 50000, '{}');
"""

queries2 = [query12, query13, query14]

for query in queries2:
    my_cursor.execute(query)
    connection.commit()

my_cursor.close()
