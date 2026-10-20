# Fundamentals

### Stack using Arrays
```cpp
class ArrayStack {
private:
    vector<int> data;

public:
    ArrayStack() {}

    // Push element onto stack
    void push(int value) {
        data.push_back(value);
    }

    // Remove and return top element
    int pop() {
        if (isEmpty()) {
            throw runtime_error("Stack Underflow");
        }

        int topValue = data.back();
        data.pop_back();
        return topValue;
    }

    // Return top element without removing
    int top() {
        if (isEmpty()) {
            throw runtime_error("Stack is Empty");
        }

        return data.back();
    }

    // Check if stack is empty
    bool isEmpty() {
        return data.empty();
    }

    // Optional: size of stack
    int size() {
        return data.size();
    }
};
```

### Queue using Arrays
```cpp
class ArrayQueue {
private:
    vector<int> data;
    int frontIndex, rearIndex;
    int currentSize, capacity;

public:
    ArrayQueue(int size = 10) {
        capacity = size;
        data.resize(capacity);

        frontIndex = 0;
        rearIndex = -1;
        currentSize = 0;
    }

    // Insert element
    void push(int value) {

        if (currentSize == capacity) {
            throw runtime_error("Queue Overflow");
        }

        rearIndex = (rearIndex + 1) % capacity;
        data[rearIndex] = value;
        currentSize++;
    }

    // Remove element
    int pop() {

        if (isEmpty()) {
            throw runtime_error("Queue Underflow");
        }

        int value = data[frontIndex];

        frontIndex = (frontIndex + 1) % capacity;
        currentSize--;

        return value;
    }

    // Get front element
    int peek() {

        if (isEmpty()) {
            throw runtime_error("Queue is Empty");
        }

        return data[frontIndex];
    }

    // Check empty
    bool isEmpty() {
        return currentSize == 0;
    }

    // Optional
    int size() {
        return currentSize;
    }
};
```

### Stack using Queue
```cpp
class QueueStack {
private:
    queue<int> q;

public:
    QueueStack() {}

    // Push element onto stack
    void push(int value) {

        int size = q.size();

        q.push(value);

        /*
        Rotate previous elements behind new element
        So newest element comes to front
        */
        for (int i = 0; i < size; i++) {
            q.push(q.front());
            q.pop();
        }
    }

    // Remove top element
    int pop() {

        if (isEmpty()) {
            throw runtime_error("Stack Underflow");
        }

        int topValue = q.front();
        q.pop();
        return topValue;
    }

    // Get top element
    int top() {

        if (isEmpty()) {
            throw runtime_error("Stack is Empty");
        }

        return q.front();
    }

    bool isEmpty() {
        return q.empty();
    }
};
```

### Queue using Stack
```cpp
class StackQueue {
private:
    stack<int> inStack, outStack;

    // Move elements only when needed
    void transfer() {
        while (!inStack.empty()) {
            outStack.push(inStack.top());
            inStack.pop();
        }
    }

public:
    StackQueue() {}

    // Push → always goes to inStack
    void push(int x) {
        inStack.push(x);
    }

    // Pop → from outStack
    int pop() {

        if (isEmpty()) {
            throw runtime_error("Queue Underflow");
        }

        if (outStack.empty()) {
            transfer();
        }

        int val = outStack.top();
        outStack.pop();
        return val;
    }

    // Peek → front element
    int peek() {

        if (isEmpty()) {
            throw runtime_error("Queue is Empty");
        }

        if (outStack.empty()) {
            transfer();
        }

        return outStack.top();
    }

    bool isEmpty() {
        return inStack.empty() && outStack.empty();
    }
};
```

### Stack using Linkedlist
```cpp
class LinkedListStack {
private:
    struct Node {
        int val;
        Node* next;
        Node(int v, Node* n = nullptr) : val(v), next(n) {}
    };

    Node* head;   // top of stack
    int sz;       // optional: track size

public:
    LinkedListStack() : head(nullptr), sz(0) {}

    // Push → insert at head
    void push(int x) {
        head = new Node(x, head);
        sz++;
    }

    // Pop → remove from head
    int pop() {
        if (isEmpty()) {
            throw runtime_error("Stack Underflow");
        }
        Node* temp = head;
        int value = temp->val;

        head = head->next;
        delete temp;        // avoid memory leak
        sz--;

        return value;
    }

    // Top → read head value
    int top() {
        if (isEmpty()) {
            throw runtime_error("Stack is Empty");
        }
        return head->val;
    }

    bool isEmpty() {
        return head == nullptr;
    }

    int size() {
        return sz;
    }

    // Destructor → free memory
    ~LinkedListStack() {
        while (head) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }
};
```

