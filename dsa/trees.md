## Traversals

### Inorder Traversal
```cpp
void solve(TreeNode* root, vector<int>& res) {
    if (root == nullptr) {
        return;
    }
    solve(root->left, res);
    res.push_back(root->data);
    solve(root->right, res);
}
vector<int> inorder(TreeNode* root){
    vector<int> res;
    solve(root, res);
    return res;   
}
```

```cpp
vector<int> inorder(TreeNode* root) {

    vector<int> res;
    stack<TreeNode*> st;

    TreeNode* curr = root;

    while (curr != nullptr || !st.empty()) {

        // Reach the leftmost node
        while (curr != nullptr) {
            st.push(curr);
            curr = curr->left;
        }

        // Process the node
        curr = st.top();
        st.pop();

        res.push_back(curr->data);

        // Move to the right subtree
        curr = curr->right;
    }

    return res;
}
```

### PreOrder Traversal
```cpp
void solve(TreeNode* root, vector<int>& res) {
    if (root == nullptr) {
        return;
    }
    res.push_back(root->data);
    solve(root->left, res);
    solve(root->right, res);
}
vector<int> preorder(TreeNode* root){
    vector<int> res;
    solve(root, res);
    return res;   
}
```
```cpp
vector<int> preorder(TreeNode* root) {

    vector<int> res;

    if (root == nullptr)
        return res;

    stack<TreeNode*> st;
    st.push(root);

    while (!st.empty()) {

        TreeNode* node = st.top();
        st.pop();

        // Process current node
        res.push_back(node->data);

        /*
            Push right child first so that
            left child is processed first
            (stack is LIFO)
        */
        if (node->right)
            st.push(node->right);

        if (node->left)
            st.push(node->left);
    }

    return res;
}
```

### PostOrder Traversal
```cpp
void solve(TreeNode* root, vector<int>& res) {
    if (root == nullptr) {
        return;
    }
    solve(root->left, res);
    solve(root->right, res);
    res.push_back(root->data);
}
vector<int> postorder(TreeNode* root){
    vector<int> res;
    solve(root, res);
    return res;   
}
```
```cpp
vector<int> postorder(TreeNode* root) {

    vector<int> res;

    if (root == nullptr)
        return res;

    stack<TreeNode*> st;
    st.push(root);

    while (!st.empty()) {

        TreeNode* node = st.top();
        st.pop();

        // Add node value
        res.push_back(node->data);

        // Push left first
        if (node->left)
            st.push(node->left);

        // Push right next
        if (node->right)
            st.push(node->right);
    }

    // Reverse to get postorder
    reverse(res.begin(), res.end());

    return res;
}
```

### LevelOrder Traversal
```cpp
vector<vector<int>> levelOrder(TreeNode* root) {
    // Result vector storing nodes level by level
    vector<vector<int>> res;

    // If the tree is empty, return empty result
    if (root == nullptr)
        return res;

    // Queue used for BFS traversal
    queue<TreeNode*> q;

    // Start with the root node
    q.push(root);

    // Process nodes level by level
    while (!q.empty()) {

        // Number of nodes in the current level
        int size = q.size();

        // Vector to store values of the current level
        vector<int> aux;

        // Process all nodes at the current level
        for (int i = 0; i < size; i++) {

            // Get the front node from the queue
            TreeNode* node = q.front();
            q.pop();

            // Store its value
            aux.push_back(node->data);

            // Add left child to queue if it exists
            if (node->left)
                q.push(node->left);

            // Add right child to queue if it exists
            if (node->right)
                q.push(node->right);
        }

        // Add the current level to the result
        res.push_back(aux);
    }

    return res;
}
```
```cpp
// DFS helper function that keeps track of the current level
void dfs(TreeNode* root, int level, vector<vector<int>>& res) {

    // Base case: if node is null, stop recursion
    if (root == nullptr)
        return;

    /*
        If we reached a new level for the first time,
        create a new vector to store nodes of this level.
        
        Example:
        level = 0 → create res[0]
        level = 1 → create res[1]
        level = 2 → create res[2]
    */
    if (res.size() == level)
        res.push_back({});

    // Add the current node's value to its corresponding level
    res[level].push_back(root->data);

    // Traverse left subtree and increase level
    dfs(root->left, level + 1, res);

    // Traverse right subtree and increase level
    dfs(root->right, level + 1, res);
}


vector<vector<int>> levelOrder(TreeNode* root) {

    // Result container storing nodes level-by-level
    vector<vector<int>> res;

    // Start DFS from root at level 0
    dfs(root, 0, res);

    return res;
}
```

