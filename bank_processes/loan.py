import datetime
from typing import List, Dict


class Loan:
    """
    A class to represent a loan and perform various loan-related calculations.

    Attributes
    ----------
    principal : float
        The initial amount of the loan.
    annual_interest_rate : float
        The annual interest rate of the loan as a percentage.
    term_years : int
        The term of the loan in years.
    loan_type : str
        The type of the loan (e.g., 'personal', 'mortgage', 'auto', 'student').
    start_date : datetime.date
        The start date of the loan.

    Methods
    -------
    monthly_payment():
        Calculates the monthly payment amount.
    total_payment():
        Calculates the total payment amount over the term of the loan.
    total_interest():
        Calculates the total interest paid over the term of the loan.
    repayment_schedule():
        Generates the repayment schedule as a list of dictionaries.
    """

    def __init__(self, principal: float, annual_interest_rate: float, term_years: int, loan_type: str,
                 start_date: datetime.date):
        """
        Constructs all the necessary attributes for the Loan object.

        Parameters
        ----------
        principal : float
            The initial amount of the loan.
        annual_interest_rate : float
            The annual interest rate of the loan as a percentage.
        term_years : int
            The term of the loan in years.
        loan_type : str
            The type of the loan (e.g., 'personal', 'mortgage', 'auto', 'student').
        start_date : datetime.date
            The start date of the loan.
        """
        self.principal = principal
        self.annual_interest_rate = annual_interest_rate
        self.term_years = term_years
        self.loan_type = loan_type
        self.start_date = start_date

    def monthly_payment(self) -> float:
        """
        Calculates the monthly payment amount.

        Returns
        -------
        float
            The monthly payment amount.
        """
        monthly_interest_rate = self.annual_interest_rate / 100 / 12
        num_payments = self.term_years * 12
        if monthly_interest_rate == 0:
            return self.principal / num_payments
        payment = (self.principal * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
        return round(payment, 2)

    def total_payment(self) -> float:
        """
        Calculates the total payment amount over the term of the loan.

        Returns
        -------
        float
            The total payment amount.
        """
        return round(self.monthly_payment() * self.term_years * 12, 2)

    def total_interest(self) -> float:
        """
        Calculates the total interest paid over the term of the loan.

        Returns
        -------
        float
            The total interest amount.
        """
        return round(self.total_payment() - self.principal, 2)

    def repayment_schedule(self) -> List[Dict]:
        """
        Generates the repayment schedule as a list of dictionaries.

        Returns
        -------
        List[Dict]
            The repayment schedule, where each entry is a dictionary with keys 'month', 'payment', 'principal_paid', 'interest_paid', and 'remaining_balance'.
        """
        schedule = []
        remaining_balance = self.principal
        monthly_payment = self.monthly_payment()
        monthly_interest_rate = self.annual_interest_rate / 100 / 12

        for month in range(1, self.term_years * 12 + 1):
            interest_paid = round(remaining_balance * monthly_interest_rate, 2)
            principal_paid = round(monthly_payment - interest_paid, 2)
            remaining_balance = round(remaining_balance - principal_paid, 2)
            schedule.append({
                "month": month,
                "payment": monthly_payment,
                "principal_paid": principal_paid,
                "interest_paid": interest_paid,
                "remaining_balance": remaining_balance
            })

        return schedule

    def __str__(self):
        """
        Returns a string representation of the loan details.

        Returns
        -------
        str
            A string representation of the loan details.
        """
        return (f"Loan Type: {self.loan_type}\n"
                f"Principal: {self.principal}\n"
                f"Annual Interest Rate: {self.annual_interest_rate}%\n"
                f"Term: {self.term_years} years\n"
                f"Start Date: {self.start_date}\n"
                f"Monthly Payment: {self.monthly_payment()}\n"
                f"Total Payment: {self.total_payment()}\n"
                f"Total Interest: {self.total_interest()}")


# Example usage
if __name__ == "__main__":
    loan = Loan(10000, 5, 5, 'personal', datetime.date(2024, 6, 1))
    print(loan)
    print(loan.monthly_payment())
    for payment in loan.repayment_schedule():
        print(payment)
