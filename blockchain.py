blockchain = [[1]]

# Utility functions


def get_choice():
    """ Get user input to know what action to perform."""
    choice = input('')
    return choice


def display_blockchain_by_block():
    """ Display all blocks in order on screen."""
    print("------------")
    for idx, block in enumerate(blockchain):
        print("Block " + str(idx) + ": " + str(block))
        if idx < len(blockchain) - 1:
            print("⬇")

    print("------------")


def get_user_transaction_input():
    """ Get user input and return it as float."""
    transaction_amount = float(input('Enter transaction amount: '))
    return transaction_amount


def output(value):
    """ Display a formatted message in the terminal."""
    print("------------")
    print(value)
    print("------------")


# Blockchain logic functions


def get_last_blockchain_value():
    """Return the last block in the current chain."""
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


def add_value(transaction_amount, last_transaction):
    """ Add a float value to the blockchain.
    Arguments:
        :transaction_amount: the float value to be added.
        :last_transaction: the previous transaction needed for the blockchain.
    """
    if last_transaction == None:
        last_transaction = [1]
    new_block = [last_transaction, transaction_amount]
    blockchain.append(new_block)
    output("Added " + str(new_block) + " to the blockchain.")


def verify_blockchain():
    """ Return True if all blocks are valid. A block is valid if its item 0 is identical to the previous block. """
    for idx, block in enumerate(blockchain):
        if idx - 1 >= 0 and block[0] != blockchain[idx - 1]:
            return False
    return True


# main loop

print("Your options:")
while True:
    print("1 - add a transaction.")
    print("2 - show the blockchain.")
    choice = get_choice()
    if choice == "1":
        # add a transaction
        transaction_amount = get_user_transaction_input()
        add_value(transaction_amount, get_last_blockchain_value())
    elif choice == "2":
        # show the blockchain
        display_blockchain_by_block()
    else:
        # invalid choice
        output("\"" + choice + "\" is an invalid choice.")

    # verify the chain after all actions
    if not verify_blockchain():
        print("The blockchain has become corrupt. Exiting.")
        break
