# Fundamentals

Sliding Window is an optimization technique used to reduce nested loops (O(n²)) into linear time (O(n)) by maintaining a window (subarray/substring) that slides over data.

### When to Use Sliding Window

* Contiguous subarray / substring
* “Longest / shortest / count / max / min”
* Fixed size k OR variable size

### How to Identify Sliding Window

1. Is it contiguous? → YES
2. Need optimal (min/max/longest)? → YES
3. Can we avoid recomputation? → YES
→ Sliding Window

### Maximum Points You Can Obtain from Cards
>Given N cards arranged in a row, each card has an associated score denoted by the cardScore array. Choose exactly k cards. In each step, a card can be chosen either from the beginning or the end of the row. The score is the sum of the scores of the chosen cards.
Return the maximum score that can be obtained.
```cpp
int maxScore(vector<int>& cardScore , int k){

    int n = cardScore.size();

    int leftSum = 0;   // sum of first k elements (taking all from left)
    int rightSum = 0;  // sum of elements taken from right
    int maxSum = 0;

    // Step 1: Take all k cards from left initially
    for (int i = 0; i < k; i++) {
        leftSum += cardScore[i];
    }

    maxSum = leftSum;

    // DRY:
    // [1,2,3,4,5,6,1], k=3
    // leftSum = 1+2+3 = 6

    int rightIdx = n - 1;

    // Step 2: Gradually move window:
    // remove from left, add from right
    for (int i = k - 1; i >= 0; i--) {

        leftSum -= cardScore[i];           // remove one from left
        rightSum += cardScore[rightIdx];   // add one from right
        rightIdx--;

        // check max of all combinations
        maxSum = max(maxSum, leftSum + rightSum);

        // DRY:
        // remove 3, add 1 → sum = 1+2 + 1 = 4
        // remove 2, add 6 → sum = 1 + (1+6) = 8
        // remove 1, add 5 → sum = (1+6+5) = 12 ← max
    }

    return maxSum;
}
```

### Longest Substring Without Repeating Characters
```cpp
int longestNonRepeatingSubstring(string& s) {

    int n = s.size();

    int lastSeen[256];  // lastSeen[ch] = last index where 'ch' appeared

    // initialize → character not seen yet
    for (int i = 0; i < 256; i++) {
        lastSeen[i] = -1;
    }

    int windowStart = 0;   // left boundary of current window
    int maxLength = 0;     // answer

    for (int windowEnd = 0; windowEnd < n; windowEnd++) {

        char currentChar = s[windowEnd];

        // if character was seen before, shrink window
        if (lastSeen[currentChar] != -1) {
            windowStart = max(windowStart, lastSeen[currentChar] + 1);
        }

        // update maximum length
        int currentLength = windowEnd - windowStart + 1;
        maxLength = max(maxLength, currentLength);

        // update last seen index
        lastSeen[currentChar] = windowEnd;
    }

    return maxLength;
}
```

### Max Consecutive Ones III
```cpp
int longestOnes(vector<int>& nums, int k) {
    int left = 0;          // window start
    int zeros = 0;         // count of zeros in current window
    int maxLen = 0;

    for (int right = 0; right < nums.size(); right++) {

        // expand window → include nums[right]
        if (nums[right] == 0)
            zeros++;

        // shrink window if more than k zeros
        while (zeros > k) {
            if (nums[left] == 0)
                zeros--;
            left++;
        }

        // window is valid here (zeros <= k)
        maxLen = max(maxLen, right - left + 1);

        // DRY:
        // nums = [1,1,1,0,0,0,1,1,1], k=2
        // expand → zeros=3 → shrink → valid window
    }

    return maxLen;
}
```

### Atmost 2 distinct elements
```cpp
int totalFruits(vector<int>& fruits){

    unordered_map<int, int> freq;  // fruit → count in current window

    int windowStart = 0;
    int maxLength = 0;

    int k = 2; // atmost 2 distinct elements

    for (int windowEnd = 0; windowEnd < fruits.size(); windowEnd++) {

        // expand window → include current fruit
        freq[fruits[windowEnd]]++;

        // shrink window if more than 2 distinct fruits
        while (freq.size() > k) {

            freq[fruits[windowStart]]--;

            // remove fruit completely if count becomes 0
            if (freq[fruits[windowStart]] == 0) {
                freq.erase(fruits[windowStart]);
            }

            windowStart++;
        }

        // valid window (≤ 2 types)
        maxLength = max(maxLength, windowEnd - windowStart + 1);

        // DRY:
        // fruits = [1,2,1,2,3]
        // window expands → {1,2}
        // add 3 → shrink → remove 1 → valid again
    }

    return maxLength;
}
```

### Atmost K Distinct elements
```cpp
int kDistinctChar(string& s, int k) {

    int n = s.size();

    unordered_map<char, int> freq;  // character → count in window

    int windowStart = 0;
    int maxLength = 0;

    for (int windowEnd = 0; windowEnd < n; windowEnd++) {

        // expand window → include current character
        freq[s[windowEnd]]++;

        // shrink window until valid (≤ k distinct chars)
        while (freq.size() > k) {

            freq[s[windowStart]]--;

            // remove char completely if count becomes 0
            if (freq[s[windowStart]] == 0)
                freq.erase(s[windowStart]);

            windowStart++;
        }

        // valid window → update answer
        maxLength = max(maxLength, windowEnd - windowStart + 1);

        // DRY:
        // s = "eceba", k = 2
        // window grows: "ece" → valid
        // add 'b' → shrink → "ceb"
    }

    return maxLength;
}
```

