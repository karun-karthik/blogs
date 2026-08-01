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

```cpp
class Solution {
public:

    int search(vector<int>& nums, int target, bool findFirst) {

        int low = 0, high = nums.size() - 1;
        int ans = -1;

        while (low <= high) {

            int mid = low + (high - low) / 2;

            if (nums[mid] == target) {

                // Store current occurrence
                ans = mid;

                // Continue searching towards the required boundary
                if (findFirst)
                    high = mid - 1;
                else
                    low = mid + 1;
            }
            else if (nums[mid] < target) {

                low = mid + 1;
            }
            else {

                high = mid - 1;
            }
        }

        return ans;
    }

    vector<int> searchRange(vector<int>& nums, int target) {

        int first = search(nums, target, true);

        // Target not present
        if (first == -1)
            return {-1, -1};

        int last = search(nums, target, false);

        return {first, last};
    }
};
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
int findKRotation(vector<int> &arr) {
    // INTUITION:
    // Number of rotations = index of the minimum element.
    // So the problem reduces to finding the minimum element in a
    // rotated sorted array using Binary Search.

    int low = 0, high = arr.size() - 1;

    int minValue = INT_MAX;
    int rotationIndex = -1;

    while (low <= high) {

        int mid = low + (high - low) / 2;

        // If the current search space is already sorted,
        // arr[low] is the minimum in this range.
        if (arr[low] <= arr[high]) {
            if (arr[low] < minValue) {
                minValue = arr[low];
                rotationIndex = low;
            }
            break;
        }

        // Left half is sorted.
        if (arr[low] <= arr[mid]) {

            // The first element of a sorted half is its minimum.
            // Record it and search the unsorted half.
            if (arr[low] < minValue) {
                minValue = arr[low];
                rotationIndex = low;
            }

            low = mid + 1;
        }
        // Right half is sorted.
        else {

            // Mid is the smallest element of this half.
            // Record it and continue searching left.
            if (arr[mid] < minValue) {
                minValue = arr[mid];
                rotationIndex = mid;
            }

            high = mid - 1;
        }
    }

    return rotationIndex;
}
```

### Single element in rotated sorted array
- **Mid is an Even index**
  - If `arr[mid] == arr[mid + 1]` → single element is in **right half**
  - If `arr[mid] == arr[mid - 1]` → single element is in **left half**

- **Mid is an Odd index**
  - If `arr[mid] == arr[mid + 1]` → single element is in **left half**
  - If `arr[mid] == arr[mid - 1]` → single element is in **right half**

```cpp
int singleNonDuplicate(vector<int> &nums) {
    int n = nums.size();

    // Edge cases
    if (n == 1) return nums[0];

    if (nums[0] != nums[1]) return nums[0];

    if (nums[n - 1] != nums[n - 2]) return nums[n - 1];

    int low = 1;
    int high = n - 2;

    while (low <= high) {

        int mid = low + (high - low) / 2;

        // Found the unique element
        if (nums[mid] != nums[mid - 1] &&
            nums[mid] != nums[mid + 1]) {
            return nums[mid];
        }

        /*
        Left half is "properly paired" if:
        1. mid is even and matches next
        2. mid is odd and matches previous

        In that case, unique element lies on the right.
        Otherwise, it lies on the left.
        */
        if ((mid % 2 == 0 && nums[mid] == nums[mid + 1]) ||
            (mid % 2 == 1 && nums[mid] == nums[mid - 1])) {

            low = mid + 1;
        }
        else {
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
int floorSqrt(int n) {
    // INTUITION:
    // We need the largest number x such that x*x <= n.
    // As x increases, x*x also increases (monotonic property),
    // making Binary Search applicable.

    int low = 0, high = n;
    int ans = 0;

    while (low <= high) {

        int mid = low + (high - low) / 2;

        // Use long long to prevent integer overflow
        long long square = 1LL * mid * mid;

        if (square <= n) {

            // mid is a valid answer.
            // Try to find a larger valid square root.
            ans = mid;
            low = mid + 1;
        }
        else {

            // mid is too large.
            // Search in the smaller half.
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
long long power(int base, int exp, int limit) {
    long long ans = 1;

    // Compute base^exp.
    // Stop early if the value exceeds the limit,
    // since we only care whether it is <=, == or > limit.
    while (exp--) {

        ans *= base;

        if (ans > limit)
            return ans;
    }

    return ans;
}

int NthRoot(int N, int M) {

    // INTUITION:
    // We need to find an integer x such that:
    //      x^N = M
    //
    // As x increases, x^N also increases monotonically.
    // Hence, Binary Search can be applied on the answer.

    int low = 0, high = M;

    while (low <= high) {

        int mid = low + (high - low) / 2;

        long long currPower = power(mid, N, M);

        if (currPower == M) {
            // Exact Nth root found
            return mid;
        }
        else if (currPower < M) {
            // mid is too small.
            // Search for a larger root.
            low = mid + 1;
        }
        else {
            // mid is too large.
            // Search in the left half.
            high = mid - 1;
        }
    }

    // No integer Nth root exists
    return -1;
}
```

