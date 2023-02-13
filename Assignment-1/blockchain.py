import argparse
import random
from numpy import random as rd
import copy 
from queue import PriorityQueue
from tqdm import tqdm 

kb = 1 # kilobyte
rho = None # speed of light delay
Mbps = 1000*1000 # value of Mbps
kbbits = 1000 # value of kbbits
interarrivalTime = 10 # seconds
miningFee = 50 
noOfTransactions = 0 # total number of transaction taken place
noOfBlocks = 0 # total number of blocks formed

class Transaction:
    
    size = 1 * kb

    def __str__(self):
        return str({ 'txnID': self.txnID, 'idx': self.idx, 'idy': self.idy, 'coins': self.coins}) 

    def __init__(self, idx, idy, coins):
        global noOfTransactions
        noOfTransactions = noOfTransactions + 1
        self.txnID = noOfTransactions 
        self.idx = idx
        self.idy = idy
        self.coins = coins

class Block:
    blkID : int
    transactionList : list[Transaction]

    def __str__(self):
        return str(self.blkID) + ", " + (str(self.prevBlock.blkID) if self.prevBlock else str(0)) + ", " + (str(self.transactionList[0].idy) if len(self.transactionList) else str(-1))
        # return str(self.blkID) + "->" + (str(self.prevBlock.blkID) if self.prevBlock else str(0)) + "-".join([str(tx) for tx in self.transactionList])

    def store_info(self):
        f = open("block_data.txt", "a")
        f.write(str(self.blkID) + "->" + (str(self.prevBlock.blkID) if self.prevBlock else str(0)) + str([str(tx) for tx in self.transactionList]) + "\n")
        f.close()

    def __init__(self, transactionList: list, prevBlock):
        global noOfBlocks
        noOfBlocks = noOfBlocks + 1
        self.blkID = noOfBlocks
        self.transactionList = transactionList
        self.prevBlock = prevBlock
        self.store_info()