### Queue using Linkedlist
```cpp
class LinkedListQueue {
private:
    struct Node {
        int val;
        Node* next;
        Node(int v) : val(v), next(nullptr) {}
    };

    Node* frontPtr;   // points to front element (dequeue from here)
    Node* rearPtr;    // points to last element (enqueue here)
    int sz;

public:
    LinkedListQueue() {
        frontPtr = nullptr;
        rearPtr = nullptr;
        sz = 0;
    }

    // Enqueue → insert at rear
    void push(int x) {
        Node* newNode = new Node(x);

        if (isEmpty()) {
            frontPtr = rearPtr = newNode;
        } else {
            rearPtr->next = newNode;
            rearPtr = newNode;
        }

        sz++;
    }

    // Dequeue → remove from front
    int pop() {
        if (isEmpty()) {
            throw runtime_error("Queue Underflow");
        }

        Node* temp = frontPtr;
        int value = temp->val;

        frontPtr = frontPtr->next;

        // If queue becomes empty → reset rear
        if (frontPtr == nullptr) {
            rearPtr = nullptr;
        }

        delete temp;
        sz--;

        return value;
    }

    // Peek → front element
    int peek() {
        if (isEmpty()) {
            throw runtime_error("Queue is Empty");
        }

        return frontPtr->val;
    }

    bool isEmpty() {
        return frontPtr == nullptr;
    }

    int size() {
        return sz;
    }

    // Destructor to avoid memory leaks
    ~LinkedListQueue() {
        while (!isEmpty()) {
            pop();
        }
    }
};
```

### Balanced Paranthesis
```cpp
class Solution {
public:
    bool isValid(string str) {

        stack<char> st;

        for (char ch : str) {

            // If opening bracket → push
            if (ch == '(' || ch == '{' || ch == '[') {
                st.push(ch);
            }
            else {
                // If stack empty → no matching opening
                if (st.empty()) return false;

                char top = st.top();
                st.pop();

                // Check matching pair
                if ((ch == ')' && top != '(') ||
                    (ch == '}' && top != '{') ||
                    (ch == ']' && top != '[')) {
                    return false;
                }
            }
        }

        // Stack must be empty for valid string
        return st.empty();
    }
};
```

# Important: Monotonic stack

### Next Greater Element
> Use a monotonic decreasing stack while traversing from right to efficiently find next greater elements in O(N).
```cpp
vector<int> nextLargerElement(vector<int> arr) {

    int n = arr.size();
    vector<int> ans(n);

    stack<int> st;  // stores elements

    for (int i = n - 1; i >= 0; i--) {

        // Remove all smaller or equal elements
        while (!st.empty() && st.top() <= arr[i]) {
            st.pop();
        }

        // If stack empty → no greater element
        if (st.empty()) {
            ans[i] = -1;
        } else {
            ans[i] = st.top();
        }

        // Push current element
        st.push(arr[i]);
    }

    return ans;
}
```

### Next Greater Element-2
```cpp
vector<int> nextGreaterElements(vector<int> &arr) {

    int n = arr.size();
    vector<int> ans(n, -1);
    stack<int> st;  // stores candidates for next greater (values)

    /* Traverse twice (right → left) to simulate circular array.
        First pass helps build the stack, second pass fills answers */
    for (int i = 2 * n - 1; i >= 0; i--) {

        int curr = arr[i % n];  // wrap around using modulo

        // Maintain a decreasing stack:
        // remove all elements <= current, as they can't be next greater
        while (!st.empty() && st.top() <= curr) {
            st.pop();
        }

        // Fill answer only for real indices (second half of traversal)
        if (i < n) {
            if (!st.empty()) {
                ans[i] = st.top();  // next greater element
            }
            // else remains -1 (no greater element exists)
        }

        // Push current element as a future candidate
        st.push(curr);
    }

    return ans;
}
```

### Asteroid Collision
```cpp
vector<int> asteroidCollision(vector<int>& asteroids) {

    /*
        INTUITION:
        The stack stores asteroids that are still alive.

        A collision is possible only when:
            stack top > 0  → moving right
            current < 0    → moving left

        If they collide:
            smaller asteroid → destroyed
            equal asteroids   → both destroyed
            larger asteroid   → survives and may collide again
        
        * Stack empty → nothing to collide with.
        * Top is negative → same direction, no collision.
        * Therefore → current negative asteroid survives.
    */

    vector<int> st;

    for (int asteroid : asteroids) {

        // Positive asteroid moves right, so it cannot
        // collide with anything currently behind it.
        if (asteroid > 0) {
            st.push_back(asteroid);
            continue;
        }

        // Current asteroid is moving left.
        // Keep destroying smaller right-moving asteroids.
        while (!st.empty() &&
               st.back() > 0 &&
               st.back() < abs(asteroid)) {

            st.pop_back();
        }

        // Equal sizes → both asteroids are destroyed.
        if (!st.empty() && st.back() == abs(asteroid)) {
            st.pop_back();
        }

        // No collision partner remains.
        // Current asteroid survives.
        else if (st.empty() || st.back() < 0) {
            st.push_back(asteroid);
        }
    }

    return st;
}
```

