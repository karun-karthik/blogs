# Fundamentals
* A spanning tree is a subset of a weighted graph in which there are N nodes(i.e. all the nodes present in the original graph) and N-1 edges and all nodes are reachable from each other.

* The minimum spanning tree is the one for which the sum of all the edge weights is the minimum.

There are two algorithms for finding the Minimum spanning tree for a given graph:
1. Prim's Algorithm ~ grows MST from a node using a heap
2. Kruskal Algorithm ~ builds MST by sorting edges and using DSU to avoid cycles

### DSU
> DSU maintains connected components using path compression and union by rank/size for near O(1) operations.
```cpp
class DisjointSet {
    vector<int> rank, size, parent;

public:
    DisjointSet(int n) {

        // rank → approx tree height (used in union by rank)
        rank.resize(n + 1, 0);

        // size → number of nodes in component (used in union by size)
        size.resize(n + 1, 1);

        // parent → representative of each node
        parent.resize(n + 1);

        // Initially, every node is its own parent (separate components)
        for (int i = 0; i <= n; i++) {
            parent[i] = i;
        }
    }

    /*  FIND with Path Compression
        --------------------------
        Returns ultimate parent (root of component)

        Path compression flattens the tree:
        Makes future queries nearly O(1)
    */
    int findUltimateParent(int node) {

        if (node == parent[node])
            return node;

        return parent[node] = findUltimateParent(parent[node]);
    }

    /* Check if two nodes belong to same component */
    bool isConnected(int u, int v) {
        return findUltimateParent(u) == findUltimateParent(v);
    }

    /*  UNION BY RANK
        -------------
        Attach smaller height tree under larger height tree
        Keeps tree shallow → faster find
    */
    void unionByRank(int u, int v) {

        int rootU = findUltimateParent(u);
        int rootV = findUltimateParent(v);

        if (rootU == rootV) return;  // already in same set

        if (rank[rootU] < rank[rootV]) {
            parent[rootU] = rootV;
        }
        else if (rank[rootV] < rank[rootU]) {
            parent[rootV] = rootU;
        }
        else {
            parent[rootV] = rootU;
            rank[rootU]++;  // increase height
        }
    }

    /*  UNION BY SIZE
        -------------
        Attach smaller component under larger component
        Keeps tree balanced
    */
    void unionBySize(int u, int v) {

        int rootU = findUltimateParent(u);
        int rootV = findUltimateParent(v);

        if (rootU == rootV) return;

        if (size[rootU] < size[rootV]) {
            parent[rootU] = rootV;
            size[rootV] += size[rootU];
        }
        else {
            parent[rootV] = rootU;
            size[rootU] += size[rootV];
        }
    }
};
```

### Find the MST Weight
```cpp
#include <bits/stdc++.h>
using namespace std;

#define P pair<int,int>

/* ===================== DISJOINT SET ===================== */
class DisjointSet {
    vector<int> parent, rank, size;

public:
    DisjointSet(int n) {
        parent.resize(n);
        rank.resize(n, 0);
        size.resize(n, 1);

        for (int i = 0; i < n; i++)
            parent[i] = i;
    }

    // Find with path compression
    int findUltimateParent(int node) {
        if (node == parent[node])
            return node;
        return parent[node] = findUltimateParent(parent[node]);
    }

    // Check if two nodes belong to same component
    bool isConnected(int u, int v) {
        return findUltimateParent(u) == findUltimateParent(v);
    }

    // Union by size (better in practice)
    void unionBySize(int u, int v) {
        int rootU = findUltimateParent(u);
        int rootV = findUltimateParent(v);

        if (rootU == rootV) return;

        if (size[rootU] < size[rootV]) {
            parent[rootU] = rootV;
            size[rootV] += size[rootU];
        } else {
            parent[rootV] = rootU;
            size[rootU] += size[rootV];
        }
    }
};

/* ===================== SOLUTION ===================== */
class Solution {
    
    /* ----------- PRIM'S ALGORITHM ----------- */
    int primsMST(int V, vector<vector<int>> adj[]) {

        priority_queue<P, vector<P>, greater<P>> minHeap;
        vector<int> visited(V, 0);

        minHeap.push({0, 0}); // {weight, node}

        int mstWeight = 0;

        /*
        Grow MST:
        Always pick smallest edge connecting to new node
        */
        while (!minHeap.empty()) {

            auto [weight, node] = minHeap.top();
            minHeap.pop();

            if (visited[node]) continue;

            visited[node] = 1;
            mstWeight += weight;

            for (auto &neighbor : adj[node]) {

                int nextNode = neighbor[0];
                int edgeWeight = neighbor[1];

                if (!visited[nextNode]) {
                    minHeap.push({edgeWeight, nextNode});
                }
            }
        }

        return mstWeight;
    }


    /* ----------- KRUSKAL'S ALGORITHM ----------- */
    int kruskalMST(int V, vector<vector<int>> adj[]) {

        vector<pair<int, pair<int,int>>> edges;

        // Convert adjacency list → edge list (avoid duplicates)
        for (int u = 0; u < V; u++) {
            for (auto &neighbor : adj[u]) {

                int v = neighbor[0];
                int wt = neighbor[1];

                if (u < v) {  // prevent duplicate edges
                    edges.push_back({wt, {u, v}});
                }
            }
        }

        // Sort edges by weight
        sort(edges.begin(), edges.end());

        DisjointSet ds(V);

        int mstWeight = 0;

        /*
        Pick smallest edges that don't form cycle
        */
        for (auto &edge : edges) {

            int wt = edge.first;
            int u = edge.second.first;
            int v = edge.second.second;

            if (!ds.isConnected(u, v)) {
                mstWeight += wt;
                ds.unionBySize(u, v);
            }
        }

        return mstWeight;
    }

public:

    int spanningTree(int V, vector<vector<int>> adj[]) {

        // Choose one:
        return primsMST(V, adj);
        // return kruskalMST(V, adj);
    }
};
```

