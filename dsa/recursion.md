## Basics

### Pow(x, n)
```cpp
// TC: O(logN) SC: O(logN)
double power(double x, long n) {
    // Base case: anything raised to 0 is 1
    if (n == 0) return 1.0;

    // Base case: anything raised to 1 is itself
    if (n == 1) return x;

    // If 'n' is even
    if (n % 2 == 0) {
        // Recursive call: x * x, n / 2
        return power(x * x, n / 2);
    }
    // If 'n' is odd
    // Recursive call: x * power(x, n-1)
    return x * power(x, n - 1);
}

double myPow(double x, int n) {
    long long num = n;

    // If n is negative
    if (num < 0) {
        // Calculate the power of -n and take reciprocal
        return (1.0 / power(x, -1 * num));
    }
    // If n is non-negative
    return power(x, num);
}
```

### Generate parentheses
Given an integer n.Generate all possible combinations of well-formed parentheses of length 2 x N.
```
Input : 2
Output : [ "(())" , "()()" ]
```
```cpp
// TC: O((4^n / sqrt(n))*n) & SC: O((4^n / sqrt(n))*n),
void generate(int idx, string s, int open, int close, vector<string>&res, int n) {
    if (open > n)   return;
    if ((open + close == 2*n) && open == close) {
        res.push_back(s);
        return;
    }
    generate(idx + 1, s + '(', open + 1, close, res, n);
    if (open > close) {
        generate(idx + 1, s + ')', open, close + 1, res, n);
    }
}
vector<string> generateParenthesis(int n) {
    vector<string> res;
    generate(0, "", 0, 0, res, n);
    return res;
}
```

### Power Set
Given an array of integers nums of unique elements. Return all possible subsets (power set) of the array.
Do not include the duplicates in the answer.
```
Input : nums = [1, 2, 3]
Output : [[] , [1] , [2] , [1, 2] , [3] , [1, 3] , [2, 3] , [1, 2 ,3]]
```

```cpp
// TC: O(2^N) SC: O(N* 2^N)
void solve(int idx, vector<int>&nums, vector<int> &aux, vector<vector<int>>&res) {
    if (idx == nums.size()) {
        res.push_back(aux);
        return;
    }
    aux.push_back(nums[idx]);
    solve(idx + 1, nums, aux, res);
    aux.pop_back();
    solve(idx + 1, nums, aux, res);
}

vector<vector<int> > powerSet(vector<int>& nums) {
    vector<vector<int>> res;
    vector<int> aux;
    solve(0, nums, aux, res);
    return res;
}
```

## Subsequence Problems

### Check if there exists a subsequence with sum K
Given an array nums and an integer k. Return true if there exist subsequences such that the sum of all elements in subsequences is equal to k else false.

```cpp
// TC: O(2^N) SC: O(N)
bool solve(int idx, int sum, vector<int>&nums, int k) {
    if (idx == nums.size()) {
        return sum == k;
    }
    bool pick = solve(idx+1, sum + nums[idx], nums, k);
    bool notPick = solve(idx+1, sum, nums, k);
    return pick || notPick;
}

bool checkSubsequenceSum(vector<int>& nums, int k) {
    return solve(0, 0, nums, k);
}
```

### Count all subsequences with sum K
```cpp
// TC: O(2^N) SC: O(N)
int solve(int idx, vector<int>& nums, int k, int sum) {
    if (idx == nums.size()) {
        if (sum == k) {
            return 1;
        }
        return 0;
    }

    int pick = solve(idx + 1, nums, k, sum + nums[idx]);
    int notPick = solve(idx + 1, nums, k, sum);

    return pick + notPick;
}

int countSubsequenceWithTargetSum(vector<int>& nums, int k){
    return solve(0, nums, k, 0);
}
```

## Medium

### Combination Sum
Provided with a goal integer target and an array of unique integer candidates, provide a list of all possible combinations of candidates in which the selected numbers add up to the target. The combinations can be returned in any order.
A candidate may be selected from the pool an infinite number of times. There are two distinct combinations if the frequency of at least one of the selected figures differs.
The test cases are created so that, for the given input, there are fewer than 150 possible combinations that add up to the target.
If there is no possible subsequences then return empty vector.

