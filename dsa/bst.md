## Fundamentals
### Search in BST
```cpp
TreeNode* searchBST(TreeNode* root, int val) {
    // Base case: reached end of tree
    if (root == NULL)   return NULL;

    // If current node contains the value
    if (root->data == val)  return root;

    // If value is greater, search in right subtree
    else if (val > root->data)  return searchBST(root->right, val);

    // Otherwise search in left subtree
    return searchBST(root->left, val);
}
```

### Floor and Ceil in a BST
```cpp
// floor = largest value ≤ key
// ceil  = smallest value ≥ key
vector<int> floorCeilOfBST(TreeNode* root, int key) {
    int floor = -1, ceil = -1;
    TreeNode* curr = root;

    while (curr != NULL) {

        // If exact key is found, both floor and ceil are the key itself
        if (curr->data == key) {
            floor = ceil = curr->data;
            break;
        }

        // Current node is smaller than key → potential floor candidate
        // Move right to try finding a larger value still ≤ key
        if (curr->data < key) {
            floor = curr->data;
            curr = curr->right;
        }

        // Current node is greater than key → potential ceil candidate
        // Move left to try finding a smaller value still ≥ key
        else {
            ceil = curr->data;
            curr = curr->left;
        }
    }

    // Return floor and ceil values
    return { floor, ceil };
}
```

### Insert a node in BST
```cpp
TreeNode* insertIntoBST(TreeNode* root, int val) {
    // If we reached a null position, create the new node here
    if (root == NULL)
        return new TreeNode(val);

    // If value is smaller than current node,
    // it must go to the left subtree (BST property)
    if (val < root->data)
        root->left = insertIntoBST(root->left, val);

    // If value is greater than current node,
    // it must go to the right subtree
    else if (val > root->data)
        root->right = insertIntoBST(root->right, val);

    // Return the unchanged root to maintain the tree structure
    return root;
}
```

### Delete a node in BST
```cpp
TreeNode* findMinNode(TreeNode* node) {

    // Leftmost node is the inorder successor.
    while (node->left)
        node = node->left;

    return node;
}

TreeNode* deleteNode(TreeNode* root, int key) {

    // INTUITION:
    // Search for the node as in a normal BST.
    //
    // 0/1 child -> Replace the node with its existing child.
    // 2 children -> Copy the inorder successor, then delete it.
    //
    // MEMORY:
    // Search -> Replace -> Delete Successor

    // Base Case: Key not found.
    if (root == nullptr)
        return nullptr;

    // Search for the node to delete.
    if (key < root->data) {
        root->left = deleteNode(root->left, key);
    }
    else if (key > root->data) {
        root->right = deleteNode(root->right, key);
    }
    else {

        // Node has at most one child.
        if (root->left == nullptr)
            return root->right;

        if (root->right == nullptr)
            return root->left;

        // Node has two children.
        // Replace it with its inorder successor
        // and remove the duplicate successor.
        TreeNode* inorderSuccessor = findMinNode(root->right);

        root->data = inorderSuccessor->data;

        root->right = deleteNode(root->right, inorderSuccessor->data);
    }

    return root;
}
```

### Kth Smallest and Largest element in BST
```cpp
void inorder(TreeNode* node, vector<int>& values) {
    if (!node) return;

    inorder(node->left, values);
    values.push_back(node->data);
    inorder(node->right, values);
}

vector<int> kLargesSmall(TreeNode* root, int k) {

    vector<int> values;
    // Get sorted elements using inorder traversal
    inorder(root, values);

    int n = values.size();
    int kthSmallest = values[k - 1];
    int kthLargest  = values[n - k];
    return {kthSmallest, kthLargest};
}
```