### Find the smallest divisor
Given an array of integers nums and an integer limit as the threshold value,
find the smallest positive integer divisor such that upon dividing all the elements of the array by this divisor,
the sum of the division results is less than or equal to the threshold value.
After dividing each element by the chosen divisor,
take the ceiling of the result (i.e., round up to the next whole number).

```cpp
// Returns the sum of ceil(nums[i] / divisor) for all elements.
// Integer alternative: ceil(a / b) = (a + b - 1) / b
int divisorSum(vector<int>& nums, int divisor) {
    int sum = 0;

    for (int num : nums) {
        // sum += ceil((double)num / divisor);
        // Equivalent integer formula:
        sum += (num + divisor - 1) / divisor;
    }

    return sum;
}

int smallestDivisor(vector<int>& nums, int limit) {
    int low = 1;
    int high = *max_element(nums.begin(), nums.end());

    int ans = -1;

    // Binary search for the smallest valid divisor.
    while (low <= high) {
        int mid = low + (high - low) / 2;

        // Sum after dividing each element by 'mid' (rounded up).
        int divSum = divisorSum(nums, mid);

        if (divSum <= limit) {
            // 'mid' is valid. Try to find a smaller valid divisor.
            ans = mid;
            high = mid - 1;
        } else {
            // Divisor is too small, resulting sum exceeds the limit.
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

```cpp
// Returns true if Koko can finish all bananas at 'rate' bananas/hour.
bool canComplete(int rate, vector<int>& nums, int h) {
    long long hours = 0;

    for (int bananas : nums) {
        // Hours needed for the current pile.
        // ceil(a / b) = (a + b - 1) / b
        hours += (bananas + rate - 1) / rate;
    }

    return hours <= h;
}

int minimumRateToEatBananas(vector<int> nums, int h) {
    int low = 1;
    int high = *max_element(nums.begin(), nums.end());

    int ans = high;

    // Binary search for the minimum valid eating rate.
    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (canComplete(mid, nums, h)) {
            // Current rate works. Try a smaller one.
            ans = mid;
            high = mid - 1;
        } else {
            // Current rate is too slow.
            low = mid + 1;
        }
    }

    return ans;
}
```

### Minimum days to make M bouquets

Given n roses and an array nums where nums[i] denotes that the 'ith' rose will bloom on the nums[i]th day, only adjacent bloomed roses can be picked to make a bouquet. Exactly k adjacent bloomed roses are required to make a single bouquet. Find the minimum number of days required to make at least m bouquets, each containing k roses. Return -1 if it is not possible.

```cpp
// Returns true if it's possible to make at least 'm' bouquets
// by 'day', where each bouquet requires 'k' adjacent bloomed flowers.
bool canMakeBouquet(int day, vector<int>& nums, int k, int m) {
    int bouquets = 0;
    int flowerCount = 0;

    for (int flowersOnDay : nums) {

        if (flowersOnDay <= day) {
            // Flower has bloomed by 'day'.
            flowerCount++;
        } else {
            // Current streak ends. Form as many bouquets as possible.
            bouquets += flowerCount / k;
            flowerCount = 0;
        }
    }

    // Count bouquets from the last streak.
    bouquets += flowerCount / k;

    return bouquets >= m;
}

