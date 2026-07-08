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

int longestConsecutive(vector<int>& nums) {
    if (nums.empty()) return 0;

    // Store all unique elements for O(1) average-time lookups
    unordered_set<int> st(nums.begin(), nums.end());

    int longest = 1;

    for (int num : st) {
        // Process only if 'num' is the first element of a sequence.
        // If (num - 1) exists, this sequence will be counted
        // when we reach its actual starting element.
        if (!st.count(num - 1)) {
            int curr = num;
            int len = 1;

            // Count consecutive elements starting from 'num'
            while (st.count(curr + 1)) {
                curr++;
                len++;
            }

            // Update the maximum sequence length found so far
            longest = max(longest, len);
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
int longestSubarray(vector<int> &nums, int k) {
    unordered_map<int, int> mp; // Stores the first occurrence of each prefix sum

    int sum = 0;
    int longest = 0;

    for (int i = 0; i < nums.size(); i++) {
        // Compute the prefix sum up to the current index
        sum += nums[i];

        // If the prefix sum itself is k, then the subarray
        // from index 0 to i has the required sum.
        if (sum == k) {
            longest = max(longest, i + 1);
        }

        // Intuition:
        // If currentPrefixSum - previousPrefixSum = k,
        // then the elements between those two prefix sums
        // form a subarray with sum k.
        //
        // previousPrefixSum = currentPrefixSum - k
        int rem = sum - k;

        if (mp.find(rem) != mp.end()) {
            int len = i - mp[rem];
            longest = max(longest, len);
        }

        // Store only the first occurrence of each prefix sum.
        // Intuition:
        // Keeping the earliest index gives the longest possible
        // subarray when the same prefix sum is encountered later.
        if (mp.find(sum) == mp.end()) {
            mp[sum] = i;
        }
    }

    return longest;
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
int longestSubarray(vector<int> &nums, int k) {
    int n = nums.size();

    int maxLen = 0;

    // Sliding window boundaries
    int left = 0, right = 0;

    // Sum of the current window
    int sum = nums[0];

    while (right < n) {

        // Intuition:
        // Since all elements are non-negative, if the window sum exceeds k,
        // expanding the window will only increase the sum further.
        // Therefore, shrink the window from the left until the sum <= k.
        while (left <= right && sum > k) {
            sum -= nums[left];
            left++;
        }

        // Update the answer if the current window has the required sum
        if (sum == k) {
            maxLen = max(maxLen, right - left + 1);
        }

        // Expand the window by including the next element
        right++;
        if (right < n) {
            sum += nums[right];
        }
    }

    return maxLen;
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
int subarraySum(vector<int>& nums, int k) {
    unordered_map<int, int> prefixFreq;

    // A prefix sum of 0 exists once before the array starts.
    // This helps count subarrays that begin from index 0.
    prefixFreq[0] = 1;

    int prefixSum = 0;
    int count = 0;

    for (int num : nums) {
        // Update the running prefix sum.
        prefixSum += num;

        // If there was an earlier prefix sum equal to (prefixSum - k),
        // then the elements between that prefix and the current index
        // form a subarray whose sum is k.
        if (prefixFreq.find(prefixSum - k) != prefixFreq.end()) {
            count += prefixFreq[prefixSum - k];
        }

        // Record the current prefix sum for future subarrays.
        prefixFreq[prefixSum]++;
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
    unordered_map<int, int> xorFreq;

    // XOR of an empty prefix is 0.
    // This helps count subarrays starting from index 0.
    xorFreq[0] = 1;

    int prefixXor = 0;
    int count = 0;

    for (int num : nums) {
        // Compute XOR of elements from index 0 to current index.
        prefixXor ^= num;

        // If a previous prefix XOR is (prefixXor ^ k),
        // then the XOR of the subarray between them is k.
        if (xorFreq.find(prefixXor ^ k) != xorFreq.end()) {
            count += xorFreq[prefixXor ^ k];
        }

        // Store the current prefix XOR for future subarrays.
        xorFreq[prefixXor]++;
    }

    return count;
}
```