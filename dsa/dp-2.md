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

### Count partitions with given difference
Given an array arr of n integers and an integer diff, count the number of ways to partition the array into two subsets S1 and S2 such that: 
∣S1−S2∣ = diff and S1 ≥ S2
Where |S1| and |S2| are sum of Subsets S1 and S2 respectively.

Return the result modulo 109 + 7.

Note: A partition means that the union of S1 and S2 is the original array, and no element is left out or used twice — every element of the array belongs to exactly one of the two subsets.

> “Count Partitions with a difference D” is equivalent to “Count Number of subsets with sum (totSum - D)/2 ”.
```cpp
int MOD = (int)1e9 + 7;
public:

int solve(int idx, int target, vector<int>& arr, vector<vector<int>>& dp) {
    if (idx == 0) {
        if (target == 0 && arr[0] == 0) return 2;
        if (target == 0 || target == arr[0])  return 1;
        return 0;
    }

    if (dp[idx][target] != -1)  return dp[idx][target];
    int notPick = solve(idx-1, target, arr, dp);
    int pick = 0;
    if (arr[idx] <= target)
        pick = solve(idx-1, target-arr[idx], arr, dp);
    return dp[idx][target] = (pick + notPick) % MOD;
}

int countPartitionsMemo(int n, int diff, vector<int>& arr) {
    int totSum = 0;
    for (auto i: arr) totSum += i;
    if (totSum < diff)  return 0;
    if ((totSum - diff) % 2)  return 0;
    int s2 = (totSum - diff) / 2;
    vector<vector<int>> dp(n, vector<int>(s2 + 1, -1));
    return solve(n-1, s2, arr, dp);
}

int countPartitionsTab(int n, int diff, vector<int>& arr) {
    int totSum = 0;
    for (auto i: arr) totSum += i;
    if (totSum < diff)  return 0;
    if ((totSum - diff) % 2)  return 0;
    int k = (totSum - diff) / 2;
    vector<vector<int>> dp(n, vector<int>(k + 1, 0));

    // 2 ways if we include, 1 way if we exclude
    if (arr[0] == 0)  dp[0][0] = 2;
    else dp[0][0] = 1;

    // usual check if elem <= target then we can have 1 way
    if (arr[0] != 0 && arr[0] <= k)  dp[0][arr[0]] = 1;

    for (int idx = 1; idx < n; idx++) {
        for (int target = 0; target <= k; target++) {
            int notPick = dp[idx - 1][target];
            int pick = 0;
            if (arr[idx] <= target) {
                pick = dp[idx - 1][target - arr[idx]];
            }
            dp[idx][target] = (pick + notPick) % MOD;
        }
    }
    return dp[n-1][k];
}

int countPartitionsConstant(int n, int diff, vector<int>& arr) {
    int totSum = 0;
    for (auto i: arr) totSum += i;
    if (totSum < diff)  return 0;
    if ((totSum - diff) % 2)  return 0;
    int k = (totSum - diff) / 2;
    vector<int> prev(k + 1, 0), curr(k + 1, 0);

    // 2 ways if we include, 1 way if we exclude
    if (arr[0] == 0)  {
        prev[0] = 2;
        // curr[0] = 2; this is not required since we run target from 0 to k
        // unlike other problems where it's from 1 to k
    } else {
        prev[0] = 1;
        // curr[0] = 1; this is not required since we run target from 0 to k,
        // unlike other problems where it's from 1 to k
    }

    // usual check if elem <= target then we can have 1 way
    if (arr[0] != 0 && arr[0] <= k)  prev[arr[0]] = 1;

    for (int idx = 1; idx < n; idx++) {
        for (int target = 0; target <= k; target++) {
            int notPick = prev[target];
            int pick = 0;
            if (arr[idx] <= target) {
                pick = prev[target - arr[idx]];
            }
            curr[target] = (pick + notPick) % MOD;
        }
        prev = curr;
    }
    return prev[k];
}

int countPartitions(int n, int diff, vector<int>& arr) {
    // return countPartitionsMemo(n, diff, arr);
    // return countPartitionsTab(n, diff, arr);
    return countPartitionsConstant(n, diff, arr);
}
```

### 0 and 1 Knapsack

Given two integer arrays, val and wt, each of size N, which represent the values and weights of N items respectively, and an integer W representing the maximum capacity of a knapsack, determine the maximum value achievable by selecting a subset of the items such that the total weight of the selected items does not exceed the knapsack capacity W.

Each item can either be picked in its entirety or not picked at all (0-1 property). The goal is to maximize the sum of the values of the selected items while keeping the total weight within the knapsack's capacity.

