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