```cpp
void solve(int idx, vector<int> &aux, vector<vector<int>>& res, vector<int>&candidates, int target) {
    if (target == 0) {
        res.push_back(aux);
        return;
    }
    if (target < 0 || idx >= candidates.size()) return;
    aux.push_back(candidates[idx]);
    solve(idx, aux, res, candidates, target-candidates[idx]);
    aux.pop_back();
    solve(idx + 1, aux, res, candidates, target);
}

vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    vector<vector<int>> res;
    vector<int> aux;
    solve(0, aux, res, candidates, target);
    return res;
}
```

>TC: O(K*N(Target/m)), where N is the number of elements, and m is the minimum value among the elements. This is because the algorithm explores an exponential number of possible combinations in the worst case, as elements can be chosen repeatedly to form the target. For each valid combination found, it may take up to K operations to copy or process the combination, where K is the maximum length of any combination in the result.
SC: O(Target/m), because the deepest recursion and the longest combination both occur when repeatedly choosing the smallest element.

### Combination Sum II

Given collection of candidate numbers (candidates) and a integer target.Find all unique combinations in candidates where the sum is equal to the target.There can only be one usage of each number in the candidates combination and return the answer in sorted order.

e.g : The combination [1, 1, 2] and [1, 2, 1] are not unique.

```cpp
// TC: O(2^N * N) SC: O(N)
void solve(int idx, vector<int>& candidates, int target, vector<vector<int>> &res, vector<int>& ans) {
    if (target == 0) {
        res.push_back(ans);
        return;
    }
    if (target < 0 || idx == candidates.size()) return;
    ans.push_back(candidates[idx]);
    solve(idx + 1, candidates, target-candidates[idx], res, ans);
    ans.pop_back();
    for (int i = idx + 1; i < candidates.size(); i++) {
        if (candidates[i] != candidates[idx]) {
            solve(i, candidates, target, res, ans);
            break;
        }
    }
}
vector<vector<int> > combinationSum2(vector<int>& candidates, int target) {
    vector<vector<int>> ans; 
    vector<int> nums; 
    sort(candidates.begin(), candidates.end()); 
    solve(0, candidates, target, ans, nums);
    return ans; 
}
```

### Combination Sum III
Determine all possible set of k numbers that can be added together to equal n while meeting the following requirements:
* There is only use of numerals 1 through 9.
* A single use is made of each number.

Return list of every feasible combination that is allowed. The combinations can be returned in any order, but the list cannot have the same combination twice.
```
Input : k = 3, n = 9
Output : [[1, 2, 6],[1, 3, 5],[2, 3, 4]]
```
```cpp
void solve(vector<vector<int>>& res, vector<int>& curr, int k, int target, int start, int sum) {

    // Base Case:
    // If we have picked exactly k numbers,
    // check whether they form the required sum.
    if (curr.size() == k) {
        if (sum == target) res.push_back(curr);
        return;
    }

    // Pruning:
    // Since numbers are positive, the sum can only increase.
    // If we've already exceeded the target,
    // no point exploring further.
    if (sum > target) return;

    // Try every possible next number.
    // 'start' ensures:
    // 1. Numbers are chosen only once.
    // 2. Combinations remain sorted.
    for (int num = start; num <= 9; num++) {

        // Choose
        curr.push_back(num);

        // Explore remaining numbers
        solve(res, curr, k, target, num + 1, sum + num);

        // Backtrack
        curr.pop_back();
    }
}

vector<vector<int>> combinationSum3(int k, int n) {

    // INTUITION:
    // We need all combinations of exactly k distinct numbers
    // from the range [1...9] whose sum equals n.
    //
    // At every step we decide:
    // - Pick the current number
    // - Continue with larger numbers only
    //
    // This naturally fits Backtracking.

    vector<vector<int>> res;
    vector<int> curr;

    solve(res, curr, k, n, 1, 0);

    return res;
}
```


### Subsets I

Given an array nums of n integers. Return array of sum of all subsets of the array nums.
Output can be returned in any order.

```cpp
// TC: O(2^N) SC: O(N)
void solve(int idx, int sum, vector<int> &s, vector<int> &nums) {
    if (idx == nums.size()) {
        s.push_back(sum);
        return;
    }
    solve(idx + 1, sum + nums[idx], s, nums);
    solve(idx + 1, sum, s, nums);
}

vector<int> subsetSums(vector<int>& nums) {
    vector<int> s;
    solve(0, 0, s, nums);
    return s;
}
```

### Subsets II
Given an integer array nums, which can have duplicate entries, provide the power set.
Duplicate subsets cannot exist in the solution set. Return the answer in any sequence.

