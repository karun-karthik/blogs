## DP on Subsequences

### Subset sum equals to target
Given an array arr of n integers and an integer target, determine if there is a subset of the given array with a sum equal to the given target. 

```cpp
bool solve(int idx, vector<int>&arr, int target, vector<vector<int>> &dp) {
    if (target == 0)    return true;
    if (idx == 0)  return arr[0] == target;
    if (dp[idx][target] != -1)  return dp[idx][target];
    int pick = 0;
    if (arr[idx] <= target)
        pick = solve(idx - 1, arr, target - arr[idx], dp);
    int notPick = solve(idx - 1, arr, target, dp);
    return dp[idx][target] = pick || notPick;
}

bool isSubsetSumMemo(vector<int>arr, int target){
    int n = arr.size();
    vector<vector<int>> dp(n, vector<int>(target+1, -1));
    return solve(n-1, arr, target, dp);
}

bool isSubsetSumTab(vector<int>arr, int target) {
    int n = arr.size();
    vector<vector<int>> dp(n, vector<int>(target + 1, 0));
    for (int i = 0; i < n; i++) {
        dp[i][0] = true;
    }
    if (arr[0] <= target) {
        // this condition is to prevent outofbounds exception
        dp[0][arr[0]] = true;
    }
    for (int idx = 1; idx < n; idx++) {
        for (int val = 1; val <= target; val++) {
            int pick = 0;
            if (arr[idx] <= val)
                pick = dp[idx - 1][val - arr[idx]];
            int notPick = dp[idx - 1][val];
            dp[idx][val] = pick || notPick;
        }
    }
    return dp[n-1][target];
}

bool isSubsetSumConstant(vector<int>arr, int target) {
    int n = arr.size();
    vector<int> curr(target + 1, 0);
    vector<int> prev(target + 1, 0);
    // for (int i = 0; i < n; i++) {
    //     prev[0] = true;   
    // } -> this is simplified to below line
    // prev[0] = true; and curr[0] = true;
    prev[0] = true;
    curr[0] = true;
    if (arr[0] <= target) {
        // this condition is to prevent outofbounds exception
        prev[arr[0]] = true;
    }
    for (int idx = 1; idx < n; idx++) {
        for (int val = 1; val <= target; val++) {
            int pick = 0;
            if (arr[idx] <= val)
                pick = prev[val - arr[idx]];
            int notPick = prev[val];
            curr[val] = pick || notPick;
        }
        prev = curr;
    }
    return prev[target];
}

bool isSubsetSum(vector<int>arr, int target){
    // return isSubsetSumMemo(arr, target);
    // return isSubsetSumTab(arr, target);
    return isSubsetSumConstant(arr, target);
}
```

### Partition equal subset sum
Given an array arr of n integers, return true if the array can be partitioned into two subsets such that the sum of elements in both subsets is equal else return false.

```cpp
bool solve(int idx, int target, vector<int>&arr, vector<vector<int>> &dp) {
    if (target == 0)    return true;
    if (idx == 0)   return arr[0] == target;
    if (dp[idx][target] != -1)  return dp[idx][target];

    bool notPick = solve(idx - 1, target, arr, dp);
    bool pick = false;
    if (arr[idx] <= target)
        pick = solve(idx - 1, target - arr[idx], arr, dp);
    return dp[idx][target] = pick || notPick;
}

bool equalPartitionMemo(int n, vector<int> arr) {
    int target = accumulate(arr.begin(), arr.end(), 0);
    if (target % 2) return false;
    vector<vector<int>> dp(n, vector<int>(target/2 + 1, -1));
    return solve(n-1, target/2, arr, dp);
}

bool equalPartitionTab(int n, vector<int> arr) {
    int target = accumulate(arr.begin(), arr.end(), 0);
    if (target % 2) return false;
    int k = target / 2;
    vector<vector<int>> dp(n, vector<int>(k + 1, 0));
    for (int i = 0; i < n; i++) {
        dp[i][0] = true;
    }
    if (arr[0] <= k) {
        dp[0][arr[0]] = true;
    }

    for (int idx = 1; idx < n; idx++) {
        for (int val = 1; val <= k; val++) {
            bool notPick = dp[idx - 1][val];
            bool pick = false;
            if (arr[idx] <= val)
                pick = dp[idx - 1][val - arr[idx]];
            dp[idx][val] = pick || notPick;
        }
    }
    return dp[n-1][k];
}

bool equalPartitionConstant(int n, vector<int> arr) {
    int target = accumulate(arr.begin(), arr.end(), 0);
    if (target % 2) return false;
    int k = target / 2;
    vector<int> prev(k + 1, 0);
    vector<int> curr(k + 1, 0);

    prev[0] = true;
    curr[0] = true;
    
    if (arr[0] <= k) {
        prev[arr[0]] = true;
    }

    for (int idx = 1; idx < n; idx++) {
        for (int val = 1; val <= k; val++) {
            bool notPick = prev[val];
            bool pick = false;
            if (arr[idx] <= val)
                pick = prev[val - arr[idx]];
            curr[val] = pick || notPick;
        }
        prev = curr;
    }
    return prev[k];
}

bool equalPartition(int n, vector<int> arr) {
    // return equalPartitionMemo(n, arr);
    // return equalPartitionTab(n, arr);
    return equalPartitionConstant(n, arr);
}
```

### Partition a set into two subsets with minimum absolute sum difference
Given an array arr of n integers, partition the array into two subsets such that the absolute difference between their sums is minimized.

