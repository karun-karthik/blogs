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

### Lower Bound ==(1st element &gt;= x)==
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


### Upper Bound ==(1st element &gt; x)==
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

### Search in a rotated sorted array 1
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

### Search in a rotated sorted array 2
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

### Find Minimum using BS

```cpp
// TC: O(logN) SC: O(1)
int findMin(vector<int> &arr)  {
    int low = 0, high = arr.size()-1;
    int ans = INT_MAX;

    while (low <= high) {
        int mid = (low + high)/2;
        if (arr[low] <= arr[mid]) {
            // left space is sorted
            ans = min(arr[low], ans);
            low = mid + 1;
        } else {
            ans = min(ans, arr[mid]);
            high = mid - 1;
        }
    }

    return ans;
}
```

### Find no. of right rotations in sorted array

```
Input : nums = [4, 5, 6, 7, 0, 1, 2, 3]
Output: 4
Explanation: The original array should be [0, 1, 2, 3, 4, 5, 6, 7].
So, we can notice that the array has been rotated 4 times.
```

```cpp
int findKRotation(vector<int> &arr)  {
    int low = 0, high = arr.size()-1;
    int idx = -1;
    int mini = INT_MAX;

    while (low <= high) {
        int mid = (low + high)/2;
        if (arr[low] <= arr[mid]) {
            if (arr[low] <= mini) {
                idx = low;
                mini = arr[low];
            }
            low = mid + 1;
        } else {
            if (arr[mid] <= mini) {
                idx = mid;
                mini = arr[mid];
            }
            high = mid - 1;
        }
    }

    return idx;
}
```

### Single element in rotated sorted array
- **Mid is an Even index**
  - If `arr[mid] == arr[mid + 1]` → single element is in **right half**
  - If `arr[mid] == arr[mid - 1]` → single element is in **left half**

- **Mid is an Odd index**
  - If `arr[mid] == arr[mid + 1]` → single element is in **left half**
  - If `arr[mid] == arr[mid - 1]` → single element is in **right half**

```
int singleNonDuplicate(vector<int> &nums) {
    int n = nums.size();
    if (n == 1) return nums[0];
    if (nums[0] != nums[1]) return nums[0];
    if (nums[n-1] != nums[n-2]) return nums[n-1];

    int low = 1, high = n-2;
    while (low <= high) {
        int mid = (low + high) / 2;

        if (nums[mid-1] != nums[mid] && nums[mid] != nums[mid+1])
            return nums[mid];   // mid is a single element

        bool oddIndex = (mid % 2 == 1 && nums[mid] == nums[mid - 1]);
        bool evenIndex = (mid % 2 == 0 && nums[mid] == nums[mid + 1]);

        if (oddIndex || evenIndex) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    return -1;
}
```

### Find square root of a number

```
Given a positive integer n. Find and return its square root.
If n is not a perfect square, then return the floor value of sqrt(n).
```

```cpp
int floorSqrt(int n)  {
    int low = 1, high = n;
    int ans = 0;
    while (low <= high) {
        int mid = low + (high - low)/2;
        long long val = 1LL * mid * mid;

        if (val <= (long long)n) {
            low = mid + 1;
            ans = mid;
        } else {
            high = mid - 1;
        }
    }
    return ans;
}
```

### Find nth root of a number

```
Given two numbers N and M, find the Nth root of M.
The Nth root of a number M is defined as a number X
such that when X is raised to the power of N, it equals M.
If the Nth root is not an integer, return -1.
```