```cpp
int solve(int idx, int W, vector<int>&wt, vector<int>&val, vector<vector<int>> &dp) {
    if (W == 0) return 0;
    if (idx == 0) {
        if (wt[0] <= W) return val[0];
        else return 0;
    }

    if (dp[idx][W] != -1)   return dp[idx][W];

    int notPick = 0 + solve(idx - 1, W, wt, val, dp);
    int pick = 0;
    if (wt[idx] <= W)
        pick = val[idx] + solve(idx - 1, W - wt[idx], wt, val, dp);
    
    return dp[idx][W] = max(pick, notPick);
}

int knapsack01Memo(vector<int>& wt, vector<int>& val, int n, int W) {
    vector<vector<int>> dp(n, vector<int>(W + 1, -1));
    return solve(n-1, W, wt, val, dp);
}

int knapsack01Tab(vector<int>& wt, vector<int>& val, int n, int W) {
    vector<vector<int>> dp(n, vector<int>(W + 1, 0));

    for (int i = wt[0]; i <= W; i++) dp[0][i] = val[0];

    for (int idx = 1; idx < n; idx++) {
        for (int w = 0; w <= W; w++) {
            int notPick = 0 + dp[idx - 1][w];
            int pick = 0;
            if (wt[idx] <= w)
                pick = val[idx] + dp[idx - 1][w - wt[idx]];
            dp[idx][w] = max(pick, notPick);   
        }
    }

    return dp[n-1][W];
}

int knapsack01Const(vector<int>& wt, vector<int>& val, int n, int W) {
    vector<int> prev(W + 1, 0), curr(W + 1, 0);

    for (int i = wt[0]; i <= W; i++) prev[i] = val[0];

    for (int idx = 1; idx < n; idx++) {
        for (int w = 0; w <= W; w++) {
            int notPick = 0 + prev[w];
            int pick = 0;
            if (wt[idx] <= w)
                pick = val[idx] + prev[w - wt[idx]];
            curr[w] = max(pick, notPick);   
        }
        prev = curr;
    }

    return prev[W];
}

int knapsack01(vector<int>& wt, vector<int>& val, int n, int W) {
    // return knapsack01Memo(wt, val, n, W);
    // return knapsack01Tab(wt, val, n, W);
    return knapsack01Const(wt, val, n, W);
}
```

### Minimum coins
Given an integer array of coins representing coins of different denominations and an integer amount representing a total amount of money. Return the fewest number of coins that are needed to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1. There are infinite numbers of coins of each type

```cpp
int solve(int idx, vector<int>& coins, int amount, vector<vector<int>> &dp) {
    if (amount == 0)	return 0;
    if (idx == 0) {
        if (amount % coins[0] == 0) return amount/coins[0];
        else return 1e9;
    }
    if (dp[idx][amount] != -1)  return dp[idx][amount];

    int notPick = 0 + solve(idx-1, coins, amount, dp);

    int pick = 1e9;
    if (coins[idx] <= amount)
        // we are not decrementing idx in below step as we can choose infinite no. of coins
        pick = 1 + solve(idx, coins, amount-coins[idx], dp);

    return dp[idx][amount] = min(pick, notPick);
}

int MinimumCoinsMemo(vector<int>& coins, int amount) {
    int n = coins.size();
    vector<vector<int>> dp(n, vector<int> (amount + 1, -1));
    int res = solve(n-1, coins, amount, dp);
    return res >= 1e9 ? -1 : res;
}

int MinimumCoinsTab(vector<int>& coins, int amount) {
    int n = coins.size();
    vector<vector<int>> dp(n, vector<int> (amount+1, 0));
    for (int i=0; i <= amount; i++) {
        dp[0][i] = i % coins[0] == 0 ? i/coins[0] : 1e9;
    }
    for (int idx = 1; idx < n; idx++) {
        for (int amt = 0; amt <= amount; amt++) {
            int notPick = 0 + dp[idx-1][amt];

            int pick = 1e9;
            if (coins[idx] <= amt)
                pick = 1 + dp[idx][amt-coins[idx]];
            dp[idx][amt] = min(pick, notPick);
        }
    }
    return dp[n-1][amount] >= 1e9 ? -1 : dp[n-1][amount];
}

int MinimumCoinsConstant(vector<int>& coins, int amount) {
    int n = coins.size();
    vector<int> prev(amount+1, 0), curr(amount+1, 0);
    for (int i=0; i<=amount; i++) {
        prev[i] = i % coins[0] == 0 ? i/coins[0] : 1e9;
    }
    for (int idx = 1; idx < n; idx++) {
        for (int amt = 0; amt <= amount; amt++) {
            int notPick = 0 + prev[amt];

            int pick = 1e9;
            if (coins[idx] <= amt)
                pick = 1 + curr[amt-coins[idx]];
            curr[amt] = min(pick, notPick);
        }
        prev = curr;
    }
    return prev[amount] >= 1e9 ? -1 : prev[amount];
}

int MinimumCoins(vector<int>& coins, int amount) {
    // return MinimumCoinsMemo(coins, amount);
    // return MinimumCoinsTab(coins, amount);
    return MinimumCoinsConstant(coins, amount);
}
```

### Target Sum
Given an array nums of n integers and an integer target, build an expression using the integers from nums where each integer can be prefixed with either a '+' or '-' sign.

The goal is to achieve the target sum by evaluating all possible combinations of these signs.

Determine the number of ways to achieve the target sum and return your answer with modulo 109+7.

