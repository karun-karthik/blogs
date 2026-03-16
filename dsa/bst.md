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