### In, Pre, Post in One Traversal
```cpp
// DFS helper that fills preorder, inorder, and postorder in one traversal
void dfs(TreeNode* root, vector<int>& preorder, vector<int>& inorder,
            vector<int>& postorder) {
    // Base case: if node is null, stop recursion
    if (root == nullptr) return;

    /*
        PREORDER traversal
        Order: Node → Left → Right
        So we process the node BEFORE exploring children
    */
    preorder.push_back(root->data);

    // Traverse left subtree
    dfs(root->left, preorder, inorder, postorder);

    /*
        INORDER traversal
        Order: Left → Node → Right
        So we process the node AFTER finishing left subtree
    */
    inorder.push_back(root->data);

    // Traverse right subtree
    dfs(root->right, preorder, inorder, postorder);

    /*
        POSTORDER traversal
        Order: Left → Right → Node
        So we process the node AFTER finishing both subtrees
    */
    postorder.push_back(root->data);
}

vector<vector<int>> treeTraversal(TreeNode* root) {
    // Vectors to store each traversal
    vector<int> inorder;
    vector<int> preorder;
    vector<int> postorder;

    // Run DFS to populate all three traversals
    dfs(root, preorder, inorder, postorder);

    /*
        Return traversals in the required order:
        index 0 → inorder
        index 1 → preorder
        index 2 → postorder
    */
    return {inorder, preorder, postorder};
}
```

## Medium
### Maximum Dept of a Binary Tree
```cpp
// Function to calculate the maximum depth of a binary tree
int maxDepth(TreeNode* root) {

    // Base Case:
    // If the current node is null, the depth contributed by this branch is 0
    if (root == nullptr)
        return 0;

    // Recursively compute the depth of the left subtree
    int leftDepth = maxDepth(root->left);

    // Recursively compute the depth of the right subtree
    int rightDepth = maxDepth(root->right);

    // The depth of the current node is:
    // 1 (for the current node itself) + the greater depth of its two subtrees
    return 1 + max(leftDepth, rightDepth);
}
```
```cpp
#include <queue>

// Iterative solution using BFS (Level Order Traversal)
int maxDepth(TreeNode* root) {

    // If the tree is empty, depth is 0
    if (root == nullptr)
        return 0;

    queue<TreeNode*> q;
    q.push(root);

    int depth = 0;

    // Process the tree level by level
    while (!q.empty()) {

        int levelSize = q.size();  // Number of nodes at the current level
        depth++;                   // Moving to the next level increases depth

        // Process all nodes in the current level
        for (int i = 0; i < levelSize; i++) {

            TreeNode* node = q.front();
            q.pop();

            // Add left child to queue if it exists
            if (node->left)
                q.push(node->left);

            // Add right child to queue if it exists
            if (node->right)
                q.push(node->right);
        }
    }

    return depth;
}
```

### Check if two trees are idential
```cpp
// Function to check if two binary trees are identical
bool isSameTree(TreeNode* p, TreeNode* q) {

    // Case 1: If both nodes are null, the trees match at this branch
    if (p == nullptr && q == nullptr)
        return true;

    // Case 2: If one node is null and the other is not, trees are different
    if (p == nullptr || q == nullptr)
        return false;

    // Case 3: If current node values differ, trees are not identical
    if (p->data != q->data)
        return false;

    // Recursively check left and right subtrees
    return isSameTree(p->left, q->left) &&
           isSameTree(p->right, q->right);
}
```
```cpp

bool isSameTree(TreeNode* p, TreeNode* q) {

    queue<TreeNode*> queue1, queue2;
    queue1.push(p);
    queue2.push(q);

    while (!queue1.empty() && !queue2.empty()) {

        TreeNode* n1 = queue1.front(); queue1.pop();
        TreeNode* n2 = queue2.front(); queue2.pop();

        // If both nodes are null, continue
        if (!n1 && !n2)
            continue;

        // If one is null or values differ
        if (!n1 || !n2 || n1->data != n2->data)
            return false;

        // Push children for comparison
        queue1.push(n1->left);
        queue2.push(n2->left);

        queue1.push(n1->right);
        queue2.push(n2->right);
    }

    return queue1.empty() && queue2.empty();
}
```

