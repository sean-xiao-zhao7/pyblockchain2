# global vars

genesis_block = {'last_hash': '', 'index': 0, 'transactions': []}
blockchain = [genesis_block]
open_transactions = []
owner = 'Sean'

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
    tx_recipient = input('Specify the recipient:')
    tx_amount = float(input('Enter transaction amount: '))
    return tx_recipient, tx_amount


def output(value):
    """ Display a formatted message in the terminal."""
    print("------------")
    print(value)
    print("------------")


def hash_block(block):
    """ Calculate a new hash based on the block"""
    return '-'.join([str(block[key]) for key in block])


# Blockchain logic functions


def get_last_blockchain_value():
    """Return the last block in the current chain."""
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Add a float value to the blockchain.
    Arguments:
        :sender: the float value to be added.
        :recipient: the previous transaction needed for the blockchain.
    """
    transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    open_transactions.append(transaction)


def mine_block():
    last_block = blockchain[-1]
    new_hash = hash_block(last_block)
    block = {'last_hash': new_hash, 'index': len(
        blockchain), 'transactions': open_transactions}
    blockchain.append(block)


def verify_blockchain():
    """ Return True if all blocks are valid. A block is valid if its item 0 is identical to the previous block. """
    for idx, block in enumerate(blockchain):
        if idx == 0:
            continue
        if block['last_hash'] != hash_block(blockchain[idx - 1]):
            return False
    return True


# main loop
print("Your options:")
while True:
    print("1 - add a transaction.")
    print("2 - mine block.")
    print("0 - show the blockchain.")
    choice = get_choice()
    if choice == "1":
        # add a transaction
        tx_data = get_user_transaction_input()
        tx_recipient, tx_amount = tx_data
        add_transaction(tx_recipient, amount=tx_amount)
    elif choice == '2':
        # mine block
        mine_block()
    elif choice == "0":
        # show the blockchain
        display_blockchain_by_block()
    else:
        # invalid choice
        output("\"" + choice + "\" is an invalid choice.")

    # verify the chain after all actions
    if not verify_blockchain():
        print("The blockchain has become corrupt. Exiting.")
        break