int roseGarden(int n, vector<int>& nums, int k, int m) {

    // Not enough flowers to make the required bouquets.
    if ((long long)k * m > n)
        return -1;

    int low = *min_element(nums.begin(), nums.end());
    int high = *max_element(nums.begin(), nums.end());

    int ans = -1;

    // Binary search for the minimum day on which all bouquets can be made.
    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (canMakeBouquet(mid, nums, k, m)) {
            // 'mid' works. Try to find an earlier valid day.
            ans = mid;
            high = mid - 1;
        } else {
            // Not enough flowers have bloomed yet.
            low = mid + 1;
        }
    }

    return ans;
}
```

## FAQ

### Aggressive Cows
Given an array nums of size n, which denotes the positions of stalls, and an integer k, which denotes the number of aggressive cows, assign stalls to k cows such that the minimum distance between any two cows is the maximum possible. Find the maximum possible minimum distance.
```cpp
bool canPlace(vector<int>& nums, int minDistance, int k) {
    // Place the first cow at the first stall
    int placedCows = 1;
    int lastCowPosition = nums[0];

    // Greedily place each next cow at the earliest valid stall
    for (int i = 1; i < nums.size(); i++) {

        // Current stall is far enough from the last placed cow
        if (nums[i] - lastCowPosition >= minDistance) {

            placedCows++;
            lastCowPosition = nums[i];
        }

        // Successfully placed all cows
        if (placedCows == k)
            return true;
    }

    // Unable to place all cows with the given minimum distance
    return false;
}