### Check if a binary tree is balanced
```cpp
// Helper function that returns height if balanced, otherwise -1
int checkHeight(TreeNode* root) {
    // Base case: empty subtree has height 0
    if (root == nullptr) return 0;

    // Check height of left subtree
    int leftHeight = checkHeight(root->left);

    // If left subtree is unbalanced, propagate -1
    if (leftHeight == -1) return -1;

    // Check height of right subtree
    int rightHeight = checkHeight(root->right);

    // If right subtree is unbalanced, propagate -1
    if (rightHeight == -1) return -1;

    // If height difference > 1, tree is not balanced
    if (abs(leftHeight - rightHeight) > 1) return -1;

    // Otherwise return height of current node
    return 1 + max(leftHeight, rightHeight);
}

bool isBalanced(TreeNode* root) {
    // If helper returns -1, tree is unbalanced
    return checkHeight(root) != -1;
}
```

### Diameter of a binary tree
```cpp
// Helper function to calculate height of a subtree
int height(TreeNode* node) {

    // Base case: empty subtree has height 0
    if (node == nullptr)
        return 0;

    // Height of current node = 1 + maximum height of its subtrees
    return 1 + max(height(node->left), height(node->right));
}

// Function to calculate diameter of binary tree (Brute Force)
int diameterOfBinaryTree(TreeNode* root) {

    // If tree is empty, diameter is 0
    if (root == nullptr)
        return 0;

    // Step 1: Calculate height of left subtree
    int leftHeight = height(root->left);

    // Step 2: Calculate height of right subtree
    int rightHeight = height(root->right);

    // Step 3: Diameter passing through the current node
    // This is the longest path that goes through this node
    int currentDiameter = leftHeight + rightHeight;

    // Step 4: Recursively calculate diameter of left subtree
    int leftDiameter = diameterOfBinaryTree(root->left);

    // Step 5: Recursively calculate diameter of right subtree
    int rightDiameter = diameterOfBinaryTree(root->right);

    // Step 6: Return the maximum diameter found
    return max(currentDiameter, max(leftDiameter, rightDiameter));
}
```
```cpp
// Helper function to compute height while updating diameter
int height(TreeNode* root, int& diameter) {

    // Base case: if node is null, height is 0
    if (root == nullptr)
        return 0;

    // Recursively compute height of left subtree
    int lh = height(root->left, diameter);

    // Recursively compute height of right subtree
    int rh = height(root->right, diameter);

    // Update the diameter if the path through current node is longer
    // Path length = height of left subtree + height of right subtree
    diameter = max(diameter, lh + rh);

    // Return height of current node
    // Height = 1 (current node) + max height of its subtrees
    return 1 + max(lh, rh);
}

int diameterOfBinaryTree(TreeNode* root) {

    // Variable to store maximum diameter found during traversal
    int diameter = 0;

    // Start DFS traversal to compute heights and update diameter
    height(root, diameter);

    // Return the maximum diameter found
    return diameter;
}
```

### Maximum Path Sum of a Tree
```cpp
// Helper function to compute maximum path sum going downward
int maxDownwardPath(TreeNode* node) {

    if (node == nullptr)
        return 0;

    int left = maxDownwardPath(node->left);
    int right = maxDownwardPath(node->right);

    // Return best downward path starting at this node
    return max(0, node->val + max(left, right));
}

int maxPathSum(TreeNode* root) {

    if (root == nullptr)
        return INT_MIN;

    // Compute maximum downward paths
    int left = maxDownwardPath(root->left);
    int right = maxDownwardPath(root->right);

    // Path passing through this node
    int throughRoot = root->val + left + right;

    // Recursively compute for subtrees
    int leftMax = maxPathSum(root->left);
    int rightMax = maxPathSum(root->right);

    // Return best among the three
    return max(throughRoot, max(leftMax, rightMax));
}
```
```cpp
int dfs(TreeNode* node, int& maxSum) {
    // Base case
    if (node == nullptr)
        return 0;

    // Get max path sum from left and right subtrees
    int left = max(0, dfs(node->left, maxSum));
    int right = max(0, dfs(node->right, maxSum));

    // Update global maximum path sum
    maxSum = max(maxSum, node->data + left + right);

    // Return best path going upward (parent can only take one side)
    return node->data + max(left, right);
}

int maxPathSum(TreeNode* root) {
    int maxSum = INT_MIN;
    dfs(root, maxSum);
    return maxSum;
}
```

