## Dynamic Programming (DP)

**Definition**: Solve problems by breaking into **smaller overlapping subproblems** and **caching results** to avoid recomputation.

---

### Core Concepts

#### Optimal Substructure
- Optimal solution built from optimal solutions of subproblems
- Example: `F(n) = F(n - 1) + F(n - 2)`

#### Overlapping Subproblems
- Same subproblems solved multiple times
- **Solution**: Cache results to avoid recomputation

---

### DP Approaches

#### Memoization (Top-Down)
- **Type**: Recursive
- **Storage**: Cache (array or hashmap)
- **Strategy**: Solve subproblems on-demand

#### Tabulation (Bottom-Up)
- **Type**: Iterative
- **Strategy**: Start from base cases
- **Approach**: Build solution iteratively

---

## 1D DP

### Climbing Stairs
Given an integer n, there is a staircase with n steps, starting from the 0th step.
Determine the number of unique ways to reach the nth step, given that each move can be either 1 or 2 steps at a time.

```cpp
int climbStairsRecursion(int n) {
    if (n == 0) return 1;
    if (n == 1) return 1;
    int oneStep = climbStairsRecursion(n-1);
    int twoStep = climbStairsRecursion(n-2);
    return oneStep + twoStep;
}

int helperMemo(int n, vector<int> &dp) {
    if (n <= 1) return 1;
    if (dp[n] != -1)    return dp[n];
    return dp[n] = helperMemo(n-1, dp) + helperMemo(n-2, dp);
}

int climbStairsMemo(int n) {
    vector<int> dp(n+1, -1);
    return helperMemo(n, dp);
}

int climbStairsTabulation(int n) {
    vector<int> dp(n+1, -1);
    dp[0] = 1;
    dp[1] = 1;
    for (int i=2; i<=n; i++)
        dp[i] = dp[i-1] + dp[i-2];
    return dp[n];
}

int climbStairsConstant(int n) {
    int prev = 1;
    int prev2 = 1;
    for (int i = 2; i <= n; i++) {
        int curr = prev2 + prev;
        prev2 = prev;
        prev = curr;
    }
    return prev;
}

int climbStairs(int n) {
    // return climbStairsRecursion(n);
    // return climbStairsMemo(n);
    // return climbStairsTabulation(n);
    return climbStairsConstant(n);
}
```

### Frog Jump

A frog wants to climb a staircase with n steps. Given an integer array heights, where heights[i] contains the height of the ith step.

To jump from the ith step to the jth step, the frog requires abs(heights[i] - heights[j]) energy, where abs() denotes the absolute difference. The frog can jump from any step either one or two steps, provided it exists.

Return the minimum amount of energy required by the frog to go from the 0th step to the (n-1)th step.

```cpp
int helper(int idx, vector<int>& heights, vector<int> &dp) {
    if (idx == 0)   return 0;
    if (dp[idx] != -1)  return dp[idx];

    int jumpOne = helper(idx-1, heights, dp) + abs(heights[idx]-heights[idx-1]);
    int jumpTwo = INT_MAX;
    if (idx > 1)
        jumpTwo = helper(idx-2, heights, dp) + abs(heights[idx]-heights[idx-2]);
    return dp[idx] = min(jumpOne, jumpTwo);
}

int frogJumpMemo(vector<int>& heights) {
    int n = heights.size();
    vector<int> dp(n, -1);
    return helper(n-1, heights, dp);
}

int frogJumpTabulation(vector<int> &heights) {
    int n = heights.size();
    vector<int> dp(n, -1);
    dp[0] = 0;
    for (int i=1; i<n; i++) {
        int jumpOne = dp[i-1] + abs(heights[i-1] - heights[i]);
        int jumpTwo = INT_MAX;
        if (i > 1)
            jumpTwo = dp[i-2] + abs(heights[i-2] - heights[i]);
        dp[i] = min(jumpOne, jumpTwo);
    }
    return dp[n-1];
}

int frogJumpConstant(vector<int> &heights) {
    int n = heights.size();
    int prev = 0;
    int prev2 = 0;
    for (int i=1; i<n; i++) {
        int jumpOne = prev + abs(heights[i-1] - heights[i]);
        int jumpTwo = INT_MAX;
        if (i > 1)
            jumpTwo = prev2 + abs(heights[i-2] - heights[i]);
        int curr = min(jumpOne, jumpTwo);
        prev2 = prev;
        prev = curr;
    }
    return prev;
}

int frogJump(vector<int>& heights) {
    // return frogJumpMemo(heights);
    // return frogJumpTabulation(heights);
    return frogJumpConstant(heights);
}
```

### Frog Jump with K distances

A frog wants to climb a staircase with n steps. Given an integer array heights, where heights[i] contains the height of the ith step, and an integer k.

To jump from the ith step to the jth step, the frog requires abs(heights[i] - heights[j]) energy, where abs() denotes the absolute difference. The frog can jump from the ith step to any step in the range [i + 1, i + k], provided it exists.

Return the minimum amount of energy required by the frog to go from the 0th step to the (n-1)th step.

