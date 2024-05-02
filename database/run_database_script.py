import pymysql as sql

connection = sql.connect(
    host='localhost',
    user='root',
    password='',
    database='bankApp_db'
)

my_cursor = connection.cursor()

query0 = """
CREATE DATABASE IF NOT EXISTS bankApp_db
"""

query1 = """
CREATE TABLE `Account` (
  `account_id` int(11) NOT NULL,
  `account_number` varchar(10) NOT NULL,
  `account_type` varchar(15) NOT NULL,
  `account_holder` varchar(70) NOT NULL,
  `account_balance` float NOT NULL,
  `transaction_pin` varchar(4) NOT NULL,
  `account_status` varchar(10) NOT NULL,
  `account_tier` varchar(10) NOT NULL,
  `overdraft_protection` enum('yes','no') NOT NULL,
  `transaction_limit` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
  `account_type` varchar(15) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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

query7 = """
ALTER TABLE `Transaction`
  ADD UNIQUE KEY `transaction_id` (`transaction_id`);
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
COMMIT;
"""

queries = [query0, query1, query2, query3, query4, query5, query6, query7, query8, query9, query10, query11]

for query in queries:
    my_cursor.execute(query)

query12 = """
INSERT INTO `Account` (`account_id`, `account_number`, `account_type`, `account_holder`, `account_balance`, 
`transaction_pin`, `account_status`, `account_tier`, `overdraft_protection`, `transaction_limit`) VALUES
(1, '2739713114', 'savings', 'Ohanenye-Ohiaekpete Chidera Divine-Gift', 500.5, '1234', 'active', 'Tier 1', 'no', '10');
"""

query13 = """
INSERT INTO `Bank_Verification_Number` (`id`, `first_name`, `middle_name`, `last_name`, `gender`, `address`, 
`phone_number`, `date_of_birth`, `nationality`, `email`, `bvn_number`, `created_date`, `last_updated`, `bvn_status`) 
VALUES (5, 'Chidera', 'Divine-Gift', 'Ohanenye-Ohiaekpete', 'Male', 'Lagos', '07033327493', '2001-09-27', 'Nigeria', 
'chrischidera6@gmail.com', '698718792902', '2024-05-01 18:18:09', '2024-05-01 18:18:09', 'active');
"""

query14 = """
INSERT INTO `User` (`id`, `username`, `password`, `first_name`, `middle_name`, `last_name`, `gender`, `email`, 
`phone_number`, `address`, `date_of_birth`, `linked_accounts`, `last_login_timestamp`, `account_open_date`, 
`account_close_date`) VALUES (1, 'CHI', 'chi', 'Chidera', 'Divine-Gift', 'Ohanenye-Ohiaekpete', 'Male', 
'chrischidera6@gmail.com', '07033327493', 'Lagos', '2001-09-27', '[]', '2024-05-01 18:18:57', '2024-05-01 18:18:57', 
NULL);
"""

queries2 = [query12, query13, query14]

for query in queries2:
    my_cursor.execute(query)
    connection.commit()

my_cursor.close()
