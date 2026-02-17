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