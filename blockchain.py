import hashlib
from collections import OrderedDict
from functions import hash_block
import json


# global vars

genesis_block = {'last_hash': '', 'index': 0, 'transactions': [], 'proof': 100}
blockchain = [genesis_block]
open_transactions = []
owner = 'Sean'
participants = {'Sean'}
MINING_REWARD = 5


# Blockchain functions

def add_transaction(recipient, sender=owner, amount=1.0):
    """ Add a float value to the blockchain.
    Arguments:
        :sender: the float value to be added.
        :recipient: the previous transaction needed for the blockchain.
    """
    # transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}

    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
    else:
        return False

    participants.add(sender)
    participants.add(recipient)
    save_data()
    return True


def verify_transaction(transaction):
    """ Return True if transaction is valid."""
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def mine_block():
    last_block = blockchain[-1]
    new_hash = hash_block(last_block)
    proof = proof_of_work()

    # issue reward
    reward_transaction = OrderedDict([
        ('sender', 'MINING'),
        ('recipient', owner),
        ('amount', MINING_REWARD),
    ])
    copied_txs = open_transactions[:]
    copied_txs.append(reward_transaction)

    block = {'last_hash': new_hash, 'index': len(
        blockchain), 'transactions': copied_txs, 'proof': proof}
    blockchain.append(block)

    return True


def valid_proof(txs, hash, proof):
    """Validate a proof of work"""
    guess = (str(txs) + str(hash) + str(proof)).encode()
    ghash = hashlib.sha256(guess).hexdigest()
    return ghash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def verify_blockchain():
    """ Return True if all blocks are valid. A block is valid if its item 0 is identical to the previous block. """
    for idx, block in enumerate(blockchain):
        if idx == 0:
            continue
        if block['last_hash'] != hash_block(blockchain[idx - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['last_hash'], block['proof']):
            return False
    return True


def get_last_blockchain_value():
    """Return the last block in the current chain."""
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


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
    open_totals = [transaction['amount']
                   for transaction in open_transactions if transaction['sender'] == participant]
    blocks_totals.append(open_totals)
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


def save_data():
    """Write blockchain to disk."""
    with open('blockchain.txt', mode='w') as file:
        file.write(json.dumps(blockchain))
        file.write('\n')
        file.write(json.dumps(open_transactions))


def load_data():
    """Load blockchain and open transactions from text file."""
    with open('blockchain.txt', mode='r') as file:
        file_content = file.readlines()
        if (len(file_content) <= 0):
            return

        global blockchain
        global open_transactions

        blockchain = json.loads(file_content[0:-1])
        updated_blockchain = []
        for block in blockchain:
            updated_block = {
                'last_hash': block['last_hash'],
                'index': block['index'],
                'proof': block['proof'],
                'transactions': [
                    OrderedDict([
                        ('sender', tx['sender']),
                        ('recipient', tx['recipient']),
                        ('amount', tx['amount']),
                    ])
                    for tx in block['transactions']
                ]
            }
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain

        open_transactions = json.loads(file_content[-1])
        updated_transactions = []
        for tx in open_transactions:
            updated_transaction = OrderedDict([
                ('sender', tx['sender']),
                ('recipient', tx['recipient']),
                ('amount', tx['amount']),
            ])
            updated_transactions.append(updated_transaction)
        open_transactions = updated_transactions


# main loop
print("Your options:")
load_data()
while True:
    print("1 - add a transaction.")
    print("2 - mine block.")
    print("0 - show the blockchain.")
    choice = get_choice()
    if choice == "1":
        # add a transaction
        tx_data = get_user_transaction_input()
        tx_recipient, tx_amount = tx_data
        if not add_transaction(tx_recipient, amount=tx_amount):
            print('Unable to add transaction.')
    elif choice == '2':
        # mine block
        if mine_block():
            open_transactions = []
            save_data()

    elif choice == "0":
        # show the blockchain
        display_blockchain_by_block()
        print("Your balance is now {:.2f}".format(get_balance('Sean')))
    else:
        # invalid choice
        output("\"" + choice + "\" is an invalid choice.")

    # verify the chain after all actions
    if not verify_blockchain():
        print("The blockchain has become corrupt. Exiting.")
        break