int aggressiveCows(vector<int> &nums, int k) {

    sort(nums.begin(), nums.end());

    // INTUITION:
    // We need to maximize the minimum distance between any two cows.
    //
    // Instead of directly finding the answer,
    // Binary Search on the possible distance.
    //
    // Search Space:
    // Minimum possible distance = 0
    // Maximum possible distance = last stall - first stall

    int low = 0;
    int high = nums.back() - nums.front();

    int ans = -1;

    while (low <= high) {

        int mid = low + (high - low) / 2;

        // Can we place all cows while keeping
        // at least 'mid' distance between them?
        if (canPlace(nums, mid, k)) {

            // 'mid' is feasible.
            // Try to maximize the minimum distance.
            ans = mid;
            low = mid + 1;
        }
        else {

            // Distance is too large.
            // Reduce the required minimum distance.
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
// I have total pages in nums (sum of it)
// no. of students is m
// page is the number of pages each student can get
bool canAllocate(int page, vector<int>& nums, int m) {
    int allocated = 1;
    int pageCount = 0;

    for (int i = 0; i < nums.size(); i++) {
        if (pageCount + nums[i] <= page) {
            pageCount += nums[i];
        } else {
            allocated++;
            pageCount = nums[i];
        }
    }

    return allocated <= m;
}

int findPages(vector<int>& nums, int m) {

    if (m > nums.size())
        return -1;

    int low = *max_element(nums.begin(), nums.end());
    int high = accumulate(nums.begin(), nums.end(), 0);

    int ans = -1;

    // Binary search for the minimum feasible page limit.
    while (low <= high) {

        int mid = low + (high - low) / 2;

        if (canAllocate(mid, nums, m)) {
            ans = mid;
            high = mid - 1;      // Try a smaller limit.
        } else {
            low = mid + 1;       // Increase the page limit.
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

    // INTUITION:
    // A peak is an element greater than both its neighbors.
    //
    // Instead of checking every element, Binary Search works because:
    // - If we're on an increasing slope, a peak must exist on the right.
    // - If we're on a decreasing slope, a peak must exist on the left.
    //
    // We simply move towards the side that is guaranteed to contain a peak.

    // Single element is always a peak
    if (n == 1) return 0;

    // Check boundary peaks
    if (arr[0] > arr[1]) return 0;
    if (arr[n - 1] > arr[n - 2]) return n - 1;

    int low = 1;
    int high = n - 2;

    while (low <= high) {

        int mid = low + (high - low) / 2;

        // Current element is greater than both neighbours
        if (arr[mid] > arr[mid - 1] &&
            arr[mid] > arr[mid + 1]) {
            return mid;
        }

        // Increasing slope
        // A peak is guaranteed to exist on the right
        else if (arr[mid] > arr[mid - 1]) {
            low = mid + 1;
        }

        // Decreasing slope
        // A peak is guaranteed to exist on the left
        else {
            high = mid - 1;
        }
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
```
Binary Search on Partition

    Example:
    a = [1, 3, 8]
    b = [7, 9, 10, 11]

    Merged array:
    [1, 3, 7, 8, 9, 10, 11]

    Goal:
    Partition both arrays such that:
    1. Left half contains (n + m + 1) / 2 elements.
    2. Every element in the left half <= every element in the right half.

    Example partition:

    a : [1 3 8 | ]
    b : [7 | 9 10 11]

    left1  = 8
    right1 = INF
    left2  = 7
    right2 = 9

    Conditions:
    left1 <= right2  (8 <= 9)  ✓
    left2 <= right1  (7 <= INF) ✓

    Valid partition found.

    Odd total elements:
    Median = max(left1, left2) = 8

    Even total elements:
    Median = (max(left1, left2) + min(right1, right2)) / 2

    ----------------------------------------------------

    How do we move the partition?

    Case 1:
    left1 > right2

    a : [1 3 8 | 9]
    b : [5 6 | 7]

    8 > 7

    => Too many elements taken from array 'a'.
    => Move partition LEFT.

    high = cut1 - 1

    ----------------------------------------------------

    Case 2:
    left2 > right1

    a : [1 3 | 4]
    b : [5 6 | 7]

    6 > 4

    => Too few elements taken from array 'a'.
    => Move partition RIGHT.

    low = cut1 + 1

    Time Complexity : O(log(min(n, m)))
    Space Complexity: O(1)
```

```cpp
double median(vector<int>& a, vector<int>& b) {
    int n = a.size(), m = b.size();

    // Always binary search on the smaller array.
    if (n > m)
        return median(b, a);

    int total = n + m;
    int leftSize = (total + 1) / 2;

    int low = 0, high = n;

    while (low <= high) {

        // Partition index in both arrays.
        int cut1 = low + (high - low) / 2;
        int cut2 = leftSize - cut1;

        // Elements around the partition.
        int left1  = (cut1 > 0) ? a[cut1 - 1] : INT_MIN;
        int right1 = (cut1 < n) ? a[cut1]     : INT_MAX;

        int left2  = (cut2 > 0) ? b[cut2 - 1] : INT_MIN;
        int right2 = (cut2 < m) ? b[cut2]     : INT_MAX;

        // Correct partition found.
        if (left1 <= right2 && left2 <= right1) {

            // Odd length -> largest element in the left half.
            if (total & 1)
                return max(left1, left2);

            // Even length -> average of the middle two elements.
            return (max(left1, left2) + min(right1, right2)) / 2.0;
        }

        // Too many elements taken from the first array.
        if (left1 > right2)
            high = cut1 - 1;

        // Too few elements taken from the first array.
        else
            low = cut1 + 1;
    }

    return 0.0;
}
```

### Kth element of 2 sorted arrays

```cpp
/*
    Binary Search on Partition

    Goal:
    Find the k-th smallest element in the merged sorted array
    without actually merging the arrays.

    Idea:
    Partition both arrays such that:
    1. Left partition contains exactly 'k' elements.
    2. Every element in the left partition <= every element in the right partition.

    Partition:

    a : [ ... left1 | right1 ... ]
                ^
                cut1

    b : [ ... left2 | right2 ... ]
                ^
                cut2

    Since the left partition must contain exactly 'k' elements:

        cut1 + cut2 = k
        cut2 = k - cut1

    ----------------------------------------------------

    Search Space

    cut1 must satisfy TWO constraints.

    From array 'a':
        0 <= cut1 <= n

    From array 'b':
        0 <= cut2 <= m

    Substitute:

        0 <= k - cut1 <= m

    Solving gives:

        k - m <= cut1 <= k

    Combine both ranges:

        max(0, k - m) <= cut1 <= min(k, n)

    Hence,

        low  = max(0, k - m)
        high = min(k, n)

    ----------------------------------------------------

    Move Partition

    left1 > right2
    => Took too many elements from array 'a'
    => Move LEFT

    left2 > right1
    => Took too few elements from array 'a'
    => Move RIGHT

    ----------------------------------------------------

    Once the partition is valid,

    left1 <= right2
    left2 <= right1

    the k-th smallest element is simply

        max(left1, left2)

    Time Complexity : O(log(min(n, m)))
    Space Complexity: O(1)
*/
int kthElement(vector<int>& a, vector<int>& b, int k) {
    int n = a.size();
    int m = b.size();

    // Always binary search on the smaller array.
    if (n > m)
        return kthElement(b, a, k);

    // Valid search range for the partition in array 'a'.
    int low = max(0, k - m);
    int high = min(k, n);

    while (low <= high) {
        // Partition indices.
        int cut1 = low + (high - low) / 2;
        int cut2 = k - cut1;

        // Elements around the partitions.
        int left1  = (cut1 > 0) ? a[cut1 - 1] : INT_MIN;
        int right1 = (cut1 < n) ? a[cut1]     : INT_MAX;

        int left2  = (cut2 > 0) ? b[cut2 - 1] : INT_MIN;
        int right2 = (cut2 < m) ? b[cut2]     : INT_MAX;

        // Correct partition found.
        if (left1 <= right2 && left2 <= right1)
            return max(left1, left2);

        // Too many elements taken from the first array.
        if (left1 > right2)
            high = cut1 - 1;

        // Too few elements taken from the first array.
        else
            low = cut1 + 1;
    }

    return -1; // Unreachable for valid input.
}
```

### Split array - largest sum
Given an integer array a of size n and an integer k. Split the array a into k non-empty subarrays such that the largest sum of any subarray is minimized. Return the minimized largest sum of the split.

```cpp
int countPartition(vector<int>& nums, int maxAllowedSum) {

    // Start with one partition
    int partitions = 1;
    long long currentSum = 0;

    for (int i = 0; i < nums.size(); i++) {

        // Current element fits in the existing partition
        if (currentSum + nums[i] <= maxAllowedSum) {
            currentSum += nums[i];
        } else {
            // Current partition is full.
            // Start a new partition from this element.
            partitions++;
            currentSum = nums[i];
        }
    }

    return partitions;
}

int largestSubarraySumMinimized(vector<int> &nums, int k) {

    // INTUITION:
    // Split the array into exactly k subarrays
    // such that the largest subarray sum is minimized.
    //
    // Instead of guessing the partition,
    // Binary Search on the answer (maximum allowed subarray sum).

    // Minimum possible answer:
    // Largest element (cannot split an element)
    int low = *max_element(nums.begin(), nums.end());

    // Maximum possible answer:
    // Entire array as one partition
    int high = accumulate(nums.begin(), nums.end(), 0);

    int ans = -1;

    while (low <= high) {

        int mid = low + (high - low) / 2;

        // Number of partitions needed if each partition
        // is allowed a maximum sum of 'mid'
        int partitions = countPartition(nums, mid);

        if (partitions > k) {
            // Too many partitions required.
            // Increase the allowed partition sum.
            low = mid + 1;
        } else {
            // Feasible solution.
            // Try to further minimize the maximum partition sum.
            ans = mid;
            high = mid - 1;
        }
    }

    return ans;
}
```

## 2D Arrays

### Find row with maximum 1s

Given a non-empty grid mat consisting of only 0s and 1s, where all the rows are sorted in ascending order, find the index of the row with the maximum number of ones.

If two rows have the same number of ones, consider the one with a smaller index. If no 1 exists in the matrix, return -1.

```cpp
int lower_bound(vector<int>& arr, int x) {

    // INTUITION:
    // Find the first index where value >= x.
    //
    // Since each row is sorted,
    // the first occurrence of 1 divides the row into:
    // [0 ... 0 | 1 ... 1]

    int low = 0;
    int high = arr.size() - 1;

    // Default answer:
    // If x is not found, insertion position is at the end.
    int ans = arr.size();

    while (low <= high) {

        int mid = low + (high - low) / 2;

        if (arr[mid] >= x) {

            // mid is a valid lower bound.
            // Search further left for the first occurrence.
            ans = mid;
            high = mid - 1;
        }
        else {

            // First occurrence must lie on the right.
            low = mid + 1;
        }
    }

    return ans;
}

int rowWithMax1s(vector<vector<int>>& mat) {

    // INTUITION:
    // Since every row is sorted,
    // Number of 1's = Total columns - First occurrence of 1.
    //
    // Find the row having the maximum count of 1's.

    int maxOnes = 0;
    int answerRow = -1;

    for (int row = 0; row < mat.size(); row++) {

        // Index of first 1 in current row
        int firstOne = lower_bound(mat[row], 1);

        // Count of 1's in current row
        int oneCount = mat[row].size() - firstOne;

        // Update answer if current row has more 1's
        if (oneCount > maxOnes) {
            maxOnes = oneCount;
            answerRow = row;
        }
    }

    return answerRow;
}
```

### Search in 2D Matrix

Given a 2-D array mat where the elements of each row are sorted in non-decreasing order, and the first element of a row is greater than the last element of the previous row (if it exists), and an integer target, determine if the target exists in the given mat or not.

```cpp
// TC: O(log(N*M)) SC: O(1)
bool searchMatrix(vector<vector<int>>& mat, int target) {
    // Handle empty matrix cases.
    if (mat.empty() || mat[0].empty())
        return false;

    int m = mat.size();
    int n = mat[0].size();

    // Since:
    // 1. Each row is sorted.
    // 2. First element of a row > last element of previous row.
    //
    // The entire matrix can be viewed as one sorted 1D array
    // of size (m * n). So, we perform a normal binary search
    // on the virtual array.

    int low = 0;
    int high = m * n - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        // Convert the virtual 1D index back to its 2D position.
        // row = mid / n
        // col = mid % n
        int ele = mat[mid / n][mid % n];

        if (ele == target) {
            return true;
        }
        else if (ele < target) {
            // Target lies in the right half.
            low = mid + 1;
        }
        else {
            // Target lies in the left half.
            high = mid - 1;
        }
    }

    // Target was not found.
    return false;
}
```

### Search in 2D Matrix ii

Given a 2D array matrix where each row is sorted in ascending order from left to right and each column is sorted in ascending order from top to bottom, write an efficient algorithm to search for a specific integer target in the matrix.

```cpp
bool searchMatrix(vector<vector<int>>& mat, int target) {
    int m = mat.size();
    int n = mat[0].size();

    // Start from the top-right corner because it gives us
    // two possible directions to eliminate:
    //
    // - Left  -> smaller values
    // - Down  -> larger values
    //
    // At every step, we can discard either an entire row
    // or an entire column, making the search efficient.

    int row = 0;
    int col = n - 1;

    while (row < m && col >= 0) {
        if (mat[row][col] == target) {
            return true;
        }
        else if (mat[row][col] > target) {
            // Current value is too large.
            // Everything below in this column is even larger,
            // so move left to a smaller value.
            col--;
        }
        else {
            // Current value is too small.
            // Everything to the left in this row is even smaller,
            // so move down to a larger value.
            row++;
        }
    }

    // Target does not exist in the matrix.
    return false;
}
```

### Find Peak Element ii

Given a 0-indexed n x m matrix mat where no two adjacent cells are equal, find any peak element mat[i][j] and return the array [i, j].A peak element in a 2D grid is an element that is strictly greater than all of its adjacent neighbours to the left, right, top, and bottom.

Assume that the entire matrix is surrounded by an outer perimeter with the value -1 in each cell.

Note: As there can be many peak values, 1 is given as output if the returned index is a peak number, otherwise 0.

```cpp
vector<int> findPeakGrid(vector<vector<int>>& mat) {
    int rows = mat.size();
    int cols = mat[0].size();

    // INTUITION:
    // Apply Binary Search on columns.
    //
    // For every middle column, consider only its maximum element.
    // If even the maximum element isn't a peak, then no other element
    // in that column can be a peak.
    //
    // Compare this maximum element with its left and right neighbours
    // to decide which half is guaranteed to contain a peak.

    int low = 0;
    int high = cols - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        // Find the row containing the maximum element
        // in the current middle column.
        int maxRow = 0;
        for (int row = 1; row < rows; row++) {
            if (mat[row][mid] > mat[maxRow][mid]) {
                maxRow = row;
            }
        }

        // Treat out-of-bound neighbours as -∞
        int left = (mid > 0) ? mat[maxRow][mid - 1] : -1;
        int right = (mid < cols - 1) ? mat[maxRow][mid + 1] : -1;

        // Current element is greater than both horizontal neighbours
        // Since it is already the maximum in its column,
        // it is also greater than its vertical neighbours.
        if (mat[maxRow][mid] > left && mat[maxRow][mid] > right) {
            return {maxRow, mid};
        }

        // A larger element exists on the left.
        // A peak is guaranteed to exist in the left half.
        if (left > mat[maxRow][mid]) {
            high = mid - 1;
        }

        // Otherwise, move towards the larger element on the right.
        else {
            low = mid + 1;
        }
    }

    return {-1, -1};
}
```

### Matrix Median 
Given a 2D array matrix that is row-wise sorted. The task is to find the median of the given matrix.

```cpp
int upperBound(vector<int>& row, int x) {
    // INTUITION:
    // Find the first element strictly greater than x.
    // The returned index equals the number of elements <= x.

    int low = 0;
    int high = row.size() - 1;

    // Default insertion position if no element > x exists
    int ans = row.size();

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (row[mid] > x) {
            // mid is a valid upper bound.
            // Try to find an earlier one.
            ans = mid;
            high = mid - 1;
        } else {
            // Elements <= x lie on the right.
            low = mid + 1;
        }
    }

    return ans;
}

int findMedian(vector<vector<int>>& matrix) {
    int rows = matrix.size();
    int cols = matrix[0].size();

    // INTUITION:
    // We are NOT searching for the median's position.
    // We are searching for its VALUE.
    //
    // For every candidate value 'mid',
    // count how many elements are <= mid.
    //
    // This count is monotonic:
    // Larger value → Larger count
    // Hence, Binary Search on the value range.

    // Smallest possible value in the matrix
    int low = INT_MAX;

    // Largest possible value in the matrix
    int high = INT_MIN;

    for (int i = 0; i < rows; i++) {
        low = min(low, matrix[i][0]);
        high = max(high, matrix[i][cols - 1]);
    }

    // Median should have exactly 'required' elements before it
    int required = (rows * cols) / 2;

    int ans = -1;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        // Count elements <= mid across all rows
        int count = 0;

        for (int i = 0; i < rows; i++) {
            count += upperBound(matrix[i], mid);
        }

        if (count > required) {
            // Enough elements are <= mid.
            // mid could be the median.
            // Try finding a smaller valid value.
            ans = mid;
            high = mid - 1;
        } else {
            // Too few elements are <= mid.
            // Median must be larger.
            low = mid + 1;
        }
    }

    return ans;
}
```

## Contest

### Neightbours within K distance
Given an integer array nums with n values and a value k, return an array containing the number of neighbours for each element of the array.

An element x is the neighbour of element y if x falls in the range [y-k, y+k] (inclusive).
```
Input: nums = [1, 4, 7, 8, 9], k = 3
Output: [2, 3, 4, 3, 3]

Explanation: Neighbours of 1 = [1, 4]
Neighbours of 4 = [1, 4, 7]
Neighbours of 7 = [4, 7, 8, 9]
Neighbours of 8 = [7, 8, 9]
Neighbours of 9 = [7, 8, 9]
```
```cpp
vector<int> neighboursWithKDistance(vector<int>& nums, int k) {

    int n = nums.size();

    // INTUITION:
    // For every element x, count how many elements lie in
    // the range [x-k, x+k].
    //
    // Sorting allows us to Binary Search the left and right
    // boundaries of this range in O(log n).

    vector<pair<int, int>> arr;

    // Store {value, original index}
    // so that after sorting we can place answers
    // back in the original order.
    for (int i = 0; i < n; i++) {
        arr.push_back({nums[i], i});
    }

    // Sort by value
    sort(arr.begin(), arr.end());

    // Extract only the sorted values
    // to perform Binary Search.
    vector<int> values;
    for (auto p : arr) {
        values.push_back(p.first);
    }

    vector<int> ans(n);

    for (int i = 0; i < n; i++) {

        int val = arr[i].first;

        // First element >= (val - k)
        int left = lower_bound(values.begin(), values.end(), val - k)
                   - values.begin();

        // First element > (val + k)
        int right = upper_bound(values.begin(), values.end(), val + k)
                    - values.begin();

        // Number of elements in [val-k, val+k]
        ans[arr[i].second] = right - left;
    }

    return ans;
}
```

### Z-Score
Given an array of integers marks containing the marks of a student in each subject and a multiplicative factor k. Return the Z-Score of the student.

Z-Score is defined as the maximum value of x, where the student has at least x subjects where they have scored at least x * k.

```cpp
int subjectCount(vector<int>& marks, int x, int k) {
    // Count how many subjects have marks >= x * k
    int count = 0;
    int requiredMarks = x * k;

    for (int mark : marks) {
        if (mark >= requiredMarks) {
            count++;
        }
    }

    return count;
}

int ZScore(vector<int>& marks, int k) {

    // INTUITION:
    // We need the maximum value of x such that
    // there are at least x subjects having marks >= x * k.
    //
    // Instead of checking every possible x,
    // Binary Search on the answer.
    //
    // Search Space:
    // x can never exceed the number of subjects.

    int n = marks.size();

    int low = 0;
    int high = n;

    int ans = 0;

    while (low <= high) {

        int mid = low + (high - low) / 2;

        // Number of subjects satisfying:
        // marks >= mid * k
        int count = subjectCount(marks, mid, k);

        if (count >= mid) {
            // 'mid' is a valid Z-Score.
            // Try to maximize it.
            ans = mid;
            low = mid + 1;
        } else {
            // Not enough qualifying subjects.
            // Reduce the candidate Z-Score.
            high = mid - 1;
        }
    }

    return ans;
}
```