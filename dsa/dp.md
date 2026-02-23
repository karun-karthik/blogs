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

#### Flow of solving DP problems!
* If greedy fails, then try all possible ways
* If trying all possible ways => Recursion O(k^n); k < n, [could lead to TLE or OOM] 
* Once recursion is done, convert to memoization O(n^k), [k < n]
* Convert memoized solution to tabulation
* Convert tabulation to space optimized solution!

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

## 2D DP
### Ninja's Training

A ninja has planned a n-day training schedule. Each day he has to perform one of three activities - running, stealth training, or fighting practice. The same activity cannot be done on two consecutive days and the ninja earns a specific number of merit points, based on the activity and the given day.



Given a n x 3-sized matrix, where matrix[i][0], matrix[i][1], and matrix[i][2], represent the merit points associated with running, stealth and fighting practice, on the (i+1)th day respectively. Return the maximum possible merit points that the ninja can earn.

>   Input: matrix = [[10, 40, 70], [20, 50, 80], [30, 60, 90]]
    Output: 210
    Explanation:
    Day 1: fighting practice = 70
    Day 2: stealth training = 50
    Day 3: fighting practice = 90
    Total = 70 + 50 + 90 = 210

```cpp
int solve(int day, int last, vector<vector<int>>& matrix, vector<vector<int>> &dp) {
    if (dp[day][last] != -1)    return dp[day][last];

    if (day == 0) {
        // then find max of all scores;
        int maxi = 0;
        for (int i = 0; i < 3; i++) {
            if (i != last)  maxi = max(maxi, matrix[0][i]);
        }
        return dp[day][last] = maxi;
    }

    int maxi = 0;
    for (int i = 0; i<3; i++) {
        if (i != last)  {
            int score = matrix[day][i] + solve(day - 1, i, matrix, dp);
            maxi = max(maxi, score);
        }
    }

    return dp[day][last] = maxi;
}

int ninjaTrainingMemo(vector<vector<int>>& matrix) {
    int days = matrix.size();
    // [days X m] is dp order; (m, -1) => m is no. of activities
    int last = 3;
    vector<vector<int>> dp(days, vector<int>(last + 1, -1));
    return solve(days - 1, last, matrix, dp);
}

// Tabulation -----------
int ninjaTrainingTabulation(vector<vector<int>> &matrix) {
    int days = matrix.size();
    // [days X m] is dp order; (m, -1) => m is no. of activities
    int last = 3;
    vector<vector<int>> dp(days, vector<int>(last + 1, 0));
    dp[0][0] = max(matrix[0][1], matrix[0][2]);
    dp[0][1] = max(matrix[0][0], matrix[0][2]);
    dp[0][2] = max(matrix[0][0], matrix[0][1]);
    dp[0][3] = max(matrix[0][0], max(matrix[0][1], matrix[0][2]));
    
    // iterate on all days
    for (int day = 1; day < days; day++) {
        // for every day I can have tasks either of 0, 1, 2, 3
        for (int last = 0; last < 4; last++) {
            // dp[day][last] = 0;
            // iterate through the tasks
            for (int task = 0; task < 3; task++) {
                if (task != last) {
                    int score = matrix[day][task] + dp[day-1][task];
                    dp[day][last] = max(dp[day][last], score);
                }
            }
        }
    }
    return dp[days - 1][last];
}

// Space -----------
int ninjaTrainingConstant(vector<vector<int>>& matrix) {
    int days = matrix.size();
    int last = 3;
    vector<int> prev(last + 1, 0), curr(last + 1, 0);
    prev[0] = max(matrix[0][1], matrix[0][2]);
    prev[1] = max(matrix[0][0], matrix[0][2]);
    prev[2] = max(matrix[0][0], matrix[0][1]);
    prev[3] = max(matrix[0][0], max(matrix[0][1], matrix[0][2]));
    // iterate on all days
    for (int day = 1; day < days; day++) {
        // for every day I can have tasks either of 0, 1, 2, 3
        for (int last = 0; last < 4; last++) {
            // iterate through the tasks
            for (int task = 0; task < 3; task++) {
                if (task != last) {
                    int score = matrix[day][task] + prev[task];
                    curr[last] = max(curr[last], score);
                }
            }
        }
        prev = curr;
    }
    return prev[last];
}

int ninjaTraining(vector<vector<int>>& matrix) {
    // return ninjaTrainingMemo(matrix);
    // return ninjaTrainingTabulation(matrix);
    return ninjaTrainingConstant(matrix);
}
```

## DP on Grids

### Grid Unique Paths

Given two integers m and n, representing the number of rows and columns of a 2d array named matrix. Return the number of unique ways to go from the top-left cell (matrix[0][0]) to the bottom-right cell (matrix[m-1][n-1]).