# FAQs

### Number of operations to make network connected
```cpp
class Solution{
public:
    int solve(int n, vector<vector<int>> &edges){

        int m = edges.size();

        // Minimum edges required to connect n nodes = n - 1
        if (m < n - 1) return -1;

        DisjointSet ds(n);

        // Build connected components using DSU
        for (auto &edge : edges) {
            int u = edge[0];
            int v = edge[1];
            ds.unionBySize(u, v);
        }

        /*  Count number of components
            A node is a component root if parent[node] == node */
        int components = 0;

        for (int i = 0; i < n; i++) {
            if (ds.findUltimateParent(i) == i) {
                components++;
            }
        }

        // To connect k components → need (k - 1) edges
        return components - 1;
    }
};
```

### Account Merge
```cpp
class Solution{
public:
    vector<vector<string>> accountsMerge(vector<vector<string>> accounts){

        int n = accounts.size();

        DisjointSet ds(n);

        // Map each email → account index
        // Helps detect which accounts should be merged
        unordered_map<string, int> emailToAccount;

        // Step 1: Build DSU connections
        for (int acc = 0; acc < n; acc++) {

            for (int j = 1; j < accounts[acc].size(); j++) {

                string email = accounts[acc][j];

                // First time seeing this email
                if (emailToAccount.find(email) == emailToAccount.end()) {
                    emailToAccount[email] = acc;
                }
                else {
                    // Same email → same person → union accounts
                    ds.unionBySize(acc, emailToAccount[email]);
                }
            }
        }

        // Step 2: Group emails by their ultimate parent
        vector<vector<string>> groupedEmails(n);

        for (auto &it : emailToAccount) {

            string email = it.first;
            int accountIndex = it.second;

            int parent = ds.findUltimateParent(accountIndex);

            groupedEmails[parent].push_back(email);
        }

        // Step 3: Build final answer
        vector<vector<string>> result;

        for (int i = 0; i < n; i++) {

            if (groupedEmails[i].empty()) continue;

            // Sort emails lexicographically
            sort(groupedEmails[i].begin(), groupedEmails[i].end());

            vector<string> mergedAccount;

            // Use parent account name (more correct)
            mergedAccount.push_back(accounts[i][0]);

            for (auto &email : groupedEmails[i]) {
                mergedAccount.push_back(email);
            }

            result.push_back(mergedAccount);
        }

        // Optional: sort result (problem dependent)
        sort(result.begin(), result.end());

        return result;
    }
};
```

