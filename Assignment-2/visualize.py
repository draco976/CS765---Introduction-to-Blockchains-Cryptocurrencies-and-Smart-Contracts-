# Generates the Blockhain Tree Visualisation Plots
import networkx as nx
import matplotlib.pyplot as plt 
import random
from networkx.relabel import relabel_nodes
from pathlib import Path

# Function for the Blockchain tree Visualisation, ref: https://stackoverflow.com/a/29597209/2966723
def hierarchy_pos(G, root=None, width=1., vert_gap = 2000, vert_loc = 0, xcenter = 0.5):

    # if not nx.is_tree(G):
    #     raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 2000, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos     
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


if __name__ == '__main__':

    for i in range(2):
        filename = f"./data/treedata_{i}.txt"
    
        G = nx.DiGraph()
        
        adj_dict ={}
        nodelist = []
        time = {}
        creator = {}

        with open(filename, 'r') as infile:
            
            tree_file = infile.read().split("\n")
            tree_file = tree_file[3:-1]
            
            for line in tree_file:
                entry = line.split(", ")
                
                u = int(entry[1])
                v = int(entry[0])
                time[int(entry[0])] = round(float(entry[3]), 2)
                creator[int(entry[0])] = entry[2]
                
                if u not in nodelist:
                    nodelist.append(u)
                    G.add_node(u)
                if v not in nodelist:
                    nodelist.append(v)
                    G.add_node(v)
                
                if u in adj_dict:
                    adj_dict[u].append(v)
                else:
                    adj_dict[u]=[v]
                if v in adj_dict:
                    adj_dict[v].append(u)
                else:
                    adj_dict[v]=[u]

                G.add_edge(u, v)

        print(nodelist)

        time[1] = 0
        creator[1] = -1

        naming = {}
        colorMap = []
        for node in nodelist:
            # naming[node] = str(time[node])
            naming[node] = time[node]
            if creator[node] == '0':
                colorMap.append("Red") 
            else:
                colorMap.append("Green") 
        
        naming[1] = "G"
        
        relabel_nodes(G, naming, copy = False)
        pos = hierarchy_pos(G, "G")
        fig = plt.figure()
        fig.set_figheight(0.5*len(nodelist))
        fig.set_figwidth(12)
        nx.draw(G, pos = pos, with_labels = True, node_color = colorMap)

        Path("./graph").mkdir(parents=True, exist_ok=True)
        plt.title("Blockchain Tree")
        plt.savefig(f"./graph/Blockchain_Node_{i}.png")
        plt.clf()