```cpp
int solve(int m, int n, vector<vector<int>> &dp) {
    if (m == 0 && n == 0)   return 1;
    if (m < 0 || n < 0) return 0;
    if (dp[m][n] != -1) return dp[m][n];
    return dp[m][n] = solve(m-1, n, dp) + solve(m, n-1, dp);
}

int uniquePathsMemo(int m, int n) {
    vector<vector<int>>dp(m, vector<int>(n, -1));
    return solve(m-1, n-1, dp);
}

int uniquePathsTab(int m, int n) {
    vector<vector<int>>dp(m, vector<int>(n, 0));
    for (int i=0; i<m; i++) {
        for (int j=0; j<n; j++) {
            if (i == 0 && j == 0) {
                dp[0][0] = 1;
                continue;
            } else {
                int top = (i > 0) ? dp[i-1][j] : 0;
                int left = (j > 0) ? dp[i][j-1] : 0;
                dp[i][j] = top + left;
            }
        }
    }
    return dp[m-1][n-1];
}

int uniquePathsConst(int m, int n) {
    vector<int> prev(n, 0), curr(n, 0);
    for (int i=0; i<m; i++) {
        for (int j=0; j<n; j++) {
            if (i == 0 && j == 0) {
                curr[0] = 1;
                continue;
            } else {
                int top = i > 0 ? prev[j] : 0;
                int left = j > 0 ? curr[j-1] : 0;
                curr[j] = top + left;
            }
        }
        prev = curr;
    }
    return prev[n-1];
}

int uniquePaths(int m, int n) {
    // return uniquePathsMemo(m, n);
    // return uniquePathsTab(m, n);
    return uniquePathsConst(m, n);
}
```

### Unique Paths ii
Given an m x n 2d array named matrix, where each cell is either 0 or 1. Return the number of unique ways to go from the top-left cell (matrix[0][0]) to the bottom-right cell (matrix[m-1][n-1]). A cell is blocked if its value is 1, and no path is possible through that cell.

>   Input: matrix = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
<br/>Output: 2

```cpp
int solve(int m, int n, vector<vector<int>> &matrix, vector<vector<int>> &dp) {
    if (m < 0 || n < 0 || matrix[m][n] == 1)  return 0;
    if (m == 0 && n == 0)   return 1;
    if (dp[m][n] != -1) return dp[m][n];

    return dp[m][n] = solve(m-1, n, matrix, dp) + solve(m, n-1, matrix, dp);
}

int memo(vector<vector<int>>& matrix) {
    int m = matrix.size();
    int n = matrix[0].size();
    vector<vector<int>>dp (m, vector<int>(n, -1));
    return solve(m-1, n-1, matrix, dp);
}

int tab(vector<vector<int>> &matrix) {
    int m = matrix.size();
    int n = matrix[0].size();
    vector<vector<int>>dp (m, vector<int>(n, 0));
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (matrix[i][j] == 1) {
                // if there are obstacles at cell,
                // then it cannot be passed, i.e dp[i][j] = 0
                dp[i][j] = 0;
                continue;
            }
            if (i == 0 && j == 0) {
                // if we're at starting point,
                // then there's one path 
                dp[0][0] = 1;
                continue;
            }
            int top = i > 0 ? dp[i-1][j] : 0;
            int left = j > 0 ? dp[i][j-1] : 0;
            dp[i][j] = top + left;
        }
    }
    return dp[m-1][n-1];
}

int space(vector<vector<int>> &matrix) {
    int m = matrix.size();
    int n = matrix[0].size();
    vector<int> prev(n, 0), curr(n, 0);
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (matrix[i][j] == 1) {
                curr[j] = 0;
                continue;
            }
            if (i == 0 && j == 0) {
                curr[0] = 1;
                continue;
            }
            int top = i > 0 ? prev[j] : 0;
            int left = j > 0 ? curr[j-1] : 0;
            curr[j] = top + left;
        }
        prev = curr;
    }
    return prev[n-1];
}

int uniquePathsWithObstacles(vector<vector<int>>& matrix) {
    // return memo(matrix);
    // return tab(matrix);
    return space(matrix);
}
```

### Minimum Falling Path Sum

Given a 2d array called matrix consisting of integer values. Return the minimum path sum that can be obtained by starting at any cell in the first row and ending at any cell in the last row.

Movement is allowed only to the bottom, bottom-right, or bottom-left cell of the current cell.

> Input: matrix = [[1, 2, 10, 4], [100, 3, 2, 1], [1, 1, 20, 2], [1, 2, 2, 1]]
Output: 6
Explanation:
One optimal route can be:-
Start at 1st cell of 1st row -> bottom-right -> bottom -> bottom-left.

