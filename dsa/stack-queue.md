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