# Fundamentals
### Decision Flow
```
1. Is it optimization (min/max)?
   ↓
2. Can sorting simplify?
   ↓
3. Can I make a local best choice?
   ↓
4. Will that never hurt future choices?
   ↓
YES → Greedy
NO  → Try DP / Backtracking
```

### Common Pitfalls

1. **Greedy Choice Property** → Ensure local optimum leads to global optimum
2. **Optimal Substructure** → Ensure solution to subproblems combine to form global solution
3. **Overlapping Subproblems** → May need DP instead of greedy
4. **Greedy vs DP** → Greedy makes irrevocable choices; DP explores all
5. **Edge Cases** → Empty input, single element, all same values, constraints

# Problems

### Assign Cookies
```cpp
int findMaximumCookieStudents(vector<int>& Student, vector<int>& Cookie){

    // Sort both arrays:
    // Student → greed (minimum cookie size required)
    // Cookie  → available cookie sizes
    // Sorting enables greedy matching (smallest need with smallest valid cookie)
    sort(Student.begin(), Student.end());
    sort(Cookie.begin(), Cookie.end());

    int s = Student.size();
    int c = Cookie.size();

    int i = 0; // pointer for students (least greedy first)
    int j = 0; // pointer for cookies (smallest first)

    // Traverse both arrays
    while (i < s && j < c) {

        // If current cookie satisfies current student's greed
        if (Cookie[j] >= Student[i]) {
            // Assign cookie → move to next student and next cookie
            i++;
            j++;
        } else {
            // Cookie too small → try next larger cookie
            j++;
        }
    }

    // i = number of students successfully assigned cookies
    return i;
}
```

### Lemonade Change
```cpp
bool lemonadeChange(vector<int>& bills){

    int five = 0, ten = 0; // track available change

    for (int bill : bills) {

        if (bill == 5) {
            // No change needed → just collect
            five++;

        } else if (bill == 10) {
            // Need to give back $5
            if (five == 0) return false;

            five--;   // give one $5
            ten++;    // collect one $10

        } else { // bill == 20

            // Need to give back $15
            // Prefer giving (10 + 5) instead of (5 + 5 + 5)
            // → saves $5 bills for future transactions

            if (ten > 0 && five > 0) {
                ten--;   // give one $10
                five--;  // give one $5
            }
            else if (five >= 3) {
                five -= 3; // give three $5 bills
            }
            else {
                // Not enough change
                return false;
            }
        }
    }

    return true;
}
```

### Can Jump
```cpp
bool canJump(vector<int>& nums) {

    int maxIdx = 0;  // farthest index we can reach so far

    for (int i = 0; i < nums.size(); i++) {

        // If current index is beyond reachable range → stuck
        if (i > maxIdx)
            return false;

        // Update the farthest reachable index
        // either keep previous max or jump from current index
        maxIdx = max(maxIdx, i + nums[i]);

        // Optimization: if we can already reach the end, stop early
        if (maxIdx >= nums.size() - 1)
            return true;
    }

    // If we never got stuck → end is reachable
    return true;
}
```

### Shortest Job First
```cpp
int shortestJobFirst(vector<int>& burstTime) {

    int n = burstTime.size();

    // Sort jobs by burst time (shortest first)
    sort(burstTime.begin(), burstTime.end());

    int totalWaitTime = 0;
    int currentTime = 0; // time when current job starts

    for (int i = 0; i < n; i++) {

        // Wait time for current job = time it starts
        totalWaitTime += currentTime;

        // Update current time after this job finishes
        currentTime += burstTime[i];
    }

    // Average wait time
    return totalWaitTime / n;
}
```

### Job Sequencing Problem
```cpp
vector<int> JobScheduling(vector<vector<int>>& jobs) {

    int n = jobs.size();

    // Step 1: Sort jobs by profit (descending)
    sort(jobs.begin(), jobs.end(), [](auto &a, auto &b) {
        return a[2] > b[2];
    });

    // Step 2: Find maximum deadline
    int maxDeadline = 0;
    for (auto &job : jobs)
        maxDeadline = max(maxDeadline, job[1]);

    // Slot array to track occupied time slots (-1 = free)
    vector<int> slot(maxDeadline + 1, -1);

    int countJobs = 0, maxProfit = 0;

    // Step 3: Assign jobs
    for (auto &job : jobs) {

        int id = job[0];
        int deadline = job[1];
        int profit = job[2];

        // Try placing job in latest available slot ≤ deadline
        for (int d = deadline; d > 0; d--) {

            if (slot[d] == -1) { // slot is free
                slot[d] = id;
                countJobs++;
                maxProfit += profit;
                break;
            }
        }
    }

    return {countJobs, maxProfit};
}
```