```cpp
int helper(int idx, int k, vector<int>& heights, vector<int> &dp) {
    if (idx == 0)   return 0;
    if (dp[idx] != -1)  return dp[idx];
    int minJump = INT_MAX;

    for (int i = 1; i <= k; i++) {
        int currIdx = idx - i;
        if (currIdx >= 0) {
            int value = helper(currIdx, k, heights, dp) + abs(heights[currIdx] - heights[idx]);
            minJump = min(minJump, value);
        }
    }
    return dp[idx] = minJump;
}

int frogJumpMemo(vector<int>& heights, int k) {
    // TC: O(k^n) SC: O(N)
    int n = heights.size();
    vector<int> dp(n, -1);
    return helper(n-1, k, heights, dp);
}

int frogJumpTab(vector<int>& heights, int k) {
    // TC: O(k^n) SC: O(N)
    int n = heights.size();
    vector<int> dp(n, 0);
    dp[0] = 0;
    for (int idx = 1; idx < n; idx++) {
        int minJump = INT_MAX;
        for (int i = 1; i <= k; i++) {
            int currIdx = idx - i;
            if (currIdx >= 0) {
                int value = dp[currIdx] + abs(heights[currIdx] - heights[idx]);
                minJump = min(minJump, value);
            }
        }
        dp[idx] = minJump;
    }
    return dp[n-1];
}

int frogJumpConstant(vector<int>& heights, int k) {
    int n = heights.size();
    vector<int> dp(k, 0); // since we only need last k values
    for (int idx = 1; idx < n; idx++) {
        int minJump = INT_MAX;
        for (int i = 1; i <= k; i++) {
            int currIdx = idx - i;
            if (currIdx >= 0) {
                int prevIdx = currIdx % k;
                int value = dp[prevIdx] + abs(heights[currIdx] - heights[idx]);
                minJump = min(minJump, value);
            }
        }
        dp[idx % k] = minJump;
    }
    return dp[(n-1) % k];
}

int frogJump(vector<int>& heights, int k) {
    // return frogJumpMemo(heights, k);
    // return frogJumpTab(heights, k);
    return frogJumpConstant(heights, k);
}
```

### Maxiumum Sum of Non Adjacent Elements

Given an integer array nums of size n. Return the maximum sum possible using the elements of nums such that no two elements taken are adjacent in nums.

```cpp
int helper(int idx, vector<int>&dp, vector<int>& nums) {
    if (idx == 0) return nums[idx];
    if (idx < 0)  return 0;
    if (dp[idx] != -1)  return dp[idx];
    int take = nums[idx] + helper(idx - 2, dp, nums);
    int notTake = 0 + helper(idx - 1, dp, nums);
    return dp[idx] = max(take, notTake);
}

int nonAdjacentMemo(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n, -1);
    return helper(n-1, dp, nums);
}

int nonAdjacentTab(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n, 0);
    dp[0] = nums[0];
    for (int idx = 1; idx < n; idx++) {
        int notTake = 0 + dp[idx - 1];
        int take = nums[idx]; // imp to consider nums[idx] than take = 0 as it doesn't consider the value when only 2 elements are present
        if (idx - 2 >= 0) {
            take = take + dp[idx - 2];
        }
        dp[idx] = max(take, notTake);
    }
    return dp[n-1];
}

int nonAdjacentConstant(vector<int>&nums) {
    int n = nums.size();
    int prev = 0, prev2 = 0;
    prev = nums[0];
    for (int idx = 1; idx < n; idx++) {
        int notTake = 0 + prev;
        int take = nums[idx];
        if (idx - 2 >= 0) {
            take = take + prev2;
        }
        int curr = max(take, notTake);
        prev2 = prev;
        prev = curr;
    }
    return prev;
}

int nonAdjacent(vector<int>& nums) {
    // return nonAdjacentMemo(nums);
    // return nonAdjacentTab(nums);
    return nonAdjacentConstant(nums);
}
```

### House Robber
A robber is targeting to rob houses from a street. Each house has security measures that alert the police when two adjacent houses are robbed. The houses are arranged in a circular manner, thus the first and last houses are adjacent to each other.

Given an integer array money, where money[i] represents the amount of money that can be looted from the (i+1)th house. Return the maximum amount of money that the robber can loot without alerting the police.

```cpp
int helper(int idx, vector<int>& nums, vector<int>& dp) {
    if (idx == 0) return nums[0];
    if (idx < 0) return 0;
    if (dp[idx] != -1) return dp[idx];
    int select = nums[idx] + helper(idx - 2, nums, dp);
    int notSelect = 0 + helper(idx - 1, nums, dp);
    return dp[idx] = max(select, notSelect);
}

int nonAdjacentMemo(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n, -1);
    return helper(n - 1, nums, dp);
}

int nonAdjacentTab(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n, 0);
    if (n == 0) return 0;
    dp[0] = nums[0];
    if (n > 1) {
        dp[1] = max(nums[0], nums[1]);
    }
    for (int i = 2; i < n; i++) {
        dp[i] = max(nums[i] + dp[i - 2], dp[i - 1]);
    }
    return dp[n - 1];
}

int nonAdjacentConstant(vector<int>& nums) {
    int n = nums.size();
    if (n == 0) return 0;
    int prev2 = 0;
    int prev = nums[0];
    for (int i = 1; i < n; i++) {
        int select = nums[i] + prev2;
        int notSelect = prev;
        int curr = max(select, notSelect);
        prev2 = prev;
        prev = curr;
    }
    return prev;
}

int houseRobber(vector<int>& money) {
    int n = money.size();
    if (n == 0) return 0;
    if (n == 1) return money[0];
    vector<int> a, b;
    for (int i = 0; i < n; i++) {
        if (i != 0) a.push_back(money[i]);
        if (i != n - 1) b.push_back(money[i]);
    }
    // return max(nonAdjacentTab(a), nonAdjacentTab(b));
    // return max(nonAdjacentMemo(a), nonAdjacentMemo(b));
    return max(nonAdjacentConstant(a), nonAdjacentConstant(b));
}
```