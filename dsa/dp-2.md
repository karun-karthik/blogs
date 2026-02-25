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