### Check if a binary tree is symmetric
```cpp
// Helper function to check if two subtrees are mirror images
bool isEqual(TreeNode* p, TreeNode* q) {

    // Case 1: If both nodes are null, they are symmetric
    if (p == NULL && q == NULL)
        return true;

    // Case 2: If only one node is null, trees are not symmetric
    if (p == NULL || q == NULL)
        return false;

    // Case 3: If node values differ, symmetry breaks
    if (p->data != q->data)
        return false;

    // Recursive mirror comparison
    // left of first subtree should match right of second subtree
    // right of first subtree should match left of second subtree
    return isEqual(p->left, q->right) &&
           isEqual(p->right, q->left);
}


// Main function to check if tree is symmetric
bool isSymmetric(TreeNode* root) {

    // An empty tree is symmetric
    if (root == NULL)
        return true;

    // Check if left and right subtrees are mirrors
    return isEqual(root->left, root->right);
}
```
```cpp
bool isSymmetric(TreeNode* root) {

    if (root == NULL)
        return true;

    queue<TreeNode*> q;
    q.push(root->left);
    q.push(root->right);

    while (!q.empty()) {

        TreeNode* n1 = q.front(); q.pop();
        TreeNode* n2 = q.front(); q.pop();

        if (n1 == NULL && n2 == NULL)
            continue;

        if (n1 == NULL || n2 == NULL)
            return false;

        if (n1->data != n2->data)
            return false;

        // Push mirror children
        q.push(n1->left);
        q.push(n2->right);

        q.push(n1->right);
        q.push(n2->left);
    }

    return true;
}
```

## FAQs

### Zig-Zag Level order traversal
```cpp
vector<vector<int>> zigzagLevelOrder(TreeNode* root) {

    // Result container storing all levels
    vector<vector<int>> res;

    // Edge case: empty tree
    if (root == nullptr)
        return res;

    // Queue for BFS traversal
    queue<TreeNode*> q;
    q.push(root);

    // Direction flag
    // true  -> left to right
    // false -> right to left
    bool leftToRight = true;

    while (!q.empty()) {

        // Number of nodes in current level
        int levelSize = q.size();

        // Preallocate vector for current level
        vector<int> currentLevel(levelSize);

        for (int i = 0; i < levelSize; ++i) {

            TreeNode* node = q.front();
            q.pop();

            // Decide index based on traversal direction
            int idx = leftToRight ? i : levelSize - i - 1;

            // Place node value at correct position
            currentLevel[idx] = node->data;

            // Add children to queue for next level
            if (node->left)
                q.push(node->left);

            if (node->right)
                q.push(node->right);
        }

        // Toggle direction for next level
        leftToRight = !leftToRight;

        // Add current level to result
        res.push_back(currentLevel);
    }

    return res;
}
```

### Boundary Traversal
```cpp
bool isLeaf(TreeNode* node) {
    return (node->left == nullptr && node->right == nullptr);
}

// Add left boundary excluding leaf nodes
void addLeftBoundary(TreeNode* root, vector<int>& res) {

    TreeNode* curr = root->left;

    while (curr) {

        if (!isLeaf(curr))
            res.push_back(curr->data);

        // Prefer left child, otherwise go right
        if (curr->left)
            curr = curr->left;
        else
            curr = curr->right;
    }
}

// Add all leaf nodes using DFS
void addLeaves(TreeNode* root, vector<int>& res) {

    if (root == nullptr)
        return;

    if (isLeaf(root)) {
        res.push_back(root->data);
        return;
    }

    addLeaves(root->left, res);
    addLeaves(root->right, res);
}

// Add right boundary in reverse order
void addRightBoundary(TreeNode* root, vector<int>& res) {

    TreeNode* curr = root->right;
    vector<int> temp;

    while (curr) {

        if (!isLeaf(curr))
            temp.push_back(curr->data);

        // Prefer right child, otherwise go left
        if (curr->right)
            curr = curr->right;
        else
            curr = curr->left;
    }

    // Add nodes in reverse
    for (int i = temp.size() - 1; i >= 0; i--)
        res.push_back(temp[i]);
}

vector<int> boundary(TreeNode* root) {

    vector<int> res;

    if (root == nullptr)
        return res;

    // Root is always part of boundary
    if (!isLeaf(root))
        res.push_back(root->data);

    // Add left boundary
    addLeftBoundary(root, res);

    // Add leaf nodes
    addLeaves(root, res);

    // Add right boundary
    addRightBoundary(root, res);

    return res;
}
```