```cpp
// TC: O(2^N * N) SC: O(N)
void solve(int idx, vector<int> &aux, vector<vector<int>> &res, vector<int>&nums) {
    res.push_back(aux);
    for (int i = idx; i < nums.size(); i++) {
        if (i > idx && nums[i] == nums[i-1])    continue;
        aux.push_back(nums[i]);
        solve(i + 1, aux, res, nums);
        aux.pop_back();
    }
}

vector<vector<int> > subsetsWithDup(vector<int>& nums) {
    vector<vector<int>> res;
    vector<int> aux;
    sort(nums.begin(), nums.end());
    solve(0, aux, res, nums);
    return res;
}
```

## Hard

### Letter Combinations of Phone Number
Given a string consisting of digits from 2 to 9 (inclusive). Return all possible letter combinations that the number can represent.
Mapping of digits to letters is given in first example.
```
Input : digits = "34"
Output : [ "dg", "dh", "di", "eg", "eh", "ei", "fg", "fh", "fi" ]
```
```cpp
// TC: O(4^N * N), SC: O(N)
void solve(int idx, string aux, vector<string>& res, string digits, map<char, string> mp) {
    if (idx == digits.length()) {
        res.push_back(aux);
        return;
    }
    string alpha = mp[digits[idx]];
    for (int i = 0; i < alpha.size(); i++) {
        solve(idx + 1, aux + alpha[i], res, digits, mp);
    }
}

vector<string> letterCombinations(string digits) {
    map<char, string> mp {
        {'2', "abc"},
        {'3', "def"},
        {'4', "ghi"},
        {'5', "jkl"},
        {'6', "mno"},
        {'7', "pqrs"},
        {'8', "tuv"},
        {'9', "wxyz"}
    };
    string s = "";
    vector<string> res;
    solve(0, s, res, digits, mp);
    return res;
}
```

### Palindrome Partioning

```cpp
// TC: O(N * 2^N)   SC: O(N)
bool isPalindrome(string s, int start, int end) {
    while (start <= end) {
        if (s[start++] != s[end--]) return false;
    }
    return true;
}

void dfs(int idx, string s, vector<string> &aux, vector<vector<string>> &res) {
    if (idx == s.size()) {
        res.push_back(aux);
        return;
    }
    // Iterate over the substring starting from 'idx'
    for (int i = idx; i < s.size(); ++i) {
        // Check if the substring s[idx..i] is a palindrome
        if (isPalindrome(s, idx, i)) {
            aux.push_back(s.substr(idx, i - idx + 1));
            dfs(i + 1, s, aux, res);
            // Backtrack: remove the last added substring
            aux.pop_back();
        }
    }
}

vector<vector<string>> partition(string s) {
    vector<vector<string>> res;
    vector<string> aux;
    dfs(0, s, aux, res);
    return res;
}
```

### Word Search
Given a grid of n x m dimension grid of characters board and a string word.The word can be created by assembling the letters of successively surrounding cells, whether they are next to each other vertically or horizontally. It is forbidden to use the same letter cell more than once.

Return true if the word exists in the grid otherwise false.
```cpp
bool isFound(vector<vector<char> > & board, int i, int j, string& word, int idx) {
    // If all characters of the word are found
    if (idx == word.length()) {
        return true;
    }
    // Boundary conditions and character mismatch check
    if (i < 0 || j < 0 || i >= board.size() || j >= board[0].size() || word[idx] != board[i][j]) {
        return false;
    }

    // Initialize answer as false
    bool ans = false;

    // Temporarily mark the cell as visited
    char x = board[i][j];
    board[i][j] = ' ';

    // Check all four possible directions (down, up, right, left)
    ans |= isFound(board, i + 1, j, word, idx + 1);
    ans |= isFound(board, i - 1, j, word, idx + 1);
    ans |= isFound(board, i, j + 1, word, idx + 1);
    ans |= isFound(board, i, j - 1, word, idx + 1);

    // Restore the original character in the cell
    board[i][j] = x;
    
    return ans;
}


bool exist(vector<vector<char> >& board, string word) {
    for (int i = 0; i < board.size(); i++) {
        for (int j = 0; j < board[0].size(); j++) {
            // If the first character matches, start the search
            if (board[i][j] == word[0]) {
                // If the word is found, return true
                if (isFound(board, i, j, word, 0)) {
                    return true;
                }
            }
        }
    }
    return false;
}
```
```
TC : O(N * M * 4^L) where N is rows, M is columns and L is the word length; recursive search through board.
SC : O(L) due to recursive call stack depth, where L is the length of the word.
```

