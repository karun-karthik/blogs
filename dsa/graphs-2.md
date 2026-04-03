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

### Shortest distance in binary maze
>Given an n x m matrix grid where each cell contains either 0 or 1, determine the shortest distance between a source cell and a destination cell. You can move to an adjacent cell (up, down, left, or right) if that adjacent cell has a value of 1. The path can only be created out of cells containing 1. If the destination cell is not reachable from the source cell, return -1.

```cpp
int shortestPath(vector<vector<int>> &grid, pair<int, int> source, pair<int, int> destination) {
    int n = grid.size();
    int m = grid[0].size();

    // If source == destination → no movement needed
    if (source == destination) return 0;

    // Distance matrix → stores shortest steps to reach each cell
    vector<vector<int>> dist(n, vector<int>(m, 1e9));
    dist[source.first][source.second] = 0;

    // Queue stores: {distance, {row, col}}
    queue<pair<int, pair<int,int>>> q;
    q.push({0, {source.first, source.second}});

    // 4-directional movement (up, right, down, left)
    int dr[] = {-1, 0, 1, 0};
    int dc[] = {0, 1, 0, -1};

    /*
    INTUITION:
    ----------
        - Grid is an unweighted graph (each move = cost 1)
        - BFS guarantees shortest path
        - dist[][] avoids revisiting with longer paths
    */

    while (!q.empty()) {

        auto [dis, cell] = q.front();
        q.pop();

        int row = cell.first;
        int col = cell.second;

        // Explore all 4 directions
        for (int i = 0; i < 4; i++) {

            int newRow = row + dr[i];
            int newCol = col + dc[i];

            // Check:
            // 1. Inside grid
            // 2. Cell is walkable (grid = 1)
            // 3. Found shorter path
            if (newRow >= 0 && newRow < n &&
                newCol >= 0 && newCol < m &&
                grid[newRow][newCol] == 1 &&
                dis + 1 < dist[newRow][newCol]) {

                dist[newRow][newCol] = dis + 1;

                // Early exit → BFS guarantees shortest path
                if (make_pair(newRow, newCol) == destination)
                    return dis + 1;

                q.push({dis + 1, {newRow, newCol}});
            }
        }
    }

    // Destination not reachable
    return -1;
}
```

### Path with Minimum Effort
>A hiker is preparing for an upcoming hike. Given heights, a 2D array of size rows x columns, where heights[row][col] represents the height of the cell (row, col). The hiker is situated in the top-left cell, (0, 0), and hopes to travel to the bottom-right cell, (rows-1, columns-1) (i.e.,0-indexed). He can move up, down, left, or right. He wishes to find a route that requires the minimum effort.
>A route's effort is the maximum absolute difference in heights between two consecutive cells of the route.
```cpp
#define P pair<int, pair<int, int>>
class Solution {
public:
    int MinimumEffort(vector<vector<int>> &heights) {

        int n = heights.size();
        int m = heights[0].size();

        // Directions: up, right, down, left
        vector<int> dr = {-1, 0, 1, 0};
        vector<int> dc = {0, 1, 0, -1};

        /*
        maxDiff[r][c] = minimum "effort" required to reach cell (r,c)
        Effort = maximum absolute height difference encountered along the path
        */
        vector<vector<int>> maxDiff(n, vector<int>(m, 1e9));
        maxDiff[0][0] = 0;

        // Min heap → {effort so far, {row, col}}
        priority_queue<P, vector<P>, greater<P>> pq;
        pq.push({0, {0, 0}});

        /*
        INTUITION:
        ----------
        This is NOT normal shortest path.

        Instead of:
            dist[u] + weight

        We use:
            max(previous_effort, current_edge_cost)

        Because:
            We want to MINIMIZE the MAXIMUM edge cost along the path
        */

        while (!pq.empty()) {

            auto p = pq.top();
            pq.pop();

            int diff = p.first;
            int row = p.second.first;
            int col = p.second.second;

            // If destination reached → this is optimal
            // (Dijkstra guarantee: first time we reach = minimum effort)
            if (row == n - 1 && col == m - 1)
                return diff;

            // Explore 4 directions
            for (int i = 0; i < 4; i++) {

                int newRow = row + dr[i];
                int newCol = col + dc[i];

                // Check bounds
                if (newRow >= 0 && newRow < n &&
                    newCol >= 0 && newCol < m) {

                    // Effort of this step (edge weight)
                    int currDiff = abs(heights[newRow][newCol] - heights[row][col]);

                    /*
                    New path effort =
                    max(previous effort, current edge cost)
                    */
                    int newEffort = max(diff, currDiff);

                    // Relaxation: update if we found a better path
                    if (newEffort < maxDiff[newRow][newCol]) {

                        maxDiff[newRow][newCol] = newEffort;

                        pq.push({newEffort, {newRow, newCol}});
                    }
                }
            }
        }

        return -1;  // should not happen normally
    }
};
```

