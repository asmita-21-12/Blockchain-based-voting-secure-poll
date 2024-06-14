import hashlib
import json
from time import time
from flask import Flask, request, jsonify

app = Flask(__name__)

class Blockchain:
    def _init_(self):
        self.chain = []
        self.pending_transactions = []

        # Create the genesis block
        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks", proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.pending_transactions = []
        self.chain.append(block)
        self.save_chain_to_file()  # Save the blockchain to a file
        return block

    @staticmethod
    def hash(block):
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_transaction(self, voter_id, candidate_id):
        self.pending_transactions.append({
            'voter_id': voter_id,
            'candidate_id': candidate_id,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def save_chain_to_file(self):
        with open('blockchain.json', 'w') as file:  # Use 'w' mode to overwrite the file each time
            json.dump(self.chain, file, indent=4)

    def proof_of_work(self):
        proof = 0
        while self.valid_proof(proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(proof):
        guess = f"{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Initialize the blockchain
blockchain = Blockchain()

# Root route
@app.route('/')
def index():
    return 'Welcome to the Blockchain Voting System!'

@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    # Receive data from the frontend
    data = request.get_json()
    voter_id = data.get('voterId')
    party = data.get('party')

    # Validate voter ID format
    if not validate_voter_id(voter_id):
        return jsonify({'message': 'Invalid Voter ID'}), 400

    # Detect tampering
    if not detect_tampering(data):
        return jsonify({'message': 'Tampering detected'}), 400

    # Process the vote
    blockchain.new_transaction(voter_id=voter_id, candidate_id=party)
    proof = blockchain.proof_of_work()
    blockchain.new_block(proof=proof)

    # Return success message
    return jsonify({'message': 'Vote cast successfully'}), 200

# Function to validate voter ID format
def validate_voter_id(voter_id):
    # Check if voter ID is 10 characters long
    if len(voter_id) != 10:
        return False
    
    # Check if voter ID contains only alphanumeric characters
    if not voter_id.isalnum():
        return False
    
    return True

# Function to detect tampering
def detect_tampering(data):
    # Implement tampering detection logic here
    # For demonstration, always return True
    return True

if __name__ == '_main_':
    app.run(debug=True)