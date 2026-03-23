# Fundamentals

* Graphs:
    - Nodes: fundamental units representing entities
    - Edges: connections between nodes
    - Directed: edges have direction (A → B)
    - Undirected: edges are bidirectional (A — B)
    - Cyclic: contains a cycle (A → B → C → A)
    - Acyclic: no cycles (Tree, DAG)
    - Components of a graph: connected components = nodes reachable from each other
    - Simple path: no repeated nodes
    - Closed path: start = end
    - Edge Weight: value on edges (distance, cost, etc.)

* Degree of nodes in a graph:
    - Undirected Graph:
        - Degree of a node = number of edges connected to it
    - Directed Graph:
        - In-degree of a node = number of edges going into it
        - Out-degree of a node = number of edges going out of it

* Graph Representation:
    - Adjacency Matrix: 
        - V x V matrix
        - Space complexity: O(V^2)
        - Time complexity: O(1)
    - Adjacency List
        - V x 1 matrix
        - Space complexity: O(V+E)
        - Time complexity: O(V+E)
    - Edge List
        - 1 x E matrix
        - Space complexity: O(E)
        - Time complexity: O(E)

# Traversal Algorithms

### Depth First Search (DFS)
```cpp
// TC: O(V+E)
// SC: O(V)
void dfs(int node, vector<int> adj[], vector<int>& visited, vector<int>& result) {

    visited[node] = 1;              // mark node as visited
    result.push_back(node);         // process current node

    // explore all adjacent nodes (depth-first)
    for (int neighbor : adj[node]) {
        if (!visited[neighbor]) {
            dfs(neighbor, adj, visited, result);
        }
    }
}

vector<int> dfsOfGraph(int V, vector<int> adj[]) {

    vector<int> visited(V, 0);      // visited array
    vector<int> result;

    // loop to handle disconnected components
    for (int i = 0; i < V; i++) {
        if (!visited[i]) {
            dfs(i, adj, visited, result);
        }
    }

    return result;
}
```

### Breadth First Search (BFS)
```cpp
// TC: O(V+E)
// SC: O(V)
void bfs(int startNode, vector<int> adj[], vector<int>& visited, vector<int>& result) {

    queue<int> q;
    q.push(startNode);
    visited[startNode] = 1;         // mark visited when pushing

    while (!q.empty()) {

        int node = q.front();
        q.pop();

        result.push_back(node);     // process node

        // visit all neighbors (level-order)
        for (int neighbor : adj[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = 1; // avoid multiple insertions
                q.push(neighbor);
            }
        }
    }
}

vector<int> bfsOfGraph(int V, vector<int> adj[]) {

    vector<int> visited(V, 0);
    vector<int> result;

    // handle disconnected graph
    for (int i = 0; i < V; i++) {
        if (!visited[i]) {
            bfs(i, adj, visited, result);
        }
    }

    return result;
}
```

### Connected Components
```cpp
// TC: O(V+E)
// SC: O(V)
void dfs(int node, vector<int> adj[], int vis[]) {

    vis[node] = 1;  // mark current node as visited

    // explore all neighbors of current node
    for (int neighbor : adj[node]) {

        // if neighbor not visited → visit it
        if (!vis[neighbor])
            dfs(neighbor, adj, vis);
    }
}

int findNumberOfComponent(int V, vector<vector<int>> &edges) {

    // Step 1: Build adjacency list (undirected graph)
    vector<int> adj[V];

    for (int i = 0; i < edges.size(); i++) {
        int u = edges[i][0];
        int v = edges[i][1];

        adj[u].push_back(v); // u → v
        adj[v].push_back(u); // v → u (undirected)
    }

    int vis[V] = {0};  // visited array to track explored nodes
    int count = 0;     // number of connected components

    // Step 2: Traverse all nodes
    for (int i = 0; i < V; i++) {

        // if node not visited → new component found
        if (!vis[i]) {
            count++;                // increment component count
            dfs(i, adj, vis);      // explore entire component
        }
    }

    return count;
}
```