### Cheapest flight within K stops
```cpp
class Solution{
public:
    int CheapestFlight(int n, vector<vector<int>> &flights, int src, int dst, int K) {
        // Step 1: Build graph
        vector<pair<int,int>> adj[n];
        for (auto &it : flights) {
            adj[it[0]].push_back({it[1], it[2]});
        }

        // Queue → {stops, node, cost}
        queue<pair<int, pair<int,int>>> q;
        q.push({0, {src, 0}});

        // Distance array (minimum cost to reach node)
        vector<int> dist(n, 1e9);
        dist[src] = 0;

        /*
        INTUITION:
        ----------
            We explore level-by-level (like BFS), where each level = number of stops.
            Unlike Dijkstra, we don't finalize nodes early because stops constraint matters.
        */

        while (!q.empty()) {

            auto [stops, p] = q.front();
            q.pop();

            int node = p.first;
            int cost = p.second;

            // If stops exceed limit → skip
            if (stops > K) continue;

            for (auto [adjNode, edgeWt] : adj[node]) {

                int newCost = cost + edgeWt;

                // Relax only if cheaper
                if (newCost < dist[adjNode]) {

                    dist[adjNode] = newCost;

                    q.push({stops + 1, {adjNode, newCost}});
                }
            }
        }

        return dist[dst] == 1e9 ? -1 : dist[dst];
    }
};
```

### Minimum multiplications to reach end
>Model numbers as nodes and multiplication as edges; since all edges have equal cost, use BFS to find minimum steps.
```cpp
#define P pair<int,int>
class Solution{
public:
    int minimumMultiplications(vector<int> &arr, int start, int end) {

        // If already at target
        if (start == end) return 0;

        int MOD = 100000;

        /*
        minSteps[x] = minimum steps required to reach value x
        Range: [0, 99999] due to modulo
        */
        vector<int> minSteps(MOD, INT_MAX);

        // Queue → {steps, current value}
        queue<P> q;

        minSteps[start] = 0;
        q.push({0, start});

        /*  INTUITION:
        ----------
            Think of numbers as nodes.
            From a node 'val', you can go to:
                (val * arr[i]) % 100000
            This is an unweighted graph → BFS gives shortest steps.
        */

        while (!q.empty()) {

            auto [steps, val] = q.front();
            q.pop();

            // Try all multiplications
            for (int i = 0; i < arr.size(); i++) {

                int next = (val * arr[i]) % MOD;

                // If we reach target → return immediately
                if (next == end)
                    return steps + 1;

                // If this path is better → update
                if (steps + 1 < minSteps[next]) {

                    minSteps[next] = steps + 1;

                    q.push({steps + 1, next});
                }
            }
        }

        // Target not reachable
        return -1;
    }
};
```

### Number of ways to arrive at destination
> Combine Dijkstra with DP: update ways when distances improve or match.
```cpp
#define P pair<long long, int>

class Solution{
public:
    int countPaths(int n, vector<vector<int>> &roads) {

        const int MOD = 1e9 + 7;

        // Adjacency list: node → {neighbor, time}
        vector<vector<pair<int,int>>> adj(n);
        for (auto &r : roads) {
            adj[r[0]].push_back({r[1], r[2]});
            adj[r[1]].push_back({r[0], r[2]});
        }

        // dist[i]  = shortest time to reach node i
        // ways[i]  = number of shortest ways to reach node i
        vector<long long> dist(n, LLONG_MAX);
        vector<long long> ways(n, 0);

        dist[0] = 0;
        ways[0] = 1;

        // Min-heap on distance → always expand closest node
        priority_queue<P, vector<P>, greater<P>> pq;
        pq.push({0, 0});  // {time, node}

        /*  CORE IDEA:
        ----------
            Standard Dijkstra + counting paths
            - First time we improve dist[v] → inherit ways from u
            - If we find another path with SAME shortest dist → add ways
        */

        while (!pq.empty()) {

            auto [currTime, node] = pq.top();
            pq.pop();

            // Skip stale entries (typical Dijkstra optimization)
            if (currTime > dist[node]) continue;

            for (auto [nbr, time] : adj[node]) {

                long long newTime = currTime + time;

                // Found strictly shorter path → reset ways
                if (newTime < dist[nbr]) {
                    dist[nbr] = newTime;
                    ways[nbr] = ways[node];   // inherit paths
                    pq.push({newTime, nbr});
                }

                // Found another shortest path → accumulate ways
                else if (newTime == dist[nbr]) {
                    ways[nbr] = (ways[nbr] + ways[node]) % MOD;
                }
            }
        }

        // ways[n-1] = number of shortest paths to destination
        return ways[n - 1] % MOD;
    }
};
```

