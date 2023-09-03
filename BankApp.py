from account_manager import Account
import os
import pickle  # For serializing/deserializing account data


def load_accounts():
    accounts = {}
    if os.path.exists("accounts.pkl"):
        with open("accounts.pkl", "rb") as file:
            accounts = pickle.load(file)
    return accounts


def save_accounts(accounts):
    with open("accounts.pkl", "wb") as file:
        pickle.dump(accounts, file)


def input_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def login(accounts):
    account_number = input("Enter your account number: ")
    if account_number in accounts:
        account = accounts[account_number]
        print("Logging in...")
        while True:
            pin = input("Enter your PIN: ")
            if account.pin == pin:
                print("Login successful.")
                return account
            else:
                print("Incorrect PIN. Login failed.")
    else:
        print("Account not found. Please create a new account.")


def perform_account_operations(account, accounts):
    while True:
        print("\nOptions:")
        print("1. Deposit")
        print("2. Transfer")
        print("3. Withdraw")
        print("4. View Account Details")
        print("5. View Transaction History")
        print("6. Logout")

        operation = input("Enter your choice: ")

        if operation == '1':
            amount = input_float("Enter the deposit amount: ")
            if amount < 0:
                print("Invalid amount. Please enter a positive value.")
            else:
                account.deposit(amount)
        elif operation == '2':
            target_account_number = input(
                "Enter the recipient's account number: ")
            if not target_account_number.isdigit():
                print("Invalid account number. Please enter a valid integer.")
                continue
            target_account_number = target_account_number
            if target_account_number in accounts:
                target_account = accounts[target_account_number]
                amount = input_float("Enter the transfer amount: ")
                if amount < 0:
                    print("Invalid amount. Please enter a positive value.")
                else:
                    account.transfer(amount, target_account)
            else:
                print("Recipient account not found.")
        elif operation == '3':
            amount = input_float("Enter the withdrawal amount: ")
            if amount < 0:
                print("Invalid amount. Please enter a positive value.")
            else:
                account.withdraw(amount)
        elif operation == '4':
            account.view_account_details()
        elif operation == '5':
            account.view_transaction_history()
        elif operation == '6':
            print("Logged out successfully.")
            save_accounts(accounts)
            break
        else:
            print("Invalid choice. Please select a valid option.")


def main():
    print("Welcome to PME BankApp!")

    while True:
        print("\nOptions:")
        print("1. Create a New Account")
        print("2. Login to Existing Account")
        print("3. Exit")

        selection = input("Enter your choice: ")

        if selection == '1':
            accounts = load_accounts()
            account_name = input(
                "Enter your account name to create a new account: ")
            pin = input("Set your transaction PIN: ")

            account = Account(account_name)  # Initial balance is 0
            account.set_pin(pin)

            accounts[account.account_number] = account

            print("New account created successfully.")
            print("Logging in...")
            user_account = perform_account_operations(account, accounts)
            if user_account:
                accounts[user_account.account_number] = user_account
        elif selection == '2':
            accounts = load_accounts()
            user_account = login(accounts)
            if user_account:
                perform_account_operations(user_account, accounts)
        elif selection == '3':
            try:
                with open("account_numbers.txt", "a") as file:
                    file.write(account.account_number + "\n")
            except UnboundLocalError:
                pass

            save_accounts(accounts)
            print("Exiting the BankApp. Thank you!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