```cpp
int check(int mid, int n, int m) {
    long long res = 1;
    for (int i = 0; i < n; i++) {
      res = res * mid;
      if (res > m)  return 2; // larger than required
    }
    if (res == m)  return 1; // exact match found
    return 0; // smaller than required
}

int checkLogN(int mid, int n, int m) {
    long long res = 1;
    long long base = mid;

    while (n > 0) {
      // if n is odd, multiply once
        if (n & 1) {
            res *= base;
            if (res > m) return 2;
            n--;
        } else {
            // if even, square the base
            base *= base;
            if (base > m) return 2;
            n = n/2;
        }
    }
    if (res == m) return 1;
    return 0;
}

int NthRoot(int N, int M) {
    int low = 1, high = M;

    while (low <= high) {
        int mid = low + (high - low) / 2;
        int res = checkLogN(mid, N, M);
        // int res = check(mid, N, M);

        if (res == 1) return mid;
        else if (res == 2)  high = mid - 1;
        else low = mid + 1; // when res = 0
    }
    return -1; // no integer with Nth root
}
```

### Find the smallest divisor
Given an array of integers nums and an integer limit as the threshold value,
find the smallest positive integer divisor such that upon dividing all the elements of the array by this divisor,
the sum of the division results is less than or equal to the threshold value.
After dividing each element by the chosen divisor,
take the ceiling of the result (i.e., round up to the next whole number).

```cpp
int helper(int mid, vector<int>& nums) {
    int sum = 0;
    for (auto it: nums) {
        sum += ceil((double)(it) / (double)(mid));
    }
    return sum;
}
int smallestDivisor(vector<int> &nums, int limit) {
    int max = *max_element(nums.begin(), nums.end());
    int low = 1, high = max;
    int ans = -1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        int sumDivisor = helper(mid, nums);
        if (sumDivisor <= limit) {
            ans = mid;
            high = mid - 1; // if it's within the limit then go further less
        } else {
            low = mid + 1;
        }
    }
    return ans;
}
```

### Koko eating bananas

A monkey is given n piles of bananas, where the 'ith' pile has nums[i] bananas. An integer h represents the total time in hours to eat all the bananas.



Each hour, the monkey chooses a non-empty pile of bananas and eats k bananas. If the pile contains fewer than k bananas, the monkey eats all the bananas in that pile and does not consume any more bananas in that hour.



Determine the minimum number of bananas the monkey must eat per hour to finish all the bananas within h hours.

```
int helper(int mid, vector<int> &nums) {
    int sum = 0;
    for (int i: nums) {
        sum += ceil((double) i / (double) mid);
    }
    return sum;
}

int minimumRateToEatBananas(vector<int> nums, int h) {
    int low = 1, high = *max_element(nums.begin(), nums.end());
    int ans = -1;
    while (low <= high) {
        int mid = (low + high) / 2;
        int minimumBananas = helper(mid, nums);
        if (minimumBananas <= h) {
            ans = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return ans;
}
```

### Minimum days to make M bouquets

Given n roses and an array nums where nums[i] denotes that the 'ith' rose will bloom on the nums[i]th day, only adjacent bloomed roses can be picked to make a bouquet. Exactly k adjacent bloomed roses are required to make a single bouquet. Find the minimum number of days required to make at least m bouquets, each containing k roses. Return -1 if it is not possible.

```
bool checkBouquets(vector<int> &nums, int mid, int m, int k) {
    int countOfFlowers = 0;
    int noOfBouquets = 0;

    for (int flowerOnDay: nums) {
        if (flowerOnDay <= mid) {
        countOfFlowers++;
        } else {
        // if more flowers are available on a day
        noOfBouquets += (countOfFlowers)/k;
        countOfFlowers = 0;
        }
    }

    // create another bouquet with remaining flowers
    noOfBouquets += (countOfFlowers)/k;
    return noOfBouquets >= m; // true if required bouquet count is met 
}

int roseGarden(int n,vector<int> nums, int k, int m) {
    long long targetFlowers = m * k;
    if (targetFlowers > n)  return -1;
    int low = *min_element(nums.begin(), nums.end());
    int high = *max_element(nums.begin(), nums.end());
    int ans = -1;
    while (low <= high) {
        int mid = low + (high - low)/2;
        if (checkBouquets(nums, mid, m, k)) {
            ans = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return ans;
  }
```

## FAQ

