## Fundamentals

### Iterative Search
```cpp
// TC: O(logN) SC: O(1)
int search(vector<int> &nums, int target) {
    int n = nums.size();
    int low = 0, high = n-1;
    while (low <= high) {
        int mid = (low + high)/2;
        if (nums[mid] == target)    return mid;
        else if (target > nums[mid])    low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}
```

### Recursive Search
```cpp
// TC: O(logN) SC: O(logN) -> due to recursion stack
int bs(vector<int>&nums, int low, int high, int target) {
    if (low > high) return -1;
    int idx;
    int mid = (low + high)/2;
    if (nums[mid] == target)    idx = mid;
    else if (target > nums[mid])    idx = bs(nums, mid+1, high, target); // right search space
    else idx = bs(nums, low, mid-1, target); // left search space
    return idx;
}

int search(vector<int> &nums, int target) {
    int n = nums.size();
    return bs(nums, 0, n-1, target);
}
```

### Lower Bound ==(1st element >= x)==
Lower bound is the first element in the array i.e greater than or equal to x.

**Brute**
```cpp
// TC: O(N) SC: O(1)
int lowerBound(vector<int>&nums, int x) {
    int n = nums.size();
    for (int i = 0; i < n; i++) {
        if (nums[i] >= x)
            return i;
    }
    return n; // no lowerbound found
}
```

**Optimal**
Valid → save & go left,
Too small → go right.
```cpp
// TC: O(logN) SC: O(1)
int lowerBound(vector<int> &nums, int x){
    int low = 0, high = nums.size()-1;
    int ans = nums.size();
    while (low <= high) {
        int mid = (low + high)/2;
        if (nums[mid] >= x) {
            // potential answer, so save and go left to find even smaller element
            ans = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return ans;
}
```


### Upper Bound ==(1st element > x)==
Upper bound is the first element in the array i.e greater than x.

**Brute**
```cpp
// TC: O(N) SC: O(1)
int upperBound(vector<int>&nums, int x) {
    int n = nums.size();
    for (int i = 0; i < n; i++) {
        if (nums[i] > x)
            return i;
    }
    return n; // no upperbound found
}
```

**Optimal**
Valid → save & go left,
Too small → go right.
```cpp
// TC: O(logN) SC: O(1)
int upperBound(vector<int> &nums, int x){
    int low = 0, high = nums.size()-1;
    int ans = nums.size();
    while (low <= high) {
        int mid = (low + high)/2;
        if (nums[mid] > x) {
            // potential answer, so save and go left to find even smaller element
            ans = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return ans;
}
```

## Logic Building

### Search Insert Position
Given a sorted array of nums consisting of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

```cpp
// TC: O(logN) SC: O(1)
int searchInsert(vector<int> &nums, int target)  {
    // This can be solved using lower-bound
    int low = 0;
    int high = nums.size()-1;
    int ans = nums.size();
    while (low <= high) {
        int mid = low + ((high - low) / 2);
        if (nums[mid] >= target) {
            ans = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return ans;
}
```

### Floor
The floor of x is the largest element <= x
```cpp
int findFloor(vector<int>& nums, int x) {
    int n = nums.size();
    int low = 0, high = n - 1;
    int ans = -1;

    while (low <= high) {
        int mid = (low + high) / 2;
        if (nums[mid] <= x) {
            ans = nums[mid];
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return ans;
}
```

### Ceil
The ceil of x is the smallest element <= x.
[This is lower_bound]
```cpp
int findCeil(vector<int>& nums, int x) {
    int n = nums.size();
    int low = 0, high = n - 1;
    int ans = -1;

    while (low <= high) {
        int mid = (low + high) / 2;
        if (nums[mid] >= x) {
            ans = nums[mid];
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return ans;
}
```

### ==Relation between floor, ceil, lower_bound and upper_bound==
| Concept | Meaning | Binary Search `mid` Condition |
|--------|--------|-------------------------------|
| **Lower Bound (LB)** | First element ≥ x | If `nums[mid] ≥ x` → move left (`high = mid - 1`) |
| **Upper Bound (UB)** | First element > x | If `nums[mid] > x` → move left (`high = mid - 1`) |
| **Floor(x)** | Greatest element ≤ x | If `nums[mid] ≤ x` → move right (`low = mid + 1`) |
| **Ceil(x)** | Smallest element ≥ x | If `nums[mid] ≥ x` → move left (`high = mid - 1`) |

### First and last occurance

**Brute**
1. Consider 2 variables first and last set to -1.
2. Linear search to find element and it's index.
3. While setting values check if first == -1, if yes then set it's value as index.
4. if first != -1, that means it's the last element.

**Code**
```cpp
vector<int> searchRange(vector<int>& nums, int target) {
    int first = -1, last = -1;
    for (int i = 0; i < nums.size(); i++) {
        // if curr element is target
        if (nums[i] == target) {
            if (first == -1)   first = i; 
            last = i; 
        }
    }
    return {first, last};
}
```
**Better**
1. Use lower_bound to find the (first) element
2. Use upper_bound to find the (last + 1)th element
```cpp
vector<int> searchRange(vector<int> &nums, int target) {
    // find the first occurange (lb)
    int first = lowerBound(nums, target);
    if (first == nums.size() || nums[first] != target) {
        return {-1, -1}; 
    }
    // find the last occurrence (ub)
    int last = upperBound(nums, target) - 1;
    return {first, last};  
}
```

### Search in a rotated sorted array - 1
Given an integer array nums, sorted in ascending order (with distinct values) and a target value k. The array is rotated at some pivot point that is unknown. Find the index at which k is present and if k is not present return -1.
```cpp
int search(vector<int> &nums, int k) {
    int low = 0, high = nums.size()-1;
    while (low <= high) {
        int mid = (low + high) / 2;
        if (nums[mid] == k) return mid;

        // if left part is sorted
        if (nums[low] <= nums[mid]) {
            if (nums[low] <= k && k <= nums[mid]) {
                // k exist in left sorted space
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        } else {
            if (nums[mid] <= k && k <= nums[high]) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
    }

    return -1;
}
```

### Search in a rotated sorted array - 2
Given an integer array nums, sorted in ascending order (may contain duplicate values) and a target value k. Now the array is rotated at some pivot point unknown to you. Return True if k is present and otherwise, return False.
```cpp
bool searchInARotatedSortedArrayII(vector<int> &nums, int k) {
    int low = 0, high = nums.size() - 1;
    while (low <= high) {
        int mid = (low + high) / 2;
        if (nums[mid] == k) return true;

        // Handle duplicates: if nums[low] == nums[mid] == nums[high]
        if (nums[low] == nums[mid] && nums[mid] == nums[high]) {
            low = low + 1;
            high = high - 1;
            continue;
        }

        // if left part is sorted
        if (nums[low] <= nums[mid]) {
            if (nums[low] <= k && k <= nums[mid]) {
                // k exist in left sorted space
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        } else {
            if (nums[mid] <= k && k <= nums[high]) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
    }
    return false;
}
```