### Check if a tree is BST or not
```cpp
// Helper function that validates the BST property using value ranges
bool validateBST(TreeNode* node, long minAllowed, long maxAllowed) {
    // An empty subtree is always valid
    if (node == nullptr)
        return true;

    // Current node must lie strictly within the allowed range
    if (node->data <= minAllowed || node->data >= maxAllowed)
        return false;

    // Recursively validate:
    // left subtree → values must be < current node
    // right subtree → values must be > current node
    return validateBST(node->left, minAllowed, node->data) &&
           validateBST(node->right, node->data, maxAllowed);
}

bool isBST(TreeNode* root) {
    // Initially the valid range is (-∞, +∞)
    return validateBST(root, LONG_MIN, LONG_MAX);
}
```

### LCA in a Tree
```cpp
TreeNode* lca(TreeNode* root, int p, int q) {

    // Base case:
    // If we reach NULL or find one of the target nodes,
    // return the current node
    if (root == nullptr || root->data == p || root->data == q)
        return root;

    // Search for p and q in the left subtree
    TreeNode* leftResult = lca(root->left, p, q);

    // Search for p and q in the right subtree
    TreeNode* rightResult = lca(root->right, p, q);

    // If p and q are found in different subtrees,
    // current node is their Lowest Common Ancestor
    if (leftResult && rightResult)
        return root;

    // Otherwise return whichever side found a node
    return leftResult ? leftResult : rightResult;
}
```
```cpp
// This is using the BST property!!!
TreeNode* lca(TreeNode* root, int p, int q) {

    while (root) {

        // Both nodes lie in left subtree
        if (p < root->data && q < root->data)
            root = root->left;

        // Both nodes lie in right subtree
        else if (p > root->data && q > root->data)
            root = root->right;

        // Nodes split here → this is the LCA
        else
            return root;
    }
    return nullptr;
}
```

## Construct a BST from a preorder traversal
```cpp
TreeNode* buildBST(vector<int>& preorder, int& index, long minVal, long maxVal) {

    // If all elements are used, stop
    if (index >= preorder.size())
        return nullptr;

    int value = preorder[index];

    // If current value violates BST range, it does not belong here
    if (value <= minVal || value >= maxVal)
        return nullptr;

    // Create the node
    TreeNode* node = new TreeNode(value);
    index++;

    // Build left subtree (values < node->data)
    node->left = buildBST(preorder, index, minVal, value);

    // Build right subtree (values > node->data)
    node->right = buildBST(preorder, index, value, maxVal);

    return node;
}

TreeNode* bstFromPreorder(vector<int>& preorder) {
    int index = 0;
    return buildBST(preorder, index, LONG_MIN, LONG_MAX);
}
```

### Inorder Successor and Predecessor
```cpp
vector<int> succPredBST(TreeNode* root, int key) {

    int predecessor = -1;   // largest value strictly less than key
    int successor   = -1;   // smallest value strictly greater than key

    TreeNode* curr = root;

    // -------- Find Inorder Predecessor --------
    // Idea:
    // If node value < key → it could be a predecessor candidate.
    // But there might exist a larger value (< key) in the right subtree,
    // so we move right to try improving the candidate.
    while (curr) {

        if (curr->data < key) {
            predecessor = curr->data;   // update best predecessor so far
            curr = curr->right;         // search for a closer value
        }
        else {
            // current node >= key → predecessor cannot be here
            // move left to find smaller values
            curr = curr->left;
        }
    }

    curr = root;

    // -------- Find Inorder Successor --------
    // Idea:
    // If node value > key → it could be a successor candidate.
    // But there might exist a smaller value (> key) in the left subtree,
    // so we move left to try improving the candidate.
    while (curr) {

        if (curr->data > key) {
            successor = curr->data;     // update best successor so far
            curr = curr->left;          // search for a closer value
        }
        else {
            // current node <= key → successor cannot be here
            // move right to find larger values
            curr = curr->right;
        }
    }

    // Return {predecessor, successor}
    return {predecessor, successor};
}
```

