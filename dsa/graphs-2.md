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