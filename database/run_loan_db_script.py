import pymysql as sql

connection = sql.connect(
    host='localhost',
    user='root',
    password='',
    database='bankApp_db'
)

my_cursor = connection.cursor()

queries = [
    """
    CREATE TABLE LoanUsers (
        user_id INT PRIMARY KEY AUTO_INCREMENT,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        phone_number VARCHAR(15),
        address VARCHAR(255),
        date_of_birth DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE LoanTypes (
        loan_type_id INT PRIMARY KEY AUTO_INCREMENT,
        type_name VARCHAR(50) NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE LoanStatus (
        status_id INT PRIMARY KEY AUTO_INCREMENT,
        status_name VARCHAR(50) NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE Loans (
        loan_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT,
        loan_type_id INT,
        amount DECIMAL(15, 2) NOT NULL,
        interest_rate DECIMAL(5, 2) NOT NULL,
        monthly_payment DECIMAL(15,2) NOT NULL,
        start_date DATE NOT NULL,
        due_date DATE NOT NULL,
        end_date DATE NOT NULL,
        status_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES LoanUsers(user_id),
        FOREIGN KEY (loan_type_id) REFERENCES LoanTypes(loan_type_id),
        FOREIGN KEY (status_id) REFERENCES LoanStatus(status_id)
    );
    """,
    """
    CREATE TABLE LoansPayments (
        payment_id INT PRIMARY KEY AUTO_INCREMENT,
        loan_id INT,
        amount DECIMAL(15, 2) NOT NULL,
        payment_date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (loan_id) REFERENCES Loans(loan_id)
    );
    """,
]

for query in queries:
    my_cursor.execute(query)

insert_queries = [
    """
    INSERT INTO `LoanStatus` (`status_id`, `status_name`, `description`, `created_at`, `updated_at`) VALUES
    (1, 'approved', 'The loan has been approved.', '2024-06-10 21:11:31', '2024-06-10 21:11:31'),
    (2, 'rejected', 'The Loan has been rejected.', '2024-06-10 21:11:47', '2024-06-10 21:11:47'),
    (3, 'completed', 'The Loan has been completed.', '2024-06-10 21:42:54', '2024-06-10 21:42:54');
    """,
    """
    INSERT INTO `LoanTypes` (`loan_type_id`, `type_name`, `description`, `created_at`, `updated_at`) VALUES
    (1, 'Personal Loan', 'Personal loans are typically unsecured loans that individuals can use for various personal expenses, such as consolidating debt, financing a large purchase, or covering unexpected expenses. They usually have fixed interest rates and repayment terms.', '2024-06-10 20:43:32', '2024-06-10 21:16:58'),
    (2, 'Mortgage Loan', 'Mortgage loans are secured loans used to purchase real estate.', '2024-06-10 21:22:07', '2024-06-10 21:22:07'),
    (3, 'Auto Loan', 'Auto loans are secured loans used to purchase vehicles.', '2024-06-10 21:30:25', '2024-06-10 21:30:25'),
    (4, 'Student Loan', 'Student loans are designed to help cover the cost of higher education.', '2024-06-10 21:30:25', '2024-06-10 21:30:25'),
    (5, 'Small Business Loan', 'Small business loans provide capital to help businesses start, grow, or manage cash flow.', '2024-06-10 21:30:25', '2024-06-10 21:30:25'),
    (6, 'Payday Loan', 'Payday loans are short-term, high-interest loans designed to provide quick cash until the borrower’s next paycheck.', '2024-06-10 21:30:25', '2024-06-10 21:30:25'),
    (7, 'Home Equity Loan', 'These loans allow homeowners to borrow against the equity in their home.', '2024-06-10 21:30:25', '2024-06-10 21:30:25'),
    (8, 'Debt Consolidation Loan', 'These loans are used to combine multiple debts into a single loan with a potentially lower interest rate.', '2024-06-10 21:30:25', '2024-06-10 21:30:25'),
    (9, 'Credit Builder Loan', 'Credit builder loans are designed to help individuals build or improve their credit scores.', '2024-06-10 21:30:25', '2024-06-10 21:30:25'),
    (10, 'Peer to Peer Loan', 'Peer-to-peer (P2P) loans are funded by individual investors through online platforms, bypassing traditional financial institutions.', '2024-06-10 21:30:25', '2024-06-10 21:30:25'),
    (11, 'Title Loan', 'Title loans are short-term secured loans where the borrower uses their vehicle title as collateral.', '2024-06-10 21:30:25', '2024-06-10 21:30:25'),
    (12, 'Bridge Loan', 'Bridge loans provide short-term financing to bridge the gap between the sale of an existing property and the purchase of a new one.', '2024-06-10 21:30:25', '2024-06-10 21:30:25');
    """,
]
for query in insert_queries:
    my_cursor.execute(query)
    connection.commit()

my_cursor.close()
