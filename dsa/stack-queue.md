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
vector<int> asteroidCollision(vector<int> &asteroids){
    int n = asteroids.size();
    vector<int> st;

    for (int i=0; i<n; i++) {
        if (asteroids[i] > 0) {
            st.push_back(asteroids[i]);
        } else {
            while(!st.empty() && st.back() > 0 && st.back() < abs(asteroids[i])) {
                // if opp direction and diff sizes then both will collide & one remains
                st.pop_back();
            }
            if(!st.empty() && st.back() == abs(asteroids[i])) {
                // if opp direction and same size then both collide & removed
                st.pop_back();
            } else if (st.empty() || st.back() < 0) {
                // what ever asteriod remains in line 12 gets considered again
                st.push_back(asteroids[i]);
            }
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
    Next Smaller Element (Strictly Smaller)
    ---------------------------------------
    Find next index where element < current
    If none → n

    Use >= to ensure duplicates handled correctly
    */
    vector<int> findNextSmaller(vector<int>& arr) {
        int n = arr.size();
        vector<int> next(n);
        stack<int> st;  // stores indices

        for (int i = n - 1; i >= 0; i--) {

            while (!st.empty() && arr[st.top()] >= arr[i]) {
                st.pop();
            }

            next[i] = st.empty() ? n : st.top();

            st.push(i);
        }
        return next;
    }

    /*
    Previous Smaller or Equal Element
    --------------------------------
    Find previous index where element <= current
    If none → -1

    Use > to break tie and avoid double counting
    */
    vector<int> findPrevSmallerEqual(vector<int>& arr) {
        int n = arr.size();
        vector<int> prev(n);
        stack<int> st;

        for (int i = 0; i < n; i++) {

            while (!st.empty() && arr[st.top()] > arr[i]) {
                st.pop();
            }

            prev[i] = st.empty() ? -1 : st.top();

            st.push(i);
        }
        return prev;
    }

    int sumSubarrayMins(vector<int> &arr) {

        int n = arr.size();
        const int MOD = 1e9 + 7;

        vector<int> next = findNextSmaller(arr);
        vector<int> prev = findPrevSmallerEqual(arr);

        long long total = 0;

        for (int i = 0; i < n; i++) {

            /*
            Contribution logic:
            -------------------
            arr[i] is minimum in:
            left choices  = i - prev[i]
            right choices = next[i] - i

            total subarrays = left * right
            */

            long long left = i - prev[i];
            long long right = next[i] - i;

            long long contribution = (left * right) % MOD;
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

    // ---------- MINIMUM CONTRIBUTION ----------

    vector<int> nextSmaller(vector<int>& arr) {
        int n = arr.size();
        vector<int> ans(n);
        stack<int> st;

        for (int i = n - 1; i >= 0; i--) {
            while (!st.empty() && arr[st.top()] >= arr[i]) {
                st.pop();
            }
            ans[i] = st.empty() ? n : st.top();
            st.push(i);
        }
        return ans;
    }

    vector<int> prevSmallerEqual(vector<int>& arr) {
        int n = arr.size();
        vector<int> ans(n);
        stack<int> st;

        for (int i = 0; i < n; i++) {
            while (!st.empty() && arr[st.top()] > arr[i]) {
                st.pop();
            }
            ans[i] = st.empty() ? -1 : st.top();
            st.push(i);
        }
        return ans;
    }

    long long sumSubarrayMins(vector<int>& arr) {
        int n = arr.size();

        vector<int> next = nextSmaller(arr);
        vector<int> prev = prevSmallerEqual(arr);

        long long sum = 0;

        for (int i = 0; i < n; i++) {
            long long left = i - prev[i];
            long long right = next[i] - i;

            sum += left * right * arr[i];
        }

        return sum;
    }

    // ---------- MAXIMUM CONTRIBUTION ----------

    vector<int> nextGreater(vector<int>& arr) {
        int n = arr.size();
        vector<int> ans(n);
        stack<int> st;

        for (int i = n - 1; i >= 0; i--) {
            while (!st.empty() && arr[st.top()] <= arr[i]) {
                st.pop();
            }
            ans[i] = st.empty() ? n : st.top();
            st.push(i);
        }
        return ans;
    }

    vector<int> prevGreaterEqual(vector<int>& arr) {
        int n = arr.size();
        vector<int> ans(n);
        stack<int> st;

        for (int i = 0; i < n; i++) {
            while (!st.empty() && arr[st.top()] < arr[i]) {
                st.pop();
            }
            ans[i] = st.empty() ? -1 : st.top();
            st.push(i);
        }
        return ans;
    }

    long long sumSubarrayMaxs(vector<int>& arr) {
        int n = arr.size();

        vector<int> next = nextGreater(arr);
        vector<int> prev = prevGreaterEqual(arr);

        long long sum = 0;

        for (int i = 0; i < n; i++) {
            long long left = i - prev[i];
            long long right = next[i] - i;

            sum += left * right * arr[i];
        }

        return sum;
    }

    // ---------- FINAL ANSWER ----------
    long long subArrayRanges(vector<int> &nums) {

        long long maxSum = sumSubarrayMaxs(nums);
        long long minSum = sumSubarrayMins(nums);

        return maxSum - minSum;
    }
};
```

### Remove K digits
```cpp
string removeKdigits(string nums, int k) {
    string st;  // acts like a stack

    for (char digit : nums) {

        /*  Remove previous digits if they are larger than current
            This helps in making number smaller */
        while (!st.empty() && k > 0 && st.back() > digit) {
            st.pop_back();
            k--;
        }

        st.push_back(digit);
    }

    /*
    If still k > 0 → remove from end
    (number is already increasing)
    */
    while (k > 0 && !st.empty()) {
        st.pop_back();
        k--;
    }

    /* Remove leading zeros */
    int i = 0;
    while (i < st.size() && st[i] == '0') {
        i++;
    }

    string result = st.substr(i);

    return result.empty() ? "0" : result;
}
```

# FAQs
### Implement a Min-Stack
```cpp
class MinStack {
private:
    stack<long long> st;
    long long mini;

public:
    MinStack() {
        mini = LLONG_MAX;
    }

    void push(int value) {

        if (st.empty()) {
            st.push(value);
            mini = value;
        }
        else {
            if (value >= mini) {
                st.push(value);
            }
            else {
                /* Encode value: store a smaller number to track previous min */
                st.push(2LL * value - mini);
                mini = value;
            }
        }
    }

    void pop() {

        if (st.empty()) return;

        long long topVal = st.top();
        st.pop();

        if (topVal < mini) {
            /* Encoded value detected; Recover previous minimum */
            mini = 2LL * mini - topVal;
        }
    }

    int top() {

        long long topVal = st.top();

        if (topVal < mini) {
            // Encoded → actual value is current minimum
            return mini;
        }

        return topVal;
    }

    int getMin() {
        return mini;
    }
};
```

### Sliding Window Maximum
```cpp
vector<int> maxSlidingWindow(vector<int> &arr, int k) {

    int n = arr.size();
    vector<int> result;

    deque<int> dq;  
    // stores indices
    // maintains decreasing values: arr[dq[0]] >= arr[dq[1]] >= ...

    for (int i = 0; i < n; i++) {

        // 1) Remove indices out of current window [i-k+1, i]
        if (!dq.empty() && dq.front() <= i - k) {
            dq.pop_front();
        }

        // 2) Maintain monotonic decreasing order
        // Remove all smaller/equal elements from back
        while (!dq.empty() && arr[dq.back()] <= arr[i]) {
            dq.pop_back();
        }

        // 3) Add current index
        dq.push_back(i);

        // 4) Record answer when window is valid
        if (i >= k - 1) {
            result.push_back(arr[dq.front()]);  // max of window
        }
    }

    return result;
}
```

### Trapping Rainwater Problem
```cpp
class Solution {
public:
    int trap(vector<int> &height) {

        int n = height.size();
        int left = 0, right = n - 1;
        int leftMax = 0, rightMax = 0;
        int water = 0;

        /*
        CORE IDEA:
        ----------
        Water at index i depends on:
        min(max height on left, max height on right) - height[i]

        Instead of precomputing arrays,
        we use two pointers and maintain running max.
        */

        while (left < right) {

            /*
            Always move the side with smaller height
            because it is the limiting factor
            */
            if (height[left] <= height[right]) {

                // If current bar is lower than leftMax → water can be trapped
                if (height[left] < leftMax) {
                    water += leftMax - height[left];
                }
                else {
                    // Update left boundary
                    leftMax = height[left];
                }

                left++;
            }
            else {

                // Same logic for right side
                if (height[right] < rightMax) {
                    water += rightMax - height[right];
                }
                else {
                    // Update right boundary
                    rightMax = height[right];
                }

                right--;
            }
        }

        return water;
    }
};
```

### Largest rectangle in a Histogram
```cpp
class Solution {
public:
    int largestRectangleArea(vector<int> &heights) {

        int n = heights.size();

        stack<int> st;
        // Monotonic increasing stack (stores indices)
        // heights[st[0]] < heights[st[1]] < ...

        int maxArea = 0;

        /*
        IDEA:
        -----
        Each bar tries to expand left and right
        until a smaller bar blocks it.

        When a bar is popped:
        - Current index (i) becomes its Next Smaller Element (NSE)
        - New stack top becomes its Previous Smaller Element (PSE)

        → This gives us full width for that bar
        */

        for (int i = 0; i <= n; i++) {

            /*
            For i == n:
            Treat height as 0 (sentinel)
            → Forces all remaining bars to be processed
            → Eliminates need for a separate cleanup loop
            */
            int currHeight = (i == n ? 0 : heights[i]);

            /*
            If current bar is smaller,
            it becomes the "right boundary" for taller bars in stack
            */
            while (!st.empty() && currHeight < heights[st.top()]) {

                int idx = st.top();
                st.pop();

                int height = heights[idx];

                /*
                Boundaries:
                - Right boundary → current index i
                - Left boundary → new stack top after pop
                */
                int right = i;
                int left = st.empty() ? -1 : st.top();

                int width = right - left - 1;

                maxArea = max(maxArea, height * width);
            }

            /*
            Push current index:
            It may act as a future PSE for upcoming bars
            */
            st.push(i);
        }

        return maxArea;
    }
};
```

### Maximum Rectangles
Given a m x n binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.

```cpp
class Solution {
public:

    // Helper: Largest Rectangle in Histogram
    int largestRectangleArea(vector<int> &heights) {

        int n = heights.size();
        stack<int> st;
        int maxArea = 0;

        for (int i = 0; i <= n; i++) {

            int currHeight = (i == n ? 0 : heights[i]);

            while (!st.empty() && currHeight < heights[st.top()]) {

                int idx = st.top();
                st.pop();

                int height = heights[idx];

                int right = i;
                int left = st.empty() ? -1 : st.top();

                int width = right - left - 1;

                maxArea = max(maxArea, height * width);
            }

            st.push(i);
        }

        return maxArea;
    }


    int maximalAreaOfSubMatrixOfAll1(vector<vector<int>> &matrix) {

        int n = matrix.size();
        int m = matrix[0].size();

        vector<int> heights(m, 0);

        int maxArea = 0;

        // Build histogram row by row
        for (int row = 0; row < n; row++) {

            for (int col = 0; col < m; col++) {

                // If cell = 1 → extend height
                // If cell = 0 → reset height

                if (matrix[row][col] == 1)
                    heights[col] += 1;
                else
                    heights[col] = 0;
            }

            /* Treat current row as histogram */
            int area = largestRectangleArea(heights);

            maxArea = max(maxArea, area);
        }

        return maxArea;
    }
};
```

### Stock Span
```cpp
class Solution
{
private:
    vector<int> findPGE(vector<int> &arr) {

        int n = arr.size();
        vector<int> res(n);

        stack<int> st;
        // Monotonic decreasing stack (stores indices)
        // arr[st.top()] always represents a candidate for previous greater

        for (int i = 0; i < n; i++) {

            int curr = arr[i];

            // Remove all elements <= current
            // because they cannot be "previous greater" anymore
            while (!st.empty() && arr[st.top()] <= curr) {
                st.pop();
            }

            // If stack is empty → no greater element on left
            // Else → top of stack is nearest greater element
            res[i] = st.empty() ? -1 : st.top();

            // Push current index for future comparisons
            st.push(i);
        }

        return res;
    }

public:
    vector<int> stockSpan(vector<int> arr, int n) {

        // Step 1: Find Previous Greater Element indices
        vector<int> pge = findPGE(arr);

        vector<int> span(n);

        // Step 2: Compute span
        for (int i = 0; i < n; i++) {

            // If no greater element → span = i + 1
            // Else → span = distance from previous greater
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
class Solution
{
public:
    int celebrity(vector<vector<int>> &M) {

        int n = M.size();

        int top = 0, bottom = n - 1;

        // Step 1: Eliminate non-celebrities
        while (top < bottom) {

            // If top knows bottom → top cannot be celebrity
            if (M[top][bottom] == 1) {
                top++;
            }
            // Else → bottom cannot be celebrity
            else {
                bottom--;
            }
        }

        // Potential celebrity
        int candidate = top;

        // Step 2: Verify candidate

        for (int i = 0; i < n; i++) {

            if (i == candidate) continue;

            // Candidate should NOT know anyone
            if (M[candidate][i] == 1) return -1;

            // Everyone should know candidate
            if (M[i][candidate] == 0) return -1;
        }

        return candidate;
    }
};
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

    int capacity;  // maximum size of cache

    unordered_map<int, Node*> mp;  
    // key → pointer to node in DLL

    Node* head; // dummy head → most recently used side
    Node* tail; // dummy tail → least recently used side

    // Remove a node from its current position in DLL
    void removeNode(Node* node) {
        Node* prevNode = node->prev;
        Node* nextNode = node->next;

        prevNode->next = nextNode;
        nextNode->prev = prevNode;
    }

    // Insert node right after head → mark as most recently used
    void insertAfterHead(Node* node) {
        node->next = head->next;
        node->prev = head;

        head->next->prev = node;
        head->next = node;
    }

public:

    LRUCache(int capacity) {
        this->capacity = capacity;

        // Create dummy head and tail to simplify operations
        head = new Node(-1, -1);
        tail = new Node(-1, -1);

        head->next = tail;
        tail->prev = head;
    }

    int get(int key_) {

        // If key not present → return -1
        if (mp.find(key_) == mp.end()) {
            return -1;
        }
        Node* node = mp[key_];

        // Move accessed node to front (MRU)
        removeNode(node);
        insertAfterHead(node);

        return node->value;
    }

    void put(int key_, int value) {

        // If key already exists → update value and move to front
        if (mp.find(key_) != mp.end()) {
            Node* node = mp[key_];
            node->value = value;
            removeNode(node);
            insertAfterHead(node);
        } else {
            // If cache is full → remove least recently used node
            if (mp.size() == capacity) {
                Node* lru = tail->prev;  // last real node
                removeNode(lru);
                mp.erase(lru->key);
                delete lru;  // free memory
            }

            // Insert new node at front (MRU position)
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
