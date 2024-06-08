import datetime

class Loan:
    def __init__(self, loan_id, user_id, loan_type, amount, interest_rate, start_date, end_date, status, database):
        self.loan_id = loan_id
        self.user_id = user_id
        self.loan_type = loan_type
        self.amount = amount
        self.interest_rate = interest_rate
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.database = database

    def add_loan(self):
        new_loan = {
            "loan_id": self.loan_id,
            "user_id": self.user_id,
            "loan_type": self.loan_type,
            "amount": self.amount,
            "interest_rate": self.interest_rate,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now()
        }
        self.database.append(new_loan)
        print("Loan added successfully!")

    def update_loan(self, loan_id, **kwargs):
        for loan in self.database:
            if loan["loan_id"] == loan_id:
                for key, value in kwargs.items():
                    if key in loan:
                        loan[key] = value
                        loan["updated_at"] = datetime.datetime.now()
                print("Loan updated successfully!")
                return
        print("Loan not found!")

    def display_loan_details(self, loan_id):
        for loan in self.database:
            if loan["loan_id"] == loan_id:
                for key, value in loan.items():
                    print(f"{key}: {value}")
                return
        print("Loan not found!")

# Example usage
if __name__ == "__main__":
    # In-memory loan database
    loan_database = []

    # Creating a loan object
    loan1 = Loan(
        loan_id=1,
        user_id=101,
        loan_type="Personal Loan",
        amount=5000.00,
        interest_rate=5.0,
        start_date="2024-01-01",
        end_date="2025-01-01",
        status="Approved",
        database=loan_database
    )

    # Adding the loan to the database
    loan1.add_loan()

    # Display loan details
    loan1.display_loan_details(1)

    # Update loan details
    loan1.update_loan(1, amount=6000.00, status="Pending")

    # Display updated loan details
    loan1.display_loan_details(1)
