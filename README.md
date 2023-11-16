# Blockchain P2P Concurrency Network

## Assignment 1

In this assignment you will build your own discrete-event simulator for a P2P cryptocurrency network. This assignment can be done in groups consisting of at most 3 persons. A discrete-event simulator maintains an ”event-queue” from which the earliest event is executed. This event may create further future events which get added to the queue. For example, an event in which one node ”sends a block” to connected peers will create future events of ”receive block” at its peers.

## Assignment 2

### Selfish Mining Attack 
This is the same attack which was proposed by Eyal and Sirer in the paper ”Majority is not Enough” (4th link mentioned in ”Useful links”). The key idea behind this strategy is for a selfish miner (Adversary) to keep its discovered blocks private,thereby intentionally forking the chain. The honest nodes continue to mine on the public chain, while the adversary mines on its own private branch. If the adversary mines more blocks, it develops a longer lead over the public chain and continues to keep these new blocks private.

### Stubborn Mining Attack
In selfish mining, when lead = 2 and if the honest node finds the next block and closes the gap by 1, the selfish miner would immediately reveal her private chain to guarantee that the network chooses her private chain over the honest (public) chain. Therefore, the state transitions to lead = 0. In stubborn mining, instead of revealing her entire private chain, the adversary reveals the next block on her private chain only to match the length of the public chain. In this case, γ fraction of honest node will mine on adversary private chain, and 1 −γ fraction mines on honest (public) fork; and the state transitions to lead = 1. This has pros and cons for the attacker: if the (1 −γ) fraction of honest node succeeds in advancing public chain, an adversary may risk losing her private chain. However, if the adversary or the γ fraction of honest node advances adversary’s private fork, then adversary has successfully diverted a part of honest, (1 −γ) fraction to 1 do useless work.



## Assignment 3

A Dapp, or decentralized application, is a software application that runs on a distributed network. It’s not hosted on a centralized server, but instead on a peer-to-peer decentralized network, such as Ethereum. Ethereum is a network protocol that allows users to create and run smart contracts over a decentralized network. A smart contract contains code that runs specific operations and interacts with other smart contracts, which has to be written by a developer. Unlike Bitcoin which stores a number (user balance in the form of UTXO), Ethereum stores executable code. Dapp you are going to develop is accessed by different users where each user will form a joint account with other users of interest, i.e., with whom they want to transact. Each user specify their individual contribution (amount or balance) in the joint account. This way, the users will form a network, say user network Gu, where each user is a node, and a joint account between two individuals is an edge
