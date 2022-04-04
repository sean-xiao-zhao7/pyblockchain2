blockchain = [[1]]

# Utility functions


def get_initial_choice():
    choice = input('')
    return choice


def display_blockchain_by_block():
    print("----")
    for idx, block in enumerate(blockchain):
        print("Block " + str(idx) + ": " + str(block))
        if idx < len(blockchain) - 1:
            print("⬇")

    print("----")

# Blockchain logic functions


def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    """ Add a float value to the blockchain.
    Arguments:
        :transaction_amount: the float value to be added.
        :last_transaction: the previous transaction needed for the blockchain.
    """
    blockchain.append([last_transaction, transaction_amount])


def get_user_transaction_input():
    """ Get user input and return it as float."""
    transaction_amount = float(input('Enter transaction amount: '))
    return transaction_amount

# main loop


transaction_amount = get_user_transaction_input()
add_value(transaction_amount)
while True:
    print("Your options:")
    print("1 - add a transaction.")
    print("2 - show the blockchain.")
    choice = get_initial_choice()
    if choice == "1":
        transaction_amount = get_user_transaction_input()
        add_value(transaction_amount)
    elif choice == "2":
        display_blockchain_by_block()
