-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 11, 2024 at 01:30 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bankApp_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `Account`
--

CREATE TABLE `Account` (
  `account_id` int(11) NOT NULL,
  `account_number` varchar(10) NOT NULL,
  `account_type` varchar(15) NOT NULL,
  `account_holder` varchar(70) NOT NULL,
  `account_balance` float NOT NULL,
  `minimum_balance` float NOT NULL,
  `account_fee` float NOT NULL,
  `transaction_pin` varchar(4) NOT NULL,
  `account_status` varchar(10) NOT NULL,
  `account_tier` varchar(10) NOT NULL,
  `overdraft_protection` enum('yes','no') NOT NULL,
  `transaction_limit` varchar(5) NOT NULL,
  `beneficiaries` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Account`
--

INSERT INTO `Account` (`account_id`, `account_number`, `account_type`, `account_holder`, `account_balance`, `minimum_balance`, `account_fee`, `transaction_pin`, `account_status`, `account_tier`, `overdraft_protection`, `transaction_limit`, `beneficiaries`) VALUES
(1, '4773494548', 'savings', 'Ohanenye-Ohiaekpete Chidera Divine-Gift', 500.5, 50, 100, '1234', 'active', 'Tier 1', 'no', '10', '{\"1\": [\"1234567\", \"James\"], \"2\": [\"5678907\", \"Chi\"]}'),
(2, '1513500889', 'savings', 'Oboh Victory Akhere', 500.5, 50, 100, '2000', 'active', 'Tier 1', 'no', '10', ''),
(3, '5409484424', 'savings', 'Ezenwa Chiedozie Emmanuel', 500.5, 50, 100, '2094', 'active', 'Tier 1', 'no', '10', ''),
(4, '2936502510', 'savings', 'Hello Abdul Bye', 500.5, 50, 100, '1234', 'active', 'Tier 1', 'no', '10', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `Bank_Verification_Number`
--

CREATE TABLE `Bank_Verification_Number` (
  `id` int(11) NOT NULL,
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
  `bvn_status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Bank_Verification_Number`
--

INSERT INTO `Bank_Verification_Number` (`id`, `first_name`, `middle_name`, `last_name`, `gender`, `address`, `phone_number`, `date_of_birth`, `nationality`, `email`, `bvn_number`, `created_date`, `last_updated`, `bvn_status`) VALUES
(1, 'Chidera', 'Divine-Gift', 'Ohanenye-Ohiaekpete', 'Male', 'Lagos', '07033327493', '2001-09-27', 'Nigeria', 'chrischidera6@gmail.com', '357455498371', '2024-05-04 19:57:21', '2024-05-04 19:57:21', 'active'),
(2, 'Victory', 'Akhere', 'Oboh', 'Male', '29 Sufianu Street', '09048786573', '2000-03-14', 'Nigeria', 'victoryoboh10@gmail.com', '450986277846', '2024-05-07 14:47:33', '2024-05-07 14:47:33', 'active'),
(3, 'Chiedozie', 'Emmanuel', 'Ezenwa', 'Male', '8 Lawanson Street Lagos', '09134030147', '2004-09-03', 'Nigeria', 'chiedoziee@gmail.com', '583707628558', '2024-05-07 15:05:45', '2024-05-07 15:05:45', 'active'),
(4, 'Abdul', 'Bye', 'Hello', 'Male', 'Olajide', '09065433456', '1999-10-29', 'Nigeria', 'abdul@gmail.com', '966145324014', '2024-05-11 11:17:41', '2024-05-11 11:17:41', 'active');

-- --------------------------------------------------------

--
-- Table structure for table `Transaction`
--

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

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE `User` (
  `id` int(11) NOT NULL,
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
  `account_close_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`id`, `username`, `password`, `first_name`, `middle_name`, `last_name`, `gender`, `email`, `phone_number`, `address`, `date_of_birth`, `linked_accounts`, `last_login_timestamp`, `account_open_date`, `account_close_date`) VALUES
(1, 'CHI', 'chi', 'Chidera', 'Divine-Gift', 'Ohanenye-Ohiaekpete', 'Male', 'chrischidera6@gmail.com', '07033327493', 'Lagos', '2001-09-27', '[]', '2024-05-11 11:23:10', '2024-05-04 19:58:00', NULL),
(2, 'VICTORYAKHERE', '!INternational10', 'Victory', 'Akhere', 'Oboh', 'Male', 'victoryoboh10@gmail.com', '09048786573', '29 Sufianu Street', '2000-03-14', '[]', '2024-05-09 13:15:23', '2024-05-07 14:49:17', NULL),
(3, 'CHIEDOZIEEMMANUEL', 'Dozie12$', 'Chiedozie', 'Emmanuel', 'Ezenwa', 'Male', 'chiedoziee@gmail.com', '09134030147', '8 Lawanson Street Lagos', '2004-09-03', '[]', '2024-05-07 15:07:47', '2024-05-07 15:06:51', NULL),
(4, 'ABDULBYE', 'Password 234', 'Abdul', 'Bye', 'Hello', 'Male', 'abdul@gmail.com', '09065433456', 'Olajide', '1999-10-29', '[]', '2024-05-11 11:19:55', '2024-05-11 11:18:41', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Account`
--
ALTER TABLE `Account`
  ADD PRIMARY KEY (`account_id`),
  ADD UNIQUE KEY `account_number` (`account_number`);

--
-- Indexes for table `Bank_Verification_Number`
--
ALTER TABLE `Bank_Verification_Number`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `phone_number` (`phone_number`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `bvn_number` (`bvn_number`);

--
-- Indexes for table `Transaction`
--
ALTER TABLE `Transaction`
  ADD UNIQUE KEY `transaction_id` (`transaction_id`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `phone_number` (`phone_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Account`
--
ALTER TABLE `Account`
  MODIFY `account_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Bank_Verification_Number`
--
ALTER TABLE `Bank_Verification_Number`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `User`
--
ALTER TABLE `User`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