### Vertical Order Traversal
```cpp
vector<vector<int>> verticalTraversal(TreeNode* root) {
    /*
        Data structure used to organize nodes by vertical position.
        map<column, map<row, multiset<values>>>

        Why this structure?
        1. Outer map (column):
           Keeps columns automatically sorted from left → right.
        2. Inner map (row):
           Keeps nodes ordered from top → bottom.
        3. multiset:
           If multiple nodes share the same (row, column),
           their values must be sorted. multiset maintains this order.
    */
    map<int, map<int, multiset<int>>> nodes;


    /*
        BFS queue storing:
        - current node pointer
        - (row, column) coordinates of that node
        We use BFS so that nodes are naturally processed
        level by level (top → bottom).
    */
    queue<pair<TreeNode*, pair<int,int>>> q;

    /* Root node starts at coordinate (row = 0, column = 0) */
    q.push({root, {0,0}});

    /* Standard BFS traversal of the binary tree */
    while (!q.empty()) {

        /*
            Structured binding:
            Extract node and its (row, column) coordinates
        */
        auto [node, pos] = q.front();
        q.pop();

        int row = pos.first;
        int col = pos.second;


        /*
            Insert the node value into the structure.

            nodes[col][row] groups nodes that share the same
            vertical column and depth level.

            multiset ensures sorted order when multiple nodes
            appear in the same position.
        */
        nodes[col][row].insert(node->data);


        /*
            Assign coordinates to child nodes.

            Left child:
                row increases (going down)
                column decreases (moving left)

            Right child:
                row increases
                column increases (moving right)
        */
        if (node->left) q.push({node->left, {row + 1, col - 1}});
        if (node->right) q.push({node->right, {row + 1, col + 1}});
    }


    /*
        Build the final result.

        Because 'nodes' is a map:
        - columns are already sorted from leftmost → rightmost
    */
    vector<vector<int>> res;


    for (auto &[col, rows] : nodes) {
        /*
            This vector will store all nodes belonging
            to the current vertical column.
        */
        vector<int> v;

        /*
            Iterate rows from top → bottom
        */
        for (auto &[row, vals] : rows) {
            /*
                Insert all values stored in the multiset.
                Values are already sorted if multiple nodes
                share the same (row, column).
            */
            v.insert(v.end(), vals.begin(), vals.end());
        }

        res.push_back(v);
    }

    return res;
}
```

### Top View of a Binary Tree
```cpp
vector<int> topView(TreeNode* root) {
    /*
        Map to store the first node encountered at each horizontal distance.

        Key   → horizontal distance (column)
        Value → pointer to the node visible from the top

        map is used instead of unordered_map because
        it keeps keys sorted from leftmost → rightmost.
    */
    map<int, TreeNode*> mp;

    /*
        Queue for BFS traversal.

        Each entry stores:
        - horizontal distance from root
        - pointer to the current node

        Horizontal distance rules:
            root → 0
            left child → hd - 1
            right child → hd + 1
    */
    queue<pair<int, TreeNode*>> q;

    q.push({0, root});

    /*
        BFS traversal ensures we process nodes level by level.

        This is important because the top view requires the
        FIRST node encountered at each horizontal distance.
    */
    while (!q.empty()) {
        auto node = q.front();
        q.pop();

        int hd = node.first;  // horizontal distance
        TreeNode* curr = node.second;

        /*
            If this horizontal distance has not been seen before,
            store this node as the visible node for that column.

            We do NOT overwrite it later because the first node
            encountered in BFS is the topmost node.
        */
        if (mp.find(hd) == mp.end()) mp[hd] = curr;

        /*
            Add left child with updated horizontal distance
        */
        if (curr->left) q.push({hd - 1, curr->left});

        /*
            Add right child with updated horizontal distance
        */
        if (curr->right) q.push({hd + 1, curr->right});
    }

    /*
        Extract nodes from the map.

        Since map keeps keys sorted,
        we automatically get the order:
        leftmost column → rightmost column.
    */
    vector<int> aux;

    for (auto i : mp) aux.push_back(i.second->data);

    return aux;
}
```

### Bottom View of a Binary Tree
```cpp
vector<int> bottomView(TreeNode *root) {
    /*
        Map storing the latest node encountered
        at each horizontal distance (column).

        key   → column index
        value → node value visible from bottom
    */
    map<int, int> mp;

    /*
        Queue used for BFS traversal.

        Each entry stores:
        - horizontal distance from root
        - pointer to the current node
    */
    queue<pair<int, TreeNode *>> q;

    /*
        Root starts at horizontal distance 0
    */
    q.push({0, root});

    /*
        Perform BFS traversal
    */
    while (!q.empty()) {
        auto [hd, node] = q.front();
        q.pop();

        /*
            For bottom view we always overwrite.

            Since BFS processes nodes level by level,
            deeper nodes naturally replace earlier ones.
        */
        mp[hd] = node->data;

        /*
            Left child moves one column left
        */
        if (node->left) q.push({hd - 1, node->left});

        /*
            Right child moves one column right
        */
        if (node->right) q.push({hd + 1, node->right});
    }

    /*
        Extract nodes from leftmost column
        to rightmost column.
    */
    vector<int> res;

    for (auto &[col, value] : mp) res.push_back(value);

    return res;
}
```