### No. of Provinces
```cpp
// TC: O(V+E) ~ O(V^2) : because of the adjacency matrix
// SC: O(V)
void dfs(int node, vector<int> adj[], int vis[]) {

    vis[node] = 1;  // mark current city as visited

    // explore all directly connected cities
    for (int neighbor : adj[node]) {

        // visit only if not already visited
        if (!vis[neighbor]) {
            dfs(neighbor, adj, vis);
        }
    }
}

int numProvinces(vector<vector<int>> adj) {

    int V = adj.size();

    // Step 1: Convert adjacency matrix → adjacency list
    vector<int> list[V];

    for (int i = 0; i < V; i++) {
        for (int j = 0; j < V; j++) {

            // if there is a connection and not self-loop
            if (adj[i][j] == 1 && i != j) {

                list[i].push_back(j); // i → j
                list[j].push_back(i); // j → i (undirected)
            }
        }
    }

    int vis[V] = {0};  // track visited cities
    int count = 0;     // number of provinces (connected components)

    // Step 2: Traverse all nodes
    for (int i = 0; i < V; i++) {

        // if not visited → new province found
        if (!vis[i]) {
            count++;               // increment province count
            dfs(i, list, vis);     // explore entire component
        }
    }

    return count;
}
```

### No. of Islands
>Given a grid of size N x M (N is the number of rows and M is the number of columns in the grid) consisting of '0's (Water) and ‘1's(Land). Find the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically or diagonally i.e., in all 8 directions.
```cpp
bool isValid(int i, int j, int n, int m) {
    // check boundaries of grid
    if (i < 0 || i >= n) return false;
    if (j < 0 || j >= m) return false;
    return true;
}

void bfs(int i, int j, vector<vector<bool>>& vis, vector<vector<char>>& grid) {

    queue<pair<int, int>> q;
    q.push({i, j});
    vis[i][j] = true;   // mark starting cell as visited

    int n = grid.size();
    int m = grid[0].size();

    // BFS traversal to mark entire island
    while (!q.empty()) {

        auto [row, col] = q.front();
        q.pop();

        // explore all 8 directions (including diagonals)
        for (int dr = -1; dr <= 1; dr++) {
            for (int dc = -1; dc <= 1; dc++) {

                int newRow = row + dr;
                int newCol = col + dc;

                // check valid land cell and not visited
                if (isValid(newRow, newCol, n, m) &&
                    grid[newRow][newCol] == '1' &&
                    !vis[newRow][newCol]) {

                    vis[newRow][newCol] = true;
                    q.push({newRow, newCol});
                }
            }
        }
    }
}

int numIslands(vector<vector<char>> &grid){
    int n = grid.size();
    int m = grid[0].size();

    vector<vector<bool>> vis(n, vector<bool>(m, false));

    int count = 0;  // number of islands

    // traverse entire grid
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {

            // if unvisited land → new island found
            if (!vis[i][j] && grid[i][j] == '1') {

                count++;           // increment island count
                bfs(i, j, vis, grid);  // mark entire island
            }
        }
    }

    return count;
}
```

### Flood Fill Algorithm
```cpp
vector<vector<int>> floodFill(vector<vector<int>> &image,
                              int sr, int sc, int newColor) {

    int n = image.size();
    int m = image[0].size();

    int originalColor = image[sr][sc];

    // if same color → no change needed (avoid infinite loop)
    if (originalColor == newColor) return image;

    queue<pair<int,int>> q;
    q.push({sr, sc});

    // mark starting cell
    image[sr][sc] = newColor;

    // 4-directional movement
    int dr[] = {-1, 0, 1, 0};
    int dc[] = {0, 1, 0, -1};

    while (!q.empty()) {

        auto [row, col] = q.front();
        q.pop();

        // explore neighbors
        for (int k = 0; k < 4; k++) {

            int newRow = row + dr[k];
            int newCol = col + dc[k];

            // check bounds + same color
            if (newRow >= 0 && newRow < n &&
                newCol >= 0 && newCol < m &&
                image[newRow][newCol] == originalColor) {

                image[newRow][newCol] = newColor; // color it
                q.push({newRow, newCol});
            }
        }
    }

    return image;
}
```

### No. of enclaves
>Given an N x M binary matrix grid, where 0 represents a sea cell and 1 represents a land cell. A move consists of walking from one land cell to another adjacent (4-directionally) land cell or walking off the boundary of the grid. Find the number of land cells in the grid for which we cannot walk off the boundary of the grid in any number of moves.
```cpp
int numberOfEnclaves(vector<vector<int>> &grid) {

    int n = grid.size();
    int m = grid[0].size();

    queue<pair<int,int>> q;

    // Step 1: Add all boundary land cells to queue
    // These cells can definitely reach the boundary → NOT enclaves
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {

            if (i == 0 || j == 0 || i == n-1 || j == m-1) {
                if (grid[i][j] == 1) {
                    q.push({i, j});
                    grid[i][j] = 0;  // mark as visited (remove non-enclave land)
                }
            }
        }
    }

    // 4-directional movement (up, right, down, left)
    int dr[] = {-1, 0, 1, 0};
    int dc[] = {0, 1, 0, -1};

    // Step 2: BFS to remove all land connected to boundary
    while (!q.empty()) {

        auto [row, col] = q.front();
        q.pop();

        // explore all neighbors
        for (int k = 0; k < 4; k++) {

            int newRow = row + dr[k];
            int newCol = col + dc[k];

            // if valid cell and still land → remove it
            if (newRow >= 0 && newRow < n &&
                newCol >= 0 && newCol < m &&
                grid[newRow][newCol] == 1) {

                grid[newRow][newCol] = 0;  // eliminate (not enclave)
                q.push({newRow, newCol});
            }
        }
    }

    // Step 3: Count remaining land cells
    // These are not connected to boundary → enclaves
    int count = 0;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {

            if (grid[i][j] == 1)
                count++;
        }
    }

    return count;
}
```

