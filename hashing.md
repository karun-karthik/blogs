## Longest Consecutive Sequence in an Array

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

## Longest Subarry with sum K

**Brute**
1. The first loop handles the starting indexes from 0 to n-1, i
2. The second loop handles the ending indexes from i to n-1, j
3. The third loops runs from i to j and sum of elements from [i, j] is calculated
4. if sum == k, then length  is (j - i + 1)
5. Return the max value of (j - i + 1)

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
}
```

**Optimal-1 (Pos & Neg)**
We use prefix sum to find the longest subarray with sum as K
1. Use a map to store the prefix sum and their index.
2. Iterate from 0 to n-1
    - for each index i, include arr[i] in prefixSum
    - if prefixSum == K, then longest is max(longest, i+1)
    - calculate remainingSum for rest of the array (prefixSum - K)
    - if remainingSum exist in map, then find length of subarray from i and starting after prefix sum i.e i-map[remainingSum], update longest
    - handle edge-case where 0's could be a part of array, they don't contribute to sum but would increase the length
        - check if prefixSum is not in the map, then mark it against the index
**Code**
```cpp
int longestSubarray(vector<int>& nums, int K) {
    unordered_map<int, int> mp;
    int prefixSum = 0;
    int longest = 0;

    for (int i=0; i<nums.size(); i++) {
        prefixSum += nums[i];
        
        if (prefixSum == k) longest = max(longest, i + 1);

        int remainingSum = prefixSum - k;

        if (mp.find(remainingSum) != mp.end()) {
            int len = i - mp[remainingSum];
            longest = max(longest, len);
        }

        if (mp.find(prefixSum) == mp.end())   mp[prefixSum] = i;
    }
    return longest;
}
```