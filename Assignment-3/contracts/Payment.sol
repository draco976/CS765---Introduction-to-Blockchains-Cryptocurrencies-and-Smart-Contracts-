// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Payment {
  struct node {
    string user_name; 
    uint user_id; 
  }

  node[100] public nodes; // List of nodes present in the network
  uint[][100] public edges; // Adjacency List - dynamic list to speed up bfs 
  uint[100][100] public bal; // bal[i][j] represents the balance i has in (i,j) connection edge
  uint public success = 0 ;

  function registerUser(uint user_id, string memory user_name) public {
    nodes[user_id] = node({user_name: user_name, user_id: user_id});
  }

  function createAcc(uint user_id1, uint user_id2, uint balance) public {
    edges[user_id1].push(user_id2) ;
    bal[user_id1][user_id2] = balance ;
    edges[user_id2].push(user_id1) ;
    bal[user_id2][user_id1] = balance ;
  }

  function sendAmount(uint user_id1, uint user_id2) public {

    uint[] memory bfs_queue = new uint[](100); // bfs queue containing nodes to be explored
    uint[] memory parent = new uint[](100); // parent of a node according to 
    uint[] memory explored = new uint[](100);

    for (uint i=0; i<100; i++) {
      explored[i] = 0;
      parent[i] = 100 ;
    }

    uint start = 0;
    uint end = 0;
    uint head ;

    explored[user_id1] = 1;
    bfs_queue[end] = user_id1; 
    end++;
    
    while(start<end)
    {
      head = bfs_queue[start];
      start++;
    
      if (head==user_id2){ // there is a path to user_id2
        uint x = user_id2 ;

        while(parent[x] != 100) {
          // change balances on path edges
          bal[x][parent[x]] += 1 ; 
          bal[parent[x]][x] -= 1 ;
          x = parent[x] ;
        }
        success = 1 ;
        return ;
      }
      else{
        for(uint i=0; i<edges[head].length; i++)
        {
          // if edge does not exist between user_id and i
          if (bal[head][edges[head][i]] == 0) continue;

          // if edge exists and is unexplored
          if(explored[edges[head][i]]==0)
          { 
            explored[edges[head][i]]=1;
            parent[edges[head][i]] = head ;
    
            bfs_queue[end] = edges[head][i];
            end++;
          }
        }
      }
    }
    success = 0 ;
    return ;
  }

  // check if the previous transaction was successful
  function check_success() public view returns (uint) {
    return success ;
  }

  function closeAccount(uint user_id1, uint user_id2) public {
    bal[user_id1][user_id2] = 0;
    bal[user_id2][user_id1] = 0;
  }
}