```cpp
	bool solve(int idx, int target, vector<int>& arr,  vector<vector<int>>& dp) {
    if (target == 0)	return true;
    if (idx == 0)	return arr[0] == target;
    if (dp[idx][target] != -1)	return dp[idx][target];

    bool notPick = solve(idx - 1, target, arr, dp);

    bool pick = false;
    if (arr[idx] <= target)
        pick = solve(idx - 1, target - arr[idx], arr, dp);

    return dp[idx][target] = pick || notPick;
}

int minDifferenceMemo(vector<int>& arr, int n) {
    int total = accumulate(arr.begin(), arr.end(), 0);
    vector<vector<int>> dp(n, vector<int>(total + 1, -1));
    solve(n - 1, total, arr, dp);
    int mini = INT_MAX;
    for (int s1 = 0; s1 <= total / 2; s1++) {
        if (dp[n-1][s1]) {
            int s2 = total - s1;
            mini = min(mini, abs(s1 - s2));
        }
    }
    return mini;
}

int minDifferenceTab(vector<int>& arr, int n) {
    int total = accumulate(arr.begin(), arr.end(), 0);
    vector<vector<int>> dp(n, vector<int>(total + 1, 0));

    for (int i = 0; i < n; i++)	dp[i][0] = true;

    if (arr[0] <= total)	dp[0][arr[0]] = true;

    for (int idx = 1; idx < n; idx++) {
        for (int target = 0; target <= total; target++) {
            bool notPick = dp[idx - 1][target];

            bool pick = false;
            if (arr[idx] <= target)
                pick = dp[idx - 1][target - arr[idx]];

            dp[idx][target] = pick || notPick;
        }
    }

    int mini = INT_MAX;
    for (int s1 = 0; s1 <= total / 2; s1++) {
        if (dp[n-1][s1]) {
            int s2 = total - s1;
            mini = min(mini, abs(s1 - s2));
        }
    }
    return mini;
}

int minDifferenceConstant(vector<int>& arr, int n) {
    int total = accumulate(arr.begin(), arr.end(), 0);
    vector<int> prev(total + 1, 0), curr(total + 1, 0);

    prev[0] = curr[0] = true;

    if (arr[0] <= total)	prev[arr[0]] = true;

    for (int idx = 1; idx < n; idx++) {
        for (int target = 0; target <= total; target++) {
            bool notPick = prev[target];

            bool pick = false;
            if (arr[idx] <= target)
                pick = prev[target - arr[idx]];

            curr[target] = pick || notPick;
        }
        prev = curr;
    }

    int mini = INT_MAX;
    for (int s1 = 0; s1 <= total / 2; s1++) {
        if (prev[s1]) {
            int s2 = total - s1;
            mini = min(mini, abs(s1 - s2));
        }
    }
    return mini;
}

int minDifference(vector<int>& arr, int n) {
    // return minDifferenceMemo(arr, n);
    // return minDifferenceTab(arr, n);
    return minDifferenceConstant(arr, n);
}
```

### Count subsets with sum K
Given an array arr of n integers and an integer K, count the number of subsets of the given array that have a sum equal to K. Return the result modulo (10^9 + 7).
>Input: arr = [2, 3, 5, 16, 8, 10], K = 10
>Output: 3
>Explanation: The subsets are [2, 8], [10], and [2, 3, 5].
```cpp
int MOD = 1e9 + 7;
int solve(int idx, int target, vector<int>&arr, vector<vector<int>> &dp) {
    if (target == 0)	return 1;
    if (idx == 0)	return arr[0] == target;
    if (dp[idx][target] != -1)	return dp[idx][target];
    int notPick = solve(idx - 1, target, arr, dp);
    int pick = 0;
    if (arr[idx] <= target)
        pick = solve(idx - 1, target - arr[idx], arr, dp);
    return dp[idx][target] = (pick + notPick) % MOD;
}

int perfectSumMemo(vector<int>&arr, int K){
    int n = arr.size();
    vector<vector<int>> dp(n, vector<int>(K + 1, -1));
    return solve(n-1, K, arr, dp);
}

int perfectSumTab(vector<int>&arr, int K) {
    int n = arr.size();
    vector<vector<int>> dp(n, vector<int>(K + 1, 0));
    for (int i = 0; i < n; i++)	dp[i][0] = 1;
    if (arr[0] <= K)	dp[0][arr[0]] = 1;

    for (int idx = 1; idx < n; idx++) {
        for (int target = 0; target <= K; target++) {
            int notPick = dp[idx-1][target];
            int pick = 0;
            if (arr[idx] <= target)
                pick = dp[idx-1][target-arr[idx]];
            dp[idx][target] = (pick + notPick) % MOD;
        }
    }

    return dp[n-1][K];
}

int perfectSumConstant(vector<int>&arr, int K) {
    int n = arr.size();
    vector<int> prev(K + 1, 0), curr(K + 1, 0);
    prev[0] = curr[0] = 1;
    if (arr[0] <= K)	prev[arr[0]] = 1;

    for (int idx = 1; idx < n; idx++) {
        for (int target = 0; target <= K; target++) {
            int notPick = prev[target];
            int pick = 0;
            if (arr[idx] <= target)
                pick = prev[target-arr[idx]];
            curr[target] = (pick + notPick) % MOD;
        }
        prev = curr;
    }

    return prev[K];
}

int perfectSum(vector<int>&arr, int K){
    // return perfectSumMemo(arr, K);
    // return perfectSumTab(arr, K);
    return perfectSumConstant(arr, K);
}
```