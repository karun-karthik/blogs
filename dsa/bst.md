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
// Helper function: returns the smallest node in a subtree
TreeNode* findMinNode(TreeNode* node) {
    while (node->left) {
        node = node->left;   // keep moving left to find the minimum
    }
    return node;
}

TreeNode* deleteNode(TreeNode* root, int key) {
    // Base case: if tree is empty
    if (root == nullptr)
        return nullptr;

    // If key is smaller, the node to delete lies in the left subtree
    if (key < root->data) {
        root->left = deleteNode(root->left, key);
    }

    // If key is larger, the node to delete lies in the right subtree
    else if (key > root->data) {
        root->right = deleteNode(root->right, key);
    }

    // Node to delete is found
    else {

        // Case 1: Node has no left child
        // Replace node with its right child
        if (root->left == nullptr)
            return root->right;

        // Case 2: Node has no right child
        // Replace node with its left child
        if (root->right == nullptr)
            return root->left;

        // Case 3: Node has two children
        // Find the inorder successor (smallest node in right subtree)
        TreeNode* inorderSuccessor = findMinNode(root->right);

        // Copy successor's value into current node
        root->data = inorderSuccessor->data;

        // Delete the successor from the right subtree (as the value was copied to root)
        root->right = deleteNode(root->right, inorderSuccessor->data);
    }

    // Return the updated subtree root
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
class Solution {

    // Information returned from each subtree during postorder traversal
    struct SubtreeInfo {
        int minValue;   // smallest value in this subtree
        int maxValue;   // largest value in this subtree
        int size;       // number of nodes in this subtree (if it forms a BST)
        bool isBST;     // whether this subtree itself is a valid BST
    };

    /*
        Postorder traversal helper that evaluates each subtree and returns
        information needed by its parent to determine whether it forms a BST.

        While returning, we update the global maximum BST size found so far.
    */
    SubtreeInfo evaluateSubtree(TreeNode* node, int& largestBSTSize) {
        // Base case: an empty subtree is considered a valid BST
        // Using extreme values ensures parent comparisons work correctly
        if (!node)  return {INT_MAX, INT_MIN, 0, true};

        // Recursively evaluate left and right subtrees
        SubtreeInfo leftInfo  = evaluateSubtree(node->left, largestBSTSize);
        SubtreeInfo rightInfo = evaluateSubtree(node->right, largestBSTSize);

        SubtreeInfo currentInfo;

        /*
            A subtree rooted at 'node' is a valid BST if:
            1. Left subtree is BST
            2. Right subtree is BST
            3. node->data is greater than the maximum value in left subtree
            4. node->data is smaller than the minimum value in right subtree
        */
        if (leftInfo.isBST && rightInfo.isBST
            && node->data > leftInfo.maxValue && node->data < rightInfo.minValue) {

            currentInfo.isBST = true;

            // Size of BST = left subtree + right subtree + current node
            currentInfo.size = leftInfo.size + rightInfo.size + 1;

            // Update range values for parent checks
            currentInfo.minValue = min(node->data, leftInfo.minValue);
            currentInfo.maxValue = max(node->data, rightInfo.maxValue);

            // Track the largest BST encountered so far
            largestBSTSize = max(largestBSTSize, currentInfo.size);
        } else {
            // This subtree is NOT a BST
            currentInfo.isBST = false;
            currentInfo.size = 0;
            // These values are set so parent nodes will fail BST checks
            currentInfo.minValue = INT_MIN;
            currentInfo.maxValue = INT_MAX;
        }

        return currentInfo;
    }

public:
    int largestBST(TreeNode* root) {
        int largestBSTSize = 0;
        // Start postorder traversal
        evaluateSubtree(root, largestBSTSize);
        return largestBSTSize;
    }
};
```