### N-Queen
The challenge of arranging n queens on a n × n chessboard so that no two queens attack one another is known as the "n-queens puzzle". Return every unique solution to the n-queens puzzle given an integer n. The answer can be returned in any sequence.

Every solution has a unique board arrangement for the placement of the n-queens, where 'Q' and '.' stand for a queen and an empty space, respectively.

```cpp
// TC: O(N!) SC: O(N)
bool isSafe(int row, int col, vector<string>& board) {
    int r = row, c = col;
    // upper left diagonal
    while (r >= 0 && c >= 0) {
        if (board[r][c] == 'Q') return false;
        r--;
        c--;
    }

    r = row, c = col;
    // left
    while (c >= 0) {
        if (board[r][c] == 'Q') return false;
        c--;
    }

    r = row, c = col;
    // lower left diagonal
    while (r < board.size() && c >= 0) {
        if (board[r][c] == 'Q') return false;
        r++;
        c--;
    }

    // if no queens return true;
    return true;
}

void solve(int col, vector<vector<string>>&ans, vector<string>&board) {
    if (col == board.size()) {
        ans.push_back(board);
        return;
    }
    for (int row = 0; row < board.size(); row++) {
        if (isSafe(row, col, board)) {
            board[row][col] = 'Q';
            solve(col + 1, ans, board);
            board[row][col] = '.';
        }
    }
}

vector<vector<string> > solveNQueens(int n) {
    vector<vector<string>> ans;
    vector<string> board(n, string(n, '.'));
    solve(0, ans, board);
    return ans;
}
```

### Rate in a Maze
```cpp
// TC: O(4^(N^2)) SC: O(N^2)
void solve(int row, int col, string s, vector<string> &res, vector<vector<int> > &grid) {
    int n = grid.size();
    if (row < 0 || row > n-1 || col < 0 || col > n-1 || grid[row][col]==0)   return;
    if (row == n-1 && col == n-1) {
        res.push_back(s);
        return;
    }
    grid[row][col] = 0;
    solve(row + 1, col, s + "D", res, grid);
    solve(row - 1, col, s + "U", res, grid);
    solve(row, col + 1, s + "R", res, grid);
    solve(row, col - 1, s + "L", res, grid);
    grid[row][col] = 1;
}

vector<string> findPath(vector<vector<int> > &grid) {
    vector<string> res;
    string s = "";
    solve(0, 0, s, res, grid);
    return res;
}
```

### Sudoku Solver
```cpp
bool canPlace(vector<vector<char>>& board, int row, int col, char digit) {
    for (int i=0; i<9; i++) {
        if (board[row][i] == digit || board[i][col] == digit)
            return false;
    }
    int startRow = (row / 3)*3;
    int startCol = (col / 3)*3;
    for (int i=startRow; i < startRow + 3; i++) {
        for (int j=startCol; j < startCol + 3; j++) {
            if (board[i][j] == digit)   return false;
        }
    }
    return true;
}

bool solve(vector<vector<char>> &board) {
    int n = 9;
    for (int i=0; i<n; i++) {
        for (int j=0; j<n; j++) {
            if (board[i][j] == '.') {
                for (char digit = '1'; digit <= '9'; digit++) {
                    if (canPlace(board, i, j, digit)) {
                        board[i][j] = digit;
                        if (solve(board)) {
                            return true;
                        } else {
                            board[i][j] = '.';
                        }
                    }
                }
                return false;
            }
        }
    }
    return true;
}

void solveSudoku(vector<vector<char> >& board) {
    solve(board);
}
```
```
TC: O(9E), where E (<= 81) is the number of empty cells.
As each empty cell can be filled with 1 to 9 digits.
SC: O(E), because of the recursive stack space.
```

### M Coloring Problem
Given an integer M and an undirected graph with N vertices (zero indexed) and E edges. The goal is to determine whether the graph can be coloured with a maximum of M colors so that no two of its adjacent vertices have the same colour applied to them.

In this context, colouring a graph refers to giving each vertex a different colour. If the colouring of vertices is possible then return true, otherwise return false.