### Bellman Ford Algorithm
> Relax all edges V-1 times and check for further relaxation to detect negative cycles.
```cpp
class Solution {
public:
    vector<int> bellman_ford(int V, vector<vector<int>>& edges, int S) {

        // dist[i] = shortest distance from source S to node i
        vector<int> dist(V, 1e9);   // use 1e8 as "infinity"
        dist[S] = 0;

        /*  CORE IDEA:
        ----------
            Relax all edges V-1 times.
            Why V-1?
            → Longest possible shortest path in a graph has at most V-1 edges.
        */

        for (int i = 0; i < V - 1; i++) {

            for (auto &e : edges) {

                int u = e[0];
                int v = e[1];
                int wt = e[2];

                // Relax edge only if source node is reachable
                if (dist[u] != 1e9 && dist[u] + wt < dist[v]) {
                    dist[v] = dist[u] + wt;
                }
            }
        }

        /*  NEGATIVE CYCLE CHECK:
        ---------------------
            If we can still relax any edge → negative cycle exists
        */

        for (auto &e : edges) {

            int u = e[0];
            int v = e[1];
            int wt = e[2];

            if (dist[u] != 1e9 && dist[u] + wt < dist[v]) {
                return {-1};  // negative cycle detected
            }
        }

        return dist;
    }
};
```

### Floyd-Warshall Algorithm
> Compute all-pairs shortest paths by iteratively considering each node as an intermediate node.
```cpp
class Solution {
public:
    void shortestDistance(vector<vector<int>>& matrix) {

        int n = matrix.size();

        /*
        STEP 1: Convert -1 → INF
        -1 means no direct edge
        Use large value so it doesn't affect min()
        */
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] == -1) {
                    matrix[i][j] = 1e9;
                }
            }
        }

        /*
        STEP 2: Distance from node to itself = 0
        */
        for (int i = 0; i < n; i++) {
            matrix[i][i] = 0;
        }

        /* CORE IDEA:
        ----------
            Try every node as an intermediate node (via)
            
            If going through 'via' gives shorter path → update
        */
        for (int via = 0; via < n; via++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {

                    // Relaxation using intermediate node
                    if (matrix[i][via] + matrix[via][j] < matrix[i][j]) {
                        matrix[i][j] = matrix[i][via] + matrix[via][j];
                    }
                }
            }
        }

        /* STEP 3: Convert INF back to -1 (unreachable) */
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] == 1e9) {
                    matrix[i][j] = -1;
                }
            }
        }
    }
};
```

### Find the city with the smallest number of neighbors
> Use Floyd-Warshall to compute all-pairs shortest paths, then count reachable cities for each node.
```cpp
class Solution {
public:
    int findCity(int n, int m, vector<vector<int>>& edges, int distanceThreshold) {

        const int INF = 1e9;

        // Step 1: Initialize adjacency matrix
        vector<vector<int>> dist(n, vector<int>(n, INF));

        // Distance to itself = 0
        for (int i = 0; i < n; i++) {
            dist[i][i] = 0;
        }

        // Fill edges (undirected)
        for (auto &it : edges) {
            int u = it[0], v = it[1], w = it[2];
            dist[u][v] = w;
            dist[v][u] = w;
        }

        /*
        STEP 2: Floyd-Warshall
        ----------------------
        Try every node as intermediate (via)
        */
        for (int via = 0; via < n; via++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {

                    // Avoid overflow when path doesn't exist
                    if (dist[i][via] == INF || dist[via][j] == INF) continue;

                    dist[i][j] = min(dist[i][j],
                                     dist[i][via] + dist[via][j]);
                }
            }
        }

        /*
        STEP 3: Find city with minimum reachable nodes
        (within distanceThreshold)
        
        If tie → pick city with larger index
        */
        int minCount = INF;
        int result = -1;

        for (int i = 0; i < n; i++) {

            int count = 0;

            for (int j = 0; j < n; j++) {
                if (i != j && dist[i][j] <= distanceThreshold) {
                    count++;
                }
            }

            // Tie-breaking handled automatically (<=)
            if (count <= minCount) {
                minCount = count;
                result = i;
            }
        }

        return result;
    }
};
```