```cpp
    int MOD = (int)1e9 + 7;

    public:
    int solve(int idx, int target, vector<int>& arr, vector<vector<int>>& dp) {
        if (idx == 0) {
            if (target == 0 && arr[0] == 0) return 2;
            if (target == 0 || target == arr[0]) return 1;
            return 0;
        }
        if (dp[idx][target] != -1) return dp[idx][target];
        int notPick = solve(idx - 1, target, arr, dp);
        int pick = 0;
        if (arr[idx] <= target)
            pick = solve(idx - 1, target - arr[idx], arr, dp);
        return dp[idx][target] = (pick + notPick) % MOD;
    }

    int countPartitionsMemo(int n, int diff, vector<int>& arr) {
        int totSum = 0;
        for (auto i : arr) totSum += i;
        if (totSum < diff) return 0;
        if ((totSum - diff) % 2) return 0;
        int s2 = (totSum - diff) / 2;
        vector<vector<int>> dp(n, vector<int>(s2 + 1, -1));
        return solve(n - 1, s2, arr, dp);
    }

    int countPartitionsTab(int n, int diff, vector<int>& arr) {
        int totSum = 0;
        for (auto i : arr) totSum += i;
        if (totSum < diff) return 0;
        if ((totSum - diff) % 2) return 0;
        int k = (totSum - diff) / 2;
        vector<vector<int>> dp(n, vector<int>(k + 1, 0));

        // 2 ways if we include, 1 way if we exclude
        if (arr[0] == 0)
            dp[0][0] = 2;
        else
            dp[0][0] = 1;

        // usual check if elem <= target then we can have 1 way
        if (arr[0] != 0 && arr[0] <= k) dp[0][arr[0]] = 1;

        for (int idx = 1; idx < n; idx++) {
            for (int target = 0; target <= k; target++) {
                int notPick = dp[idx - 1][target];
                int pick = 0;
                if (arr[idx] <= target) {
                    pick = dp[idx - 1][target - arr[idx]];
                }
                dp[idx][target] = (pick + notPick) % MOD;
            }
        }
        return dp[n - 1][k];
    }

    int countPartitionsConstant(int n, int diff, vector<int>& arr) {
        int totSum = 0;
        for (auto i : arr) totSum += i;
        if (totSum < diff) return 0;
        if ((totSum - diff) % 2) return 0;
        int k = (totSum - diff) / 2;
        vector<int> prev(k + 1, 0), curr(k + 1, 0);

        // 2 ways if we include, 1 way if we exclude
        if (arr[0] == 0) {
            prev[0] = 2;
            // curr[0] = 2; this is not required since we run target from 0 to k
            // unlike other problems where it's from 1 to k
        } else {
            prev[0] = 1;
            // curr[0] = 1; this is not required since we run target from 0 to
            // k, unlike other problems where it's from 1 to k
        }

        // usual check if elem <= target then we can have 1 way
        if (arr[0] != 0 && arr[0] <= k) prev[arr[0]] = 1;

        for (int idx = 1; idx < n; idx++) {
            for (int target = 0; target <= k; target++) {
                int notPick = prev[target];
                int pick = 0;
                if (arr[idx] <= target) {
                    pick = prev[target - arr[idx]];
                }
                curr[target] = (pick + notPick) % MOD;
            }
            prev = curr;
        }
        return prev[k];
    }

    int targetSum(int n, int target, vector<int>& nums) {
        // return countPartitionsMemo(n, target, nums);
        // return countPartitionsTab(n, target, nums);
        return countPartitionsConstant(n, target, nums);
    }
```

### Coin Change ii
Give an array coins of n integers representing coin denominations. Your task is to find the number of distinct combinations that sum up to a specified amount of money. If it's impossible to achieve the exact amount with any combination of coins, return 0.

Single coin can be used any number of times.

Return your answer with modulo 109+7.

```cpp
    int MOD = 1e9 + 7;
    int solve(int idx, vector<int>&coins, int N, int amount, vector<vector<int>> &dp) {
        if (idx == 0) {
            if (amount % coins[0] == 0)
                return 1;
            else
                return 0;
        }
        if (dp[idx][amount] != -1)  return dp[idx][amount];

        int notPick = solve(idx - 1, coins, N, amount, dp) % MOD;
        int pick = 0;
        if (coins[idx] <= amount)
            pick = solve(idx, coins, N, amount-coins[idx], dp) % MOD;

        return dp[idx][amount] = (pick + notPick) % MOD;
    }

    int countMemo(vector<int>&coins, int N, int amount) {
        vector<vector<int>> dp(N, vector<int>(amount + 1, -1));
        return solve(N-1, coins, N, amount, dp);
    }

    int countTab(vector<int>&coins, int N, int amount) {
        vector<vector<int>> dp(N, vector<int>(amount + 1, 0));

        for (int i=0; i <= amount; i++) {
            dp[0][i] = i % coins[0] == 0;
        }

        for (int idx = 1; idx < N; idx++) {
            for (int amt = 0; amt <= amount; amt++) {
                int notPick =  dp[idx - 1][amt] % MOD;
                int pick = 0;
                if (coins[idx] <= amt)
                    pick = dp[idx][amt-coins[idx]] % MOD;

                dp[idx][amt] = (pick + notPick) % MOD;
            }
        }

        return dp[N-1][amount];
    }

    int countConstant(vector<int>&coins, int N, int amount) {
        vector<int> prev(amount + 1, 0), curr(amount + 1, 0);

        for (int i=0; i <= amount; i++) {
            prev[i] = i % coins[0] == 0;
        }

        for (int idx = 1; idx < N; idx++) {
            for (int amt = 0; amt <= amount; amt++) {
                int notPick =  prev[amt] % MOD;
                int pick = 0;
                if (coins[idx] <= amt)
                    pick = curr[amt-coins[idx]] % MOD;

                curr[amt] = (pick + notPick) % MOD;
            }
            prev = curr;
        }

        return prev[amount];
    }

    int count(vector<int>&coins, int N, int amount) {
        // return countMemo(coins, N, amount);
        // return countTab(coins, N, amount);
        return countConstant(coins, N, amount);
    }
```