class Peer:
    connectedPeers :list
    transactionList : list[Transaction]
    blockchain : list[Block] 
    timelist : list[float]
    longestChain: Block
    longestChainLength: int 

    def __str__(self):
        return "\n".join([ str(block) + ", " + str(self.timelist[idx]) for idx, block in enumerate(self.blockchain)])

    def validTransaction(self, transaction: Transaction):
        block = copy.deepcopy(self.longestChain)
        while (block):
            for tx in block.transactionList:
                if transaction.txnID == tx.txnID:
                    return False
            block = block.prevBlock
        return True

    def generateBlock(self):
        txList = []
        txList.append(Transaction(None, self.uID, miningFee))
        balance = {}
        for id in range(self.numPeers):
            balance[id] = self.calculateBalance(id)
        for transaction in self.transactionList:
            if self.validTransaction(transaction) and balance[transaction.idx] >= transaction.coins:
                balance[transaction.idx] -= transaction.coins
                balance[transaction.idy] += transaction.coins
                txList.append(transaction)
            if len(txList) == 999:
                break 
                
        block = Block(txList, self.longestChain)
        return block

    def __init__(self, uID, speed, cpu, hashingFraction, genesisBlock, ttx, numPeers):
        self.connectedPeers = []
        self.transactionList = []
        self.blockchain = []
        self.uID = uID 
        self.speed = speed
        self.cpu = cpu
        self.blockchain.append(genesisBlock)
        self.longestChain = genesisBlock
        self.longestChainLength = 1
        self.numPeers = numPeers
        self.ttx = ttx
        self.timelist = []
        self.timelist.append(0)

        # generating first mine for self generation
        self.hashingFraction = hashingFraction

        miningTime = rd.exponential(scale=interarrivalTime/self.hashingFraction, size=(1, 1))[0][0]
        txTime = rd.exponential(scale=self.ttx, size=(1, 1))[0][0]
        
        global eventQueue
        eventQueue.put((miningTime, Event(0+miningTime, True, False, None, self, self.generateBlock())))        
        eventQueue.put((txTime, Event(0+txTime, False, False, None, self, None)))        

    def checkTransactionValidity(self, transaction: Transaction):
        sender = transaction.idx
        coins = transaction.coins
        presentBalance = 0
        
        for chain in self.blockchain:
            for transaction in chain.transactionList:
                if transaction.idx == sender:
                    presentBalance -= transaction.coins
                elif transaction.idy == sender:
                    presentBalance += transaction.coins
        
        for transaction in self.transactionList:
            if transaction.idx == sender:
                    presentBalance -= transaction.coins
            elif transaction.idy == sender:
                presentBalance += transaction.coins
        
        if coins > presentBalance:
            return False

    def handleTransactionReceive(self, transaction: Transaction, time: float, sendPeer):
        # validity = self.checkTransactionValidity(transaction)
        # if not validity:
        #     return
        if transaction in self.transactionList:
            return 

        self.transactionList.append(transaction)
        for peer in self.connectedPeers:
            if peer.uID is sendPeer.uID:
                continue
            c = 100 * Mbps
            if peer.speed == "slow" or self.speed == "slow":
                c = 5 * Mbps
            d = rd.exponential(scale=(96 * kbbits/c), size=(1, 1))[0][0]
            latency = rho[self.uID][peer.uID] + transaction.size/c + d
            eventQueue.put((time + latency, Event(time + latency, False, True, self, peer, transaction)))

    def calculateBalance(self, uID):
        balance = 0
        block = copy.deepcopy(self.longestChain)
        while (block):
            for transaction in block.transactionList:
                if transaction.idx == uID:
                    balance -= transaction.coins 
                if transaction.idy == uID:
                    balance += transaction.coins 
            block = block.prevBlock
        return balance
        
    def handleTransactionGeneration(self, time: float):
        idx = self.uID
        # Choose random idy
        idy = idx
        while idy == idx:
            idy = random.sample(list(range(0, self.numPeers)), 1)[0]
        # Random amount of coins will be put based on balance of idx
        balance = self.calculateBalance(self.uID)
        coins = random.randint(0, balance) 
        transaction = Transaction(idx, idy, coins)

        self.transactionList.append(transaction)
        for peer in self.connectedPeers:
            c = 100 * Mbps
            if peer.speed == "slow" or self.speed == "slow":
                c = 5 * Mbps
            d = rd.exponential(scale=(96 * kbbits/c), size=(1, 1))[0][0]
            latency = rho[self.uID][peer.uID] + transaction.size/c + d
            eventQueue.put((time + latency, Event(time + latency, False, True, self, peer, transaction)))

        # Generate another transaction
        txTime = rd.exponential(scale=self.ttx, size=(1, 1))[0][0]
        eventQueue.put((time + txTime, Event(time + txTime, False, False, None, self, None)))
        

    def checkBlockValidity(self, blk: Block):
        if blk in self.blockchain:
            return 0 
        balance = {}
        for id in range(self.numPeers):
            balance[id] = 0
        count = 1 
        block = copy.deepcopy(blk)
        while(block):
            for transaction in block.transactionList:
                if transaction.idx:
                    balance[transaction.idx] -= transaction.coins  
                balance[transaction.idy] += transaction.coins  
            block = block.prevBlock 
            count += 1
        for key in balance:
            if balance[key] < 0:
                return 0
        return count

    def handleBlockReceive(self, block: Block, time: float, sendPeer):
        length = self.checkBlockValidity(block)
        if length == 0:
            return
        self.blockchain.append(block) 
        self.timelist.append(time)

        if length > self.longestChainLength:
            self.longestChainLength = length
            self.longestChain = block 
            miningTime = rd.exponential(scale=interarrivalTime/self.hashingFraction, size=(1, 1))[0][0]
            eventQueue.put((time+miningTime, Event(time+miningTime, True, False, None, self, self.generateBlock())))        
        
        block_length = kbbits * (1 + len(block.transactionList))
        for peer in self.connectedPeers:
            if peer.uID is sendPeer.uID:
                continue
            c = 100 * Mbps
            if peer.speed == "slow" or self.speed == "slow":
                c = 5 * Mbps
            d = rd.exponential(scale=(96 * kbbits/c), size=(1, 1))[0][0]
            latency = rho[self.uID][peer.uID] + block_length/c + d
            eventQueue.put((time + latency, Event(time + latency, True, True, self, peer, block)))
            

    def handleBlockGeneration(self, block: Block, time: float):
        if (self.longestChain != block.prevBlock):
            return

        self.blockchain.append(block)
        self.timelist.append(time)
        self.longestChain = block
        self.longestChainLength += 1

        # broadcast to other nodes
        block_length = kbbits * (1 + len(block.transactionList))
        for peer in self.connectedPeers:
            c = 100 * Mbps
            if peer.speed == "slow" or self.speed == "slow":
                c = 5 * Mbps
            d = rd.exponential(scale=(96 * kbbits/c), size=(1, 1))[0][0]
            latency = rho[self.uID][peer.uID] + block_length/c + d
            eventQueue.put((time + latency, Event(time + latency, True, True, self, peer, block))) 

        miningTime = rd.exponential(scale=interarrivalTime/self.hashingFraction, size=(1, 1))[0][0]
        eventQueue.put((time+miningTime, Event(time+miningTime, True, False, None, self, self.generateBlock())))        
    
               

