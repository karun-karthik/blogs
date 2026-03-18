# Fundamentals

* Heap is a specialized tree-based data structure that satisfies the heap property.
* It is commonly used to implement priority queues and for efficient sorting (Heapsort).
* A heap is a **complete binary tree**, meaning all levels are completely filled except possibly the last level, which is filled from left to right.

### Heap Property

There are two types of heaps, distinguished by the heap property:

1. **Max-Heap**: For any given node, the value of the node is greater than or equal to the values of its children.
```cpp
priority_queue<int>
```
2. **Min-Heap**: For any given node, the value of the node is less than or equal to the values of its children.
```cpp
priority_queue<int, vector<int>, greater<int>>
```

* Max-Heap Example

```
      100
     /   \
    19    36
   /  \  /  \
  17  3 25   1
 / \  
2   7
```

In this Max-Heap:
- The root (100) is the largest element.
- Every parent is greater than its children (e.g., 100 > 19 and 100 > 36).

* Min-Heap Example

```
       1
     /   \
    3     2
   / \   / \
  17  19 36  100
 / \
2   7
```

In this Min-Heap:
- The root (1) is the smallest element.
- Every parent is smaller than its children (e.g., 3 < 17 and 3 < 19).

### Internal Representation

Heaps are commonly implemented using arrays due to the complete binary tree property. For a node at index `i` (0-based):

- **Parent**: `(i - 1) / 2`
- **Left Child**: `2 * i + 1`
- **Right Child**: `2 * i + 2`
- **Leaf Node**: `i >= n / 2` where `n` is the number of nodes in the heap.
    - Leaf nodes have no children.
    - n/2 to n - 1 are leaf nodes. Both inclusive.
- **Non-Leaf Node**: `i < n / 2` where `n` is the number of nodes in the heap.
    - Non-leaf nodes have at least one child.
    - 0 to n/2 - 1 are non-leaf nodes. Both inclusive.

* Example: Max-Heap Array Representation

```
Array: [100, 19, 36, 17, 3, 25, 1, 2, 7]

Index 0: 100 (Root)
  Left Child (Index 1): 19
  Right Child (Index 2): 36

Index 1: 19
  Left Child (Index 3): 17
  Right Child (Index 4): 3

Index 2: 36
  Left Child (Index 5): 25
  Right Child (Index 6): 1
```

## Implementations
### Min-Heapify
```cpp
void heapifyUp(vector<int>& arr, int idx) {
    int parent = (idx-1)/2;
    if (idx > 0 && arr[idx] < arr[parent]) {
        swap(arr[idx], arr[parent]);
        heapifyUp(arr, parent);
    }
}

void heapifyDown(vector<int>& arr, int idx) {
    int n = arr.size();
    int smallestInd = idx;

    int left = 2*idx + 1, right = 2*idx+2;

    if (left < n && arr[left] < arr[smallestInd]) {
        smallestInd = left;
    }

    if (right < n && arr[right] < arr[smallestInd]) {
        smallestInd = right;
    }

    if (smallestInd != idx) {
        swap(arr[smallestInd], arr[idx]);
        heapifyDown(arr, smallestInd);
    }
}

// Update value at index `i` and restore heap property
void heapify(vector<int>& nums, int i, int val) {
    int old = nums[i];
    nums[i] = val;
    // decide direction based on value change
    if (val < old) {
        heapifyUp(nums, i);
    } else {
        heapifyDown(nums, i);
    }
}
```

