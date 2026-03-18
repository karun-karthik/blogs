## Fundamentals

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

| | Min-Heap | Max-Heap | Index Range |
| --- | --- | --- | --- |
| **Heap Property** | Parent ≤ Children | Parent ≥ Children | — |
| **Root holds** | Smallest element | Largest element | — |
| **`heapifyUp`** | `arr[i] < arr[parent]` → bubble up. Called after **insert**. | `arr[i] > arr[parent]` → bubble up. Called after **insert**. | `n-1` → up to `0` |
| **`heapifyDown`** | `arr[child] < arr[i]` → sink down (pick smallest child). Called after **extract-min**. | `arr[child] > arr[i]` → sink down (pick largest child). Called after **extract-max**. | `0` → down to `n-1` |
| **Call Up when** | Value **decreased** — may be smaller than parent | Value **increased** — may be larger than parent | `i` → `0` |
| **Call Down when** | Value **increased** — may be larger than a child | Value **decreased** — may be smaller than a child | `i` → `n-1` |
| **Build Heap** | `heapifyDown` on each non-leaf — restore min property | `heapifyDown` on each non-leaf — restore max property | `n/2-1` → `0` (non-leaves only) |
| **Check if Heap** | `arr[child] < arr[parent]` → violation | `arr[child] > arr[parent]` → violation | `n/2-1` → `0` (non-leaves only) |

> **Why leaf nodes are skipped in Build / Check:** Leaf nodes (`n/2` to `n-1`) have **no children** — they can never violate the heap property, so there's nothing to fix. Only non-leaf nodes (`0` to `n/2 - 1`) need to be processed.


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

### Convert the min-heap to max-heap
```cpp
// Max Heapify Down
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
    // this is because leaf nodes have no children and already satisfy the property
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapifyDown(nums, i);
    }
}
```

### Heap Sort

**Idea:** Build a Max-Heap from the array, then repeatedly extract the max (swap root with last element, shrink heap size, heapifyDown). After n extractions the array is sorted in ascending order.

**Time:** O(n log n) — O(n) to build + O(log n) per extraction × n  
**Space:** O(1) — sorts in-place

```cpp
// `last` marks the current heap boundary so heapify ignores already sorted elements.
void heapifyDown(vector<int> &arr, int last, int idx) {
    int largestInd = idx; 
    int left = 2*idx + 1, right = 2*idx + 2;
    
    if(left <= last && arr[left] > arr[largestInd]) 
        largestInd = left;

    if(right <= last && arr[right] > arr[largestInd]) 
        largestInd = right;

    if(largestInd != idx) {
        swap(arr[largestInd] , arr[idx]);
        heapifyDown(arr, last, largestInd);
    }
    return; 
}

void buildMaxHeap(vector<int> &nums) {
    int n = nums.size();
    for(int i = n/2 - 1; i >= 0; i--) {
        heapifyDown(nums, n-1, i);
    }
}

void heapSort(vector<int>&nums) {
    buildMaxHeap(nums);
    int last = nums.size()-1;
    while (last > 0) {
        swap(nums[0], nums[last]);
        last--;
        if (last > 0) {
            heapifyDown(nums, last, 0);
        }
    }
}
```

### Kth Largest Element in an array
```cpp
int kthLargestElement(vector<int>& nums, int k) {
    // Min heap to keep track of k largest elements
    priority_queue<int, vector<int>, greater<int>> minHeap;
    for (int num : nums) {
        minHeap.push(num);
        // Maintain heap size as k
        if (minHeap.size() > k)
            minHeap.pop();
    }
    // Top of heap is kth largest element
    return minHeap.top();
}
```

```cpp
class Solution {
public:

    // Partition the array so that:
    // elements <= pivot are on the left
    // elements > pivot are on the right
    // Returns the final index of the pivot
    int partition(vector<int>& nums, int left, int right) {

        int pivotValue = nums[right];   // pivot placed at end
        int idx = left;          // position to place smaller elements

        for (int i = left; i < right; i++) {

            if (nums[i] <= pivotValue) {
                // swap elements smaller than pivot to left
                swap(nums[idx], nums[i]);
                idx++;
            }
        }

        // Place pivot in its correct sorted position
        swap(nums[idx], nums[right]);
        return idx;
    }


    int quickSelect(vector<int>& nums, int left, int right, int targetIndex) {

        // If only one element remains
        if (left == right)  return nums[left];

        // Pick a random pivot to avoid worst case
        int randomPivot = left + rand() % (right - left + 1);

        // Move pivot to end so partition logic works
        swap(nums[randomPivot], nums[right]);

        int pivotIndex = partition(nums, left, right);

        // If pivot lands exactly at target index → answer found
        if (pivotIndex == targetIndex)
            return nums[pivotIndex];

        // Target is on the right side
        if (pivotIndex < targetIndex)
            return quickSelect(nums, pivotIndex + 1, right, targetIndex);

        // Target is on the left side
        return quickSelect(nums, left, pivotIndex - 1, targetIndex);
    }


    int kthLargestElement(vector<int>& nums, int k) {

        int n = nums.size();

        // kth largest = (n-k)th smallest
        int targetIndex = n - k;

        return quickSelect(nums, 0, n - 1, targetIndex);
    }
};
```

### Kth Largest Element in a Stream of Numbers
```cpp
class KthLargest {
    public:
    
    int k;
    priority_queue<int, vector<int>, greater<int>> minHeap;

    KthLargest(int k, vector<int>& nums) {
        this->k = k;

        for (int num : nums) {
            add(num);
        }
    }

    int add(int val) {

        minHeap.push(val);

        // Maintain heap size k
        if (minHeap.size() > k)
            minHeap.pop();

        return minHeap.top(); // kth largest
    }
};
```

### Quick Select
```cpp
int partition(vector<int>& nums, int left, int right) {
    int pivotValue = nums[right];   // pivot placed at end
    int idx = left;          // position to place smaller elements
    for (int i = left; i < right; i++) {
        if (nums[i] <= pivotValue) {
            // swap elements smaller than pivot to left
            swap(nums[idx], nums[i]);
            idx++;
        }
    }

    // Place pivot in its correct sorted position
    swap(nums[idx], nums[right]);
    return idx;
}

// targetIndex is the Kth index we are looking for (defaultly Kth smallest)
int quickSelect(vector<int>& nums, int left, int right, int targetIndex) {

    // If only one element remains
    if (left == right)  return nums[left];

    // Pick a random pivot to avoid worst case
    int randomPivot = left + rand() % (right - left + 1);
    // Move pivot to end so partition logic works
    swap(nums[randomPivot], nums[right]);

    int pivotIndex = partition(nums, left, right);

    // If pivot lands exactly at target index → answer found
    if (pivotIndex == targetIndex)
        return nums[pivotIndex];

    // Target is on the right side
    if (pivotIndex < targetIndex)
        return quickSelect(nums, pivotIndex + 1, right, targetIndex);

    // Target is on the left side
    return quickSelect(nums, left, pivotIndex - 1, targetIndex);
}
```