### Sum of subarray minimums
```cpp
class Solution {
   public:
    /*
        INTUITION:
        For each arr[i], count how many subarrays have arr[i] as the
       minimum.

        leftChoices  = i - previousSmallerOrEqual
        rightChoices = nextSmaller - i

        So:
        contribution = arr[i] * leftChoices * rightChoices

        We use:
        - PSEE → Previous Smaller or Equal
        - NSE  → Next Smaller

        One side is strict and the other is non-strict
        to handle duplicate values without double counting.

        // Minimum → PSEE + NSE
        // PSEE → pop >
        // NSE  → pop >=
        //
        // Contribution = value × leftChoices × rightChoices
        // leftChoices  = i - previousBoundary
        // rightChoices = nextBoundary - i
    */

    vector<int> findNSE(vector<int>& arr) {
        int n = arr.size();
        vector<int> nextSmaller(n);
        stack<int> st;  // Stores indices

        // Find the next STRICTLY smaller element.
        for (int i = n - 1; i >= 0; i--) {
            // Remove elements that are >= current.
            while (!st.empty() && arr[st.top()] >= arr[i]) st.pop();

            // No smaller element on the right → use n as boundary.
            nextSmaller[i] = st.empty() ? n : st.top();

            st.push(i);
        }

        return nextSmaller;
    }

    vector<int> findPSEE(vector<int>& arr) {
        int n = arr.size();
        vector<int> prevSmallerEqual(n);
        stack<int> st;  // Stores indices

        // Find the previous smaller OR equal element.
        for (int i = 0; i < n; i++) {
            // Remove elements that are strictly greater.
            while (!st.empty() && arr[st.top()] > arr[i]) st.pop();

            // No smaller/equal element on the left → use -1.
            prevSmallerEqual[i] = st.empty() ? -1 : st.top();

            st.push(i);
        }

        return prevSmallerEqual;
    }

    int sumSubarrayMins(vector<int>& arr) {
        const long long MOD = 1e9 + 7;
        int n = arr.size();

        vector<int> nextSmaller = findNSE(arr);
        vector<int> prevSmallerEqual = findPSEE(arr);

        long long total = 0;

        for (int i = 0; i < n; i++) {
            // Number of possible starting positions.
            long long leftChoices = i - prevSmallerEqual[i];

            // Number of possible ending positions.
            long long rightChoices = nextSmaller[i] - i;

            // arr[i] is the minimum in leftChoices * rightChoices
            // subarrays.
            long long contribution = (leftChoices * rightChoices) % MOD;

            contribution = (contribution * arr[i]) % MOD;

            total = (total + contribution) % MOD;
        }

        return (int)total;
    }
};
```

### Sum of Subarray Ranges
```cpp
class Solution {
public:
    // Contribution = value × left choices × right choices
    // left  = i - previous boundary
    // right = next boundary - i

    // Next Smaller: strictly smaller element on the right.
    vector<int> nse(vector<int>& nums) {

        int n = nums.size();
        vector<int> nextSmaller(n);
        stack<int> st;

        for (int i = n - 1; i >= 0; i--) {

            // Remove elements that cannot be smaller than nums[i].
            while (!st.empty() && nums[st.top()] >= nums[i])
                st.pop();

            // No smaller element → boundary is outside the array.
            nextSmaller[i] = st.empty() ? n : st.top();

            st.push(i);
        }

        return nextSmaller;
    }

    // Previous Smaller or Equal: element on the left.
    vector<int> psee(vector<int>& nums) {

        int n = nums.size();
        vector<int> prevSmallerEqual(n);
        stack<int> st;

        for (int i = 0; i < n; i++) {

            // Remove elements strictly greater than nums[i].
            while (!st.empty() && nums[st.top()] > nums[i])
                st.pop();

            // No smaller/equal element → boundary before index 0.
            prevSmallerEqual[i] = st.empty() ? -1 : st.top();

            st.push(i);
        }

        return prevSmallerEqual;
    }

    // Sum of all subarray minimums.
    long long subArrayMin(vector<int>& nums) {

        int n = nums.size();

        vector<int> nextSmaller = nse(nums);
        vector<int> prevSmallerEqual = psee(nums);

        long long total = 0;

        for (int i = 0; i < n; i++) {

            // Number of possible starts and ends where nums[i]
            // remains the minimum.
            long long left = i - prevSmallerEqual[i];
            long long right = nextSmaller[i] - i;

            // Contribution of nums[i].
            total += nums[i] * left * right;
        }

        return total;
    }


    // Next Greater: strictly greater element on the right.
    vector<int> nge(vector<int>& nums) {

        int n = nums.size();
        vector<int> nextGreater(n);
        stack<int> st;

        for (int i = n - 1; i >= 0; i--) {

            // Remove elements that cannot be greater than nums[i].
            while (!st.empty() && nums[st.top()] <= nums[i])
                st.pop();

            // No greater element → boundary is outside the array.
            nextGreater[i] = st.empty() ? n : st.top();

            st.push(i);
        }

        return nextGreater;
    }

    // Previous Greater or Equal: element on the left.
    vector<int> pgee(vector<int>& nums) {

        int n = nums.size();
        vector<int> prevGreaterEqual(n);
        stack<int> st;

        for (int i = 0; i < n; i++) {

            // Remove elements strictly smaller than nums[i].
            while (!st.empty() && nums[st.top()] < nums[i])
                st.pop();

            // No greater/equal element → boundary before index 0.
            prevGreaterEqual[i] = st.empty() ? -1 : st.top();

            st.push(i);
        }

        return prevGreaterEqual;
    }

    // Sum of all subarray maximums.
    long long subArrayMax(vector<int>& nums) {

        int n = nums.size();

        vector<int> nextGreater = nge(nums);
        vector<int> prevGreaterEqual = pgee(nums);

        long long total = 0;

        for (int i = 0; i < n; i++) {

            // Number of possible starts and ends where nums[i]
            // remains the maximum.
            long long left = i - prevGreaterEqual[i];
            long long right = nextGreater[i] - i;

            // Contribution of nums[i].
            total += nums[i] * left * right;
        }

        return total;
    }


    long long subArrayRanges(vector<int>& nums) {

        /*
            INTUITION:
            Range = maximum - minimum.

            Therefore:
            Sum of ranges
            = Sum of subarray maximums
            - Sum of subarray minimums.
        */

        return subArrayMax(nums) - subArrayMin(nums);
    }
};
```