### Unbounded Knapsack

Given two integer arrays, val and wt, each of size N, representing the values and weights of N items respectively, and an integer W, representing the maximum capacity of a knapsack, determine the maximum value achievable by selecting a subset of the items such that the total weight of the selected items does not exceed the knapsack capacity W. The goal is to maximize the sum of the values of the selected items while keeping the total weight within the knapsack's capacity.

An infinite supply of each item can be assumed.

```cpp
    int solve(int idx, vector<int>& wt, vector<int>& val, int n, int W, vector<vector<int>> &dp) {
        if (idx == 0) {
            if (wt[0] <= W)
                return val[0] * (W / wt[0]);
            else
                return INT_MIN;
        }

        if (dp[idx][W] != -1) return dp[idx][W];

        int notPick = solve(idx-1, wt, val, n, W, dp);
        
        int pick = 0;
        if (wt[idx] <= W)
            pick = val[idx] + solve(idx, wt, val, n, W-wt[idx], dp);
        
        return dp[idx][W] = max(pick, notPick);
    }

    int unboundedKnapsackMemo(vector<int>& wt, vector<int>& val, int n, int W) {
        vector<vector<int>> dp(n, vector<int> (W+1, -1));
        return solve(n-1, wt, val, n, W, dp);
    }

    int unboundedKnapsackTab(vector<int>& wt, vector<int>& val, int n, int W) {
        vector<vector<int>> dp(n, vector<int> (W+1, 0));

        for (int w = 0; w <= W; w++) {
            dp[0][w] = wt[0] <= w ? val[0] * (w / wt[0]) : INT_MIN;
        }
        
        for (int idx=1; idx<n; idx++) {
            for (int w = 1; w <= W; w++) {
                int notPick = dp[idx-1][w];
                int pick = 0;
                if (wt[idx] <= w)
                    pick = val[idx] + dp[idx][w-wt[idx]];
                dp[idx][w] = max(pick, notPick);
            }
        }

        return dp[n-1][W];
    }

    int unboundedKnapsackConstant(vector<int>& wt, vector<int>& val, int n, int W) {
        vector<int> prev(W+1, 0), curr(W+1, 0);

        for (int w = 0; w <= W; w++) {
            prev[w] = wt[0] <= w ? val[0] * (w / wt[0]) : INT_MIN;
        }
        
        for (int idx=1; idx<n; idx++) {
            for (int w = 1; w <= W; w++) {
                int notPick = prev[w];
                int pick = 0;
                if (wt[idx] <= w)
                pick = val[idx] + curr[w-wt[idx]];
                curr[w] = max(pick, notPick);
            }
            prev = curr;
        }

        return prev[W];
    }

    int unboundedKnapsack(vector<int>& wt, vector<int>& val, int n, int W) {
        // return unboundedKnapsackMemo(wt, val, n, W);
        // return unboundedKnapsackTab(wt, val, n, W);
        return unboundedKnapsackConstant(wt, val, n, W);
    }
```

### Rod cutting problem

Given a rod of length N inches and an array price[] where price[i] denotes the value of a piece of rod of length i inches (1-based indexing). Determine the maximum value obtainable by cutting up the rod and selling the pieces. Make any number of cuts, or none at all, and sell the resulting pieces.

```cpp
int solve(int idx, vector<int> price, int n, vector<vector<int>> &dp) {
    if (idx == 0) {
        return price[0]*n;
    }
    if (dp[idx][n] != -1) return dp[idx][n];
    int notPick = 0 + solve(idx - 1, price, n, dp);
    int pick = INT_MIN;
    int rodLength = idx + 1;
    if (rodLength <= n) {
        pick = price[idx] + solve(idx, price, n-rodLength, dp);
    }
    return dp[idx][n] = max(pick, notPick);
}

int rodCuttingMemo(vector<int> price, int n) {
    vector<vector<int>> dp(n, vector<int>(n+1, -1));
    return solve(n-1, price, n, dp);
}

int rodCuttingTab(vector<int> price, int n) {
    vector<vector<int>> dp(n, vector<int>(n + 1, 0));

    for (int i=0; i<=n; i++) {
        dp[0][i] = price[0]*i;
    }
    
    for (int idx=1; idx<n; idx++) {
        for (int len = 1; len <= n; len++) {
            int notPick = 0 + dp[idx - 1][len];
            int pick = INT_MIN;
            int rodLength = idx + 1;
            if (rodLength <= len) {
                pick = price[idx] + dp[idx][len-rodLength];
            }
            dp[idx][len] = max(pick, notPick);
        }
    }

    return dp[n-1][n];
}

int rodCuttingConstant(vector<int> price, int n) {
    vector<int> prev(n + 1, 0), curr(n + 1, 0);

    for (int i=0; i<=n; i++) {
        prev[i] = price[0]*i;
    }
    
    for (int idx=1; idx<n; idx++) {
        for (int len = 1; len <= n; len++) {
            int notPick = 0 + prev[len];
            int pick = INT_MIN;
            int rodLength = idx + 1;
            if (rodLength <= len) {
                pick = price[idx] + curr[len-rodLength];
            }
            curr[len] = max(pick, notPick);
        }
        prev = curr;
    }

    return prev[n];
}

int rodCutting(vector<int> price, int n) {
    // return rodCuttingMemo(price, n);
    // return rodCuttingTab(price, n);
    return rodCuttingConstant(price, n);
}
```

