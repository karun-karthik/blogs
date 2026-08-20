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
int shortestJobFirst(vector<int>& bt) {

    // INTUITION:
    // SJF always executes the shortest job first.
    // So sort burst times and calculate the waiting time
    // contributed by each previously executed process.

    sort(bt.begin(), bt.end());

    long long waitingTime = 0;
    long long totalWaitingTime = 0;

    for (int burstTime : bt) {
        // Current process waits for all previous processes.
        totalWaitingTime += waitingTime;

        // Current process now contributes to the
        // waiting time of all following processes.
        waitingTime += burstTime;
    }

    // Return floor of average waiting time.
    return totalWaitingTime / bt.size();
}
```

### Job Sequencing Problem
```cpp
vector<int> JobScheduling(vector<vector<int>>& Jobs) {

    /*
        INTUITION:
        Each job takes 1 unit of time and must finish by its deadline.

        To maximize profit:
        1. Pick the highest-profit job first.
        2. Schedule it as late as possible before its deadline.
           This keeps earlier slots available for other jobs.

        Example:
        deadline = 3
        Try slots: 3 → 2 → 1
    */

    int n = Jobs.size();

    // Process the most profitable jobs first.
    sort(Jobs.begin(), Jobs.end(), [](auto& a, auto& b) {
        return a[2] > b[2];
    });

    // Find the latest possible time slot.
    int maxDeadline = 0;
    for (auto& job : Jobs)
        maxDeadline = max(maxDeadline, job[1]);

    // slot[d] stores the job scheduled at time d.
    vector<int> slot(maxDeadline + 1, -1);

    int countJobs = 0;
    int maxProfit = 0;

    for (auto& job : Jobs) {

        int id = job[0];
        int deadline = job[1];
        int profit = job[2];

        // Schedule the job as late as possible.
        for (int d = deadline; d > 0; d--) {

            if (slot[d] == -1) {

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

// Maximum non-overlapping → sort by end time → keep earliest finishing.
### N Meeting in One Room
```cpp
int maxMeetings(vector<int>& start, vector<int>& end) {

    /*
        INTUITION:
        To attend the maximum number of meetings,
        always choose the meeting that finishes earliest.

        Why?
        An earlier finishing meeting leaves more time for
        the remaining meetings.

        So:
        1. Sort meetings by end time.
        2. Pick a meeting if its start time is after
           the end of the previously selected meeting.
    */

    vector<pair<int, int>> meetings;

    for (int i = 0; i < start.size(); i++)
        meetings.push_back({start[i], end[i]});

    // Earliest finishing meeting first.
    sort(meetings.begin(), meetings.end(),
         [](auto& a, auto& b) {
             return a.second < b.second;
         });

    int count = 1;
    int prevEnd = meetings[0].second;

    for (int i = 1; i < meetings.size(); i++) {

        // Meeting must start after the previous one ends.
        if (meetings[i].first > prevEnd) {
            count++;
            prevEnd = meetings[i].second;
        }
    }

    return count;
}
```

// Minimum removals = Total intervals - Maximum non-overlapping intervals.
### Minimum Removals to make Intervals Non-overlapping
```cpp
int MaximumNonOverlappingIntervals(vector<vector<int>>& intervals) {
    /*
        INTUITION:
        We want to remove the minimum number of overlapping intervals.
        Equivalently, keep the maximum number of non-overlapping intervals.

        Greedy choice:
        Always keep the interval that ends earliest.
        This leaves the most room for future intervals.

        Answer = total intervals - maximum non-overlapping intervals.
    */

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
vector<vector<int>> insertNewInterval(vector<vector<int>>& intervals,
                                        vector<int>& newInterval) {
    /*
        INTUITION:
        Since intervals are already sorted and non-overlapping,
        process them in 3 parts:

        1. BEFORE → current.end < new.start → add directly
        2. OVERLAP → current.start <= new.end → merge
        3. AFTER → add everything remaining

        DRY:
        intervals = [[1,3], [6,9]]
        newInterval = [2,5]

        BEFORE:
        [1,3] is not before [2,5] because 3 >= 2.

        OVERLAP:
        [1,3] overlaps [2,5]
        → merge → [1,5]

        AFTER:
        [6,9] does not overlap [1,5]
        → add it directly

        Result = [[1,5], [6,9]]
    */

    vector<vector<int>> result;
    int i = 0;
    int n = intervals.size();

    // 1. Add intervals completely before newInterval.
    while (i < n && intervals[i][1] < newInterval[0]) {
        result.push_back(intervals[i]);
        i++;
    }

    // 2. Merge all overlapping intervals.
    while (i < n && intervals[i][0] <= newInterval[1]) {
        newInterval[0] = min(newInterval[0], intervals[i][0]);
        newInterval[1] = max(newInterval[1], intervals[i][1]);

        i++;
    }

    // Add the final merged interval.
    result.push_back(newInterval);

    // 3. Add intervals completely after newInterval.
    while (i < n) {
        result.push_back(intervals[i]);
        i++;
    }

    return result;
}
```

### Minimum number of platforms required for railways
```cpp
int findPlatform(vector<int>& Arrival, vector<int>& Departure) {

    /*
        INTUITION:
        We need the maximum number of trains present at the station
        at the same time.

        Sort arrivals and departures separately.
        Then process them like a timeline:

        Arrival  → need a platform  → count++
        Departure → free a platform → count--

        The maximum value of count is the answer.

        DRY:
        Arrival   = [900, 940, 950, 1100]
        Departure = [910, 1200, 1120, 1130]

        After sorting:
        Arrival   = [900, 940, 950, 1100]
        Departure = [910, 1120, 1130, 1200]

        900  → arrival   → count = 1
        910  → departure → count = 0
        940  → arrival   → count = 1
        950  → arrival   → count = 2
        1100 → arrival   → count = 3
        1120 → departure → count = 2
        ...
        
        Maximum platforms needed = 3
    */

    int n = Arrival.size();

    // Sort both event types independently.
    sort(Arrival.begin(), Arrival.end());
    sort(Departure.begin(), Departure.end());

    int arrive = 0;
    int depart = 0;

    int platforms = 0;
    int maxPlatforms = 0;

    while (arrive < n) {

        // If arrival happens first then we need a platform, 
        // If departure happens first then we do not need a platform
        // arrive at same time as departure, then we still need a platform
        if (Arrival[arrive] <= Departure[depart]) {
            platforms++;
            arrive++;
        } else {
            platforms--;
            depart++;
        }

        maxPlatforms = max(maxPlatforms, platforms);
    }

    return maxPlatforms;
}
```

### Valid Parenthesis
```cpp
bool isValid(string s) {

    /*
        INTUITION:
        '*' can be '(', ')' or empty.

        So instead of deciding what '*' is immediately,
        maintain a RANGE of possible open brackets:

        low  = minimum possible open brackets
        high = maximum possible open brackets

        '(' → both increase
        ')' → both decrease
        '*' → low decreases, high increases

        If high < 0, even the maximum possibility has
        too many closing brackets → invalid.

        At the end, low must be 0 so that at least one
        valid interpretation has all brackets balanced.
    */

    int low = 0;
    int high = 0;

    for (char c : s) {

        if (c == '(') {
            low++;
            high++;
        }
        else if (c == ')') {
            low--;
            high--;
        }
        else { // '*'
            low--;      // '*' acts as ')'
            high++;     // '*' acts as '('
        }

        // Even the maximum possible open brackets is negative.
        if (high < 0)
            return false;

        // We cannot have fewer than 0 open brackets.
        low = max(0, low);
    }

    // low == 0 means some interpretation can be balanced.
    return low == 0;
}
```

### Candy Problem ~ LeetCode 135
```cpp
int candy(vector<int>& ratings) {
    int n = ratings.size();

    // INTUITION:
    // Start with 1 candy for everyone.
    // Left pass satisfies the left-neighbour condition.
    // Right pass satisfies the right-neighbour condition.
    // Take the larger requirement because both conditions must hold.

    vector<int> candies(n, 1);

    // Higher than left neighbour -> need one more candy.
    for (int i = 1; i < n; i++) {
        if (ratings[i] > ratings[i - 1]) {
            candies[i] = candies[i - 1] + 1;
        }
    }

    // Higher than right neighbour -> need one more candy.
    // Keep the larger value because the left requirement
    // may already be greater.
    for (int i = n - 2; i >= 0; i--) {
        if (ratings[i] > ratings[i + 1]) {
            candies[i] = max(candies[i], candies[i + 1] + 1);
        }
    }

    return accumulate(candies.begin(), candies.end(), 0);
}
```