### Remove K digits
```cpp
string removeKdigits(string nums, int k) {

    /*
        INTUITION:
        To make the number smallest, remove a larger digit when
        a smaller digit appears after it.

        Maintain an increasing stack of digits.

        Example:
        1432
         ↑
        When 2 arrives, remove 4 because 4 > 2.

        If removals are still left after processing all digits,
        remove them from the end.

        Finally, remove leading zeros.
    */

    string st;

    for (char digit : nums) {

        // Remove larger previous digits.
        while (!st.empty() && k > 0 && st.back() > digit) {
            st.pop_back();
            k--;
        }

        st.push_back(digit);
    }

    // If k removals remain, remove from the end.
    while (k > 0 && !st.empty()) {
        st.pop_back();
        k--;
    }

    // Remove leading zeros.
    int firstNonZero = 0;

    while (firstNonZero < st.size() && st[firstNonZero] == '0')
        firstNonZero++;

    string result = st.substr(firstNonZero);

    return result.empty() ? "0" : result;
}
```

# FAQs
### Implement a Min-Stack
```cpp
class MinStack {
   private:
    stack<long long> st;
    long long minValue;

   public:
    MinStack() {}

    void push(int value) {
        // First element: it is both the value and the minimum.
        if (st.empty()) {
            st.push(value);
            minValue = value;
            return;
        }

        // If value is not a new minimum, store it normally.
        if (value >= minValue) {
            st.push(value);
            return;
        }

        /*
            value is a NEW minimum.

            Problem:
            We are only keeping one extra variable (minValue).
            If we later pop this new minimum, we need to recover
            the previous minimum.

            So instead of storing 'value' directly, encode the
            previous minimum inside the stack value.

                encoded = 2 * value - previousMin

            After this:
                minValue = value

            Since encoded < value, we can later recognize that
            this stack value is encoded rather than a normal value.
        */
        long long encoded = 2LL * value - minValue;

        st.push(encoded);
        minValue = value;
    }

    void pop() {
        /*
            Normally, the top is just the value we should remove.

            But if:
                st.top() < minValue

            then this is an encoded value. It means the current
            minimum was created when this element was pushed.

            Encoding was:
                encoded = 2 * newMin - oldMin

            At this point:
                newMin = minValue

            So we can recover:
                oldMin = 2 * minValue - encoded
        */
        if (st.top() < minValue) {
            minValue = 2LL * minValue - st.top();
        }

        st.pop();
    }

    int top() {
        /*
            If top < minValue, top is an encoded value.
            The actual element represented by it is minValue.

            Otherwise, top itself is the actual element.
        */
        if (st.top() < minValue) {
            return minValue;
        }

        return st.top();
    }

    int getMin() {
        // The minimum is always available in O(1).
        return minValue;
    }
};
```

### Sliding Window Maximum
                    current element
                           ↓
                 ┌──────────────────┐
                 │                  │
          expired?            smaller behind?
                 │                  │
             pop_front         pop_back
                 │                  │
                 └────────┬─────────┘
                          ↓
                     push current
                          ↓
                   front = maximum
