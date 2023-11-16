import json
from web3 import Web3

#connect to the local ethereum blockchain
provider = Web3.HTTPProvider('http://127.0.0.1:8545', request_kwargs={'timeout': 600})
# Web3(Web3.HTTPProvider(endpoint_uri=http://127.0.0.1:8545,request_kwargs={'timeout': 600})

w3 = Web3(provider)
#check if ethereum is connected
print(w3.is_connected())

#replace the address with your contract address (!very important)
deployed_contract_address = '0x2a9317c9dc548E3848a89817759095dD55cc80DC'

#path of the contract json file. edit it with your contract json file
compiled_contract_path ="build/contracts/Payment.json"
with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']
contract = w3.eth.contract(address = deployed_contract_address, abi = contract_abi)


'''
#Calling a contract function createAcc(uint,uint,uint)
txn_receipt = contract.functions.createAcc(1, 2, 5).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
txn_receipt_json = json.loads(w3.to_json(txn_receipt))
print(txn_receipt_json) # print transaction hash

# print block info that has the transaction)
print(w3.eth.get_transaction(txn_receipt_json)) 

#Call a read only contract function by replacing transact() with call()

'''

#Add your Code here
import networkx as nx
import matplotlib.pyplot as plt

n_nodes = 100
exponent = 2.5

G = nx.barabasi_albert_graph(n_nodes, 2, seed=0)
assert nx.is_connected(G), "Graph is not connected"

all_edges = list(G.edges())

# Print the number of edges
print("Number of edges:", len(all_edges))

#sanity check for connected
print('Is connected?', nx.is_connected(G))

#sanity check for degree distribution
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
print("Degree sequence", degree_sequence)


for i in range(n_nodes):
    user_name = "user" + str(i)
    txn_receipt = contract.functions.registerUser(i, user_name).transact({'txType':"0x3", 'from':w3.eth.accounts[0]})  


import numpy as np
np.random.seed(10)
for edge1 in all_edges:
    balance = round(np.random.exponential(10) / 2)
    txn_receipt = contract.functions.createAcc(edge1[0], edge1[1], int(balance)).transact({'txType':"0x3", 'from':w3.eth.accounts[0]})

from tqdm import tqdm
ratio = []
for i in range(10):
    num_success = 0
    num_fail = 0
    total_trans = 100

    for j in tqdm(range(total_trans)):
        sender = 0
        receiver = 0
        while sender == receiver:
            sender = np.random.randint(0, n_nodes)
            receiver = np.random.randint(0, n_nodes)

        txn_receipt = contract.functions.sendAmount(sender, receiver).transact({'txType':"0x3", 'from':w3.eth.accounts[0]})
        success = contract.functions.check_success().call({'txType':"0x3", 'from':w3.eth.accounts[0]})

        if success:
            num_success += 1
        else:
            num_fail += 1

    print("Total Transactions :",(i+1)*total_trans)
    print(num_success, num_fail)
    print(num_success / total_trans)
    ratio.append(num_success / total_trans)

for edge1 in all_edges:
    balance = round(np.random.exponential(10) / 2)
    txn_receipt = contract.functions.closeAccount(edge1[0], edge1[1]).transact({'txType':"0x3", 'from':w3.eth.accounts[0]})

print(ratio)

