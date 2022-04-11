import hashlib
import json


def hash_block(block):
    """ Calculate a new hash based on the block"""
    return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