```cpp
vector<int> maxSlidingWindow(vector<int>& arr, int k) {
    /*
        INTUITION:
        Use a max heap storing {value, index}.

        As the window moves:
        1. Add the new element to the heap.
        2. Remove elements whose index is outside the window.
        3. The heap top is the maximum of the current window.

        We store the index along with the value so we can identify
        and discard elements that have left the window.
    */

    int n = arr.size();
    vector<int> result;

    // Max heap: largest value stays on top.
    // Pair = {value, index}
    priority_queue<pair<int, int>> maxHeap;

    // Build the first window.
    for (int i = 0; i < k; i++) maxHeap.push({arr[i], i});

    result.push_back(maxHeap.top().first);

    // Slide the window from left to right.
    for (int right = k; right < n; right++) {
        // Add the new element entering the window.
        maxHeap.push({arr[right], right});

        // Current window = [windowStart ... right]
        int windowStart = right - k + 1;

        // Remove stale elements from the top.
        while (maxHeap.top().second < windowStart) maxHeap.pop();

        // Top is the maximum of the current window.
        result.push_back(maxHeap.top().first);
    }

    return result;
}
```
```cpp
vector<int> maxSlidingWindow(vector<int>& arr, int k) {

    /*
        INTUITION:
        The deque stores indices of useful candidates for the maximum.

        Maintain values in decreasing order:
            arr[dq.front()] >= arr[dq.back()]

        For every new element:
        1. Remove indices that left the window.
        2. Remove smaller/equal elements from the back because
           the current element makes them useless.
        3. Add the current index.
        4. Once the first window is complete, deque front is the maximum.
    */

    int n = arr.size();
    vector<int> result;
    deque<int> dq;  // Stores indices, not values.

    for (int right = 0; right < n; right++) {

        // Current window is [right - k + 1 ... right].
        int windowStart = right - k + 1;

        // Remove elements that are outside the current window.
        if (!dq.empty() && dq.front() < windowStart)
            dq.pop_front();

        // Remove candidates smaller than the current element.
        // They can never become the maximum while current is present.
        while (!dq.empty() && arr[dq.back()] <= arr[right])
            dq.pop_back();

        // Current element becomes a candidate.
        dq.push_back(right);

        // A complete window exists only after k elements.
        if (right >= k - 1)
            result.push_back(arr[dq.front()]);
    }

    return result;
}
```

### Trapping Rainwater Problem
```cpp
int trap(vector<int>& height) {

    /*
        INTUITION:
        Water at i = min(leftMax, rightMax) - height[i].

        We use two pointers and only process the side with
        the smaller boundary.

        If height[left] <= height[right]:
            leftMax is the limiting boundary, so we can safely
            calculate water at left and move left forward.

        Otherwise:
            rightMax is the limiting boundary, so we can safely
            calculate water at right and move right backward.

        We only need leftMax and rightMax instead of arrays.
    */

    int n = height.size();

    int left = 0;
    int right = n - 1;

    int leftMax = 0;
    int rightMax = 0;

    int water = 0;

    while (left < right) {

        // Left side has the smaller/equal boundary.
        if (height[left] <= height[right]) {

            // Current bar is below the best left boundary.
            if (height[left] < leftMax)
                water += leftMax - height[left];
            else
                leftMax = height[left];

            left++;
        }

        // Right side has the smaller boundary.
        else {

            // Current bar is below the best right boundary.
            if (height[right] < rightMax)
                water += rightMax - height[right];
            else
                rightMax = height[right];

            right--;
        }
    }

    return water;
}
```

### Largest rectangle in a Histogram
```cpp
int largestRectangleArea(vector<int>& heights) {
    /*
        INTUITION:
        For every bar, find how far its rectangle can extend.

        PSE = Previous Smaller Element
        NSE = Next Smaller Element

        When a bar is popped:
            NSE = current index i
            PSE = stack top after popping

        width = NSE - PSE - 1
        area  = height × width

        We use a monotonic increasing stack of indices.

        A virtual 0 at the end forces all remaining bars
        to be popped and their areas calculated.
    */

    int n = heights.size();
    stack<int> st;

    int largestArea = 0;

    for (int i = 0; i <= n; i++) {
        // Virtual 0 acts as NSE for remaining bars.
        int currentHeight = (i == n) ? 0 : heights[i];

        // Current height is smaller → previous bars found their NSE.
        while (!st.empty() && heights[st.top()] >= currentHeight) {
            int idx = st.top();
            st.pop();

            // After popping, stack top is the PSE.
            int PSE = st.empty() ? -1 : st.top();

            // Current index is the NSE.
            int NSE = i;

            // Bar can extend between PSE and NSE.
            int width = NSE - PSE - 1;

            int area = heights[idx] * width;

            largestArea = max(largestArea, area);
        }

        // Don't push the virtual index n.
        if (i < n) st.push(i);
    }

    return largestArea;
}
```