### Kosaraju Algorithm
> Count number of strongly connected components
```cpp
class Solution{
public:

    // First DFS: compute finishing order
    void dfsFinishTime(int node, vector<int> graph[], vector<int> &visited, stack<int> &finishStack) {
        visited[node] = 1;
        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                dfsFinishTime(neighbor, graph, visited, finishStack);
            }
        }
        // Node finishes AFTER exploring all reachable nodes
        finishStack.push(node);
    }

    // Second DFS: explore one SCC in reversed graph
    void dfsMarkComponent(int node, vector<int> reversedGraph[], vector<int> &visited) {
        visited[node] = 1;
        for (int neighbor : reversedGraph[node]) {
            if (!visited[neighbor]) {
                dfsMarkComponent(neighbor, reversedGraph, visited);
            }
        }
    }

    int kosaraju(int totalNodes, vector<int> graph[]) {

        stack<int> finishStack;
        vector<int> visited(totalNodes, 0);

        /*
        STEP 1:
        Compute nodes in decreasing finishing time
        */
        for (int node = 0; node < totalNodes; node++) {
            if (!visited[node]) {
                dfsFinishTime(node, graph, visited, finishStack);
            }
        }

        /*
        STEP 2:
        Build reversed graph
        */
        vector<int> reversedGraph[totalNodes];

        for (int node = 0; node < totalNodes; node++) {
            for (int neighbor : graph[node]) {
                reversedGraph[neighbor].push_back(node);
            }
        }

        // Reset visited for second pass
        fill(visited.begin(), visited.end(), 0);

        /*
        STEP 3:
        Process nodes in stack order → each DFS = one SCC
        */
        int stronglyConnectedComponents = 0;

        while (!finishStack.empty()) {

            int node = finishStack.top();
            finishStack.pop();

            if (!visited[node]) {
                stronglyConnectedComponents++;
                dfsMarkComponent(node, reversedGraph, visited);
            }
        }

        return stronglyConnectedComponents;
    }
};
```

### Bridges in graph (Tarjan's Algorithm)
> Find bridges in a graph using Tarjan's algorithm, An edge u–v is a bridge if removing it disconnects the graph.
```cpp
class Solution {
public:

    void dfs(int node, int parent, vector<int> adj[],
            vector<int> &visited, vector<int> &tin, vector<int> &low,
            int &timer, vector<vector<int>> &bridges) {

        visited[node] = 1;

        tin[node] = low[node] = timer++;

        /*  tin[node] → when node was first visited
            low[node] → earliest reachable node (via back edge) */

        for (int neighbor : adj[node]) {

            // Ignore the edge we came from
            if (neighbor == parent) continue;

            if (!visited[neighbor]) {

                // Tree edge
                dfs(neighbor, node, adj, visited, tin, low, timer, bridges);

                // Update low after returning
                low[node] = min(low[node], low[neighbor]);

                // 🔥 Bridge condition
                if (low[neighbor] > tin[node]) {
                    bridges.push_back({node, neighbor});
                }
            }
            else {
                // Back edge → update low
                low[node] = min(low[node], tin[neighbor]);
            }
        }
    }

    vector<vector<int>> criticalConnections(int V, vector<vector<int>>& E) {

        // Step 1: Build graph
        vector<int> adj[V];
        for (auto &e : E) {
            int u = e[0], v = e[1];
            adj[u].push_back(v);
            adj[v].push_back(u);
        }

        vector<int> visited(V, 0);
        vector<int> tin(V, -1), low(V, -1);

        int timer = 0;
        vector<vector<int>> bridges;

        // Run DFS for all components
        for (int i = 0; i < V; i++) {
            if (!visited[i]) {
                dfs(i, -1, adj, visited, tin, low, timer, bridges);
            }
        }

        return bridges;
    }
};
```

### Articulation point in graph

```cpp
class Solution {
public:

    void dfs(int node, int parent, vector<int> adj[], vector<int> &visited,
            vector<int> &tin, vector<int> &low, vector<int> &mark, int &timer) {

        visited[node] = 1;

        tin[node] = low[node] = timer++;

        int childCount = 0;

        for (int neighbor : adj[node]) {

            if (neighbor == parent) continue;

            if (!visited[neighbor]) {

                dfs(neighbor, node, adj, visited, tin, low, mark, timer);

                // Update low value after DFS
                low[node] = min(low[node], low[neighbor]);

                /*  ARTICULATION CONDITION (non-root):
                    If child cannot reach ancestors of node */
                if (low[neighbor] >= tin[node] && parent != -1) {
                    mark[node] = 1;
                }
                childCount++;
            }
            else {
                // Back edge
                low[node] = min(low[node], tin[neighbor]);
            }
        }

        /*  ROOT CONDITION:
            Root is articulation point if it has more than 1 child */
        if (parent == -1 && childCount > 1) {
            mark[node] = 1;
        }
    }

    vector<int> articulationPoints(int n, vector<int> adj[]) {

        vector<int> visited(n, 0);
        vector<int> tin(n, -1), low(n, -1);
        vector<int> mark(n, 0);

        int timer = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                dfs(i, -1, adj, visited, tin, low, mark, timer);
            }
        }

        vector<int> result;

        for (int i = 0; i < n; i++) {
            if (mark[i]) result.push_back(i);
        }

        // If no articulation points
        if (result.empty()) return {-1};

        return result;
    }
};
```