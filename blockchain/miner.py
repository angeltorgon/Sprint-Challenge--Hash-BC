import hashlib
import requests
import json

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """
    print(last_proof)
    start = timer()
    print("Searching for next proof")
    proof = 0
    #  TODO: Your code here
    # make api ruquest to get chain
    #node = "https://lambda-coin.herokuapp.com/api"
    #r = requests.get(url=node + "/full_chain")
    #data = r.json()

    ## get last block from chain 
    #last_block = data.get("chain")[-1]

    ## generate previous hash
    #block_string = json.dumps(last_block, sort_keys=True).encode()
    prev_hash = hashlib.sha256(f"{last_proof}".encode()).hexdigest()
    
    # check if proof is valid
    while valid_proof(prev_hash, proof) is False:
        proof += 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
    # TODO: Your code here!
    # generate new guess 
    guess = f"{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # check if  fist 6 digits of guess hash is the same as the last 6 characters of guess
    return last_hash[-6:] == guess_hash[:6] 


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