### Aggressive Cows
Given an array nums of size n, which denotes the positions of stalls, and an integer k, which denotes the number of aggressive cows, assign stalls to k cows such that the minimum distance between any two cows is the maximum possible. Find the maximum possible minimum distance.
```
bool canPlaceCow(vector<int>&nums, int dist, int cows) {
    int n = nums.size();
    int placedCows = 1;
    int lastCowPosition = nums[0];

    for (int i = 1; i < n; i++) {
        // if distance between curr cow and last placed cow
        // is greater than dist, then place cow and update last
        if (nums[i] - lastCowPosition >= dist) {
            placedCows++;
            lastCowPosition = nums[i];
        }
        // if more cows are placed than k,
        // then it's a possible answer, return true
        if (placedCows >= cows) return true;
    }
    return false;
}
int aggressiveCows(vector<int> &nums, int k) {
    int n = nums.size();
    sort(nums.begin(), nums.end());
    int low = 1, high = nums[n-1] - nums[0];
    // high is max possible distance between first and last stall
    int ans;
    while (low <= high) {
        int mid = (low + high) / 2;
        if (canPlaceCow(nums, mid, k)) {
            low = mid + 1; // if max then use low, min use high
            ans = mid;
        } else {
            high = mid - 1;
        }
    }
    return ans;
}
```

### Book Allocation Problem

Given an array nums of n integers, where nums[i] represents the number of pages in the i-th book, and an integer m representing the number of students, allocate all the books to the students so that each student gets at least one book, each book is allocated to only one student, and the allocation is contiguous.

Allocate the books to m students in such a way that the maximum number of pages assigned to a student is minimized. If the allocation of books is not possible, return -1.

```cpp
int countStudents(vector<int> &nums, int pageLimit) {
    int n = nums.size();
    int students = 1;
    int pages = 0;

    for (int i = 0; i<n; i++) {
        if (pages + nums[i] <= pageLimit) {
            pages += nums[i];
        } else {
            students++;
            pages = nums[i];
        }
    }

    return students;
}

int findPages(vector<int> &nums, int m)  {
    int n = nums.size();
    // if more students than books then all students cannot get atleast 1 book
    if (m > n)  return -1; 
    int low = *max_element(nums.begin(), nums.end());
    int high = accumulate(nums.begin(), nums.end(), 0);
    int ans;
    while (low <= high) {
        int mid = low + (high - low)/2;
        int students = countStudents(nums, mid);
        if (students <= m) {
            ans = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return ans;
}
```

### Find Peak Element

Given an array arr of integers. A peak element is defined as an element greater than both of its neighbors.

Formally, if arr[i] is the peak element, arr[i - 1] < arr[i] and arr[i + 1] < arr[i].


Find the index(0-based) of a peak element in the array. If there are multiple peak numbers, return the index of any peak number.

```cpp
int findPeakElement(vector<int> &arr) {
    int n = arr.size();
    if (n == 1) return 0;
    if (arr[0] > arr[1])    return 0;
    if (arr[n-1] > arr[n-2])    return n-1;
    int low = 1, high = n-2;
    while (low <= high) {
        int mid = (low + high) / 2;
        if (arr[mid] > arr[mid-1] && arr[mid] > arr[mid+1])
            return mid;
        if (arr[mid] > arr[mid-1])  low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}
```

### Median of 2 sorted arrays

Given two sorted arrays arr1 and arr2 of size m and n respectively, return the median of the two sorted arrays.

The median is defined as the middle value of a sorted list of numbers. In case the length of the list is even, the median is the average of the two middle elements.

```
Input: arr1 = [2, 4, 6], arr2 = [1, 3, 5]
Output: 3.5
Explanation: The array after merging arr1 and arr2 will be [ 1, 2, 3, 4, 5, 6 ]. As the length of the merged list is even, the median is the average of the two middle elements. Here two medians are 3 and 4. So the median will be the average of 3 and 4, which is 3.5.
```

> Brute:
Create a new array and add elements from both arrays in increasing order.
If n is odd then (n1 + n2)/2;
If n is even then (mid1 & mid2)/2