```cpp
int solve(int i, int j, vector<vector<int>>& matrix, vector<vector<int>> &dp) {
    if (j < 0 || j >= matrix[0].size()) return 1e9;
    if (i == 0)   return matrix[0][j];
    if (dp[i][j] != -1) return dp[i][j];

    int bottom = matrix[i][j] + solve(i-1, j, matrix, dp);
    int bottomRight = matrix[i][j] + solve(i-1, j+1, matrix, dp);
    int bottomLeft = matrix[i][j] + solve(i-1, j-1, matrix, dp);

    return dp[i][j] = min(bottom, min(bottomLeft, bottomRight));   
}

int minFallingPathSumMemo(vector<vector<int>>& matrix) {
    int m = matrix.size();
    int n = matrix[0].size();
    vector<vector<int>> dp(m, vector<int>(n, -1));
    int res = INT_MAX;
    for (int j = 0; j<n; j++) {
        res = min(res, solve(m-1, j, matrix, dp));
    }
    return res;
}

int minFallingPathSumTab(vector<vector<int>> &matrix) {
    int m = matrix.size();
    int n = matrix[0].size();
    vector<vector<int>> dp(m, vector<int>(n, 0));

    for (int j=0; j<n; j++) {
        dp[0][j] = matrix[0][j];
    }

    for (int i=1; i<m; i++) {
        for (int j=0; j<n; j++) {
            int up = matrix[i][j] + dp[i-1][j];
            int leftDiagonal = 0;
            if (j-1 >= 0) {
                leftDiagonal = matrix[i][j] + dp[i-1][j-1];
            } else {
                leftDiagonal = 1e9;
            }
            int rightDiagonal = 0;
            if (j+1 < n) {
                rightDiagonal = matrix[i][j] + dp[i-1][j+1];
            } else {
                rightDiagonal = 1e9;
            }
            dp[i][j] = min(up, min(leftDiagonal, rightDiagonal));
        }
    }

    int res = 1e9;
    for (int j=0; j<n; j++) {
        res = min(res, dp[m-1][j]);
    }
    return res;
}

int minFallingPathSumConstant(vector<vector<int>> &matrix) {
    int m = matrix.size();
    int n = matrix[0].size();
    vector<int> prev(n, 0);

    for (int j=0; j<n; j++) {
        prev[j] = matrix[0][j];
    }

    for (int i=1; i<m; i++) {
        vector<int> curr(n, 0);
        for (int j=0; j<n; j++) {
            int up = matrix[i][j] + prev[j];
            int leftDiagonal = 0;
            if (j-1 >= 0) {
                leftDiagonal = matrix[i][j] + prev[j-1];
            } else {
                leftDiagonal = 1e9;
            }
            int rightDiagonal = 0;
            if (j+1 < n) {
                rightDiagonal = matrix[i][j] + prev[j+1];
            } else {
                rightDiagonal = 1e9;
            }
            curr[j] = min(up, min(leftDiagonal, rightDiagonal));
        }
        prev = curr;
    }

    int res = 1e9;
    for (int j=0; j<n; j++) {
        res = min(res, prev[j]);
    }
    return res;
}

int minFallingPathSum(vector<vector<int>>& matrix) {
    // return minFallingPathSumMemo(matrix);
    // return minFallingPathSumTab(matrix);
    return minFallingPathSumConstant(matrix);
}
```

### Triangle

Given a 2d integer array named triangle with n rows. Its first row has 1 element and each succeeding row has one more element in it than the row above it.
Return the minimum falling path sum from the first row to the last.
Movement is allowed only to the bottom or bottom-right cell from the current cell.

```cpp
int solve(int i, int j, vector<vector<int>>& triangle, vector<vector<int>> &dp) {
    int n = triangle.size();
    if (dp[i][j] != -1) return dp[i][j];
    if (i == n-1)   return triangle[i][j];

    int bottom =  solve(i+1, j, triangle, dp);
    int bottomRight = solve(i+1, j+1, triangle, dp);
    return dp[i][j] = triangle[i][j] + min(bottom, bottomRight);
}

int minTriangleSumMemo(vector<vector<int>>& triangle) {
    int n = triangle.size();
    vector<vector<int> > dp(n, vector<int>(n, -1));
    return solve(0, 0, triangle, dp);
}

int minTriangleSumTab(vector<vector<int>>& triangle) {
    int n = triangle.size();
    vector<vector<int> > dp(n, vector<int>(n, -1));
    
    for (int j=0; j<n; j++) dp[n-1][j] = triangle[n-1][j];

    for (int i=n-2; i >= 0; i--) {
        for (int j=i; j >= 0; j--) {
            int down = triangle[i][j] + dp[i+1][j];
            int right = triangle[i][j] + dp[i+1][j+1];
            dp[i][j] = min(down, right);
        }
    }
    return dp[0][0];
}

int minTriangleSumConstant(vector<vector<int>>& triangle) {
    int n = triangle.size();
    vector<int> prev(n, 0);
    
    for (int j=0; j<n; j++) prev[j] = triangle[n-1][j];

    for (int i=n-2; i >= 0; i--) {
        vector<int> curr(n, 0);
        for (int j=i; j >= 0; j--) {
            int down = triangle[i][j] + prev[j];
            int right = triangle[i][j] + prev[j+1];
            curr[j] = min(down, right);
        }
        prev = curr;
    }
    return prev[0];
}

int minTriangleSum(vector<vector<int>>& triangle) {
    // return minTriangleSumMemo(triangle);
    // return minTriangleSumTab(triangle);
    return minTriangleSumConstant(triangle);
}
```