### Right View of a Binary Tree
```cpp
vector<int> rightSideView(TreeNode* root) {

    vector<int> res;
    if (root == nullptr) return res;

    queue<TreeNode*> q;
    q.push(root);

    // Level order traversal
    while (!q.empty()) {

        int levelSize = q.size();

        for (int i = 0; i < levelSize; i++) {

            TreeNode* node = q.front();
            q.pop();

            // If this is the last node of the level
            if (i == levelSize - 1)
                res.push_back(node->data);

            // Push children for next level
            if (node->left)  q.push(node->left);
            if (node->right) q.push(node->right);
        }
    }

    return res;
}
```

### Left View of a Binary Tree
```cpp
vector<int> leftSideView(TreeNode* root) {

    vector<int> res;
    if (root == nullptr) return res;

    queue<TreeNode*> q;
    q.push(root);

    while (!q.empty()) {

        int levelSize = q.size();

        for (int i = 0; i < levelSize; i++) {

            TreeNode* node = q.front();
            q.pop();

            // If this is the first node of the level
            if (i == 0)
                res.push_back(node->data);

            if (node->left)  q.push(node->left);
            if (node->right) q.push(node->right);
        }
    }

    return res;
}
```

### Print root to leaf path in BT
```cpp
void dfs(TreeNode* node, vector<int>& path, vector<vector<int>>& res) {
    if (node == nullptr) return;

    // Add current node to path
    path.push_back(node->data);

    // If leaf node, store the path
    if (node->left == nullptr && node->right == nullptr) {
        res.push_back(path);
    } else {
        // Continue exploring left and right subtrees
        dfs(node->left, path, res);
        dfs(node->right, path, res);
    }

    // Backtrack: remove current node before returning
    path.pop_back();
}

vector<vector<int>> allRootToLeaf(TreeNode* root) {
    vector<vector<int>> res;
    vector<int> path;

    dfs(root, path, res);

    return res;
}
```

### Lowest Common Ancestor
```cpp
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    /*
        Base Case:

        1. If we reach a null node → no ancestor found.
        2. If the current node is either p or q → return it.

        Returning the node signals to the parent recursion
        that one of the target nodes has been found.
    */
    if (root == NULL || root == p || root == q)
        return root;


    /* Recursively search for p and q in the left subtree */
    TreeNode* left = lowestCommonAncestor(root->left, p, q);


    /* Recursively search for p and q in the right subtree */
    TreeNode* right = lowestCommonAncestor(root->right, p, q);


    /* Now interpret the results from left and right. */

    // If p and q are both found in different subtrees,
    // current node is their Lowest Common Ancestor
    if (left != nullptr && right != nullptr)
        return root;

    /*
        If one side returned null, it means both nodes
        are located in the other subtree.
    */

    if (left == nullptr)
        return right;

    return left;
}
```

### Maximum width of a Binary Tree
```cpp
long long int widthOfBinaryTree(TreeNode* root) {
    if (!root) return 0;
    long long ans = 0;
    /*
        Queue stores:
        - node pointer
        - index representing its position in a complete binary tree
    */
    queue<pair<TreeNode*, long long>> q;
    q.push({root, 0});

    while (!q.empty()) {
        int levelSize = q.size();

        // first index of current level
        long long start = q.front().second;
        long long first, last;

        for (int i = 0; i < levelSize; i++) {
            auto [node, idx] = q.front();
            q.pop();

            /* Normalize index to prevent overflow by subtracting the starting index */
            idx -= start;

            if (i == 0) first = idx;
            if (i == levelSize - 1) last = idx;
            if (node->left) q.push({node->left, 2 * idx});
            if (node->right) q.push({node->right, 2 * idx + 1});
        }
        ans = max(ans, last - first + 1);
    }
    return ans;
}
```

