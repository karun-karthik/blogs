### Longest Consecutive Sequence in an Array

**Brute**

In this approach we look out for sequences of consecutive numbers and pick the longest one by linear-search.
1. Iterate through all the items in the array.
2. For every item (let's say k) check if the consecutive elements exist (i.e k+1, k+2, ..)
3. When a valid consecutive element is found, increment the counters

**Code**
```cpp
// TC: O(N^3), SC: O(1)
int longestConsecutiveSequence(vector<int>& arr) {
    int n = arr.size();
    if (n == 0) return 0;
    int longest = 1;

    for (int i=0; i < n; i++) {
        int curr = arr[i];
        int count = 1;

        while(ls(arr, curr + 1)) { // check if next element is present using linear_search
            curr += 1;  // increment for next element in sequence
            count += 1;
        }

        longest = max(longest, count);
    }
    return longest;
}
```

**Better**

In this approach, we sort the array and then find longest consecutive sequence by iteration.
1. Sort the array
2. Iterate the array, and for every element (curr), track last smaller element
    - if curr - 1 == lastSmaller, then increase count and update lastSmaller to curr,
    - else if curr != lastSmaller, reset count and set lastSmaller as curr
    - longest is the max of longest vs. count
3. Return longest


**Code**
```cpp
// TC: O(NlogN) + O(N), SC: O(1)
int longestConsecutiveSequence(vector<int>& arr) {
    int n = arr.size();
    if (n == 0) return 0;
    sort(arr.begin(), arr.end());
    int lastSmaller = INT_MIN;
    int count = 0;
    int longest = 1;
    for (int i = 0; i < n; i++) {
        if (arr[i]-1 == lastSmaller) { // if valid consecutive number exist
            count++;
            lastSmaller = arr[i];
        } else if (arr[i] != lastSmaller) { // if number doesn't exist
            count = 1;
            lastSmaller = arr[i];
        }
        longest = max(longest, count);
    }
    return longest;
}
```

**Optimal**
1. All elements to be inserted into a set
2. For each element (curr),
    - check if it doesn't exist in the set
    - if true, then set count as 1 and x as curr element
    - keep incrementing x and count until x+1 is not present in the set
    - update longest as max of longest, count
3. Return longest

**Code**
```cpp
// TC: O(N) + O(2N), SC: O(N)
// TC ~ O(2N) count be for set traversal in the worst case,
// also if set operations take O(N), then total time complexist will be O(NLogN)

int longestConsecutiveSequence(vector<int>& arr) {
    int n = arr.size();
    if (n == 0) return 0;

    int longest = 1;
    unordered_set<int> st;

    for (auto i: arr)   st.insert(i);

    for (auto it: st) {
        if (st.find(it - 1) == st.end()) {
            int count = 1;
            int x = it;
            while (st.find(x + 1) != st.end()) {
                count++;
                x++;
            }
            longest = max(count, longest);
        }
    }
    return longest;
}
```

### Longest Subarry with sum K

**Brute**
1. The first loop handles the starting indexes from 0 to n-1, i
2. The second loop handles the ending indexes from i to n-1, j
3. The third loops runs from i to j and sum of elements from [i, j] is calculated
4. if sum == k, then maxLength is (j - i + 1)
5. Return maxLength

**Code**
```cpp
// TC: O(N^3) SC: O(1)
int longestSubarray(vector<int>&nums, int k) {
    int n = nums.size();
    int maxLength = 0;
    for (int i = 0; i<n; i++) {
        for (int j = i; j<n; j++) {
            int currSum = 0;
            for (int l = i; l<=j; l++) {
                currSum += nums[l];
            }
            if (currSum == k) maxLength = max(maxLength, j - i + 1);
        }
    }
    return maxLength;
}
```

**Optimal-1 (Pos & Neg)**

We use prefix sum to find the longest subarray with sum as K
1. Use a map to store the prefix sum and their index.
2. Iterate from 0 to n-1
    - for each index i, include arr[i] in prefixSum
    - if prefixSum == K, then maxLength is max(maxLength, i+1)
    - calculate remainingSum for rest of the array (prefixSum - K)
    - if remainingSum exist in map, then find length of subarray from i and starting after prefix sum i.e i-map[remainingSum], update maxLength
    - handle edge-case where 0's could be a part of array, they don't contribute to sum but would increase the length
        - check if prefixSum is not in the map, then mark it against the index
**Code**
```cpp
// TC: O(N) or O(NxlogN) SC: O(N)
int longestSubarray(vector<int>& nums, int K) {
    unordered_map<int, int> mp;
    int prefixSum = 0;
    int maxLength = 0;

    for (int i=0; i<nums.size(); i++) {
        prefixSum += nums[i];
        
        if (prefixSum == k) maxLength = max(maxLength, i + 1);

        int remainingSum = prefixSum - k;

        if (mp.find(remainingSum) != mp.end()) {
            int len = i - mp[remainingSum];
            maxLength = max(maxLength, len);
        }

        if (mp.find(prefixSum) == mp.end())   mp[prefixSum] = i;
    }
    return maxLength;
}
```

**Optimal2 (Only Pos)**

This approach is only suitable for arrays with positive elements. In this, we maintain a window by using 2 pointers, left and right.
1. 2 pointers to maintain the window and sum variable to keep track of window sum
2. The right pointer shifts to include element to the right
3. If sum > k, then left pointer shifts until the sum is <= k
4. If sum == k, then maxLength is updated to (right - left + 1)
5. This is repeated, till right traverse the entire array
6. return maxLength

Code
```cpp
// TC: O(N), SC: O(1)
int longestSubarray(vector<int> &nums, int k){
    int n = nums.size();
    int maxLength = 0;
    int left = 0, right = 0, currSum = nums[0];

    while (right < n) {
        while (left <= right && currSum > k) {
            currSum -= nums[left];
            left++;
        }

        if (currSum == k) {
            maxLength = max(maxLength, right - left + 1);
        }

        right++;
        if (right < n) currSum += nums[right];
    }
    return maxLength;
}
```

### Count subarrays with given sum

**Brute**
1. The first loop handles the starting indexes from 0 to n-1, i
2. The second loop handles the ending indexes from i to n-1, j
3. The third loops runs from i to j and sum of elements from [i, j] is calculated
4. if sum == k, then count++
5. Return count

**Code**
```cpp
// TC: O(N^3) SC: O(1)
int subarraySum(vector<int>&nums, int k) {
    int n = nums.size();
    int count = 0;
    for (int i = 0; i<n; i++) {
        for (int j = i; j<n; j++) {
            int currSum = 0;
            for (int l = i; l<=j; l++) {
                currSum += nums[l];
            }
            if (currSum == k) count++;
        }
    }
    return count;
}
```

**Better**

We can optimize the brute force approach further, by skipping the inner-most loop. To find the current subarray, we only need to add the current element to the previous subarray.
```
Sum of arr[i:j] = Sum of arr[i:j-1] + arr[j]
```
1. The first loop handles the starting indexes from 0 to n-1, i
2. Set currSum = 0, for every subarray
2. The second loop handles the ending indexes from i to n-1, j
3. Calculate currSum of elements from [i, j]
4. if currSum == k, then count++
5. Return count

**Code**
```cpp
// TC: O(N^2), SC: O(1)
int subarraySum(vector<int> &nums, int k) {
    int n = nums.size();
    int count = 0;
    for (int i = 0; i < n; i++) {
        int currSum = 0;
        for (int j = i; j < n; j++) {
            currSum += nums[j];
            if (currSum == k) count++;
        }
    }
    return count;
}
```

**Optimal**

The optimal appraoch involves using prefixSum. The prefix sum of a subarray ending at index is the sum of all the elements up to that index.

Keep a map of prefix sums and how often they appear.
As you move through the array, compute the current prefix sum x.
If x − k is already in the map, add its count to the answer.
Then record x in the map and continue.

1. Use a map to store prefixSum → count.
2. Initialize map[0] = 1 (this handles subarrays starting at index 0).
3. Traverse the array:
    - Add current element to prefixSum
    - If (prefixSum − k) exists in the map, add its count to the answer
    - Increment map[prefixSum]

Why map[0] = 1?
If prefixSum == k, then prefixSum − k = 0.
Having 0 already in the map lets us correctly count subarrays that start from the beginning.

**Code**
```cpp
// TC: O(N) or O(NxlogN) SC: O(N)
int subarraySum(vector<int> &nums, int k) {
    int n = nums.size();
    unordered_map<int, int> mp;
    int currSum = 0, count = 0;

    mp[0] = 1;

    for (int i=0; i<n; i++) {
        currSum += nums[i]; // add current element to prefix sum
        count += mp[currSum - k]; // add number of subarrays with sum equal to x-k
        mp[currSum] += 1; // increment count
    }

    return count;
}
```

### Count subarrays with given xor

**Brute**
1. The first loop handles the starting indexes from 0 to n-1, i
2. The second loop handles the ending indexes from i to n-1, j
3. The third loops runs from i to j and xor of elements from [i, j] is calculated
4. if xor == k, then count++
5. Return count

**Code**
```cpp
// TC: O(N^3) SC: O(1)
int subarraysWithXorK(vector<int> &nums, int k) {
    int n = nums.size();
    int count = 0;
    for (int i = 0; i<n; i++) {
        for (int j = i; j<n; j++) {
            int xorr = 0;
            for (int l = i; l<=j; l++) {
                xorr ^= nums[l];
            }
            if (xorr == k) count++;
        }
    }
    return count;
}
```

**Better**

We can optimize the brute force approach further, by skipping the inner-most loop. To find the current subarray, we only need to xor the current element to the previous subarray.
```
XOR of arr[i:j] = XOR of arr[i:j-1] + arr[j]
```
1. The first loop handles the starting indexes from 0 to n-1, i
2. Set xorr = 0, for every subarray
2. The second loop handles the ending indexes from i to n-1, j
3. Calculate xorr of elements from [i, j]
4. if xorr == k, then count++
5. Return count

**Code**
```cpp
// TC: O(N^2), SC: O(1)
int subarraysWithXorK(vector<int> &nums, int k) {
    int n = nums.size();
    int count = 0;
    for (int i = 0; i<n; i++) {
        int xorr = 0;
        for (int j = i; j<n; j++) {
            xorr ^= nums[j];
            if (xorr == k) count++;
        }
    }
    return count;
}
```

**Optimal**

The optimal appraoch involves using prefixXor.

Let xr be the prefix XOR up to index i.
For a subarray ending at i to have XOR k:
```
XOR(l … i) = prefixXor[i] ^ prefixXor[l-1]
and  XOR(l … i) = k
then prefixXor[l-1] = prefixXor[i] ^ k
```

1. Initialize a map mp and set mp[0] = 1.
2. Maintain a running prefix XOR xr.
3. For each element:
    - xr ^= arr[i]
    - Add mp[xr ^ k] to the answer (if exists).
    - Increment mp[xr].

Return the answer.

Why mp[0] = 1?
If xr == k, then xr ^ k = 0.
Having 0 already in the map lets us correctly count subarrays that start from the beginning.

**Code**
```cpp
// TC: O(N) or O(NxlogN) SC: O(N)
int subarraysWithXorK(vector<int> &nums, int k) {
    int xr = 0;
    int count = 0;
    unordered_map<int, int> mp;
    mp[xr]++;
    for (int i=0; i<nums.size(); i++) {
        xr = xr^nums[i];
        int x = xr^k;
        count += mp[x]; // how many times I've seen it before
        mp[xr]++;
    }
    return count;
}
```