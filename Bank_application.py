import uuid
import datetime
import paystack

paystack_api_key = 'pk_test_7e0bf57d99c4466e68fe890ace6c22b7027f168d3'

class BankAccount:
    def __init__(self, name, email, password):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password
        self.balance = 0
        self.transactions = []
        self.accounts = []

    #TO DEPOSIT FUND
    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(('deposit', amount, datetime.datetime.now()))

    #TO TRANSER FUNDS
    def transfer(self, account, amount):
        if self.balance >= amount:
            self.balance -= amount
            account.balance += amount
            self.transactions.append(('transfer', amount, datetime.datetime.now()))
            account.transactions.append(('receive', amount, datetime.datetime.now()))
            return True
        else:
            return False
        
    #TO CHECK USER TRANSACTIONS
    def view_transactions(self):
        return self.transactions

    #TO CHECK USER ACCOUNT BALANCE
    def check_balance(self):
        return self.balance

class BankApplication:
    def __init__(self):
        self.accounts = []

    # REGISTER NEW USER
    def register(self, name, email, password):
        account = BankAccount(name, email, password)
        self.accounts.append(account)
        return account

    #USER LOGIN SECTION
    def login(self, email, password):
        for account in self.accounts:
            if account.email == email and account.password == password:
                return account
        return None
    
    #PAYSTACK SECTION
    def mock_transaction(self, amount, recipient):
        paystack.initialize(paystack_api_key)
        transaction = paystack.Transaction.initialize(
            amount=amount*100,
            email=recipient.email,
            reference=str(uuid.uuid4())
        )
        if transaction['status']:
            return True
        else:
            return False
        
#INTERACTIVE SECTION
if __name__ == '__main__':
    bank = BankApplication()

    while True:
        print("Welcome to the Precious Stone Bank")
        print('1. Register')
        print('2. Login')
        print('3. Deposit')
        print('4. Transfer')
        print('5. Transaction History')
        print('6. Check Balance')
        print('7. Quit')

        choice = input('Enter your choice: ')

        if choice == '1':
            name = input('Enter your name: ')
            email = input('Enter your email: ')
            password = input('Enter your password: ')
            account = bank.register(name, email, password)
            print(f'Your account ID is: {account.id}')

        elif choice == '2':
            email = input('Enter your email: ')
            password = input('Enter your password: ')
            account = bank.login(email, password)
            if account:
                print(f'Welcome, {account.name}!')
            else:
                print('Invalid email or password')

        elif choice == '3':
            email = input('Enter your email: ')
            password = input('Enter your password: ')
            account = bank.login(email, password)
            if account:
                amount = float(input('Enter the amount to deposit: '))
                account.deposit(amount)
                print(f'Deposit successful. Your new balance is: {account.check_balance()}')
            else:
                print('Invalid email or password')

        elif choice == '4':
            email = input('Enter your email: ')
            password = input('Enter your password: ')
            account = bank.login(email, password)
            if account:
                recipient_email = input('Enter the recipient email: ')
                recipient = bank.login(recipient_email, '')
                amount = float(input('Enter the amount to transfer: '))
                if account.transfer(recipient, amount):
                    if bank.mock_transaction(amount, recipient):
                        print(f'Transfer successful. Your new balance is: {account.check_balance()}')
                else:
                    print('Insufficient balance or invalid email')

        elif choice == '5':
            email = input('Enter your email: ')
            password = input('Enter your password: ')
            account = bank.login(email, password)
            if account:
                transactions = account.view_transactions()
                if transactions:
                    print('Transaction History:')
                    for transaction in transactions:
                        print(f'{transaction[0].capitalize()} of {transaction[1]} at {transaction[2]}')
                else:
                    print('No transactions yet')
            else:
                print('Invalid email or password')

        elif choice == '6':
            email = input('Enter your email: ')
            password = input('Enter your password: ')
            account = bank.login(email, password)
            if account:
                print(f'Your balance is: {account.check_balance()}')
            else:
                print('Invalid email or password')

        elif choice == '7':
            print('Thank you for using Precious Stone Bank!')
            break
        else:
            print('Invalid choice. Please try again.')