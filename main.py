import csv
import pprint

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import shutil
from os.path import exists
from tempfile import NamedTemporaryFile


def read_csv():
    # This will print to the command line
    # print('read_csv function was called!')

    with open('transactions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:

            if line_count == 0:
                row.insert(0, 'id')
            else:
                row.insert(0, line_count)

            print(row)

            line_count += 1

        csv_file.close()


def create_new_file(date, account, description, amount):
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

        read_csv()


def add_to_csv(date, description, amount, account_name):
    # This will print to the command line
    print('add_to_csv function was called!')
    previous_rows = []

    if not exists('transactions.csv'):
        create_new_file(date, account_name, description, amount)
    else:

        # This will create a new file and set it to the transactions_file variable
        with open('transactions.csv', mode='a', newline='') as transactions_file:
            # fieldnames = ['date', 'account', 'description', 'amount']
            writer = csv.writer(transactions_file)
            # writer.writeheader()

            # for previous_row in previous_rows:
            #     writer.writerow(previous_row)

            writer.writerow([
                date,
                account_name,
                description,
                amount
            ])

            transactions_file.close()

            read_csv()


def ask_date_question():
    # This will set the date variable
    date = input('\n\nWhat is the date of your transaction (MM/DD/YYYY)? ')

    valid = re.match(r"[0-1][0-9]\/[0-3][0-9]\/[1900-2022]", date)

    if valid:

        return date

    else:

        print(f'The value "{date}" is invalid. Please enter the date in this format MM/DD/YYYY.')
        ask_date_question()


def ask_transaction_questions():
    # This will set the date variable
    date = ask_date_question()

    # This will set the description variable
    description = input('\n\nWhat is the description of your transaction? ')

    # This will set the amount variable
    amount = input('\n\nHow much is the transaction for? $')

    # This will set the account variable
    account = input('\n\nWhat account does this transaction belong to?\na) Wells Fargo - Danny Jones' \
                    '\nb) Chime - Porsche Jones\nc) Chime Credit Card - Porsche Jones\n\nYour option is: ')

    # This will set the account_name variable
    account_name = ''

    if account == 'a':
        account_name = 'Wells Fargo - Danny Jones'
    elif account == 'b':
        account_name = 'Chime - Porsche Jones'
    elif account == 'c':
        account_name = 'Chime Credit Card - Porsche Jones'
    else:
        account_name = 'You did not select an account that exists.'

    confirmation = input(
        f'\n\nWould you like to input the following transaction? Yes or No?\n\ndate => {date}\ndescription => {description}\namount => {amount}\naccount => {account_name}\n\nMy answer is: ')

    if confirmation == 'yes':

        return {
            'date': date,
            'description': description,
            'amount': amount,
            'account': account_name,
        }

    else:
        ask_transaction_questions()


def add_a_transaction():
    # This will print to the command line
    # print('add_a_transaction function was called!')

    data = ask_transaction_questions()

    date = data['date']
    description = data['description']
    amount = data['amount']
    account = data['account']

    add_to_csv(date, description, amount, account)


def update_csv_row(selected_transaction, date, description, amount, account_name):
    # This will print to the command line
    print('update_csv_row function was called!')

    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open('transactions.csv') as csv_file:

        fieldnames = ['date', 'account', 'description', 'amount']
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
        line_count = 0

        for row in csv_reader:

            if str(line_count) == selected_transaction:
                csv_writer.writerow({
                    'date': date,
                    'account': account_name,
                    'description': description,
                    'amount': amount
                })

                break
            else:
                csv_writer.writerow({
                    'date': row[0],
                    'account': row[1],
                    'description': row[2],
                    'amount': row[3]
                })
            line_count += 1

    csv_file.close()

    shutil.move(tempfile.name, 'transactions.csv')

def update_a_transaction():
    print('update_a_transaction function was called!')
    # Show the transactions
    read_csv()

    # Set a variable for a selected transaction
    selected_transaction = input('\n\nWhat treansaction would you like to update?\n\nSelected transaction id: ')

    data = ask_transaction_questions()

    date = data['date']
    description = data['description']
    amount = data['amount']
    account_name = data['account']

    update_csv_row(selected_transaction,date,description,amount,account_name)


def delete_a_transaction():
    print('delete_a_transaction function was called!')


def transaction_program():
    # Use a breakpoint in the code line below to debug your script.
    while_count = 0
    while True:
        option = input('\n\nselect an option:\na) add a transaction\nb) update a transaction\nc) delete a transaction' \
                       '\n\n\nmy option: ')

        if option == 'a':
            print('\n\nYou selected to add a transaction')
            add_a_transaction()
        elif option == 'b':
            print('\n\nYou selected to update a transaction')
            update_a_transaction()
        elif option == 'c':
            print('\n\nYou selected to delete a transaction')
            delete_a_transaction()
        else:
            print(f'\n\nThere is no option for option {option}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    transaction_program()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
