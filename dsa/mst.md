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