## LIS

### Longest Increasing Subsequence
Given an integer array nums, return the length of the longest strictly increasing subsequence.

A subsequence is a sequence derived from an array by deleting some or no elements without changing the order of the remaining elements. For example, [3, 6, 2, 7] is a subsequence of [0, 3, 1, 6, 2, 2, 7].

The task is to find the length of the longest subsequence in which every element is greater than the previous one.

```cpp
int solve(int idx, int prevIdx, vector<int> &nums, vector<vector<int>> &dp) {
    if (idx == nums.size() - 1) {
        if (prevIdx == -1 || nums[prevIdx] < nums[idx])   return 1;
        return 0;
    }
    // prevIdx + 1 in the below line is for index shift as mem can't have -ve idx
    if (dp[idx][prevIdx + 1] != -1) return dp[idx][prevIdx + 1];

    int notPick = solve(idx + 1, prevIdx, nums, dp);
    int pick = 0;
    if (prevIdx == -1 || nums[idx] > nums[prevIdx])
        pick = 1 + solve(idx + 1, idx, nums, dp);

    return dp[idx][prevIdx + 1] = max(pick, notPick);
}

int LISMemo(vector<int>& nums) {
    int n = nums.size();
    vector<vector<int>> dp(n, vector<int>(n + 1, -1));
    return solve(0, -1, nums, dp);
}

int LISTab(vector<int>& nums) {
    int n = nums.size();
    vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));

    for (int idx = n - 1; idx >= 0; idx--) {
        for (int prevIdx = idx - 1; prevIdx >= -1; prevIdx--) {
            int notPick = dp[idx + 1][prevIdx + 1];
            int pick = 0;
            if (prevIdx == -1 || nums[idx] > nums[prevIdx]) {
                pick = 1 + dp[idx + 1][idx + 1];
            }
            dp[idx][prevIdx + 1] = max(pick, notPick);
        }
    }

    return dp[0][0];
}

int LISConstant(vector<int>& nums) {
    int n = nums.size();
    vector<int> curr(n + 1, 0), ahead(n + 1, 0);

    for (int idx = n - 1; idx >= 0; idx--) {
        for (int prevIdx = idx - 1; prevIdx >= -1; prevIdx--) {
            int notPick = ahead[prevIdx + 1];
            int pick = 0;
            if (prevIdx == -1 || nums[idx] > nums[prevIdx]) {
                pick = 1 + ahead[idx + 1];
            }
            curr[prevIdx + 1] = max(pick, notPick);
        }
        ahead = curr;
    }

    return ahead[0];
}

int LIS_BinarySearch(vector<int> &nums) {
    int n = nums.size();
    
    // temp[i] will store the smallest possible tail value
    // of an increasing subsequence of length (i + 1).
    // IMPORTANT: temp is NOT the actual LIS.
    vector<int> temp;

    temp.push_back(nums[0]);

    for (int idx = 1; idx < n; idx++) {

        // If current element is greater than the last element in temp,
        // it can extend the longest subsequence found so far.
        if (nums[idx] > temp.back()) {
            temp.push_back(nums[idx]);
        } 
        else {
            // For STRICTLY INCREASING subsequence:
            // Use lower_bound → first element >= nums[idx]
            //
            // For NON-DECREASING subsequence:
            // Use upper_bound → first element > nums[idx]
            //
            // Why?
            // - lower_bound prevents duplicates from extending length.
            // - upper_bound allows equal values to extend length.
            int i = lower_bound(temp.begin(), temp.end(), nums[idx]) - temp.begin();

            // Replacement logic:
            // We replace temp[i] with nums[idx] because:
            //
            // temp[i] represents the smallest tail of a subsequence of length i+1.
            //
            // If nums[idx] is smaller than temp[i],
            // replacing it keeps the subsequence length same,
            // but improves (lowers) the tail value.
            //
            // Smaller tail → more chance to extend subsequence later.
            //
            // This greedy replacement is the core reason
            // the algorithm works in O(n log n).
            temp[i] = nums[idx];
        }
    }

    // Length of LIS
    return temp.size();
}

int LIS(vector<int>& nums) {
    // return LISMemo(nums);
    // return LISTab(nums);
    // return LISConstant(nums);
    return LIST_BinarySearch(nums);
}
```

### Print Longest Increasing Subsequence