```cpp
bool isSafe(int color, int node, vector<int>& colors, vector<int> adj[]) {

    // Check whether any adjacent node
    // is already painted with the same color.
    for (int neighbour : adj[node]) {
        if (colors[neighbour] == color)
            return false;
    }

    return true;
}

bool solve(int node, int m, int n, vector<int>& colors, vector<int> adj[]) {

    // Base Case:
    // All nodes have been successfully colored.
    if (node == n)
        return true;

    // Try every available color for the current node.
    for (int color = 1; color <= m; color++) {

        // Current color doesn't violate graph coloring rules.
        if (isSafe(color, node, colors, adj)) {

            // Choose
            colors[node] = color;

            // Color the remaining nodes.
            if (solve(node + 1, m, n, colors, adj))
                return true;

            // Backtrack
            colors[node] = 0;
        }
    }

    // No valid color assignment found for this node.
    return false;
}

bool graphColoring(vector<vector<int>>& edges, int m, int n) {

    // INTUITION:
    // Color one node at a time.
    //
    // For each node, try every possible color.
    // If a color doesn't conflict with any adjacent node,
    // recursively color the remaining graph.
    //
    // If a choice leads to a dead end,
    // undo it and try the next color.

    // Build adjacency list.
    vector<int> adj[n];

    for (auto edge : edges) {
        adj[edge[0]].push_back(edge[1]);
        adj[edge[1]].push_back(edge[0]);
    }

    // 0 indicates the node is currently uncolored.
    vector<int> colors(n, 0);

    return solve(0, m, n, colors, adj);
}
```

## Contest

### Combinational XOR
Given an array of distinct integers nums and an integer k, return all unique non-empty combinations of elements with a bitwise XOR of k. Return an empty vector if no combinations are possible.
Each element can be used only once in each combination. Two combinations are unique if at least one element is present in only one combination. Answer can be returned in any order.
```cpp
void solve(int idx, int xorSum, vector<int>& curr, vector<vector<int>>& res,
           vector<int>& nums, int k) {

    // If the XOR of the current subset equals k,
    // store the current combination.
    if (xorSum == k && !curr.empty()) {
        res.push_back(curr);
    }

    // Base Case:
    // No more elements left to explore.
    if (idx >= nums.size())
        return;

    // Try every possible next element.
    for (int i = idx; i < nums.size(); i++) {

        // Choose
        curr.push_back(nums[i]);

        // Include current element in the XOR
        solve(i + 1, xorSum ^ nums[i], curr, res, nums, k);

        // Backtrack
        curr.pop_back();
    }
}

vector<vector<int>> combinationXor(vector<int> nums, int k) {

    // INTUITION:
    // Generate every possible subset.
    //
    // Keep track of the XOR of the current subset.
    // Whenever the XOR becomes equal to k,
    // record the current combination.
    //
    // Since every element can either be chosen or skipped,
    // this naturally fits Backtracking.

    vector<vector<int>> res;
    vector<int> curr;

    solve(0, 0, curr, res, nums, k);

    return res;
}
```

### Find Distinct Expressions
Given an integer array nums, return all distinct values obtained by inserting mathematical ' + ' (addition) or ' - ' (subtraction) between each element of nums and evaluating the resulting expression.
Return the results in increasing order.

```cpp
void solve(int idx, int sum, vector<int>& res, vector<int>& nums) {

    // Base Case:
    // We've assigned '+' or '-' to every number.
    // Store the resulting expression value.
    if (idx == nums.size()) {
        res.push_back(sum);
        return;
    }

    // Choice 1:
    // Place a '+' before the current number.
    solve(idx + 1, sum + nums[idx], res, nums);

    // Choice 2:
    // Place a '-' before the current number.
    solve(idx + 1, sum - nums[idx], res, nums);
}

vector<int> distinctExpressions(vector<int>& nums) {

    // INTUITION:
    // The first number is fixed.
    //
    // For every remaining number,
    // we have exactly two choices:
    //   +nums[i]
    //   -nums[i]
    //
    // Explore every possible expression using Backtracking.
    // Finally, remove duplicate expression values.

    vector<int> res;

    // Expression starts with the first number.
    solve(1, nums[0], res, nums);

    // Keep only distinct expression values.
    set<int> uniqueValues(res.begin(), res.end());

    vector<int> ans(uniqueValues.begin(), uniqueValues.end());

    sort(ans.begin(), ans.end());

    return ans;
}
```