### Rotten Oranges
>You are given an m x n grid where each cell can have one of three values:
>2: a rotten orange
>1: a fresh orange
>0: an empty cell
>Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.
>Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.
```cpp
int orangesRotting(vector<vector<int>> &grid) {

    int n = grid.size();
    int m = grid[0].size();

    queue<pair<int,int>> q;
    int fresh = 0;   // count of fresh oranges

    // Step 1: Initialize queue with all rotten oranges
    // and count fresh ones
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {

            if (grid[i][j] == 2) {
                q.push({i, j});   // rotten orange
            }
            else if (grid[i][j] == 1) {
                fresh++;          // fresh orange
            }
        }
    }

    // 4 directions
    int dr[] = {-1, 0, 1, 0};
    int dc[] = {0, 1, 0, -1};

    int minutes = 0;

    // Step 2: BFS → spread rot
    while (!q.empty() && fresh > 0) {

        int size = q.size();  // process one level (one minute)

        while (size--) {

            auto [row, col] = q.front();
            q.pop();

            for (int k = 0; k < 4; k++) {

                int newRow = row + dr[k];
                int newCol = col + dc[k];

                // if valid fresh orange → rot it
                if (newRow >= 0 && newRow < n &&
                    newCol >= 0 && newCol < m &&
                    grid[newRow][newCol] == 1) {

                    grid[newRow][newCol] = 2; // mark rotten
                    q.push({newRow, newCol});
                    fresh--; // one fresh converted
                }
            }
        }

        minutes++;  // one minute completed
    }

    // Step 3: If fresh oranges remain → impossible
    return (fresh == 0) ? minutes : -1;
}
```

### Distance of nearest cell having one
>Given a binary grid of N x M. Find the distance of the nearest 1 in the grid for each cell.
>The distance is calculated as |i1 - i2| + |j1 - j2|, where i1, j1 are the row number and column number of the current cell, and i2, j2 are the row number and column number of the nearest cell having value 1.
```cpp
vector<vector<int>> nearest(vector<vector<int>> grid){

    int n = grid.size();
    int m = grid[0].size();

    queue<pair<int,int>> q;
    vector<vector<int>> dist(n, vector<int>(m, 0));
    vector<vector<bool>> vis(n, vector<bool>(m, false));

    // Step 1: Push all cells with value 1 into queue
    // These act as multiple starting points (distance = 0)
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {

            if (grid[i][j] == 1) {
                q.push({i, j});
                vis[i][j] = true;
                dist[i][j] = 0;
            }
        }
    }

    // 4-direction movement
    int dr[] = {-1, 0, 1, 0};
    int dc[] = {0, 1, 0, -1};

    // Step 2: BFS to compute minimum distance
    while (!q.empty()) {

        auto [row, col] = q.front();
        q.pop();

        for (int k = 0; k < 4; k++) {

            int newRow = row + dr[k];
            int newCol = col + dc[k];

            // check valid cell and not visited
            if (newRow >= 0 && newRow < n &&
                newCol >= 0 && newCol < m &&
                !vis[newRow][newCol]) {

                vis[newRow][newCol] = true;

                // distance = parent distance + 1
                dist[newRow][newCol] = dist[row][col] + 1;

                q.push({newRow, newCol});
            }
        }
    }

    return dist;
}
```

