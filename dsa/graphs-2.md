# Shortest Path Algorithms

### Dijkstra's Algorithm
> From given source to all nodes ~ shortest distance
> Works only for non-negative weights ~ dijkstra fails with negative weights because a node’s distance can be improved after it has already been finalized.
```cpp
class Solution {
public:
    vector<int> dijkstra(int V, vector<vector<int>> adj[], int S) {

        // Distance array → shortest distance from source
        vector<int> dist(V, 1e9);
        dist[S] = 0;

        // Set stores {distance, node}
        // Always keeps smallest distance at begin()
        set<pair<int,int>> st;
        st.insert({0, S});

        /*
        INTUITION:
        ----------
        Set always gives us the node with minimum distance.
        When we update a node’s distance, we REMOVE its old entry
        and INSERT the new one → no duplicates, no stale entries.
        */

        while (!st.empty()) {

            auto it = *(st.begin());   // smallest distance node
            st.erase(it);

            int node = it.second;
            int currDist = it.first;

            // Explore neighbors
            for (auto &edge : adj[node]) {

                int neighbor = edge[0];
                int weight   = edge[1];

                // Relaxation step
                if (currDist + weight < dist[neighbor]) {

                    // If neighbor already has a distance in set → remove it
                    if (dist[neighbor] != 1e9) {
                        st.erase({dist[neighbor], neighbor});
                    }

                    // Update distance
                    dist[neighbor] = currDist + weight;

                    // Insert updated distance
                    st.insert({dist[neighbor], neighbor});
                }
            }
        }

        return dist;
    }
};
```

### Print Shortest Path
> If there exists a path, then return a list whose first element is the weight of the path and the remaining elements represent the shortest path from vertex 1 to vertex n.
```cpp
class Solution {
public:
    vector<int> shortestPath(int n, int m, vector<vector<int>>& edges) {

        // Step 1: Build graph (1-based)
        vector<vector<pair<int,int>>> adj(n + 1);

        for (auto &e : edges) {
            int u = e[0], v = e[1], w = e[2];

            adj[u].push_back({v, w});
            adj[v].push_back({u, w});
        }

        // Step 2: Distance + Parent
        vector<int> dist(n + 1, 1e9);
        vector<int> parent(n + 1);

        for (int i = 1; i <= n; i++) parent[i] = i;

        dist[1] = 0;

        // Step 3: Set → {distance, node}
        set<pair<int,int>> st;
        st.insert({0, 1});

        /*
        INTUITION:
        ----------
        - Always pick smallest distance node (st.begin())
        - When updating a node → remove old entry and insert new one
        */

        while (!st.empty()) {

            auto it = *(st.begin());
            st.erase(it);

            int node = it.second;
            int currDist = it.first;

            for (auto [neighbor, weight] : adj[node]) {

                if (currDist + weight < dist[neighbor]) {

                    // remove old value if exists
                    if (dist[neighbor] != 1e9) {
                        st.erase({dist[neighbor], neighbor});
                    }

                    // update distance
                    dist[neighbor] = currDist + weight;

                    // track parent
                    parent[neighbor] = node;

                    // insert updated value
                    st.insert({dist[neighbor], neighbor});
                }
            }
        }

        // Step 4: If unreachable
        if (dist[n] == 1e9) return {-1};

        // Step 5: Reconstruct path
        vector<int> path;
        int node = n;

        while (parent[node] != node) {
            path.push_back(node);
            node = parent[node];
        }

        path.push_back(1);

        reverse(path.begin(), path.end());

        // Step 6: Add total weight
        vector<int> ans;
        ans.push_back(dist[n]);

        for (auto x : path) ans.push_back(x);

        return ans;
    }
};
```