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
int maxScore(vector<int>& cardScore, int k) {

    // INTUITION:
    // We must choose exactly k cards from the two ends.
    //
    // There are only k + 1 possibilities:
    // k left + 0 right
    // k-1 left + 1 right
    // ...
    // 0 left + k right
    //
    // Start with all k cards from the left.
    // Then gradually replace left cards with right cards.

    int n = cardScore.size();

    int leftSum = 0;
    int rightSum = 0;
    int maxSum = 0;

    // Start by taking all k cards from the left.
    for (int i = 0; i < k; i++)
        leftSum += cardScore[i];

    maxSum = leftSum;

    // Move one card at a time from left selection to right selection.
    int rightIdx = n - 1;

    for (int i = k - 1; i >= 0; i--) {

        leftSum -= cardScore[i];
        rightSum += cardScore[rightIdx];
        rightIdx--;

        maxSum = max(maxSum, leftSum + rightSum);
    }

    return maxSum;
}
```
```cpp
int maxScore(vector<int>& cardScore, int k) {

    /*
        INTUITION:
        We choose exactly k cards from the two ends.

        The cards we DON'T choose will always form one
        continuous subarray in the middle.

        So instead of maximizing the chosen cards:

            max chosen score
            = total score - minimum middle score

        Middle size = n - k.

        Therefore, find the minimum-sum subarray of size n-k.
    */

    int n = cardScore.size();

    int totalSum = accumulate(cardScore.begin(), cardScore.end(), 0);

    int windowSize = n - k;

    // We are taking every card.
    if (windowSize == 0)
        return totalSum;

    // Find the sum of the first middle window.
    int windowSum = 0;

    for (int i = 0; i < windowSize; i++)
        windowSum += cardScore[i];

    int minWindowSum = windowSum;

    // Slide the middle window across the array.
    for (int right = windowSize; right < n; right++) {

        // Add the new element and remove the old one.
        windowSum += cardScore[right];
        windowSum -= cardScore[right - windowSize];

        minWindowSum = min(minWindowSum, windowSum);
    }

    // Remove the minimum possible middle portion.
    return totalSum - minWindowSum;
}
```

### Longest Substring Without Repeating Characters
```cpp
int longestNonRepeatingSubstring(string& s) {
    // INTUITION:
    // Maintain a window [left...right] with no duplicates.
    // Duplicate -> move left past its previous occurrence.
    // Never move left backwards.

    vector<int> lastSeen(26, -1);

    int left = 0;
    int maxLen = 0;

    for (int right = 0; right < s.size(); right++) {
        int idx = s[right] - 'a';

        // Move left past the previous occurrence if
        // it is inside the current window.
        left = max(left, lastSeen[idx] + 1);

        // Store the latest position of this character.
        lastSeen[idx] = right;

        // Current window = [left ... right]
        maxLen = max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

### Max Consecutive Ones III
```cpp
int longestOnes(vector<int>& nums, int k) {
        // INTUITION:
        // Keep a window with at most k zeros.
        // Expand right to grow the window.
        // If zeros > k, move left until the window becomes valid again.

        int left = 0;
        int zeros = 0;
        int maxLen = 0;

        for (int right = 0; right < nums.size(); right++) {
            // Add current element to the window.
            if (nums[right] == 0) zeros++;

            // Too many zeros -> shrink the window.
            while (zeros > k) {
                if (nums[left] == 0) zeros--;

                left++;
            }

            // Window [left...right] is valid.
            maxLen = max(maxLen, right - left + 1);
        }

        return maxLen;
    }
```

### Atmost 2 distinct elements
```cpp
int totalFruits(vector<int>& fruits) {
    // INTUITION:
    // We need the longest contiguous window containing
    // at most 2 different fruit types.
    //
    // Expand right to grow the window.
    // If we get more than 2 types, shrink from the left.

    unordered_map<int, int> freq;

    int left = 0;
    int maxLen = 0;

    for (int right = 0; right < fruits.size(); right++) {
        // Add current fruit to the window.
        freq[fruits[right]]++;

        // More than 2 fruit types -> shrink window.
        while (freq.size() > 2) {
            freq[fruits[left]]--;

            // Remove fruit type when its count becomes 0.
            if (freq[fruits[left]] == 0) freq.erase(fruits[left]);

            left++;
        }

        // Current window has at most 2 fruit types.
        maxLen = max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

### Atmost K Distinct elements
```cpp
int kDistinctChar(string& s, int k) {
    // INTUITION:
    // Keep a window with at most k distinct characters.
    // Expand right, and shrink left whenever the window
    // contains more than k distinct characters.

    unordered_map<char, int> freq;

    int left = 0;
    int maxLen = 0;

    for (int right = 0; right < s.size(); right++) {
        // Add current character to the window.
        freq[s[right]]++;

        // Too many distinct characters -> shrink window.
        while (freq.size() > k) {
            freq[s[left]]--;

            if (freq[s[left]] == 0) freq.erase(s[left]);

            left++;
        }

        // Window is now valid.
        maxLen = max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

### Longest Repeating Character Replacement
>Given an integer k and a string s, any character in the string can be selected and changed to any other uppercase English character. This operation can be performed up to k times. After completing these steps, return the length of the longest substring that contains the same letter.
```cpp
int characterReplacement(string s, int k) {
    // INTUITION:
    // Keep the most frequent character unchanged and replace
    // all other characters.
    //
    // Replacements needed = window size - maxFreq.
    // Window is valid when replacements needed <= k.
    unordered_map<char, int> freq;  // char → count in window

    int left = 0;
    int maxFreq = 0;     // highest frequency of any char in window
    int maxLength = 0;

    for (int right = 0; right < s.size(); right++) {

        char curr = s[right];

        // expand window
        freq[curr]++;

        // update most frequent character count
        // this is because we try to convert every other character to the most frequent character
        maxFreq = max(maxFreq, freq[curr]);

        // shrink window if replacements needed > k
        // we only target for minimum changes i.e windowLength - maxFrequency
        while ((right - left + 1) - maxFreq > k) {
            freq[s[left]]--;
            left++;
        }

        // valid window → update answer
        maxLength = max(maxLength, right - left + 1);
    }

    return maxLength;
}
```

### Minimum Window Substring
```cpp
string minWindow(string s, string t) {
    // INTUITION:
    // freq stores how many of each character are still required.
    // Expand right until the window contains all characters of t.
    // Once valid, shrink left as much as possible to get the minimum
    // window.

    unordered_map<char, int> freq;

    // Store the required frequency of every character in t.
    for (char ch : t) freq[ch]++;

    int left = 0;
    int matchedCount = 0;
    int minLen = INT_MAX;
    int start = -1;

    for (int right = 0; right < s.size(); right++) {
        // If this character is still required,
        // including it satisfies one required character.
        if (freq[s[right]] > 0) matchedCount++;

        // Add current character to the window.
        freq[s[right]]--;

        // Window contains all characters of t.
        while (matchedCount == t.size()) {
            // Update the minimum window.
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                start = left;
            }

            // Remove left character from the window.
            freq[s[left]]++;

            // If its required frequency becomes positive,
            // the window is no longer valid.
            if (freq[s[left]] > 0) matchedCount--;

            left++;
        }
    }

    // No valid window found.
    if (start == -1) return "";

    return s.substr(start, minLen);
}
```

### Count number of substrings containing all 3 characters
```cpp
int numberOfSubstrings(string s) {
    // INTUITION:
    // Track the latest position of a, b and c.
    //
    // For every right:
    // min(last[a], last[b], last[c]) gives the earliest
    // position that must be included to contain all 3 characters.
    //
    // Therefore, all starting positions from 0 to that position
    // form valid substrings ending at right.

    vector<int> last(3, -1);
    int totalCount = 0;
    for (int right = 0; right < s.size(); right++) {
        // Update the latest position of the current character.
        last[s[right] - 'a'] = right;

        // DRY (s = "abcabc"):
        // i=0 → 'a' → lastSeen = [0,-1,-1]
        // i=1 → 'b' → lastSeen = [0,1,-1]
        // i=2 → 'c' → lastSeen = [0,1,2] ✅

        // If all three characters have appeared,
        // count all valid starting positions.
        if (last[0] != -1 && last[1] != -1 && last[2] != -1) {
            int earliest = min({last[0], last[1], last[2]});

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
    // INTUITION:
    // Count subarrays with sum <= goal.
    //
    // Since nums contains only 0s and 1s, expanding right
    // can only increase the sum, so we can use a sliding window.
    //
    // For every right, once [left...right] is valid,
    // every subarray ending at right and starting from
    // left to right is also valid.

    if (goal < 0) return 0;

    int left = 0;
    int sum = 0;
    int count = 0;

    for (int right = 0; right < nums.size(); right++) {
        // Expand the window.
        sum += nums[right];

        // Window is invalid -> shrink from the left.
        while (sum > goal) {
            sum -= nums[left];
            left++;
        }

        // Valid starting positions:
        // left, left+1, ..., right
        // Number of such subarrays = window size.
        count += right - left + 1;
    }

    return count;
}

int numSubarraysWithSum(vector<int>& nums, int goal) {
    // exactly(goal)
    // = atMost(goal) - atMost(goal - 1)
    return solve(nums, goal) - solve(nums, goal - 1);
}
```

### Number of subarrays with exactly k odd numbers
```cpp
int solve(vector<int>& nums, int k) {
    // INTUITION:
    // Count subarrays with at most k odd numbers.
    //
    // Expand the window with right.
    // If oddCount > k, shrink from the left.
    //
    // Once the window is valid, every subarray ending at right
    // and starting from left to right also has at most k odds.

    if (k < 0) return 0;

    int left = 0;
    int oddCount = 0;
    int totalCount = 0;

    for (int right = 0; right < nums.size(); right++) {
        // Add current element to the window.
        if (nums[right] % 2 != 0) oddCount++;

        // Too many odd numbers -> shrink until valid.
        while (oddCount > k) {
            if (nums[left] % 2 != 0) oddCount--;

            left++;
        }

        // Valid starts = left ... right.
        // Number of valid subarrays ending at right = window size.
        totalCount += right - left + 1;
    }

    return totalCount;
}

int numberOfOddSubarrays(vector<int>& nums, int k) {
    // exactly(k) = atMost(k) - atMost(k - 1)
    return solve(nums, k) - solve(nums, k - 1);
}
```
