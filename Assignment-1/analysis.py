f = open("./data/peerdata.txt", "r")
speed = {}
cpu = {}
for line in f.readlines():
    data = line.split(", ")
    speed[data[0]] = data[1]
    cpu[data[0]] = data[2][:-1] if data[2][-1] == '\n' else data[2]

cont1 = {}
cont2 = {}
parent = {}
blockList = []

len = {}
len["1"] = 1

f = open("./data/treedata_0.txt", "r")
longest = f.readline().split(", ")

for line in f.readlines()[2:]:
    data = line.split(", ")

    blockList.append(data[0])
    parent[data[0]] = data[1]

    if data[2] in cont1.keys():
        cont1[data[2]] += 1 
    else:
        cont1[data[2]] = 1

    if data[0] in longest:
        if data[2] in cont2.keys():
            cont2[data[2]] += 1 
        else:
            cont2[data[2]] = 1 

    len[data[0]] = len[data[1]] + 1

# print(parent.values())
leaves = []
for block in blockList:
    if block not in parent.values():
        leaves.append(block)

branchLen = []
for leaf in leaves:
    node = leaf
    count = 1
    while(node!='1'):
        count+=1
        node = parent[node]
    branchLen.append(count)

print(branchLen)

a = [0, 0, 0, 0]
b = [0, 0, 0, 0]

for key in cont1.keys():
    if speed[key] == 'slow' and cpu[key] == 'slow':
        a[0] += cont1[key]
    if speed[key] == 'slow' and cpu[key] == 'fast':
        a[1] += cont1[key]
    if speed[key] == 'fast' and cpu[key] == 'slow':
        a[2] += cont1[key]
    if speed[key] == 'fast' and cpu[key] == 'fast':
        a[3] += cont1[key]

for key in cont2.keys():
    if speed[key] == 'slow' and cpu[key] == 'slow':
        b[0] += cont2[key]
    if speed[key] == 'slow' and cpu[key] == 'fast':
        b[1] += cont2[key]
    if speed[key] == 'fast' and cpu[key] == 'slow':
        b[2] += cont2[key]
    if speed[key] == 'fast' and cpu[key] == 'fast':
        b[3] += cont2[key]

sum = 0 
sum += b[0]
sum += b[1]
sum += b[2]
sum += b[3]
res = [0, 0, 0, 0]
res2 = [0, 0, 0, 0]
for i in range(4):
    res[i] = b[i]/a[i] if b[i]!=0 else 0
for i in range(4):
    res2[i] = b[i]/sum 

for key in cont1.keys():
    if key not in cont2.keys():
        cont2[key] = 0

print(res)
print(res2)
print(a)
print(b)

            