### Print all nodes at distance K in Binary Tree
```cpp
vector<int> distanceK(TreeNode* root, TreeNode* target, int k){

    // Map to store parent pointers for each node
    unordered_map<TreeNode*, TreeNode*> parent;

    // BFS to build parent mapping
    queue<TreeNode*> q;
    q.push(root);

    while (!q.empty()) {

        TreeNode* node = q.front();
        q.pop();

        if (node->left) {
            parent[node->left] = node;
            q.push(node->left);
        }

        if (node->right) {
            parent[node->right] = node;
            q.push(node->right);
        }
    }

    /*
        BFS starting from the target node
        to explore nodes at increasing distances
    */
    unordered_map<TreeNode*, bool> visited;
    queue<TreeNode*> bfs;

    bfs.push(target);
    visited[target] = true;

    int dist = 0;

    while (!bfs.empty()) {

        int size = bfs.size();

        // If we've reached distance k, stop expanding
        if (dist == k) break;

        dist++;

        for (int i = 0; i < size; i++) {

            TreeNode* node = bfs.front();
            bfs.pop();

            // Explore left child
            if (node->left && !visited[node->left]) {
                visited[node->left] = true;
                bfs.push(node->left);
            }

            // Explore right child
            if (node->right && !visited[node->right]) {
                visited[node->right] = true;
                bfs.push(node->right);
            }

            // Explore parent
            if (parent[node] && !visited[parent[node]]) {
                visited[parent[node]] = true;
                bfs.push(parent[node]);
            }
        }
    }

    /*
        Remaining nodes in queue are exactly k distance away
    */
    vector<int> res;

    while (!bfs.empty()) {
        res.push_back(bfs.front()->data);
        bfs.pop();
    }

    return res;
}
```

### Minimum time taken to burn a Binary Tree from a given Node
```cpp
int timeToBurnTree(TreeNode* root, int start){

    // Map to store parent of every node
    unordered_map<TreeNode*, TreeNode*> parent;

    // Queue for BFS traversal to build parent mapping
    queue<TreeNode*> q;

    q.push(root);

    TreeNode* startNode = nullptr;

    /*
        Traverse the tree to:
        1. Build parent pointers
        2. Locate the node where fire starts
    */
    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();

        if (node->data == start)
            startNode = node;

        if (node->left) {
            parent[node->left] = node;
            q.push(node->left);
        }

        if (node->right) {
            parent[node->right] = node;
            q.push(node->right);
        }
    }

    /* BFS to simulate fire spreading*/
    unordered_map<TreeNode*, bool> visited;

    queue<TreeNode*> burn;

    burn.push(startNode);
    visited[startNode] = true;

    int time = 0;

    while (!burn.empty()) {
        int size = burn.size();
        bool spread = false;  // check if fire spreads this second

        for (int i = 0; i < size; i++) {

            TreeNode* node = burn.front();
            burn.pop();

            // Burn left child
            if (node->left && !visited[node->left]) {
                spread = true;
                visited[node->left] = true;
                burn.push(node->left);
            }

            // Burn right child
            if (node->right && !visited[node->right]) {
                spread = true;
                visited[node->right] = true;
                burn.push(node->right);
            }

            // Burn parent
            if (parent[node] && !visited[parent[node]]) {
                spread = true;
                visited[parent[node]] = true;
                burn.push(parent[node]);
            }
        }

        /* Increase time only if fire spreads to at least one new node */
        if (spread) time++;
    }
    return time;
}
```

### Count Number of Trees in a Binary Tree
```cpp
int leftHeight(TreeNode* node) {
    int h = 0;
    // Traverse the leftmost path to compute height
    while (node) {
        h++;
        node = node->left;
    }
    return h;
}

int rightHeight(TreeNode* node) {
    int h = 0;
    // Traverse the rightmost path to compute height
    while (node) {
        h++;
        node = node->right;
    }
    return h;
}

int countNodes(TreeNode* root) {
    // Base case: empty tree has 0 nodes
    if (root == nullptr) return 0;

    // Compute height of leftmost path
    int lh = leftHeight(root);

    // Compute height of rightmost path
    int rh = rightHeight(root);

    /*
        If both heights are equal, the tree is a PERFECT binary tree.
        A perfect binary tree with height h has:
            Nodes = 2^h - 1
        Instead of using pow(2, h), we use bit shifting: (1 << h)

        Explanation of (1 << h):

            1 << h  means shifting binary 1 left by h positions.

        Example:
            h = 3
            1       = 0001
            1 << 3  = 1000  (binary)
            1000₂ = 8 (decimal)

        So:
            (1 << 3) - 1
            = 8 - 1
            = 7

        Which is exactly the number of nodes in a perfect binary tree
        of height 3.

        Tree example:

                1
                / \
                2   3
                / \ / \
            4  5 6  7

        Total nodes = 7
    */
    if (lh == rh) return (1 << lh) - 1;

    /*
        If the subtree is NOT perfect,
        recursively count nodes in left and right subtrees.
    */
    return 1 + countNodes(root->left) + countNodes(root->right);
}
```

