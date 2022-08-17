import csv
import pprint
from prettytable import PrettyTable

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import shutil
from os.path import exists
from tempfile import NamedTemporaryFile


def print_statement():

    csv_content = get_csv_contents()

    accounts = []

    row_count = 0
    for row in csv_content:

        if row_count > 0 and row[1] not in accounts:
            accounts.append(row[1])

        row_count += 1

    string_to_print_in_input = ''

    current_account = 0
    for account in accounts:
        string_to_print_in_input += f'\n{current_account}) {account}'

        current_account += 1

    selected_account = input(f'Select an account:\n{string_to_print_in_input}\n\nYour selection: ')

    current_account = 0

    x = PrettyTable()
    x.field_names = ["Date", "Account", "Description", "Amount", "Balance"]

    for account in accounts:

        if str(current_account) == str(selected_account):
            print(f'\n\nYou selected to print a statement for the "{account}" account.')

            csv_content2 = get_csv_contents()
            current_bal = 0
            for row in csv_content2:

                print(row)

                if row_count > 0 and row[1] == account:
                    current_bal = float(current_bal) + float(row[3])
                    row.append(current_bal)
                    x.add_row(row)

                row_count += 1



        current_account += 1

    print(x)

def read_csv():
    # This will print to the command line
    # print('read_csv function was called!')

    with open('transactions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        x = PrettyTable()
        x.field_names = ["Id","Date", "Account", "Description", "Amount"]

        for row in csv_reader:

            if line_count > 0:
                row.insert(0, line_count)

                x.add_row(row)

            line_count += 1

        print(x)


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


def get_csv_contents():
    # This will print to the command line
    # print('read_csv function was called!')
    csv_file = open('transactions.csv')
    csv_reader = csv.reader(csv_file, delimiter=',')

    return csv_reader


def add_to_csv(date, description, amount, account_name):
    # This will print to the command line
    print('add_to_csv function was called!')
    previous_rows = []
    contents_list = list(get_csv_contents()) if exists('transactions.csv') else []
    is_file_empty = len(contents_list) == 0

    if not exists('transactions.csv') or is_file_empty:
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

    valid = re.match(r"[0-1][0-9]\/[0-3][0-9]\/\d\d\d\d", date)

    if valid:

        return date

    else:

        print(f'The value "{date}" is invalid. Please enter the date in this format MM/DD/YYYY.')
        return ask_date_question()


def ask_transaction_questions(update=False):
    # This will set the date variable
    date = ask_date_question()

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
    # print('update_csv_row function was called!')

    csv_reader = get_csv_contents()
    line_count = 0
    new_file = []
    for row in csv_reader:

        if str(line_count) == selected_transaction:
            new_file.append( {
                'date': date,
                'account': account_name,
                'description': description,
                'amount': amount
            })
        else:
            new_file.append( {
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





def get_transaction(selected_transaction):
    csv_reader = get_csv_contents()
    line_count = 0
    for row in csv_reader:

        if str(line_count) == selected_transaction:
            return {
                'date': row[0],
                'account': row[1],
                'description': row[2],
                'amount': row[3]
            }

        line_count +=1


def update_a_transaction():
    """
    Updates a transaction
    """
    # print('update_a_transaction function was called!')

    contents_list = list(get_csv_contents())
    is_file_empty = len(contents_list) == 1



    if not is_file_empty:
        # Show the transactions
        read_csv()

        # Set a variable for a selected transaction
        selected_transaction = input('\n\nWhat treansaction would you like to update?\n\nSelected transaction id: ')

        retrieved_transaction = get_transaction(selected_transaction)

        print(
            f'\n\nWould you like to input the following transaction?\n\n'
            f'date => {retrieved_transaction["date"]}\n'
            f'description => {retrieved_transaction["description"]}\n'
            f'amount => {retrieved_transaction["amount"]}\n'
            f'account => {retrieved_transaction["account"]}')

        data = ask_transaction_questions(update=True)

        date = data['date']
        description = data['description']
        amount = data['amount']
        account_name = data['account']

        update_csv_row(selected_transaction, date, description, amount, account_name)
    else:

        print('You ain\'t got no damn transactions!!!!!')


def delete_a_transaction():
    print('delete_a_transaction function was called!')


def transaction_program():
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
            add_a_transaction()
        elif option == 'b':
            print('\n\nYou selected to update a transaction')
            update_a_transaction()
        elif option == 'c':
            print('\n\nYou selected to delete a transaction')
            delete_a_transaction()
        elif option == 'd':

            print_statement()

        else:
            print(f'\n\nThere is no option for option {option}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    transaction_program()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