### Cherry Pickup ii
Given a n x m 2d integer array called matrix where matrix[i][j] represents the number of cherries you can pick up from the (i, j) cell.Given two robots that can collect cherries, one is located at the top-leftmost (0, 0) cell and the other at the top-rightmost (0, m-1) cell.
Return the maximum number of cherries that can be picked by the two robots in total, following these rules:
* Robots that are standing on (i, j) cell can only move to cell (i + 1, j - 1), (i + 1, j), or (i + 1, j + 1), if it exists in the matrix.
* A robot will pick up all the cherries in a given cell when it passes through that cell.
* If both robots come to the same cell at the same time, only one robot takes the cherries.
* Both robots must reach the bottom row in matrix.


```cpp
int solve(int i, int j1, int j2, vector<vector<int>>& matrix, vector<vector<vector<int>>> &dp) {
    int m = matrix.size(); // row size
    int n = matrix[0].size(); // column size

    if (j1 < 0 || j2 < 0 || j1 >= n || j2 >= n)   return -1e8;
    if (i == m-1) {
        if (j1 == j2)   return matrix[i][j1];
        else return matrix[i][j1] + matrix[i][j2];
    }
    if (dp[i][j1][j2] != -1)    return dp[i][j1][j2];

    int maxi = -1e8;
    for (int dj1 = -1; dj1 <= 1; dj1++) {
        for (int dj2 = -1; dj2 <= 1; dj2++) {
            int value = 0;
            if (j1 == j2)   value = matrix[i][j1];
            else value = matrix[i][j1] + matrix[i][j2];
            value += solve(i+1, j1 + dj1, j2 + dj2, matrix, dp);
            maxi = max(maxi, value);
        }
    }

    return dp[i][j1][j2] = maxi;
}

int cherryPickupMemo(vector<vector<int>>& matrix) {
    int m = matrix.size(); // row size
    int n = matrix[0].size(); // column size
    vector<vector<vector<int>>> dp(m, vector<vector<int>>(n, vector<int>(n, -1)));
    return solve(0, 0, n-1, matrix, dp);
}

int cherryPickupTab(vector<vector<int>>& matrix) {
    int n = matrix.size(); // row size
    int m = matrix[0].size(); // column size
    vector<vector<vector<int>>> dp(n, vector<vector<int>>(m, vector<int>(m, 0)));
    
    // base-cases
    for (int j1 = 0; j1 < m; j1++) {
        for (int j2 = 0; j2 < m; j2++) {
            if (j1 == j2)
                dp[n - 1][j1][j2] = matrix[n - 1][j1];
            else
                dp[n - 1][j1][j2] = matrix[n - 1][j1] + matrix[n - 1][j2];
        }
    }

    for (int i = n - 2; i >= 0; i--) {
        for (int j1 = 0; j1 < m; j1++) {
            for (int j2 = 0; j2 < m; j2++) {
                int maxi = INT_MIN;

                // Inner nested loops to try out 9 options 
                for (int di = -1; di <= 1; di++) {
                    for (int dj = -1; dj <= 1; dj++) {
                        int ans;

                        if (j1 == j2)
                            ans = matrix[i][j1];
                        else
                            ans = matrix[i][j1] + matrix[i][j2];

                        // Check if the move is valid 
                        if ((j1 + di < 0 || j1 + di >= m) || (j2 + dj < 0 || j2 + dj >= m))
                            /* A very large negative value 
                            to represent an invalid move*/
                            ans += -1e9; 
                        else
                            ans += dp[i + 1][j1 + di][j2 + dj]; 
                            
                        // Update the maximum result
                        maxi = max(ans, maxi); 
                    }
                }
                /* Store the maximum result for 
                this state in the DP array*/
                dp[i][j1][j2] = maxi; 
            }
        }
    }
    return dp[0][0][m-1];
}

int cherryPickup(vector<vector<int>>& matrix) {
    // return cherryPickupMemo(matrix);
    return cherryPickupTab(matrix);
}
```