## Tree Builders
### Check if a unique BT can be constructed or not
```cpp
bool uniqueBinaryTree(int a, int b) {
    /*
        Traversal encoding:
        1 -> Preorder
        2 -> Inorder
        3 -> Postorder

        A binary tree can be uniquely constructed only if
        one traversal is INORDER and the other is either
        PREORDER or POSTORDER.

        Valid combinations:
            Preorder + Inorder
            Inorder + Postorder

        Invalid combinations:
            Preorder + Postorder
            Preorder + Preorder
            Inorder + Inorder
            Postorder + Postorder
    */

    // Check if exactly one traversal is inorder
    if ((a == 2 || b == 2) && a != b) return true;

    return false;
}
```

### Build a BT from preorder and inorder
```cpp
TreeNode* build(vector<int>& preorder, int& preIndex,
                int inStart, int inEnd,
                unordered_map<int,int>& inorderMap) {

    // Base case: no nodes to construct
    if (inStart > inEnd)
        return nullptr;

    // Current root comes from preorder traversal because preorder visits root first.
    int rootVal = preorder[preIndex++];
    TreeNode* root = new TreeNode(rootVal);

    // Find root position in inorder traversal to divide left and right subtrees.
    int rootPos = inorderMap[rootVal];

    // Build left subtree using elements before root in inorder traversal
    root->left = build(preorder, preIndex, inStart, rootPos - 1, inorderMap);

    // Build right subtree using elements after root in inorder traversal
    root->right = build(preorder, preIndex, rootPos + 1, inEnd, inorderMap);

    return root;
}

TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
    // Map [value → index] in inorder for O(1) lookup
    unordered_map<int,int> inorderMap;

    for (int i = 0; i < inorder.size(); i++)
        inorderMap[inorder[i]] = i;

    int preIndex = 0;

    return build(preorder, preIndex, 0, inorder.size() - 1, inorderMap);
}
```

### Build a BT from inorder and postorder
```cpp
TreeNode* build(vector<int>& postorder, int& postIndex,
                int inStart, int inEnd,
                unordered_map<int,int>& inorderMap) {

    // Base case: no nodes to construct
    if (inStart > inEnd)
        return nullptr;

    // Current root comes from postorder traversal because postorder visits root last.
    int rootVal = postorder[postIndex--];
    TreeNode* root = new TreeNode(rootVal);

    // Find root position in inorder traversal to divide left and right subtrees.
    int rootPos = inorderMap[rootVal];

    /*
        Important:
        Since we are consuming postorder from the end,
        we must construct the RIGHT subtree first.
    */

    // Build right subtree using elements after root in inorder traversal
    root->right = build(postorder, postIndex, rootPos + 1, inEnd, inorderMap);

    // Build left subtree using elements before root in inorder traversal
    root->left = build(postorder, postIndex, inStart, rootPos - 1, inorderMap);

    return root;
}

TreeNode* buildTree(vector<int>& inorder, vector<int>& postorder) {

    // Map [value → index] in inorder for O(1) lookup
    unordered_map<int,int> inorderMap;

    for (int i = 0; i < inorder.size(); i++)
        inorderMap[inorder[i]] = i;

    // Start from the last index of postorder (root)
    int postIndex = postorder.size() - 1;

    return build(postorder, postIndex, 0, inorder.size() - 1, inorderMap);
}
```

### Serialize and Deserialize a BT
```cpp
// Encodes a tree to a single string.
string serialize(TreeNode* root) {

    if (!root) return "";

    string res;
    queue<TreeNode*> q;
    q.push(root);

    while (!q.empty()) {

        TreeNode* node = q.front();
        q.pop();

        if (node) {
            res += to_string(node->data) + ",";
            q.push(node->left);
            q.push(node->right);
        } 
        else {
            res += "null,";
        }
    }

    return res;
}


// Decodes the string back to a tree.
TreeNode* deserialize(string data) {

    if (data.empty()) return nullptr;

    vector<string> nodes;
    string temp;

    // Split string by commas
    for (char c : data) {
        if (c == ',') {
            nodes.push_back(temp);
            temp.clear();
        } 
        else {
            temp += c;
        }
    }

    TreeNode* root = new TreeNode(stoi(nodes[0]));
    queue<TreeNode*> q;
    q.push(root);

    int i = 1;

    while (!q.empty()) {

        TreeNode* node = q.front();
        q.pop();

        // Left child
        if (nodes[i] != "null") {
            node->left = new TreeNode(stoi(nodes[i]));
            q.push(node->left);
        }
        i++;

        // Right child
        if (nodes[i] != "null") {
            node->right = new TreeNode(stoi(nodes[i]));
            q.push(node->right);
        }
        i++;
    }

    return root;
}
```