### Number of Islands ii
```cpp
class Solution{
private:
    vector<int> dr = {-1, 0, 1, 0};
    vector<int> dc = {0, 1, 0, -1};

    bool isValid(int r, int c, int n, int m) {
        return r >= 0 && r < n && c >= 0 && c < m;
    }

public:
    vector<int> numOfIslands(int n, int m, vector<vector<int>> &queries){

        DisjointSet ds(n * m);

        vector<vector<int>> vis(n, vector<int>(m, 0));

        int islandCount = 0;

        vector<int> result;

        for (auto &q : queries) {

            int row = q[0];
            int col = q[1];

            // If already land → no change
            if (vis[row][col]) {
                result.push_back(islandCount);
                continue;
            }

            // Convert water → land
            vis[row][col] = 1;
            islandCount++;

            int node = row * m + col;

            /*
            Try merging with 4 neighbors
            */
            for (int i = 0; i < 4; i++) {

                int nr = row + dr[i];
                int nc = col + dc[i];

                // Always check bounds FIRST
                if (isValid(nr, nc, n, m) && vis[nr][nc]) {

                    int adjNode = nr * m + nc;

                    // If different components → merge
                    if (!ds.find(node, adjNode)) {

                        ds.unionBySize(node, adjNode);

                        // Two islands merged → reduce count
                        islandCount--;
                    }
                }
            }

            result.push_back(islandCount);
        }

        return result;
    }
};
```


### Making a large island
```cpp
class Solution {
private:
    vector<int> dr = {-1, 0, 1, 0};
    vector<int> dc = {0, 1, 0, -1};

    bool isValid(int r, int c, int n) {
        return r >= 0 && r < n && c >= 0 && c < n;
    }

    /*
    Build initial islands using DSU
    All connected 1's → one component
    */
    void buildComponents(vector<vector<int>> &grid,
                         DisjointSet &ds, int n) {

        for (int row = 0; row < n; row++) {
            for (int col = 0; col < n; col++) {

                if (grid[row][col] == 0) continue;

                for (int d = 0; d < 4; d++) {

                    int nr = row + dr[d];
                    int nc = col + dc[d];

                    if (isValid(nr, nc, n) && grid[nr][nc] == 1) {

                        int node = row * n + col;
                        int adjNode = nr * n + nc;

                        ds.unionBySize(node, adjNode);
                    }
                }
            }
        }
    }

public:
    int largestIsland(vector<vector<int>>& grid) {

        int n = grid.size();

        DisjointSet ds(n * n);

        // Step 1: Build connected components
        buildComponents(grid, ds, n);

        int maxIsland = 0;

        /*  Step 2:
            Try converting each 0 → 1
            and merge neighboring islands
        */
        for (int row = 0; row < n; row++) {
            for (int col = 0; col < n; col++) {

                if (grid[row][col] == 1) continue;

                set<int> uniqueParents;

                for (int d = 0; d < 4; d++) {

                    int nr = row + dr[d];
                    int nc = col + dc[d];

                    if (isValid(nr, nc, n) && grid[nr][nc] == 1) {

                        int adjNode = nr * n + nc;

                        uniqueParents.insert(
                            ds.findUltimateParent(adjNode)
                        );
                    }
                }

                //  Sum sizes of unique neighboring components
                int combinedSize = 1; // current flipped cell

                for (int parent : uniqueParents) {
                    combinedSize += ds.size[parent];
                }

                maxIsland = max(maxIsland, combinedSize);
            }
        }

        /*  Step 3:
            Edge case → grid already full of 1's
        */
        for (int i = 0; i < n * n; i++) {
            int parent = ds.findUltimateParent(i);
            maxIsland = max(maxIsland, ds.size[parent]);
        }

        return maxIsland;
    }
};
```

### Most stones removed with same row or column
```cpp
class Solution {
public:
    int maxRemove(vector<vector<int>>& stones, int n) {

        int maxRow = 0, maxCol = 0;

        // Find max row & col
        for (auto &stone : stones) {
            maxRow = max(maxRow, stone[0]);
            maxCol = max(maxCol, stone[1]);
        }

        /*  We treat:
            - rows as nodes [0 → maxRow]
            - cols as nodes [maxRow+1 → maxRow+1+maxCol]

            This creates a bipartite graph:
            row ↔ column
        */

        DisjointSet ds(maxRow + maxCol + 2);

        unordered_map<int, int> usedNodes;

        // Step 1: Union row and column for each stone
        for (auto &stone : stones) {

            int rowNode = stone[0];
            int colNode = stone[1] + maxRow + 1;

            ds.unionBySize(rowNode, colNode);

            usedNodes[rowNode] = 1;
            usedNodes[colNode] = 1;
        }

        /*  Step 2: Count connected components
            Only consider nodes that were used
        */
        int components = 0;

        for (auto &it : usedNodes) {

            int node = it.first;

            if (ds.findUltimateParent(node) == node) {
                components++;
            }
        }

        /*  If we have k components,
            we can remove (n - k) stones
        */
        return n - components;
    }
};
```