### Longest Repeating Character Replacement
>Given an integer k and a string s, any character in the string can be selected and changed to any other uppercase English character. This operation can be performed up to k times. After completing these steps, return the length of the longest substring that contains the same letter.
```cpp
int characterReplacement(string s, int k) {

    unordered_map<char, int> freq;  // char → count in window

    int windowStart = 0;
    int maxFreq = 0;     // highest frequency of any char in window
    int maxLength = 0;

    for (int windowEnd = 0; windowEnd < s.size(); windowEnd++) {

        char curr = s[windowEnd];

        // expand window
        freq[curr]++;

        // update most frequent character count
        // this is because we try to convert every other character to the most frequent character
        maxFreq = max(maxFreq, freq[curr]);

        // shrink window if replacements needed > k
        // we only target for minimum changes i.e windowLength - maxFrequency
        while ((windowEnd - windowStart + 1) - maxFreq > k) {

            freq[s[windowStart]]--;
            if (freq[s[windowStart]] == 0)
                freq.erase(s[windowStart]);

            windowStart++;
        }

        // valid window → update answer
        maxLength = max(maxLength, windowEnd - windowStart + 1);
    }

    return maxLength;
}
```

### Minimum Window Substring
```cpp
string minWindow(string s, string t) {

    unordered_map<char, int> freq;  
    // freq[c] = how many more of 'c' we still need

    // build requirement map
    for (char c : t) {
        freq[c]++;
    }

    int windowStart = 0;
    int minLength = INT_MAX;
    int startIndex = -1;

    int matchedCount = 0;  
    // total characters from 't' matched so far (including duplicates)

    for (int windowEnd = 0; windowEnd < s.size(); windowEnd++) {

        char curr = s[windowEnd];

        // if curr is still needed, it contributes to match
        if (freq[curr] > 0)
            matchedCount++;

        // include curr in window (may go negative if extra)
        freq[curr]--;

        // when all characters of t are matched
        while (matchedCount == t.size()) {

            // update smallest valid window
            if (windowEnd - windowStart + 1 < minLength) {
                minLength = windowEnd - windowStart + 1;
                startIndex = windowStart;
            }

            char leftChar = s[windowStart];

            // remove leftChar from window → restore its requirement
            freq[leftChar]++;

            // if it becomes > 0, we just removed a required char
            // → window is no longer valid
            if (freq[leftChar] > 0)
                matchedCount--;

            windowStart++; // shrink window
        }
    }

    return startIndex == -1 ? "" : s.substr(startIndex, minLength);
}
```

### Count number of substrings containing all 3 characters
```cpp
int numberOfSubstrings(string s) {

    vector<int> lastSeen(3, -1);  
    // lastSeen[i] = last index where ('a' + i) appeared

    int totalCount = 0;

    for (int i = 0; i < s.size(); i++) {

        // update last seen index
        lastSeen[s[i] - 'a'] = i;

        // DRY (s = "abcabc"):
        // i=0 → 'a' → lastSeen = [0,-1,-1]
        // i=1 → 'b' → lastSeen = [0,1,-1]
        // i=2 → 'c' → lastSeen = [0,1,2] ✅

        if (lastSeen[0] != -1 && lastSeen[1] != -1 && lastSeen[2] != -1) {

            int earliest = min({lastSeen[0], lastSeen[1], lastSeen[2]});

            // DRY:
            // i=2 → earliest=0 → +1  → total=1
            // i=3 → lastSeen=[3,1,2] → earliest=1 → +2 → total=3
            // i=4 → lastSeen=[3,4,2] → earliest=2 → +3 → total=6
            // i=5 → lastSeen=[3,4,5] → earliest=3 → +4 → total=10

            totalCount += (earliest + 1);
        }
    }

    // DRY final answer for "abcabc" = 10
    return totalCount;
}
```

### Number of subarrays with sum = goal on a binary array
```cpp
int solve(vector<int>& nums, int goal) {
    // counts subarrays with sum ≤ goal
    if (goal < 0) return 0;  // edge case

    int windowStart = 0;
    int currentSum = 0;
    int totalCount = 0;

    for (int windowEnd = 0; windowEnd < nums.size(); windowEnd++) {

        currentSum += nums[windowEnd];

        // shrink window until sum ≤ goal
        while (currentSum > goal) {
            currentSum -= nums[windowStart];
            windowStart++;
        }

        // all subarrays ending at windowEnd with start in [windowStart → windowEnd]
        // are valid → count = window size
        totalCount += (windowEnd - windowStart + 1);

        // DRY:
        // nums = [1,0,1], goal=2
        // window expands → count valid subarrays ending at each index
    }

    return totalCount;
}

int numSubarraysWithSum(vector<int>& nums, int goal) {
    // exactly(goal) = atMost(goal) - atMost(goal-1)
    return solve(nums, goal) - solve(nums, goal - 1);
}
```

### Number of subarrays with exactly k odd numbers
```cpp
int solve(vector<int>& nums, int k) {
    // counts subarrays with at most k odd numbers
    if (k < 0) return 0;

    int windowStart = 0;
    int oddCount = 0;
    int totalCount = 0;

    for (int windowEnd = 0; windowEnd < nums.size(); windowEnd++) {

        if (nums[windowEnd] % 2 != 0)
            oddCount++;

        // shrink window if more than k odd numbers
        while (oddCount > k) {
            if (nums[windowStart] % 2 != 0)
                oddCount--;
            windowStart++;
        }

        // all subarrays ending at windowEnd with start in [windowStart → windowEnd]
        // have ≤ k odd numbers → count = window size
        totalCount += (windowEnd - windowStart + 1);
    }

    return totalCount;
}

int numberOfOddSubarrays(vector<int>& nums, int k) {
    // exactly(k) = atMost(k) - atMost(k-1)
    return solve(nums, k) - solve(nums, k - 1);
}
```
