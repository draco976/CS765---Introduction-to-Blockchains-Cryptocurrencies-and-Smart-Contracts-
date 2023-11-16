# Libraries to be installed 

1. numpy
```bash
pip install numpy
```
2. tqdm
```bash
pip install tqdm
```
3. matplotlib
```bash
pip install matplotlib
```
4. networkx
```bash
pip install networkx
```

# Running the file
```bash
python blockchain.py --n <No. of nodes> --z0 <Percentage of slow nodes> --z1 <Percentage of nodes with low CPU power> --ttx <Mean time of interarrival between transactions>
```

# Visualizing the blockchain tree
```bash
python visualize.py 
```

# Directory Structure

1. blockchain.py - Contains the core logic of creating the blockchain and the network
2. visualize.py - Used to visualize the blockchain tree
3. data directory - Contains properly maintained tree files for each node
4. graph directory - Contains the images of blockchain tree stored at every node