> Better:
This approach optimizes the extra space used in brute-force by eliminating the array to store final merged result.
Ultimately only 2 middle elements at indexes (m + n)/2 and (m + n)/2 - 1, are needed to solve the problem.

```cpp
double median(vector<int>& arr1, vector<int>& arr2) {
    // Sizes
    int len1 = arr1.size();
    int len2 = arr2.size();
    int totalLen = len1 + len2;

    // Median positions in merged order
    int rightMidPos = totalLen / 2;
    int leftMidPos  = rightMidPos - 1;

    int mergePos = 0;
    int leftMidValue  = -1;
    int rightMidValue = -1;

    // Pointers for merging
    int i = 0, j = 0;

    // Merge until one array is exhausted
    while (i < len1 && j < len2) {
        int picked;

        if (arr1[i] <= arr2[j]) {
            picked = arr1[i++];
        } else {
            picked = arr2[j++];
        }

        if (mergePos == leftMidPos)  leftMidValue  = picked;
        if (mergePos == rightMidPos) rightMidValue = picked;

        mergePos++;
    }

    // Remaining elements of arr1
    while (i < len1) {
        if (mergePos == leftMidPos)  leftMidValue  = arr1[i];
        if (mergePos == rightMidPos) rightMidValue = arr1[i];
        mergePos++;
        i++;
    }

    // Remaining elements of arr2
    while (j < len2) {
        if (mergePos == leftMidPos)  leftMidValue  = arr2[j];
        if (mergePos == rightMidPos) rightMidValue = arr2[j];
        mergePos++;
        j++;
    }

    // Final median calculation
    if (totalLen % 2 == 1) {
        return (double) rightMidValue;
    }

    return (leftMidValue + rightMidValue) / 2.0;
}
```

**Optimal**

```cpp
double median(vector<int> &arr1, vector<int> &arr2) {
    int n1 = arr1.size(), n2 = arr2.size();
    // Ensure arr1 is the smaller array
    if (n1 > n2)    return median(arr2, arr1);
    int n = n1 + n2; // total elements
    int left = (n1 + n2 + 1)/2; // length of left half of array
    int low = 0, high = n1; // bs on the smallest array always

    while (low <= high) {
        int mid1 = (low + high) / 2;
        int mid2 = left - mid1;
        // Calculate l1, l2, r1, and r2
        int l1 = (mid1 > 0) ? arr1[mid1 - 1] : INT_MIN;
        int r1 = (mid1 < n1) ? arr1[mid1] : INT_MAX;
        int l2 = (mid2 > 0) ? arr2[mid2 - 1] : INT_MIN;
        int r2 = (mid2 < n2) ? arr2[mid2] : INT_MAX;

        if (l1 <= r2 && l2 <= r1) {
            if (n % 2 == 1) return max(l1, l2);
            else return (max(l1, l2) + min(r1, r2)) / 2.0;
        }
        else if (l1 > r2) {
            high = mid1 - 1;
        } else {
            low = mid1 + 1;
        }
    }
    return 0;
}
```

### Kth element of 2 sorted arrays

```cpp
int kthElement(vector<int>& a, vector<int>& b, int k) {
    int m = a.size();
    int n = b.size();

    // Ensure a is smaller array for optimization
    if (m > n) {
        // Swap a and b
        return kthElement(b, a, k); 
    }
    
    // Length of the left half
    int left = k; 

    // Apply binary search
    int low = max(0, k - n), high = min(k, m);
    while (low <= high) {
        int mid1 = (low + high) >> 1;
        int mid2 = left - mid1;

        // Initialize l1, l2, r1, r2
        // l1 = largest on left of a
        // l2 = largest on left of b
        // r1 = smallest on right of a
        // r2 = smallest on right of b
        int l1 = (mid1 > 0) ? a[mid1 - 1] : INT_MIN;
        int l2 = (mid2 > 0) ? b[mid2 - 1] : INT_MIN;
        int r1 = (mid1 < m) ? a[mid1] : INT_MAX;
        int r2 = (mid2 < n) ? b[mid2] : INT_MAX;

        // Check if we have found the answer
        if (l1 <= r2 && l2 <= r1) {
            return max(l1, l2);
        } 
        else if (l1 > r2) {
            // Eliminate the right half
            high = mid1 - 1;
        } 
        else {
            // Eliminate the left half
            low = mid1 + 1;
        }
    }
    // Dummy return statement 
    return -1;
}
```