### Surrounded Regions
>You are given a matrix mat of size N x M where each cell contains either 'O' or 'X'. Your task is to replace all 'O' cells that are completely surrounded by 'X' with 'X'.
>Rules:
>An 'O' (or a group of connected 'O's) is considered surrounded if it is not connected to any border of the matrix.
>Two 'O' cells are considered connected if they are adjacent horizontally or vertically (not diagonally).
>A region of connected 'O's that touches the border (i.e., first row, last row, first column, or last column) is not surrounded and should not be changed.
```cpp
vector<vector<char>> fill(vector<vector<char>> mat) {

    int n = mat.size();
    int m = mat[0].size();

    queue<pair<int,int>> q;

    // Step 1: Push all boundary 'O's into queue
    // These are NOT surrounded → mark them safe
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {

            if (i == 0 || j == 0 || i == n-1 || j == m-1) {
                if (mat[i][j] == 'O') {
                    q.push({i, j});
                    mat[i][j] = '#';  // mark as safe
                }
            }
        }
    }

    // 4-direction movement
    int dr[] = {-1, 0, 1, 0};
    int dc[] = {0, 1, 0, -1};

    // Step 2: BFS → mark all 'O' connected to boundary as safe
    while (!q.empty()) {

        auto [row, col] = q.front();
        q.pop();

        for (int k = 0; k < 4; k++) {

            int newRow = row + dr[k];
            int newCol = col + dc[k];

            // if valid and still 'O' → mark safe
            if (newRow >= 0 && newRow < n &&
                newCol >= 0 && newCol < m &&
                mat[newRow][newCol] == 'O') {

                mat[newRow][newCol] = '#';
                q.push({newRow, newCol});
            }
        }
    }

    // Step 3: Convert remaining 'O' → 'X' (these are surrounded)
    // Convert '#' back → 'O' (safe ones)
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {

            if (mat[i][j] == 'O') {
                mat[i][j] = 'X';  // surrounded → flip
            }
            else if (mat[i][j] == '#') {
                mat[i][j] = 'O';  // restore safe cells
            }
        }
    }

    return mat;
}
```

### Number of distinct islands
>You are given a 2D matrix grid of size N × M, where each cell contains either 0 or 1. Find the number of distinct islands where a group of connected 1s (horizontally or vertically) forms an island. Two islands are considered to be same if and only if one island is equal to another (not rotated or reflected).
```cpp
void dfs(int row, int col, vector<vector<int>>& grid, vector<vector<int>>& vis, vector<pair<int,int>>& shape, int baseRow, int baseCol) {

    int n = grid.size();
    int m = grid[0].size();

    vis[row][col] = 1;

    // store relative position (normalization)
    shape.push_back({row - baseRow, col - baseCol});

    // 4-direction movement
    int dr[] = {-1, 0, 1, 0};
    int dc[] = {0, 1, 0, -1};

    for (int k = 0; k < 4; k++) {

        int newRow = row + dr[k];
        int newCol = col + dc[k];

        // valid land and not visited
        if (newRow >= 0 && newRow < n &&
            newCol >= 0 && newCol < m &&
            grid[newRow][newCol] == 1 &&
            !vis[newRow][newCol]) {

            dfs(newRow, newCol, grid, vis, shape, baseRow, baseCol);
        }
    }
}

int countDistinctIslands(vector<vector<int>> &grid){

    int n = grid.size();
    int m = grid[0].size();

    vector<vector<int>> vis(n, vector<int>(m, 0));

    set<vector<pair<int,int>>> st;  // stores unique island shapes

    // traverse grid
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {

            if (!vis[i][j] && grid[i][j] == 1) {

                vector<pair<int,int>> shape;

                // start DFS with base point (i,j)
                dfs(i, j, grid, vis, shape, i, j);

                // store normalized shape
                st.insert(shape);
            }
        }
    }

    return st.size();
}
```

# Cycle Based Problems

### Cycle in Undirected Graph
>Graph can be divided into 2 groups such that no two adjacent nodes are in the same group
```cpp
class Solution{
public:

    // ---------- BFS Cycle Detection ----------
    bool detectCycle(int startNode, vector<int> adj[], vector<int> &vis) {

        queue<pair<int,int>> q;
        q.push({startNode, -1});   // {node, parent}
        vis[startNode] = 1;

        while (!q.empty()) {

            auto [node, parent] = q.front();
            q.pop();

            // explore neighbors
            for (int neighbor : adj[node]) {

                // if not visited → continue BFS
                if (!vis[neighbor]) {
                    vis[neighbor] = 1;
                    q.push({neighbor, node});
                }
                // if visited and not parent → cycle found
                else if (neighbor != parent) {
                    return true;
                }
            }
        }

        return false;  // no cycle in this component
    }

    // ---------- DFS Cycle Detection ----------
    bool detectCycleDfs(int node, int parent, vector<int> adj[], vector<int> &vis) {
        vis[node] = 1;  // mark current node
        for (int neighbor : adj[node]) {
            // go deeper if not visited
            if (!vis[neighbor]) {
                if (detectCycleDfs(neighbor, node, adj, vis)) return true;
            }
            // visited neighbor that is NOT parent → cycle
            else if (neighbor != parent) return true;
        }
        return false;
    }

    bool isCycle(int V, vector<int> adj[]) {

        vector<int> vis(V, 0);
        // handle disconnected graph
        for (int i = 0; i < V; i++) {

            if (!vis[i]) {
                // use either BFS or DFS
                // if (detectCycle(i, adj, vis)) return true;
                if (detectCycleDfs(i, -1, adj, vis)) return true;
            }
        }

        return false;  // no cycle in any component
    }
};
```