### Maximum Rectangles
Given a m x n binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.

```cpp
class Solution {
public:

    /*
        INTUITION:
        Convert each row into a histogram.

        For every column:
            1 → increase its height
            0 → reset its height to 0

        Example:

        Matrix:
        1 0 1 1
        1 1 1 1
        1 1 1 0

        After row 0:
        heights = [1,0,1,1]

        After row 1:
        heights = [2,1,2,2]

        After row 2:
        heights = [3,2,3,0]

        Now the problem becomes:
            "Find the largest rectangle in this histogram."

        We solve that using a monotonic increasing stack.

        Overall:
            O(rows × cols)
    */

    // Largest Rectangle in Histogram
    int largestRectangleArea(vector<int>& heights) {

        int n = heights.size();
        stack<int> st;  // Stores indices of increasing heights.
        int maxArea = 0;

        // Extra iteration with height 0 flushes the stack.
        for (int i = 0; i <= n; i++) {

            int currentHeight = (i == n) ? 0 : heights[i];

            /*
                Current height is smaller than stack top.
                Therefore, stack top has found its NSE.

                NSE = i
                PSE = stack top after popping
            */
            while (!st.empty() && heights[st.top()] > currentHeight) {

                int index = st.top();
                st.pop();

                int height = heights[index];

                // Previous Smaller Element.
                int PSE = st.empty() ? -1 : st.top();

                // Next Smaller Element.
                int NSE = i;

                int width = NSE - PSE - 1;

                int area = height * width;

                maxArea = max(maxArea, area);
            }

            // Don't store the sentinel index n.
            if (i < n)
                st.push(i);
        }

        return maxArea;
    }


    int maximalAreaOfSubMatrixOfAll1(vector<vector<int>>& matrix) {

        int rows = matrix.size();
        int cols = matrix[0].size();

        vector<int> heights(cols, 0);
        int maxArea = 0;

        for (int row = 0; row < rows; row++) {

            // Build histogram for the current row.
            for (int col = 0; col < cols; col++) {

                if (matrix[row][col] == 1)
                    heights[col]++;
                else
                    heights[col] = 0;
            }

            /*
                Current heights represent consecutive 1s
                ending at this row.

                Find the largest rectangle of 1s
                using the histogram algorithm.
            */
            maxArea = max(maxArea, largestRectangleArea(heights));
        }

        return maxArea;
    }
};
```

### Stock Span
```cpp
class Solution {
private:

    /*
        INTUITION:
        Stock span for index i = number of consecutive days ending at i
        where the price is <= today's price.

        Find the Previous Greater Element (PGE).

        PGE[i] = nearest index on the left whose price > arr[i].

        Everything between PGE[i] and i has price <= arr[i],
        so:

            span[i] = i - PGE[i]

        If no PGE exists:
            PGE[i] = -1
            span[i] = i + 1
    */

    vector<int> findPGE(vector<int>& arr) {

        int n = arr.size();
        vector<int> pge(n);
        stack<int> st;  // Stores indices

        for (int i = 0; i < n; i++) {

            // Remove elements that cannot be the PGE.
            while (!st.empty() && arr[st.top()] <= arr[i])
                st.pop();

            // Nearest greater element on the left.
            pge[i] = st.empty() ? -1 : st.top();

            st.push(i);
        }

        return pge;
    }

public:

    vector<int> stockSpan(vector<int> arr, int n) {

        vector<int> pge = findPGE(arr);
        vector<int> span(n);

        for (int i = 0; i < n; i++) {

            // Number of days after the previous greater element.
            span[i] = i - pge[i];
        }

        return span;
    }
};
```

```cpp
class Solution
{
public:
    vector<int> stockSpan(vector<int> arr, int n) {

        stack<int> st;  // stores indices
        vector<int> span(n);

        for (int i = 0; i < n; i++) {

            // Remove all elements <= current
            // They cannot block span anymore
            while (!st.empty() && arr[st.top()] <= arr[i]) {
                st.pop();
            }

            // If stack empty → full span till beginning
            // Else → distance from previous greater
            span[i] = st.empty() ? (i + 1) : (i - st.top());

            // Push current index
            st.push(i);
        }

        return span;
    }
};
```

