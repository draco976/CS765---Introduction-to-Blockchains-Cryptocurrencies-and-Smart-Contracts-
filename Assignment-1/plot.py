import matplotlib.pyplot as plt

data = {'slow - slow': 0.5,
        'slow - fast': 0.7142857142857143,
        'fast - slow': 0.5,
        'fast - fast': 0.9,
        }

plt.xlabel('Group')
plt.ylabel('Ratio of blocks in longest chain to total blocks')
plt.bar(data.keys(), data.values(), width=0.4)
plt.savefig('ratio.png')