### Max-Heapify
```cpp
void heapifyUp(vector<int>& arr, int idx) {
    int parent = (idx-1)/2;
    if (idx > 0 && arr[idx] > arr[parent]) {
        swap(arr[idx], arr[parent]);
        heapifyUp(arr, parent);
    }
}

void heapifyDown(vector<int>& arr, int idx) {
    int n = arr.size();
    int largestInd = idx;

    int left = 2*idx + 1, right = 2*idx+2;

    if (left < n && arr[left] > arr[largestInd]) {
        largestInd = left;
    }

    if (right < n && arr[right] > arr[largestInd]) {
        largestInd = right;
    }

    if (largestInd != idx) {
        swap(arr[largestInd], arr[idx]);
        heapifyDown(arr, largestInd);
    }
}

// Update value at index `i` and restore heap property
void heapify(vector<int>& nums, int i, int val) {
    int old = nums[i];
    nums[i] = val;
    // decide direction based on value change
    if (val > old) {
        heapifyUp(nums, i);
    } else {
        heapifyDown(nums, i);
    }
}
```

### Build Min-Heap
```cpp
void heapifyDown(vector<int>& arr, int idx) {
    int n = arr.size();
    int smallestInd = idx;

    int left = 2*idx + 1, right = 2*idx+2;

    if (left < n && arr[left] < arr[smallestInd]) {
        smallestInd = left;
    }

    if (right < n && arr[right] < arr[smallestInd]) {
        smallestInd = right;
    }

    if (smallestInd != idx) {
        swap(arr[smallestInd], arr[idx]);
        heapifyDown(arr, smallestInd);
    }
}

// Build Min Heap from an array
void buildMinHeap(vector<int>& nums) {
    int n = nums.size();
    // Start from last non-leaf node and heapify down
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapifyDown(nums, i);
    }
}
```

### Build Max-Heap
```cpp
void heapifyDown(vector<int>& arr, int idx) {
    int n = arr.size();
    int largestInd = idx;

    int left = 2*idx + 1, right = 2*idx+2;

    if (left < n && arr[left] > arr[largestInd]) {
        largestInd = left;
    }

    if (right < n && arr[right] > arr[largestInd]) {
        largestInd = right;
    }

    if (largestInd != idx) {
        swap(arr[largestInd], arr[idx]);
        heapifyDown(arr, largestInd);
    }
}

// Build Max Heap from an array
void buildMaxHeap(vector<int>& nums) {
    int n = nums.size();
    // Start from last non-leaf node and heapify down
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapifyDown(nums, i);
    }
}
```

### Minheap from array 
```cpp
class MinHeap {
private:
    vector<int> arr;
    int count;

    void heapifyUp(vector<int>& arr, int idx) {
        int parent = (idx-1)/2;
        if (idx > 0 && arr[idx] < arr[parent]) {
            swap(arr[idx], arr[parent]);
            heapifyUp(arr, parent);
        }
    }

    void heapifyDown(vector<int>& arr, int idx) {
        int n = arr.size();
        int smallestInd = idx;

        int left = 2*idx + 1, right = 2*idx+2;

        if (left < n && arr[left] < arr[smallestInd]) {
            smallestInd = left;
        }

        if (right < n && arr[right] < arr[smallestInd]) {
            smallestInd = right;
        }

        if (smallestInd != idx) {
            swap(arr[smallestInd], arr[idx]);
            heapifyDown(arr, smallestInd);
        }
    }

public:

    void initializeHeap(){
        arr.clear();
        count = 0;
    }

    void insert(int key){
        arr.push_back(key);
        heapifyUp(arr, count);
        count = count+1;
    }

    void changeKey(int index, int new_val){
        if(arr[index] > new_val) {
            arr[index] = new_val;
            heapifyUp(arr, index);
        } else {
            arr[index] = new_val;
            heapifyDown(arr, index);
        }
    }

    void extractMin(){
        swap(arr[0], arr[count-1]);
        arr.pop_back();
        count = count-1;
        heapifyDown(arr, 0);
    }

    bool isEmpty(){
        return count == 0;
    }

    int getMin(){
        return arr[0];
    }

    int heapSize(){
        return count;
    }
};
```