### Celebrity Problem
A celebrity is a person who is known by everyone else at the party but does not know anyone in return. Given a square matrix M of size N x N where M[i][j] is 1 if person i knows person j, and 0 otherwise, determine if there is a celebrity at the party. Return the index of the celebrity or -1 if no such person exists.
```cpp
int celebrity(vector<vector<int>>& M) {
    /*
        INTUITION:
        A celebrity satisfies:

            1. Celebrity knows nobody.
            2. Everybody knows the celebrity.

        Eliminate candidates using two pointers.

        If M[leftCandidate][rightCandidate] == 1:
            leftCandidate knows rightCandidate
            → leftCandidate cannot be celebrity.

        Otherwise:
            leftCandidate does not know rightCandidate
            → rightCandidate cannot be celebrity.

        Continue until only one candidate remains.
        Then verify that candidate.
    */

    int n = M.size();

    int leftCandidate = 0;
    int rightCandidate = n - 1;

    // Eliminate candidates until only one remains.
    while (leftCandidate < rightCandidate) {

        if (M[leftCandidate][rightCandidate] == 1) {

            // Left candidate knows right candidate.
            // Therefore, left candidate cannot be celebrity.
            leftCandidate++;

        } else {

            // Left candidate does not know right candidate.
            // Therefore, right candidate cannot be celebrity.
            rightCandidate--;
        }
    }

    // Both pointers now point to the same possible celebrity.
    int candidate = leftCandidate;

    // Verify the candidate.
    for (int person = 0; person < n; person++) {

        if (person == candidate)
            continue;

        // Celebrity knows nobody.
        // Everybody else knows the celebrity.
        if (M[candidate][person] == 1 ||
            M[person][candidate] == 0) {

            return -1;
        }
    }

    return candidate;
}
```

```cpp
class Solution
{
public:
    int celebrity(vector<vector<int>> &M) {

        int n = M.size();
        stack<int> st;

        // Step 1: Push all people into stack
        for (int i = 0; i < n; i++) {
            st.push(i);
        }

        // Step 2: Eliminate non-celebrities
        while (st.size() > 1) {

            int a = st.top(); st.pop();
            int b = st.top(); st.pop();

            // If a knows b → a cannot be celebrity
            if (M[a][b] == 1) {
                st.push(b);
            }
            // Else → b cannot be celebrity
            else {
                st.push(a);
            }
        }

        // Potential celebrity
        int candidate = st.top();

        // Step 3: Verify candidate
        for (int i = 0; i < n; i++) {

            if (i == candidate) continue;

            // Candidate should not know anyone
            if (M[candidate][i] == 1) return -1;

            // Everyone should know candidate
            if (M[i][candidate] == 0) return -1;
        }

        return candidate;
    }
};
```

### LRU Cache
```cpp
class LRUCache {
   private:
    // Cache entry
    class Node {
       public:
        int key, value;
        Node* prev;
        Node* next;

        Node(int k, int v) {
            key = k;
            value = v;
            prev = next = NULL;
        }
    };

    int capacity;

    // key -> node for O(1) lookup
    unordered_map<int, Node*> mp;

    // HEAD -> MRU ... LRU -> TAIL
    Node* head;
    Node* tail;

    // Remove node from DLL
    void removeNode(Node* node) {
        Node* prevNode = node->prev;
        Node* nextNode = node->next;

        prevNode->next = nextNode;
        nextNode->prev = prevNode;
    }

    // Insert node at MRU position
    void insertAfterHead(Node* node) {
        node->next = head->next;
        node->prev = head;

        head->next->prev = node;
        head->next = node;
    }

   public:
    LRUCache(int capacity) {
        this->capacity = capacity;

        // Dummy nodes simplify edge cases
        head = new Node(-1, -1);
        tail = new Node(-1, -1);

        head->next = tail;
        tail->prev = head;
    }

    int get(int key_) {
        // Key not present
        if (mp.find(key_) == mp.end()) {
            return -1;
        }

        Node* node = mp[key_];

        // Accessed -> move to MRU
        removeNode(node);
        insertAfterHead(node);

        return node->value;
    }

    void put(int key_, int value) {
        // Key already exists
        if (mp.find(key_) != mp.end()) {
            Node* node = mp[key_];

            node->value = value;

            // Updated -> move to MRU
            removeNode(node);
            insertAfterHead(node);
        } else {
            // Evict LRU if cache is full
            if (mp.size() == capacity) {
                Node* lru = tail->prev;

                removeNode(lru);
                mp.erase(lru->key);

                delete lru;
            }

            // New node -> MRU
            Node* newNode = new Node(key_, value);

            insertAfterHead(newNode);
            mp[key_] = newNode;
        }
    }
};
```

