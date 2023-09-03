import random
from datetime import datetime


class Account:

    def __init__(self, account_name, initial_balance=0):
        self.account_name = account_name
        self.account_number = self.generate_account_number()
        self.balance = initial_balance
        self.pin = None
        self.is_locked = False
        self.transaction_history = []

    def generate_account_number(self):
        # Generate a random 11-digit account number
        return str(random.randint(10**10, 10**11 - 1))

    def set_pin(self, pin):
        self.pin = pin

    def deposit(self, amount):
        if not self.is_locked:
            self.balance += amount
            self.transaction_history.append(
                f"Deposited N{amount}  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print("Deposit successful.")
        else:
            print("Account is locked. Contact customer support.")

    def transfer(self, amount, target_account):
        if not self.is_locked and self.pin_correct():
            if self.balance >= amount:
                self.balance -= amount
                target_account.balance += amount
                self.transaction_history.append(
                    f"Transferred N{amount} to {target_account.account_name}  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                target_account.transaction_history.append(
                    f"Credit N{amount} from {self.account_name}  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                print("Transfer successful.")
            else:
                print("Insufficient balance.")
        else:
            print("Transaction not allowed. Account is locked or PIN is incorrect.")

    def withdraw(self, amount):
        if not self.is_locked and self.pin_correct():
            if self.balance >= amount:
                self.balance -= amount
                self.transaction_history.append(
                    f"withdrawal N{amount}  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                print("Withdrawal successful.")
            else:
                print("Insufficient balance.")
        else:
            print("Withdrawal not allowed. Account is locked or PIN is incorrect.")

    def view_account_details(self):
        print(f"\nAccount Name: {self.account_name}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: N{self.balance}")
        print(f"Account Status: {'Locked' if self.is_locked else 'Active'}")

    def pin_correct(self):
        if self.pin is None:
            return True

        for _ in range(3):
            entered_pin = input("Enter your PIN: ")
            if entered_pin == self.pin:
                return True
            print("Incorrect PIN. Try again.")

        self.is_locked = True
        print("Account locked due to multiple incorrect PIN attempts.")
        return False

    def view_transaction_history(self):
        print("\nTransaction History:")
        for count, transaction in enumerate(self.transaction_history):
            if count == 0:
                print("\n")
            print(transaction)
