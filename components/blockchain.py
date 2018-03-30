# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 22:36:17 2018

@author: Reezius
"""

# libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# ==BUILD==
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, prev_hash = '0')
        
    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash,
                 #'data': 
                 }
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1]
        
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            hash_operation = hashlib.sha512(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha512(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha512(str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            prev_block = block
            block_index += 1
            return True
        #'prev' is short for 'previous', because sometimes being lazy can pay off
        
# ==MINING==       
# 1- creating the web app
app = Flask(__name__)

# 2- creating the blockchain
blockchain = Blockchain()

#3- mining a block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(proof, prev_hash)
    response = {'message': 'BLOCK CREATED: Congratulations, miner!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'prev_hash': block['prev_hash']}
    return jsonify(response), 200

#4 - display full blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

#5- running the web app
app.run(host = '0.0.0.0', port = 5000)
"""
-find a good http client program to see what's happening w the mining
-look up "http://127.0.0.1:5000/get_chain" w GET request
-see what's happening
====
-don't forget this too: http://127.0.0.1:5000/mine_block
"""