```cpp
vector<int> longestIncreasingSubsequence(vector<int>& nums) {
    int n = nums.size();
    if (n == 0) return {};

    // dp[i] = length of LIS ending exactly at index i
    vector<int> dp(n, 1);

    // parent[i] = previous index in LIS chain
    // used later for reconstruction
    vector<int> parent(n, -1);

    int maxLength = 1;  // overall maximum LIS length
    int lastIndex = 0;  // index where LIS ends

    // Build DP table
    for (int idx = 0; idx < n; idx++) {
        // Try to extend subsequence from all previous elements
        for (int prev = 0; prev < idx; prev++) {
            // Strictly increasing condition
            if (nums[prev] < nums[idx]) {
                // If extending gives a longer subsequence
                if (dp[prev] + 1 > dp[idx]) {
                    dp[idx] = dp[prev] + 1;
                    parent[idx] = prev;  // remember the chain
                }
            }
        }

        // Keep track of the global best LIS
        if (dp[idx] > maxLength) {
            maxLength = dp[idx];
            lastIndex = idx;
        }
    }

    // Reconstruct LIS using parent array
    vector<int> lis;

    while (lastIndex != -1) {
        lis.push_back(nums[lastIndex]);
        lastIndex = parent[lastIndex];
    }

    reverse(lis.begin(), lis.end());
    return lis;
}
```

### Largest Divisible Subset
Given an array nums of positive integers, the task is to find the largest subset such that every pair (a, b) of elements in the subset satisfies a % b == 0 or b % a == 0.
Return the subset in any order. If there are multiple solutions, return any one of them.

```cpp
vector<int> largestDivisibleSubset(vector<int>& nums) {
    int n = nums.size();
    if (n == 0) return {};

    // Step 1: Sort the array
    // Sorting ensures that if nums[i] % nums[j] == 0,
    // then nums[i] >= nums[j], which guarantees valid chaining.
    sort(nums.begin(), nums.end());

    // dp[i] = size of largest divisible subset ending at index i
    vector<int> dp(n, 1);

    // parent[i] = previous index in the subset chain
    vector<int> parent(n, -1);

    int maxLength = 1;  // overall maximum subset size
    int lastIndex = 0;  // index where largest subset ends

    for (int idx = 0; idx < n; idx++) {
        // Check all previous elements
        for (int prev = 0; prev < idx; prev++) {
            // If nums[i] is divisible by nums[j],
            // then nums[i] can extend the subset ending at j.
            if (nums[idx] % nums[prev] == 0) {
                // Only update if this gives a longer subset
                if (dp[prev] + 1 > dp[idx]) {
                    dp[idx] = dp[prev] + 1;
                    parent[idx] = prev;  // remember the chain
                }
            }
        }

        // Track the index of the overall largest subset
        if (dp[idx] > maxLength) {
            maxLength = dp[idx];
            lastIndex = idx;
        }
    }

    // Step 2: Reconstruct subset using parent array
    vector<int> subset;

    while (lastIndex != -1) {
        subset.push_back(nums[lastIndex]);
        lastIndex = parent[lastIndex];
    }

    reverse(subset.begin(), subset.end());
    return subset;
}
```

### Longest String Chain
You are given an array of words where each word consists of lowercase English letters.

wordA is a predecessor of wordB if and only if we can insert exactly one letter anywhere in wordA without changing the order of the other characters to make it equal to wordB.

> For example, "abc" is a predecessor of "abac", while "cba" is not a predecessor of "bcad".
> A word chain is a sequence of words [word1, word2, ..., wordk] with k >= 1, where word1 is a predecessor of word2, word2 is a predecessor of word3, and so on. A single word is trivially a word chain with k == 1.

Return the length of the longest possible word chain with words chosen from the given list of words.

>Input: words = ["a", "ab", "abc", "abcd", "abcde"]
>Output: 5
>Explanation: The longest chain is ["a", "ab", "abc", "abcd", "abcde"].
>Each word in the chain is formed by adding exactly one character to the previous word.

```cpp
class Solution {
private:
    // Sort words by increasing length
    // We must process shorter words first,
    // because a word can only extend from a shorter word.
    static bool compare(string &s, string &t) {
        return s.size() < t.size();
    }

public:

    // Check if 't' is a predecessor of 's'
    // Meaning: we can insert exactly one character into 't' to get 's'
    bool isPossible(string &s, string &t) {

        // Length must differ by exactly 1
        if (s.size() != t.size() + 1)
            return false;

        int i = 0, j = 0;

        // Two pointer check
        while (i < s.size()) {

            if (j < t.size() && s[i] == t[j]) {
                i++;
                j++;
            } 
            else {
                // Skip one extra character in s
                i++;
            }
        }

        // Valid only if we matched all characters of t
        return (j == t.size());
    }

    int longestStringChain(vector<string>& words) {

        int n = words.size();
        if (n == 0) return 0;

        // Step 1: Sort by length (like sorting in divisible subset)
        sort(words.begin(), words.end(), compare);

        // dp[idx] = longest chain ending at index idx
        vector<int> dp(n, 1);

        int maxLength = 1;

        // Build DP (exact same structure as LIS)
        for (int idx = 0; idx < n; idx++) {

            for (int prev = 0; prev < idx; prev++) {

                // If words[prev] can form words[idx]
                if (isPossible(words[idx], words[prev]) &&
                    dp[prev] + 1 > dp[idx]) {

                    dp[idx] = dp[prev] + 1;
                }
            }

            // Track global maximum chain
            maxLength = max(maxLength, dp[idx]);
        }

        return maxLength;
    }
};
```