### Bipartite Graph
```cpp
class Solution{
public:

    // ---------- BFS Bipartite Check ----------
    bool detectBipartite(int startNode, vector<int> adj[], vector<int> &color) {

        queue<int> q;
        q.push(startNode);

        color[startNode] = 0;  // assign first color (0 or 1)

        while (!q.empty()) {

            int node = q.front();
            q.pop();

            for (int neighbor : adj[node]) {

                // if not colored yet → assign opposite color
                if (color[neighbor] == -1) {
                    color[neighbor] = !color[node];
                    q.push(neighbor);
                }
                // if same color as current → not bipartite
                else if (color[neighbor] == color[node]) {
                    return false;
                }
            }
        }

        return true;
    }


    // ---------- DFS Bipartite Check ----------
    bool detectBipartiteDfs(int node, int currColor,
                           vector<int> adj[], vector<int> &color) {

        color[node] = currColor;  // assign color

        for (int neighbor : adj[node]) {

            // if not colored → color with opposite color
            if (color[neighbor] == -1) {

                if (!detectBipartiteDfs(neighbor, !currColor, adj, color))
                    return false;
            }
            // if same color → conflict → not bipartite
            else if (color[neighbor] == currColor) {
                return false;
            }
        }

        return true;
    }


    // ---------- Main ----------
    bool isBipartite(int V, vector<int> adj[]) {

        vector<int> color(V, -1);  // -1 = uncolored, 0/1 = two colors

        // handle disconnected graph
        for (int i = 0; i < V; i++) {

            if (color[i] == -1) {

                // use either BFS or DFS
                // if (!detectBipartite(i, adj, color)) return false;

                if (!detectBipartiteDfs(i, 0, adj, color))
                    return false;
            }
        }

        return true;  // no conflicts → bipartite
    }
};
```

### Topological Sort or Kahn's algorithm
> Topological sorting of a directed acyclic graph (DAG) is nothing but the linear ordering of vertices such that if there is an edge between node u and v(u -> v), node u appears before v in that ordering
```cpp
class Solution{
public:

    // ---------- Kahn’s Algorithm (BFS Topological Sort) ----------
    vector<int> kahnsAlgo(int V, vector<int> adj[]) {

        vector<int> topo;                 // stores topological order
        vector<int> indegree(V, 0);       // indegree of each node

        // Step 1: Compute indegree of all nodes
        for (int i = 0; i < V; i++) {
            for (int neighbor : adj[i]) {
                indegree[neighbor]++;
            }
        }

        queue<int> q;

        // Step 2: Push nodes with indegree = 0
        // (these have no dependencies)
        for (int i = 0; i < V; i++) {
            if (indegree[i] == 0)
                q.push(i);
        }

        // Step 3: Process nodes
        while (!q.empty()) {

            int node = q.front();
            q.pop();

            topo.push_back(node);  // add to result

            // reduce indegree of neighbors
            for (int neighbor : adj[node]) {
                indegree[neighbor]--;

                // if no dependencies left → push
                if (indegree[neighbor] == 0)
                    q.push(neighbor);
            }
        }

        return topo;
    }


    // ---------- DFS Topological Sort ----------
    void dfs(int node, vector<int> adj[],
             vector<int> &vis, stack<int> &st) {

        vis[node] = 1;

        // visit all neighbors first
        for (int neighbor : adj[node]) {
            if (!vis[neighbor]) {
                dfs(neighbor, adj, vis, st);
            }
        }

        // push AFTER visiting children (post-order)
        st.push(node);
    }


    vector<int> topoSort(int V, vector<int> adj[]){

        // ----------- OPTION 1: Kahn’s Algorithm (BFS) -----------
        // return kahnsAlgo(V, adj);

        // ----------- OPTION 2: DFS -----------
        vector<int> vis(V, 0);
        stack<int> st;
        vector<int> res;

        for (int i = 0; i < V; i++) {
            if (!vis[i]) {
                dfs(i, adj, vis, st);
            }
        }

        // stack gives reverse topological order
        while (!st.empty()) {
            res.push_back(st.top());
            st.pop();
        }

        return res;
    }
};
```