### N Meeting in One Room
```cpp
int maxMeetings(vector<int>& start, vector<int>& end){

    int n = start.size();

    // Combine start & end into one structure
    vector<vector<int>> meetings;
    for (int i = 0; i < n; i++) {
        meetings.push_back({start[i], end[i]});
    }

    // Sort by end time (earliest finishing meeting first)
    // If tie → pick earlier start (not mandatory, but safe)
    sort(meetings.begin(), meetings.end(), [](const vector<int>& a, const vector<int>& b) {
        if (a[1] == b[1]) return a[0] < b[0];
        return a[1] < b[1];
    });

    int count = 1;  // first meeting always selected
    int lastEndTime = meetings[0][1];

    // Greedily pick next non-overlapping meetings
    for (int i = 1; i < n; i++) {
        // If current meeting starts AFTER last selected meeting ends
        if (meetings[i][0] > lastEndTime) {
            count++;                         // select this meeting
            lastEndTime = meetings[i][1];   // update boundary
        }
    }

    return count;
}
```

### Minimum Removals to make Intervals Non-overlapping
```cpp
int MaximumNonOverlappingIntervals(vector<vector<int>>& intervals) {

    int n = intervals.size();

    // Step 1: Sort intervals by end time (greedy choice)
    sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) {
        return a[1] < b[1];
    });

    int count = 1;                     // number of non-overlapping intervals selected
    int lastEnd = intervals[0][1];     // end time of last selected interval

    // Step 2: Select maximum non-overlapping intervals
    for (int i = 1; i < n; i++) {

        // If current interval starts after or exactly at last end → no overlap
        if (intervals[i][0] >= lastEnd) {

            count++;                        // include this interval
            lastEnd = intervals[i][1];      // update boundary
        }
    }

    // Step 3: Minimum removals = total - non-overlapping selected
    return n - count;
}
```

### Insert Interval
```cpp
vector<vector<int>> insertNewInterval(vector<vector<int>>& intervals, vector<int>& newInterval) {

    vector<vector<int>> result;
    int i = 0, n = intervals.size();

    // DRY: intervals = [[1,3],[6,9]], new = [2,5]

    // 1. Add all intervals completely before newInterval
    // condition: end < new.start
    while (i < n && intervals[i][1] < newInterval[0]) {
        result.push_back(intervals[i]);   // DRY: none added
        i++;
    }

    // 2. Merge overlapping intervals
    // condition: start <= new.end
    while (i < n && intervals[i][0] <= newInterval[1]) {

        // expand newInterval to cover overlap
        newInterval[0] = min(newInterval[0], intervals[i][0]); // DRY: 2→1
        newInterval[1] = max(newInterval[1], intervals[i][1]); // DRY: 5→5

        i++; // DRY: i moves past [1,3]
    }

    // add merged interval
    result.push_back(newInterval); // DRY: [1,5]

    // 3. Add remaining intervals (after merge)
    while (i < n) {
        result.push_back(intervals[i]);   // DRY: [6,9]
        i++;
    }

    // DRY result = [[1,5],[6,9]]
    return result;
}
```

### Minimum number of platforms required for railways
```cpp
int findPlatform(vector<int>& Arrival, vector<int>& Departure) {
    int n = Arrival.size();

    // Sort arrival and departure times separately
    // This lets us simulate timeline events
    sort(Arrival.begin(), Arrival.end());
    sort(Departure.begin(), Departure.end());

    int count = 0;     // current platforms needed
    int maxCount = 0;  // maximum platforms needed at any time

    int arrive = 0, departure = 0;

    while (arrive < n) {

        // If next event is arrival → need new platform
        if (Arrival[arrive] <= Departure[departure]) {
            count++;        // train arrives → occupy platform
            arrive++;       // move to next arrival
        } else {
            count--;        // train departs → free platform
            departure++;    // move to next departure
        }

        // Track peak platforms needed
        maxCount = max(maxCount, count);
    }

    return maxCount;
}
```

### Valid Parenthesis
```cpp
bool isValid(string s) {
    int low = 0;   // minimum open brackets possible
    int high = 0;  // maximum open brackets possible

    for (char c : s) {

        if (c == '(') {
            low++;      // must open
            high++;
        } else if (c == ')') {
            low--;      // close one if possible
            high--;
        } else { // '*'
            low--;      // treat as ')'
            high++;     // or treat as '('
        }

        // high < 0 → too many ')' → invalid
        if (high < 0) return false;

        // low should never go below 0
        // (we can't have negative open brackets)
        if (low < 0) low = 0;
    }

    // valid if we can close all opens
    return low == 0;
}
```

### Candy Problem ~ LeetCode 135
```cpp
int candy(vector<int>& ratings) {

    int n = ratings.size();
    vector<int> candies(n, 1); // each child gets at least 1

    // Left → Right pass
    // ensure: rating[i] > rating[i-1]
    for (int i = 1; i < n; i++) {
        if (ratings[i] > ratings[i - 1])
            candies[i] = candies[i - 1] + 1;
    }

    // Right → Left pass
    // ensure: rating[i] > rating[i+1]
    for (int i = n - 2; i >= 0; i--) {
        if (ratings[i] > ratings[i + 1])
            candies[i] = max(candies[i], candies[i + 1] + 1);
    }

    // Sum all candies
    int total = 0;
    for (int c : candies) total += c;

    // DRY:
    // ratings = [1,0,2]
    // L→R: [1,1,2]
    // R→L: [2,1,2]
    // sum = 5

    return total;
}
```