class Event:
    def __init__(self, time, isBlock, isReceive, sendPeer, receivePeer, transactionOrBlock):
        self.time = time
        self.isBlock = isBlock
        self.isReceive = isReceive
        self.sendPeer = sendPeer
        self.receivePeer = receivePeer
        self.transactionOrBlock = transactionOrBlock

    def simulate(self):
        if self.isBlock:
            if self.isReceive:
                self.receivePeer.handleBlockReceive(self.transactionOrBlock, self.time, self.sendPeer)
            else:
                self.receivePeer.handleBlockGeneration(self.transactionOrBlock, self.time)
        else:
            if self.isReceive:
                self.receivePeer.handleTransactionReceive(self.transactionOrBlock, self.time, self.sendPeer)
            else:
                self.receivePeer.handleTransactionGeneration(self.time)


class Network:
    def __init__(self, peerList):
        self.peerList = peerList

    def dfs(self, v, visited):
        visited[v] = True
        for u in v.connectedPeers:
            if not visited[u]:
                self.dfs(u, visited)

    def isConnected(self):
        visited={peer: False for peer in self.peerList}
        self.dfs(visited[self.peerList[0]], visited)

        for peer in self.peerList:
            if not visited[peer]:
                return False
        return True

def generateNetwork(peerList: list[Peer]):
    for peer in peerList:
        peer.connectedPeers = []

    remainingPeers = []
    for peer in peerList:
        remainingPeers.append(peer)

    for idx, peer in enumerate(peerList):
        if not peer in remainingPeers:
            continue
        remainingPeers.remove(peer)
        try:
            connList = list(random.sample(remainingPeers, min(random.randint(4,8)-len(peer.connectedPeers), len(remainingPeers))))
            peer.connectedPeers.extend(connList)
            for p in connList:
                p.connectedPeers.append(peer)
        except ValueError as error:
            return generateNetwork(peerList)

        peersToRemove = []
        for p in remainingPeers:
            if len(p.connectedPeers) == 8:
                peersToRemove.append(p)
        for p in peersToRemove:
            remainingPeers.remove(p)

    network = Network(peerList)
    if network.isConnected:
        return network
    else:
        generateNetwork(peerList)
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--peers', type=int, required=True)
    parser.add_argument('--z0', type=int, required=True)
    parser.add_argument('--z1', type=int, required=True)
    parser.add_argument('--ttx', type=int, required=True)

    args = parser.parse_args()
    slowTx = random.sample(list(range(args.peers)), int(args.peers * args.z0 / 100))
    slowCPU = random.sample(list(range(args.peers)), int(args.peers * args.z1 / 100))


    peerList = []

    rho = [[0]*args.peers]*args.peers

    for i in range(args.peers):
        for j in range(i + 1, args.peers):
            rho[j][i] = rd.uniform(low = 10 * 1e-3, high = 500 * 1e-3, size=(1, 1))[0][0]

    slowCPUnumber = len(slowCPU)

    genesisBlock = Block([Transaction(0, 0, 0)], None)

    eventQueue = PriorityQueue()

    for i in range(args.peers):
        speed = 'slow' if i in slowTx else 'fast'
        cpu = 'slow' if i in slowCPU else 'fast'
        hashingFraction = 1/(10-9*(slowCPUnumber/args.peers)) if cpu == 'slow' else 10/(10-9*(slowCPUnumber/args.peers))

        peerList.append(Peer(i, speed, cpu, hashingFraction, genesisBlock, args.ttx, args.peers))

    generateNetwork(peerList) 
    
    for i in tqdm(range(10000)):
        time, event = eventQueue.get()
        event.simulate()
        
    for idx, peer in enumerate(peerList):
        f = open("./data/treedata_" + str(idx) + ".txt", "w")
        f.write("node, prevNode, creator, time\n" + peer.__str__())
        f.close()
        