### Maxheap from array
```cpp
class MaxHeap {
    vector<int> arr;
    int count;

    void heapifyUp(vector<int>& arr, int idx) {
        int parent = (idx-1)/2;
        if (idx > 0 && arr[idx] > arr[parent]) {
            swap(arr[idx], arr[parent]);
            heapifyUp(arr, parent);
        }
    }

    void heapifyDown(vector<int>& arr, int idx) {
        int n = arr.size();
        int largestInd = idx;

        int left = 2*idx + 1, right = 2*idx+2;

        if (left < n && arr[left] > arr[largestInd]) {
            largestInd = left;
        }

        if (right < n && arr[right] > arr[largestInd]) {
            largestInd = right;
        }

        if (largestInd != idx) {
            swap(arr[largestInd], arr[idx]);
            heapifyDown(arr, largestInd);
        }
    }

public:

    void initializeHeap(){
        arr.clear();
        count = 0;
    }

    void insert(int key){
        arr.push_back(key);
        count = count + 1;
        heapifyUp(arr, count-1);
    }

    void changeKey(int index, int new_val){
        if(arr[index] < new_val) {
            arr[index] = new_val;
            heapifyUp(arr, index);
        } else {
            arr[index] = new_val;
            heapifyDown(arr, index);
        }
    }

    void extractMax(){
        int ele = arr[0];
        swap(arr[0], arr[count-1]);
        arr.pop_back();
        count = count-1;
        heapifyDown(arr, 0);
    }

    bool isEmpty(){
        return count == 0;
    }

    int getMax(){
        return arr[0];
    }

    int heapSize(){
        return count;
    }
};
```

### Matrix of Clarity
| | Min-Heap | Max-Heap |
| --- | --- | --- |
| **Heap Property** | Parent ≤ Children | Parent ≥ Children |
| **Root holds** | Smallest element | Largest element |
| **Condition** | `nums[p] <= nums[i]` | `nums[p] >= nums[i]` |
| **Left check** | `nums[l] < nums[smallest]` | `nums[l] > nums[largest]` |
| **Right check** | `nums[r] < nums[smallest]` | `nums[r] > nums[largest]` |
| **`heapifyUp`** | If node is **smaller** than its parent → swap upward. Called after **insert** (new node bubbles up until min property is restored). | If node is **larger** than its parent → swap upward. Called after **insert** (new node bubbles up until max property is restored). |
| **`heapifyDown`** | If node is **larger** than its smallest child → swap downward. Called after **extract-min** (last element placed at root sinks down until min property is restored). | If node is **smaller** than its largest child → swap downward. Called after **extract-max** (last element placed at root sinks down until max property is restored). |
| **Call Up when** | Value **decreased** — node may be smaller than parent | Value **increased** — node may be larger than parent |
| **Call Down when** | Value **increased** — node may be larger than a child | Value **decreased** — node may be smaller than a child |

### Check if array represents Min-Heap
```cpp
bool isMinHeap(vector<int>& nums) {

    int n = nums.size();

    // Only non-leaf nodes need to be checked.
    // In a binary heap array, nodes from index (n/2) to (n-1) are leaves.
    for (int parent = n/2 - 1; parent >= 0; parent--) {

        int leftChild  = 2 * parent + 1;
        int rightChild = 2 * parent + 2;

        // Min Heap property:
        // parent value must be <= its children

        if (leftChild < n && nums[leftChild] < nums[parent])
            return false;

        if (rightChild < n && nums[rightChild] < nums[parent])
            return false;
    }

    // All parent-child relationships satisfy Min Heap property
    return true;
}
```


### Check if array represents Max-Heap
```cpp
bool isMaxHeap(vector<int>& nums) {

    int n = nums.size();

    // Only non-leaf nodes need to be checked.
    // In a binary heap array, nodes from index (n/2) to (n-1) are leaves.
    for (int parent = n/2 - 1; parent >= 0; parent--) {

        int leftChild  = 2 * parent + 1;
        int rightChild = 2 * parent + 2;

        // Max Heap property:
        // parent value must be >= its children

        if (leftChild < n && nums[leftChild] > nums[parent])
            return false;

        if (rightChild < n && nums[rightChild] > nums[parent])
            return false;
    }

    // All parent-child relationships satisfy Max Heap property
    return true;
}
```