### Longest Bitonic Subsequence
Given an array arr of n integers, the task is to find the length of the longest bitonic sequence. A sequence is considered bitonic if it first increases, then decreases. The sequence does not have to be contiguous.
```cpp
class Solution {
public:
    int LongestBitonicSequence(vector<int>& nums) {

        int n = nums.size();
        if (n == 0) return 0;

        // -------------------------------
        // Step 1: Compute LIS from left
        // lis[idx] = length of longest increasing subsequence ending at idx
        // -------------------------------
        vector<int> lis(n, 1);

        for (int idx = 0; idx < n; idx++) {
            for (int prev = 0; prev < idx; prev++) {

                if (nums[prev] < nums[idx] &&
                    lis[prev] + 1 > lis[idx]) {

                    lis[idx] = lis[prev] + 1;
                }
            }
        }

        // -------------------------------
        // Step 2: Compute LDS from right
        // lds[idx] = length of longest decreasing subsequence starting at idx
        // -------------------------------
        vector<int> lds(n, 1);

        for (int idx = n - 1; idx >= 0; idx--) {
            for (int prev = n - 1; prev > idx; prev--) {

                if (nums[prev] < nums[idx] &&
                    lds[prev] + 1 > lds[idx]) {

                    lds[idx] = lds[prev] + 1;
                }
            }
        }

        // -------------------------------
        // Step 3: Combine LIS + LDS
        //
        // IMPORTANT:
        // GFG definition of Bitonic Subsequence allows:
        //   - Purely increasing
        //   - Purely decreasing
        //   - Increasing then decreasing
        //
        // So we DO NOT enforce:
        //   lis[idx] > 1 && lds[idx] > 1
        //
        // If problem explicitly requires
        // "strict mountain" (both parts non-empty),
        // then that condition should be added.
        // -------------------------------

        int maxLength = 0;

        for (int idx = 0; idx < n; idx++) {
            maxLength = max(maxLength,
                            lis[idx] + lds[idx] - 1);
        }

        return maxLength;
    }
};
```

### Number of Longest Increasing Subsequence
Given an integer array nums, find the number of Longest Increasing Subsequences (LIS) in the array.
```cpp
int numberOfLIS(vector<int> nums) {
    int n = nums.size();

    // dp[i] = length of LIS ending at index i
    vector<int> dp(n, 1);

    // count[i] = number of LIS of length dp[i] ending at index i
    vector<int> count(n, 1);

    int maxLen = 0;  // stores overall maximum LIS length
    int ans = 0;     // stores total number of LIS

    for (int idx = 0; idx < n; idx++) {
        // Try extending all previous subsequences
        for (int prev = 0; prev < idx; prev++) {
            // We can extend only if increasing
            if (nums[idx] > nums[prev]) {
                // Case 1: Found strictly longer subsequence
                if (dp[prev] + 1 > dp[idx]) {
                    dp[idx] = dp[prev] + 1;

                    // Reset count because we found better length
                    // Number of ways becomes equal to ways at prev
                    count[idx] = count[prev];
                }

                // Case 2: Found another subsequence
                // giving same maximum length
                else if (dp[prev] + 1 == dp[idx]) {
                    // Add number of ways from prev
                    count[idx] += count[prev];
                }
            }
        }

        // Track global LIS length
        maxLen = max(maxLen, dp[idx]);
    }

    // Count total number of LIS of maximum length
    for (int i = 0; i < n; i++) {
        if (dp[i] == maxLen) {
            ans += count[i];
        }
    }

    return ans;
}
```

## DP on Strings

### Longest Common Subsequence
Given two strings str1 and str2, find the length of their longest common subsequence.
A subsequence is a sequence that appears in the same relative order but not necessarily contiguous and a common subsequence of two strings is a subsequence that is common to both strings.

>Input: str1 = "bdefg", str2 = "bfg"
>Output: 3
>Explanation: The longest common subsequence is "bfg", which has a length of 3.

```cpp
class Solution {
   public:
    int solve(string a, int n, string b, int m, vector<vector<int>> &dp) {
        if (n < 0 || m < 0) return 0;
        if (dp[n][m] != -1) return dp[n][m];

        if (a[n] == b[m]) {
            return dp[n][m] = 1 + solve(a, n - 1, b, m - 1, dp);
        }

        return dp[n][m] = 0 + max(solve(a, n - 1, b, m, dp),
                                  solve(a, n, b, m - 1, dp));
    }

    int solveByIndexShift(string a, int n, string b, int m,
                          vector<vector<int>> &dp) {
        if (n == 0 || m == 0) return 0;
        if (dp[n][m] != -1) return dp[n][m];

        if (a[n - 1] == b[m - 1]) {
            return dp[n][m] = 1 + solveByIndexShift(a, n - 1, b, m - 1, dp);
        }

        return dp[n][m] = 0 + max(solveByIndexShift(a, n - 1, b, m, dp),
                                  solveByIndexShift(a, n, b, m - 1, dp));
    }

    int lcsMemo(string str1, string str2) {
        int n = str1.size();
        int m = str2.size();
        // vector<vector<int>> dp(n, vector<int>(m, -1));
        // return solve(str1, n - 1, str2, m - 1, dp);
        vector<vector<int>> dpShift(n + 1, vector<int>(m + 1, -1));
        return solveByIndexShift(str1, n, str2, m, dpShift);
    }

    int lcsTab(string str1, string str2) {
        int n = str1.size();
        int m = str2.size();

        // dp[i][j] = LCS of first i chars of a
        //            and first j chars of b
        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));

        // Base case:
        // dp[0][*] = 0  (empty string)
        // dp[*][0] = 0

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                if (str1[i - 1] == str2[j - 1]) {
                    // characters match → extend LCS
                    dp[i][j] = 1 + dp[i - 1][j - 1];
                } else {
                    // characters don’t match → take best of skipping one
                    dp[i][j] = 0 + max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[n][m];
    }

    int lcsConstant(string str1, string str2) {
        int n = str1.size();
        int m = str2.size();

        // prev[j]  → LCS of: str1[0..i-2] and str2[0..j-1]
        //
        // curr[j]  → LCS of: str1[0..i-1] and str2[0..j-1]
        //
        // We only need previous row to compute current row.
        vector<int> prev(m + 1, 0), curr(m + 1, 0);

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                // If characters match,
                // extend the LCS from diagonal (previous row, previous column)
                if (str1[i - 1] == str2[j - 1]) {
                    // dp[i][j] = 1 + dp[i-1][j-1]
                    curr[j] = 1 + prev[j - 1];
                } else {
                    // If characters don't match,
                    // we either:
                    // 1. Skip character from str1 → prev[j]
                    // 2. Skip character from str2 → curr[j-1]
                    //
                    // Take maximum of both.
                    curr[j] = max(prev[j], curr[j - 1]);
                }
            }

            // After finishing row i,
            // current row becomes previous row
            prev = curr;
        }

        // Final answer stored in last cell
        return prev[m];
    }

    int lcs(string str1, string str2) {
        // return lcsMemo(str1, str2);
        // return lcsTab(str1, str2);
        return lcsConstant(str1, str2);
    }
};

```