### BST Iterator
```cpp
class BSTIterator{
private:
    stack<TreeNode*> st;
    void pushLeftBranch(TreeNode* node) {
        while (node) {
            st.push(node);
            node = node->left;
        }
    }
public:
    BSTIterator(TreeNode* root){
        pushLeftBranch(root);
    }
    
    bool hasNext(){
        return !st.empty();
    }
    
    int next(){
        TreeNode* curr = st.top();
        st.pop();
        pushLeftBranch(curr->right);
        return curr->data;
    }
};
```

### Two sum in a BST
```cpp
class BSTIterator {

    stack<TreeNode*> st;
    bool reverse;   // false = inorder, true = reverse inorder

    void pushAll(TreeNode* node) {
        while (node) {
            st.push(node);
            node = reverse ? node->right : node->left;
        }
    }

public:

    BSTIterator(TreeNode* root, bool isReverse) {
        reverse = isReverse;
        pushAll(root);
    }

    int next() {

        TreeNode* node = st.top();
        st.pop();

        if (!reverse)
            pushAll(node->right);
        else
            pushAll(node->left);

        return node->data;
    }

    bool hasNext() {
        return !st.empty();
    }
};


bool twoSumBST(TreeNode* root, int k){

    if (!root) return false;

    // iterator for smallest elements
    BSTIterator leftIter(root, false);

    // iterator for largest elements
    BSTIterator rightIter(root, true);

    int leftVal = leftIter.next();
    int rightVal = rightIter.next();

    while (leftVal < rightVal) {

        int sum = leftVal + rightVal;

        if (sum == k)
            return true;

        else if (sum < k)
            leftVal = leftIter.next();

        else
            rightVal = rightIter.next();
    }

    return false;
}
```

### Correct BST with 2 nodes swapped
```cpp
class Solution {

    TreeNode* first  = nullptr;   // first misplaced node
    TreeNode* second = nullptr;   // second misplaced node
    TreeNode* prev   = nullptr;   // previous node in inorder traversal

    void inorder(TreeNode* node) {
        if (!node) return;

        inorder(node->left);

        // If BST property is violated
        if (prev != nullptr && prev->data > node->data) {
            // First violation → mark 'prev' as first wrong node
            if (first == nullptr) {
                first = prev;
            }
            // For both first and second violations,
            // the current node is a candidate for 'second'
            second = node;
        }
        // Update previous node
        prev = node;

        inorder(node->right);
    }

public:
    void recoverTree(TreeNode* root) {
        inorder(root);
        // Swap the values of the misplaced nodes
        if (first && second) {
            swap(first->data, second->data);
        }
    }
};
```

### Largest BST in a Binary Tree
```cpp
struct Result {
    int minValue;
    int maxValue;
    int size;
    bool isBST;
};

Result solve(TreeNode* root, int& maxSize) {

    // Empty tree is a valid BST with size 0.
    if (!root)
        return {INT_MAX, INT_MIN, 0, true};

    // Get BST information from both subtrees.
    Result left = solve(root->left, maxSize);
    Result right = solve(root->right, maxSize);

    // Current subtree is a BST if:
    // 1. Both subtrees are BSTs.
    // 2. All left values < root.
    // 3. All right values > root.
    if (left.isBST &&
        right.isBST &&
        left.maxValue < root->data &&
        root->data < right.minValue) {

        Result curr;

        // Extend the minimum/maximum range with the current node.
        curr.minValue = min(root->data, left.minValue);
        curr.maxValue = max(root->data, right.maxValue);

        // Current subtree size = left + root + right.
        curr.size = left.size + right.size + 1;
        curr.isBST = true;

        // Track the largest BST found so far.
        maxSize = max(maxSize, curr.size);

        return curr;
    }

    // Invalid BST: values are irrelevant because this subtree
    // cannot be used as a BST by its parent.
    return {INT_MIN, INT_MAX, 0, false};
}

int largestBST(TreeNode* root) {
    int maxSize = 0;
    solve(root, maxSize);
    return maxSize;
}
```