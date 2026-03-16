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