### Longest Common Substring
Given two strings str1 and str2, find the length of their longest common substring.
A substring is a contiguous sequence of characters within a string.
>Input: str1 = "abcde", str2 = "abfce"
>Output: 2
>Explanation: The longest common substring is "ab", which has a length of 2.
```cpp
class Solution {
public:

    /*
        MEMOIZATION (Top-Down)

        dp[i][j] represents:
        Length of longest common substring
        ending exactly at a[i] and b[j].

        IMPORTANT:
        Substring must be contiguous.
        So on mismatch → value becomes 0.
    */
    int solve(string &a, string &b, int i, int j,
              vector<vector<int>> &dp, int &maxLen) {

        // If any index goes out of bounds → no substring
        if (i < 0 || j < 0)
            return 0;

        if (dp[i][j] != -1)
            return dp[i][j];

        // We must explore all states because unlike LCS,
        // answer is not necessarily at (n-1, m-1).
        solve(a, b, i - 1, j, dp, maxLen);
        solve(a, b, i, j - 1, dp, maxLen);

        if (a[i] == b[j]) {
            // Extend substring diagonally
            dp[i][j] = 1 + solve(a, b, i - 1, j - 1, dp, maxLen);

            // Track global maximum because substring
            // can end anywhere in table
            maxLen = max(maxLen, dp[i][j]);
        }
        else {
            // Mismatch breaks substring continuity
            dp[i][j] = 0;
        }

        return dp[i][j];
    }

    int longestCommonSubstringMemo(string a, string b) {
        int n = a.size(), m = b.size();

        vector<vector<int>> dp(n, vector<int>(m, -1));
        int maxLen = 0;

        solve(a, b, n - 1, m - 1, dp, maxLen);

        return maxLen;
    }

    /*
        TABULATION (Bottom-Up)

        dp[i][j] =
        length of longest common substring
        ending at a[i-1] and b[j-1].

        Table size = (n+1) x (m+1)
        Row 0 and column 0 represent empty prefixes.
    */
    int longestCommonSubstringTab(string a, string b) {

        int n = a.size();
        int m = b.size();

        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));

        int maxLen = 0;

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {

                if (a[i - 1] == b[j - 1]) {

                    // Extend previous diagonal match
                    dp[i][j] = 1 + dp[i - 1][j - 1];

                    // Track maximum substring length found so far
                    maxLen = max(maxLen, dp[i][j]);
                }
                else {
                    // IMPORTANT DIFFERENCE FROM LCS:
                    // Substring must be contiguous,
                    // so mismatch resets length to 0
                    dp[i][j] = 0;
                }
            }
        }

        return maxLen;
    }

    /*
        SPACE OPTIMIZED VERSION

        We only need previous row to compute current row.
        prev[j] → dp[i-1][j]
        curr[j] → dp[i][j]

        Time  : O(n*m)
        Space : O(m)
    */
    int longestCommonSubstringConstant(string a, string b) {

        int n = a.size();
        int m = b.size();

        vector<int> prev(m + 1, 0), curr(m + 1, 0);

        int maxLen = 0;

        for (int i = 1; i <= n; i++) {

            for (int j = 1; j <= m; j++) {

                if (a[i - 1] == b[j - 1]) {

                    // Extend diagonal
                    curr[j] = 1 + prev[j - 1];

                    maxLen = max(maxLen, curr[j]);
                }
                else {
                    // Reset because continuity breaks
                    curr[j] = 0;
                }
            }

            // Move current row to previous
            prev = curr;
        }

        return maxLen;
    }

    int longestCommonSubstr(string str1, string str2) {

        // return longestCommonSubstringMemo(str1, str2);
        // return longestCommonSubstringTab(str1, str2);
        return longestCommonSubstringConstant(str1, str2);
    }
};
```