## 2D Arrays

### Find row with maximum 1s

Given a non-empty grid mat consisting of only 0s and 1s, where all the rows are sorted in ascending order, find the index of the row with the maximum number of ones.

If two rows have the same number of ones, consider the one with a smaller index. If no 1 exists in the matrix, return -1.

```cpp
int lower_bound(vector<int> arr, int x) {
    int low = 0;
    int high = arr.size() - 1;
    int ans = arr.size();
    while (low <= high) {
        int mid = (low + high)/2;
        if (arr[mid] >= x) {
            ans = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return ans;
}

int rowWithMax1s(vector < vector < int >> & mat) {
    int res = 0;
    int idx = -1;
    for (int i=0; i<mat.size(); i++) {
        int oneCount = mat[i].size() - lower_bound(mat[i], 1);
        if (oneCount > res) {
            res = oneCount;
            idx = i;
        }
    }
    return idx;
}
```

### Search in 2D Matrix

Given a 2-D array mat where the elements of each row are sorted in non-decreasing order, and the first element of a row is greater than the last element of the previous row (if it exists), and an integer target, determine if the target exists in the given mat or not.

```cpp
// TC: O(log(N*M)) SC: O(1)
bool searchMatrix(vector<vector<int>> &mat, int target){
    int m = mat.size(); // rows
    int n = mat[0].size(); // columns
    int low = 0, high = m * n-1;
    while (low <= high) {
        int mid = (low + high)/2;
        int ele = mat[mid/n][mid%n];
        if (ele == target) {
            return true;
        } else if (ele < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return false;
}
```

### Search in 2D Matrix ii

Given a 2D array matrix where each row is sorted in ascending order from left to right and each column is sorted in ascending order from top to bottom, write an efficient algorithm to search for a specific integer target in the matrix.

```cpp
bool searchMatrix(vector<vector<int>> &mat, int target){
    int m = mat.size(); // rows
    int n = mat[0].size(); // columns
    int row = 0, col = n-1;
    while (row < m && col >= 0) {
        if (mat[row][col] == target)    return true;
        else if (mat[row][col] > target)   col--;
        else row++;
    }
    return false;
}
```

### Find Peak Element ii

Given a 0-indexed n x m matrix mat where no two adjacent cells are equal, find any peak element mat[i][j] and return the array [i, j].A peak element in a 2D grid is an element that is strictly greater than all of its adjacent neighbours to the left, right, top, and bottom.

Assume that the entire matrix is surrounded by an outer perimeter with the value -1 in each cell.

Note: As there can be many peak values, 1 is given as output if the returned index is a peak number, otherwise 0.

```cpp
int maxElement(vector<vector<int>>&arr, int col) {
    int m = arr.size();
    int maxVal = INT_MIN;
    int idx = -1;
    for (int i=0; i<m; i++) {
        if (arr[i][col] > maxVal) {
            maxVal = arr[i][col];
            idx = i;
        }
    }
    return idx;
}

vector<int> findPeakGrid(vector<vector<int>>& arr) {
    int m = arr.size(); // rows
    int n = arr[0].size(); // columns

    int low = 0;
    int high = n-1;

    while (low <= high) {
        int mid = (low + high)/2;
        int row = maxElement(arr, mid);

        int leftEle = mid > 0 ? arr[row][mid-1] : INT_MIN;
        int rightEle = mid + 1 < n ? arr[row][mid+1] : INT_MIN;

        if (arr[row][mid] > leftEle && arr[row][mid] > rightEle) {
            return {row, mid};
        } else if (leftEle > arr[row][mid]) {
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }

    return {-1, -1};
}
```