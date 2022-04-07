# global vars

genesis_block = {'last_hash': '', 'index': 0, 'transactions': []}
blockchain = [genesis_block]
open_transactions = []
owner = 'Sean'
participants = {'Sean'}
MINING_REWARD = 5


# Blockchain functions

def hash_block(block):
    """ Calculate a new hash based on the block"""
    return '-'.join([str(block[key]) for key in block])


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

    if verify_transaction(transaction):
        open_transactions.append(transaction)
    else:
        return False

    participants.add(sender)
    participants.add(recipient)


def mine_block():
    last_block = blockchain[-1]
    new_hash = hash_block(last_block)

    block = {'last_hash': new_hash, 'index': len(
        blockchain), 'transactions': open_transactions}
    blockchain.append(block)

    # issue reward
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD,
    }
    open_transactions.append(reward_transaction)

    return True


def verify_blockchain():
    """ Return True if all blocks are valid. A block is valid if its item 0 is identical to the previous block. """
    for idx, block in enumerate(blockchain):
        if idx == 0:
            continue
        if block['last_hash'] != hash_block(blockchain[idx - 1]):
            return False
    return True


def verify_transaction(transaction):
    """ Return True if transaction is valid."""
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

# User functions


def get_user_transaction_input():
    """ Get user input and return it as float."""
    tx_recipient = input('Specify the recipient:')
    tx_amount = float(input('Enter transaction amount: '))
    return tx_recipient, tx_amount


def get_choice():
    """ Get user input to know what action to perform."""
    choice = input('')
    return choice


def get_balance(participant):
    """Calculate the balance for one participant."""
    # get total as sender
    blocks_totals = [[transaction['amount'] for transaction in block['transactions']
                     if transaction['sender'] == participant] for block in blockchain]
    total_sent = 0
    for block_totals in blocks_totals:
        if len(block_totals) > 0:
            total_sent += sum(block_totals)

    # get total as recipient
    blocks_totals = [[transaction['amount'] for transaction in block['transactions']
                     if transaction['recipient'] == participant] for block in blockchain]
    total_received = 0
    for block_totals in blocks_totals:
        if len(block_totals) > 0:
            total_received += sum(block_totals)

    return total_received - total_sent

# Utility functions


def display_blockchain_by_block():
    """ Display all blocks in order on screen."""
    print("------------")
    for idx, block in enumerate(blockchain):
        print("Block " + str(idx) + ": " + str(block))
        if idx < len(blockchain) - 1:
            print("⬇")

    print("------------")


def output(value):
    """ Display a formatted message in the terminal."""
    print("------------")
    print(value)
    print("------------")


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
        if mine_block():
            open_transactions = []
    elif choice == "0":
        # show the blockchain
        display_blockchain_by_block()
        print("Your balance is now " + str(get_balance('Sean')))
    else:
        # invalid choice
        output("\"" + choice + "\" is an invalid choice.")

    # verify the chain after all actions
    if not verify_blockchain():
        print("The blockchain has become corrupt. Exiting.")
        break
