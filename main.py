import csv
import os
import pprint
import time

from prettytable import PrettyTable

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import shutil
from os.path import exists
from tempfile import NamedTemporaryFile


class transaction_manager:

    def __init__(self):
        csv_file = open('transactions.csv')
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        self.transactions = []
        for row in csv_reader:

            if line_count > 0:
                row.insert(0, line_count)

                self.transactions.append(row)

            line_count += 1

        csv_file.close()

        self.print_transactions()

    def print_statement(self):

        accounts = []

        row_count = 0
        for row in self.transactions:

            if row[2] not in accounts:
                accounts.append(row[2])

            row_count += 1

        string_to_print_in_input = ''

        current_account = 0
        for account in accounts:
            string_to_print_in_input += f'\n{current_account}) {account}'

            current_account += 1

        selected_account = input(f'Select an account:\n{string_to_print_in_input}\n\nYour selection: ')

        current_account = 0

        x = PrettyTable()
        x.field_names = [ "Date", "Account", "Description", "Amount", "Balance"]

        for account in accounts:

            if str(current_account) == str(selected_account):
                print(f'\n\nYou selected to print a statement for the "{account}" account.')

                sortable_txns = self.transactions

                sortable_txns=sorted(sortable_txns, key = lambda i: i[1] ,reverse=True)

                current_bal = 0
                for row in sortable_txns:

                    if row[2] == account:
                        current_bal = f'{float(current_bal) + float(row[4]):,.2f}'
                        # row.append(current_bal)
                        x.add_row([
                            # row[0],
                            row[1],
                            row[2],
                            row[3],
                            row[4],
                            current_bal
                        ])

                    row_count += 1

            current_account += 1

        print(x)

    def read_csv(self):
        # This will print to the command line
        # print('read_csv function was called!')

        csv_file = open('transactions.csv')
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        x = PrettyTable()
        x.field_names = ["Id", "Date", "Account", "Description", "Amount"]

        for row in csv_reader:

            if line_count > 0:
                row.insert(0, line_count)

                x.add_row(row)

            line_count += 1

        print(x)

        csv_file.close()

    def create_new_file(self, date, account, description, amount):
        # This will create a new file and set it to the transactions_file variable
        with open('transactions.csv', mode='w', newline='') as transactions_file:
            fieldnames = ['date', 'account', 'description', 'amount']
            writer = csv.DictWriter(transactions_file, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerow({
                'date': date,
                'account': account,
                'description': description,
                'amount': amount
            })

            transactions_file.close()

    def update_csv(self):
        # This will print to the command line
        # print('add_to_csv function was called!')
        with open('transactions.csv', 'w', encoding='UTF8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            fieldnames = ['date', 'account', 'description', 'amount']
            writer.writerow(fieldnames)

            for row in self.transactions:
                writer.writerow([
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                ])

    def ask_date_question(self):
        # This will set the date variable
        date = input('\n\nWhat is the date of your transaction (MM/DD/YYYY)? ')

        valid = re.match(r"[0-1][0-9]\/[0-3][0-9]\/\d\d\d\d", date)

        if valid:

            return date

        else:

            print(f'The value "{date}" is invalid. Please enter the date in this format MM/DD/YYYY.')
            return self.ask_date_question()

    def ask_transaction_questions(self, update=False):
        # This will set the date variable
        date = self.ask_date_question()

        # This will set the description variable
        description = input('\n\nWhat is the description of your transaction? ')

        # This will set the amount variable
        amount = input('\n\nHow much is the transaction for? $')

        # This will set the account variable
        account = input('\n\nWhat account does this transaction belong to?\na) Wells Fargo - Danny Jones' \
                        '\nb) Chime - Porsche Jones\nc) Chime Credit Card - Porsche Jones\nd) EBT - Porsche Jones'
                        '\n\nYour option is: ')

        # This will set the account_name variable
        account_name = ''

        if account == 'a':
            account_name = 'Wells Fargo - Danny Jones'
        elif account == 'b':
            account_name = 'Chime - Porsche Jones'
        elif account == 'c':
            account_name = 'Chime Credit Card - Porsche Jones'
        elif account == 'd':
            account_name = 'EBT - Porsche Jones'
        else:
            account_name = 'You did not select an account that exists.'

        word = 'input'

        if update == True:
            word = 'update'

        confirmation = input(
            f'\n\nWould you like to {word} the following transaction?\n\n'
            f'date => {date}\ndescription => {description}\n'
            f'amount => {amount}\n'
            f'account => {account_name}\n\n'
            f''
            f'yes or no: ')

        if confirmation == 'yes':

            return {
                'date': date,
                'description': description,
                'amount': amount,
                'account': account_name,
            }

        else:
            self.ask_transaction_questions()

    def add_a_transaction(self):
        # This will print to the command line
        # print('add_a_transaction function was called!')

        data = self.ask_transaction_questions()

        date = data['date']
        account = data['account']
        description = data['description']
        amount = data['amount']

        self.transactions.append([
            len(self.transactions) + 1,
            date,
            account,
            description,
            amount,

        ])

        self.update_csv()

        self.print_transactions()

    def update_csv_row(self, selected_transaction, date, description, amount, account_name):
        # This will print to the command line
        # print('update_csv_row function was called!')

        csv_reader = get_csv_contents()
        line_count = 0
        new_file = []
        for row in csv_reader:

            if str(line_count) == selected_transaction:
                new_file.append({
                    'date': date,
                    'account': account_name,
                    'description': description,
                    'amount': amount
                })
            else:
                new_file.append({
                    'date': row[0],
                    'account': row[1],
                    'description': row[2],
                    'amount': row[3]
                })
            line_count += 1

        with open('transactions.csv', mode='w', newline='') as transactions_file:
            fieldnames = ['date', 'account', 'description', 'amount']
            writer = csv.DictWriter(transactions_file, fieldnames=fieldnames)

            for row in new_file:
                writer.writerow({
                    'date': row['date'],
                    'account': row['account'],
                    'description': row['description'],
                    'amount': row['amount']
                })

            read_csv()

    def delete_csv_row(self, selected_transaction):
        # This will print to the command line
        # print('delete_csv_row function was called!')

        line_count = 0
        new_transactions = []
        for item in self.transactions:

            if str(item[0]) != str(selected_transaction):
                new_transactions.append(item)

        self.transactions = new_transactions

        self.update_csv()

        self.print_transactions()

    def get_transaction(self, selected_transaction):

        line_count = 1
        for row in self.transactions:

            if str(line_count) == selected_transaction:
                return {
                    'date': row[1],
                    'account': row[2],
                    'description': row[3],
                    'amount': row[4]
                }

            line_count += 1

    def update_a_transaction(self):
        """
        Updates a transaction
        """
        # print('update_a_transaction function was called!')
        is_file_empty = len(self.transactions) == 0

        if not is_file_empty:
            # Show the transactions
            self.print_transactions()

            # Set a variable for a selected transaction
            selected_transaction = input('\n\nWhat treansaction would you like to update?\n\nSelected transaction id: ')

            retrieved_transaction = self.get_transaction(selected_transaction)

            print(
                f'\n\nThis is the transaction you will like to update.\n\n'
                f'date => {retrieved_transaction["date"]}\n'
                f'description => {retrieved_transaction["description"]}\n'
                f'amount => {retrieved_transaction["amount"]}\n'
                f'account => {retrieved_transaction["account"]}')

            data = self.ask_transaction_questions(update=True)

            date = data['date']
            description = data['description']
            amount = data['amount']
            account_name = data['account']

            self.transactions[int(selected_transaction) - 1] = [
                selected_transaction,
                date,
                account_name,
                description,
                amount
            ]

            self.update_csv()

            self.print_transactions()
        else:

            print('You ain\'t got no damn transactions!!!!!')

    def delete_a_transaction(self):
        # print('delete_a_transaction function was called!')
        # Show the transactions
        self.print_transactions()

        # Set a variable for a selected transaction
        selected_transaction = input('\n\nWhat transaction would you like to delete?\n\nSelected transaction id: ')

        retrieved_transaction = self.get_transaction(selected_transaction)

        if retrieved_transaction == None:
            return retrieved_transaction

        is_delete_transaction = input(
            f'\n\nAre you sure you will like to delete the following transaction?\n\n'
            f'date => {retrieved_transaction["date"]}\n'
            f'description => {retrieved_transaction["description"]}\n'
            f'amount => {retrieved_transaction["amount"]}\n'
            f'account => {retrieved_transaction["account"]}\n\n'
            f'yes or naw: ')

        if is_delete_transaction == 'yes':

            self.delete_csv_row(selected_transaction)

            print('\n\nYour transaction has been deleted.')

        elif is_delete_transaction == 'naw':
            pass
        else:
            print(
                'I don\'t understand why you put something else. Now im gonna go to the main menu. My name is spitful!!!!')

    def start(self):
        # Use a breakpoint in the code line below to debug your script.
        while_count = 0
        while True:
            option = input('\n\nselect an option:'
                           '\na) add a transaction'
                           '\nb) update a transaction'
                           '\nc) delete a transaction' \
                           '\nd) print statement'
                           '\n\n\nmy option: ')

            if option == 'a':
                print('\n\nYou selected to add a transaction')
                self.add_a_transaction()
            elif option == 'b':
                print('\n\nYou selected to update a transaction')
                self.update_a_transaction()
            elif option == 'c':
                print('\n\nYou selected to delete a transaction')
                self.delete_a_transaction()
            elif option == 'd':

                self.print_statement()

            else:
                print(f'\n\nThere is no option for option {option}')

    def print_transactions(self):
        x = PrettyTable()
        x.field_names = ["Id", "Date", "Account", "Description", "Amount"]

        current_bal = 0
        for row in self.transactions:
            # edited_row = row
            # current_bal = f'{float(current_bal) + float(row[4]):,.2f}'
            # edited_row.append(current_bal)
            x.add_row(row)

        print(x)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    transaction_program = transaction_manager()
    transaction_program.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