### LFU Cache
```cpp
class LFUCache {
    
private:
    int capacity;
    int minFreq;

    unordered_map<int, pair<int,int>> keyMap;
    // key → {value, freq}

    unordered_map<int, list<int>> freqMap;
    // freq → list of keys (LRU order within same freq)

    unordered_map<int, list<int>::iterator> pos;
    // key → position in freq list (for O(1) erase)

    // Update frequency of a key
    void updateFreq(int key) {

        int freq = keyMap[key].second;

        // Remove key from current freq list
        freqMap[freq].erase(pos[key]);

        // If this was the only key with minFreq → update minFreq
        if (freqMap[freq].empty()) {
            freqMap.erase(freq);
            if (minFreq == freq) {
                minFreq++;
            }
        }

        // Increase frequency
        keyMap[key].second++;

        int newFreq = freq + 1;

        // Insert into new freq list (most recent at front)
        freqMap[newFreq].push_front(key);

        pos[key] = freqMap[newFreq].begin();
    }

public:

    LFUCache(int capacity) {
        this->capacity = capacity;
        minFreq = 0;
    }

    int get(int key) {

        // Key not found
        if (keyMap.find(key) == keyMap.end()) {
            return -1;
        }

        // Update frequency
        updateFreq(key);

        return keyMap[key].first;
    }

    void put(int key, int value) {

        // Edge case: capacity = 0
        if (capacity == 0) return;

        // If key exists → update value and frequency
        if (keyMap.find(key) != keyMap.end()) {

            keyMap[key].first = value;

            updateFreq(key);
        }
        else {

            // If full → remove LFU key
            if (keyMap.size() == capacity) {

                // Get least frequently used list
                int lfuKey = freqMap[minFreq].back();

                // Remove least recently used within that freq
                freqMap[minFreq].pop_back();

                if (freqMap[minFreq].empty()) {
                    freqMap.erase(minFreq);
                }

                keyMap.erase(lfuKey);
                pos.erase(lfuKey);
            }

            // Insert new key with freq = 1
            keyMap[key] = {value, 1};

            freqMap[1].push_front(key);
            pos[key] = freqMap[1].begin();

            minFreq = 1;  // reset min frequency
        }
    }
};
```

# Monotonic Stack — Quick Pattern

**Use when:**
- nearest greater / smaller element
- "span" / "visibility" / "first blocking"
- histogram / ranges where element is the limiting factor

**Core idea:**
Maintain a stack that is monotonic (increasing or decreasing). Pop until the invariant holds → the top becomes the answer.

### Choose the Stack Type

| Query | Stack Type | Pop Condition |
| --- | --- | --- |
| Next Greater (>) | Decreasing | `arr[st.top()] <= curr` |
| Next Smaller (<) | Increasing | `arr[st.top()] >= curr` |
| Previous Greater | Decreasing | same as above |
| Previous Smaller | Increasing | same as above |

> “Greater → decreasing stack”, “Smaller → increasing stack”

### Templates (Index-based, O(n))
1. **Next Greater Element (to right)**
```cpp
vector<int> nextGreater(vector<int>& a) {
    int n = a.size();
    vector<int> ans(n, -1);
    stack<int> st; // decreasing stack (indices)

    for (int i = n - 1; i >= 0; --i) {
        while (!st.empty() && a[st.top()] <= a[i]) st.pop();
        ans[i] = st.empty() ? -1 : a[st.top()];
        st.push(i);
    }
    return ans;
}
```
2. **Previous Greater Element (to left)**
```cpp
vector<int> prevGreater(vector<int>& a) {
    int n = a.size();
    vector<int> ans(n, -1);
    stack<int> st; // decreasing

    for (int i = 0; i < n; ++i) {
        while (!st.empty() && a[st.top()] <= a[i]) st.pop();
        ans[i] = st.empty() ? -1 : a[st.top()];
        st.push(i);
    }
    return ans;
}
```
3. **Next Smaller Element (to right)**
```cpp
vector<int> nextSmaller(vector<int>& a) {
    int n = a.size();
    vector<int> ans(n, -1);
    stack<int> st; // increasing

    for (int i = n - 1; i >= 0; --i) {
        while (!st.empty() && a[st.top()] >= a[i]) st.pop();
        ans[i] = st.empty() ? -1 : a[st.top()];
        st.push(i);
    }
    return ans;
}
```
4. **Previous Smaller Element (to left)**
```cpp
vector<int> prevSmaller(vector<int>& a) {
    int n = a.size();
    vector<int> ans(n, -1);
    stack<int> st; // increasing

    for (int i = 0; i < n; ++i) {
        while (!st.empty() && a[st.top()] >= a[i]) st.pop();
        ans[i] = st.empty() ? -1 : a[st.top()];
        st.push(i);
    }
    return ans;
}
```

### Circular Next Greater Element
```cpp
vector<int> nextGreaterCircular(vector<int>& a) {
    int n = a.size();
    vector<int> ans(n, -1);
    stack<int> st;

    for (int i = 2*n - 1; i >= 0; --i) {
        int idx = i % n;
        while (!st.empty() && st.top() <= a[idx]) st.pop();
        if (i < n) ans[idx] = st.empty() ? -1 : st.top();
        st.push(a[idx]);
    }
    return ans;
}
```
