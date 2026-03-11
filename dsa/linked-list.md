## Single Linked List

### Traverse a Linked List
```cpp
vector<int> LLTraversal(ListNode *head) {
    // Pointer used to traverse the linked list
    ListNode* temp = head;

    // Vector to store the values of the nodes
    vector<int> ans;

    // Traverse the list until we reach the end (nullptr)
    while (temp != nullptr) {
        // Add the current node's value to the result
        ans.push_back(temp->data);

        // Move to the next node
        temp = temp->next;
    }

    // Return the collected values
    return ans;
}
```

### Deletion of the Head of Linked List
```cpp
// Deletes the first node of the linked list
ListNode* deleteHead(ListNode* head) {

    // If the list is empty, there is nothing to delete
    if (head == nullptr)
        return nullptr;

    // Store the current head node
    ListNode* temp = head;

    // Move head to the next node
    head = head->next;

    // Free memory of the old head node
    delete temp;

    // Return the updated head
    return head;
}
```

### Deletion of the Tail of Linked List
```cpp

// Deletes the last node (tail) of the linked list
ListNode* deleteTail(ListNode* head) {

    // If the list is empty or contains only one node,
    // removing the tail results in an empty list
    if (head == nullptr || head->next == nullptr)
        return nullptr;

    // Pointer used to traverse the list
    ListNode* temp = head;

    // Traverse until the second-to-last node
    while (temp->next->next != nullptr) {
        temp = temp->next;
    }

    // Delete the last node
    delete temp->next;

    // Update the second-to-last node to point to nullptr
    temp->next = nullptr;

    // Return the head of the modified list
    return head;
}
```

### Deletion of the Kth Node of Linked List
```cpp
// Deletes the k-th node (1-based index) from the linked list
ListNode* deleteKthNode(ListNode* head, int k) {

    // If the list is empty, nothing can be deleted
    if (head == nullptr)
        return nullptr;

    // If k == 1, remove the head node
    if (k == 1) {
        ListNode* temp = head;
        head = head->next;
        delete temp;
        return head;
    }

    // Pointer used to traverse the list
    ListNode* temp = head;

    // Move to the (k-1)th node
    for (int i = 0; temp != nullptr && i < k - 2; i++) {
        temp = temp->next;
    }

    // If k exceeds the length of the list, return the original list
    if (temp == nullptr || temp->next == nullptr)
        return head;

    // Remove the k-th node by adjusting pointers
    ListNode* nextNode = temp->next->next;
    delete temp->next;
    temp->next = nextNode;

    // Return the updated head
    return head;
}
```

### Deletion of the Node with value X
```cpp
// Deletes the first node containing value X from the linked list
ListNode* deleteNodeWithValueX(ListNode* &head, int X) {

    // If the list is empty, nothing to delete
    if (head == nullptr)
        return nullptr;

    // If the head node contains the value X
    if (head->data == X) {
        ListNode* temp = head;
        head = head->next;   // Move head to the next node
        delete temp;         // Free memory of the removed node
        return head;
    }

    // Traverse the list to find the node before the target node
    ListNode* temp = head;

    while (temp->next != nullptr && temp->next->data != X) {
        temp = temp->next;
    }

    // If the value X is not found, return the list unchanged
    if (temp->next == nullptr)
        return head;

    // Remove the node containing value X
    ListNode* nodeToDelete = temp->next;
    temp->next = nodeToDelete->next;
    delete nodeToDelete;

    // Return the updated head
    return head;
}
```

### Deletion fo the Node without head
```cpp
// Deletes a node when only that node pointer is given
void deleteNode(ListNode* node) {

    // Copy data from the next node
    node->data = node->next->data;

    // Store the next node
    ListNode* temp = node->next;

    // Bypass the next node
    node->next = node->next->next;

    // Delete the old next node
    delete temp;
}
```

### Insertion at the head of Linked List
```cpp
// Inserts a new node at the beginning of the list
ListNode* insertAtHead(ListNode* &head, int X) {

    // Create a new node
    ListNode* newNode = new ListNode(X);

    // Point new node to current head
    newNode->next = head;

    // Update head to the new node
    head = newNode;

    return head;
}
```

### Insertion at the tail of Linked List
```cpp
// Inserts a new node at the end of the list
ListNode* insertAtTail(ListNode*& head, int X) {
    ListNode* newNode = new ListNode(X);

    // If list is empty, new node becomes head
    if (head == nullptr) {
        head = newNode;
        return head;
    }

    // Traverse to the last node
    ListNode* temp = head;
    while (temp->next != nullptr) {
        temp = temp->next;
    }

    // Attach new node at the end
    temp->next = newNode;

    return head;
}
```

### Insertion at the Kth Position in Linked List
```cpp
// Inserts value X at the K-th position (1-based indexing)
ListNode* insertAtKthPosition(ListNode* &head, int X, int K) {

    // If inserting at head
    if (K == 1) {
        ListNode* newNode = new ListNode(X);
        // Point new node to current head
        newNode->next = head;
        // Update head to the new node
        head = newNode;
        return head;
    }

    ListNode* temp = head;

    // Traverse to (K-1)th node
    for (int i = 1; temp != nullptr && i < K - 1; i++) {
        temp = temp->next;
    }

    // If K exceeds list length, do nothing
    if (temp == nullptr)
        return head;

    // Create new node
    ListNode* newNode = new ListNode(X);

    // Insert node
    newNode->next = temp->next;
    temp->next = newNode;

    return head;
}
```

### Insertion before the value X in Linked List
```cpp
// Inserts a new node with value 'val' before the first node containing value X
ListNode* insertBeforeX(ListNode*& head, int X, int val) {
    // If the list is empty, insertion is not possible
    if (head == nullptr) {
        return nullptr;
    }

    // If X is present at the head, insert new node before head
    if (head->data == X) return new ListNode(val, head);

    // Traverse the list to find the node before the node containing X
    ListNode* curr = head;

    while (curr->next != nullptr) {
        // If the next node contains X, insert the new node before it
        if (curr->next->data == X) {
            curr->next = new ListNode(val, curr->next);
            break;
        }

        curr = curr->next;
    }

    // Return the (possibly unchanged) head
    return head;
}
```

## Doubly Linked List

### Deletion of the Head of Doubly Linked List
```cpp
// Deletes the head node of a doubly linked list
ListNode* deleteHead(ListNode* head) {

    // If the list is empty or contains only one node,
    // deleting the head results in an empty list
    if (head == nullptr || head->next == nullptr) {
        return nullptr;
    }

    // Store the current head node
    ListNode* curr = head;

    // Move head to the next node
    head = head->next;

    // Remove backward link to the old head
    head->prev = nullptr;

    // Disconnect the old head node
    curr->next = nullptr;

    // Free memory of the old head
    delete curr;

    // Return the updated head
    return head;
}
```

### Deletion of the Tail of Doubly Linked List
```cpp
// Deletes the last node (tail) of a doubly linked list
ListNode* deleteTail(ListNode* head) {

    // If the list is empty, nothing to delete
    if (head == nullptr)
        return nullptr;

    // If the list contains only one node, deleting the tail makes the list empty
    if (head->next == nullptr) {
        delete head;
        return nullptr;
    }

    // Traverse to the last node
    ListNode* curr = head;
    while (curr->next != nullptr) {
        curr = curr->next;
    }

    // Disconnect the last node from the list
    curr->prev->next = nullptr;
    curr->prev = nullptr;

    // Free memory of the removed node
    delete curr;

    // Return the head of the modified list
    return head;
}
```

### Deletion of the Kth Node of Doubly Linked List
```cpp
// Deletes the k-th node (1-based index) from a doubly linked list
ListNode* deleteKthElement(ListNode *&head, int k) {

    // If the list is empty, nothing to delete
    if (head == nullptr)
        return nullptr;

    ListNode* curr = head;
    int count = 1;

    // Traverse to the k-th node
    while (curr != nullptr && count < k) {
        curr = curr->next;
        count++;
    }

    // If k is greater than the number of nodes
    if (curr == nullptr)
        return head;

    // If deleting the head node
    if (curr == head) {
        head = head->next;
        if (head != nullptr)
            head->prev = nullptr;

        delete curr;
        return head;
    }

    // Update surrounding pointers
    if (curr->prev != nullptr)
        curr->prev->next = curr->next;

    if (curr->next != nullptr)
        curr->next->prev = curr->prev;

    // Delete the node
    delete curr;

    return head;
}
```

### Deletion of the Node without head in Doubly Linked List
```cpp
// Deletes the given node from a doubly linked list
void deleteGivenNode(ListNode *node) {

    // If node is null, nothing to delete
    if (node == nullptr)
        return;

    // Update next pointer of previous node
    if (node->prev != nullptr)
        node->prev->next = node->next;

    // Update prev pointer of next node
    if (node->next != nullptr)
        node->next->prev = node->prev;

    // Disconnect the node completely
    node->next = nullptr;
    node->prev = nullptr;

    // Free memory
    delete node;
}
```

### Insertion at the head of Doubly Linked List
```cpp
// Inserts a new node before the current head
ListNode* insertBeforeHead(ListNode* head, int X) {

    ListNode* newNode = new ListNode(X);

    // If list is empty
    if (head == nullptr)
        return newNode;

    // Link new node with current head
    newNode->next = head;
    head->prev = newNode;

    // Update head
    return newNode;
}
```

### Insertion at the tail of Doubly Linked List
```cpp
// Inserts a new node before the last node
ListNode* insertBeforeTail(ListNode* head, int X) {
    if (head == nullptr) return new ListNode(X);

    // If only one node exists
    if (head->next == nullptr) {
        // insertBeforeHead
        ListNode* newNode = new ListNode(X);

        // If list is empty
        if (head == nullptr) return newNode;

        // Link new node with current head
        newNode->next = head;
        head->prev = newNode;

        // Update head
        return newNode;
    }

    ListNode* curr = head;

    // Traverse to tail
    while (curr->next != nullptr) {
        curr = curr->next;
    }

    ListNode* newNode = new ListNode(X);

    // Insert before tail
    newNode->next = curr;
    newNode->prev = curr->prev;

    curr->prev->next = newNode;
    curr->prev = newNode;

    return head;
}
```

### Insertion at the Kth Position in Doubly Linked List
```cpp
// Inserts value X before the K-th node
ListNode* insertBeforeKthPosition(ListNode* head, int X, int K) {
    if (K == 1) {
        // insertBeforeHead
        ListNode* newNode = new ListNode(X);

        // If list is empty
        if (head == nullptr) return newNode;

        // Link new node with current head
        newNode->next = head;
        head->prev = newNode;

        // Update head
        return newNode;
    }

    ListNode* curr = head;
    int count = 1;

    // Traverse to K-th node
    while (curr != nullptr && count < K) {
        curr = curr->next;
        count++;
    }

    // If K exceeds length
    if (curr == nullptr) return head;

    ListNode* newNode = new ListNode(X);

    // Insert before K-th node
    newNode->next = curr;
    newNode->prev = curr->prev;

    curr->prev->next = newNode;
    curr->prev = newNode;

    return head;
}
```

### Insertion before the value X in Doubly Linked List
```cpp
// Inserts a new node before the given node
void insertBeforeGivenNode(ListNode* node, int X) {

    if (node == nullptr)
        return;

    ListNode* newNode = new ListNode(X);

    newNode->next = node;
    newNode->prev = node->prev;

    if (node->prev != nullptr)
        node->prev->next = newNode;

    node->prev = newNode;
}
```

## Easy

### Add two numbers in Linked List
```cpp
// Adds two numbers represented by linked lists where each node contains a single digit.
// Digits are stored in reverse order (least significant digit first).
ListNode* addTwoNumbers(ListNode* &linkedList1, ListNode* &linkedList2) {

    // Pointers to traverse both lists
    ListNode* list1 = linkedList1;
    ListNode* list2 = linkedList2;

    // Dummy node simplifies result list construction
    ListNode* dummyHead = new ListNode(-1);

    // Pointer used to build the result list
    ListNode* resultTail = dummyHead;

    int carry = 0;

    // Traverse both lists while digits exist in both
    while (list1 != nullptr && list2 != nullptr) {

        int digitSum = list1->data + list2->data + carry;

        carry = digitSum / 10;
        digitSum = digitSum % 10;

        // Append new digit to result list
        resultTail->next = new ListNode(digitSum);
        resultTail = resultTail->next;

        // Move both pointers forward
        list1 = list1->next;
        list2 = list2->next;
    }

    // Process remaining digits in list1
    while (list1 != nullptr) {

        int digitSum = list1->data + carry;

        carry = digitSum / 10;
        digitSum = digitSum % 10;

        resultTail->next = new ListNode(digitSum);
        resultTail = resultTail->next;

        list1 = list1->next;
    }

    // Process remaining digits in list2
    while (list2 != nullptr) {

        int digitSum = list2->data + carry;

        carry = digitSum / 10;
        digitSum = digitSum % 10;

        resultTail->next = new ListNode(digitSum);
        resultTail = resultTail->next;

        list2 = list2->next;
    }

    // If carry remains after processing both lists, add a final node
    if (carry != 0) {
        resultTail->next = new ListNode(carry);
    }

    // Return the head of the result list (skipping dummy node)
    return dummyHead->next;
}


// Utility function to print a linked list
void print(ListNode* head) {

    cout << "\n";

    // Traverse and print each node
    while (head != nullptr) {
        cout << head->data << " -> ";
        head = head->next;
    }
}
```

### Segregate odd and even nodes in Linked List
```cpp
// Rearranges the list so that all nodes at odd positions come first,
// followed by nodes at even positions.
ListNode* oddEvenList(ListNode* head) {

    // If list has 0 or 1 node, no rearrangement needed
    if (head == nullptr || head->next == nullptr)
        return head;

    // Pointer to the first odd node
    ListNode* odd = head;

    // Pointer to the first even node
    ListNode* even = head->next;

    // Save start of even list to attach later
    ListNode* evenHead = even;

    // Rearrange nodes by updating next pointers
    while (even != nullptr && even->next != nullptr) {

        // Link current odd node to next odd node
        odd->next = even->next;
        odd = odd->next;

        // Link current even node to next even node
        even->next = odd->next;
        even = even->next;
    }

    // Attach even list after odd list
    odd->next = evenHead;

    return head;
}
```

### Sort Linked List of 0, 1, 2
```cpp
// Sort a linked list containing only 0s, 1s, and 2s
// using node segregation (three separate lists)
ListNode* sortList(ListNode* &head) {

    if (head == nullptr || head->next == nullptr)
        return head;

    // Dummy heads for the three lists
    ListNode* zeroHead = new ListNode(-1);
    ListNode* oneHead  = new ListNode(-1);
    ListNode* twoHead  = new ListNode(-1);

    // Tail pointers for building lists
    ListNode* zero = zeroHead;
    ListNode* one  = oneHead;
    ListNode* two  = twoHead;

    ListNode* curr = head;

    // Distribute nodes into the three lists
    while (curr != nullptr) {

        if (curr->data == 0) {
            zero->next = curr;
            zero = zero->next;
        }
        else if (curr->data == 1) {
            one->next = curr;
            one = one->next;
        }
        else {
            two->next = curr;
            two = two->next;
        }

        curr = curr->next;
    }

    // Connect the three lists together
    zero->next = (oneHead->next != nullptr) ? oneHead->next : twoHead->next;
    one->next = twoHead->next;
    two->next = nullptr;

    // Updated head
    head = zeroHead->next;

    return head;
}
```

### Remove Nth node from the back of Linked List
```cpp
// Removes the N-th node from the end of the linked list
ListNode* removeNthFromEnd(ListNode* head, int n) {

    // Dummy node simplifies edge cases (like deleting head)
    ListNode* dummy = new ListNode(0);
    dummy->next = head;

    ListNode* fast = dummy;
    ListNode* slow = dummy;

    // Move fast pointer n+1 steps ahead
    for (int i = 0; i <= n; i++) {
        fast = fast->next;
    }

    // Move both pointers until fast reaches the end
    while (fast != nullptr) {
        fast = fast->next;
        slow = slow->next;
    }

    // Node to delete
    ListNode* nodeToDelete = slow->next;

    // Skip the target node
    slow->next = slow->next->next;

    delete nodeToDelete;

    return dummy->next;
}
```

### Reverse a Linked List
```cpp
// Recursively reverses a linked list and returns the new head
ListNode* reverseListRecursive(ListNode* head) {

    // Base case:
    // If list is empty or contains only one node,
    // it is already reversed
    if (head == nullptr || head->next == nullptr)
        return head;

    // Reverse the rest of the list starting from the second node
    ListNode* reversedHead = reverseListRecursive(head->next);

    // head->next currently points to the next node
    ListNode* nextNode = head->next;

    // Reverse the link
    nextNode->next = head;

    // Break the original forward link
    head->next = nullptr;

    // Return the head of the reversed list
    return reversedHead;
}


// Iteratively reverse a singly linked list
ListNode* reverseList(ListNode* head) {

    // 'prev' will become the new head of the reversed list
    ListNode* prev = nullptr;

    // Traverse the original list using 'head'
    while (head != nullptr) {

        // Store the next node before changing pointers
        // This ensures we don't lose access to the rest of the list
        ListNode* nextNode = head->next;

        // Reverse the current node's pointer
        head->next = prev;

        // Move 'prev' forward to the current node
        prev = head;

        // Move 'head' forward in the original list
        head = nextNode;
    }

    // 'prev' now points to the new head of the reversed list
    return prev;
}
```

## Medium

### Add one to a number represented by Linked List
```cpp
// Reverse a singly linked list
ListNode* reverseList(ListNode* head) {

    ListNode* prev = nullptr;

    while (head != nullptr) {
        ListNode* nextNode = head->next;
        head->next = prev;
        prev = head;
        head = nextNode;
    }

    return prev;
}


// Adds 1 to a number represented by a linked list
ListNode* addOne(ListNode* head) {

    // Step 1: Reverse the list so we start addition from the least significant digit
    ListNode* reversedHead = reverseList(head);

    ListNode* curr = reversedHead;
    int carry = 1;

    // Step 2: Add carry to digits
    while (curr != nullptr && carry) {

        int sum = curr->val + carry;

        curr->val = sum % 10;
        carry = sum / 10;

        // If carry is finished, we can stop early
        if (carry == 0)
            break;

        // If we're at the last node and carry still exists, add a new node
        if (curr->next == nullptr) {
            curr->next = new ListNode(carry);
            carry = 0;
            break;
        }

        curr = curr->next;
    }

    // Step 3: Reverse the list again to restore original order
    return reverseList(reversedHead);
}
```
```cpp
// Helper function that adds carry and returns the carry to the previous node
int addOneHelper(ListNode* node) {

    // Base case: beyond last node
    if (node == nullptr)
        return 1;   // initial +1

    // Recursively process next node
    int carry = addOneHelper(node->next);

    int sum = node->val + carry;

    node->val = sum % 10;

    return sum / 10;   // propagate carry
}


// Main function
ListNode* addOne(ListNode* head) {

    int carry = addOneHelper(head);

    // If carry remains, create new head
    if (carry) {
        ListNode* newHead = new ListNode(carry);
        newHead->next = head;
        return newHead;
    }

    return head;
}
```

### Find Middle of Linked List
```cpp
// Finds and returns the middle node of a linked list
ListNode* middleOfLinkedList(ListNode* head) {

    // 'slow' moves one step at a time
    ListNode* slow = head;

    // 'fast' moves two steps at a time
    ListNode* fast = head;

    // When fast reaches the end, slow will be at the middle
    while (fast != nullptr && fast->next != nullptr) {

        slow = slow->next;          // move 1 step
        fast = fast->next->next;    // move 2 steps
    }

    // slow now points to the middle node
    return slow;
}
```

### Delete the middle node in Linked List
```cpp
// Deletes the middle node of a linked list
ListNode* deleteMiddle(ListNode* head) {

    // If the list has only one node, deleting the middle results in an empty list
    if (head == nullptr || head->next == nullptr)
        return nullptr;

    // 'slow' will reach the middle node
    ListNode* slow = head;

    // 'fast' moves twice as fast to help locate the middle
    ListNode* fast = head;

    // 'prev' keeps track of the node before 'slow'
    ListNode* prev = nullptr;

    // Find the middle node using fast-slow pointer technique
    while (fast != nullptr && fast->next != nullptr) {

        prev = slow;
        slow = slow->next;
        fast = fast->next->next;
    }

    // Remove the middle node
    prev->next = slow->next;
    delete slow;

    return head;
}
```

### Check if Linked List is a Palindrome
```cpp
// Reverse a singly linked list and return the new head
ListNode* reverseList(ListNode* head) {

    ListNode* prev = nullptr;

    // Traverse the list and reverse pointers
    while (head != nullptr) {

        // Save the next node before modifying the link
        ListNode* nextNode = head->next;

        // Reverse the link direction
        head->next = prev;

        // Move pointers forward
        prev = head;
        head = nextNode;
    }

    // 'prev' becomes the new head of the reversed list
    return prev;
}


// Check if a linked list is a palindrome
bool isPalindrome(ListNode* head) {

    // Lists with 0 or 1 node are always palindrome
    if (head == nullptr || head->next == nullptr)
        return true;

    ListNode* slow = head;
    ListNode* fast = head;

    /*
        Step 1: Find the middle of the linked list using fast–slow pointers.

        slow moves one step
        fast moves two steps

        When the loop stops:

        EVEN length example:
        1 → 2 → 3 → 4
        slow = 3
        fast = nullptr

        ODD length example:
        1 → 2 → 3 → 2 → 1
        slow = 3
        fast = last node (not nullptr)

        Key observation:
        - fast == nullptr  → even length list
        - fast != nullptr  → odd length list
    */
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }

    /*
        Step 2: Skip the middle node for odd-length lists.

        When the list length is odd, slow stops exactly at the middle node.
        Example:
        1 → 2 → 3 → 2 → 1
                ↑
               slow

        The middle node (3) should NOT be compared because it does not affect
        palindrome symmetry. So we move slow one step ahead.

        We check:
            if (fast != nullptr)

        because after the loop:
        - fast == nullptr  → even length
        - fast != nullptr  → odd length
    */
    if (fast != nullptr) {
        slow = slow->next;
    }

    // Step 3: Reverse the second half of the list
    ListNode* secondHalfHead = reverseList(slow);

    // Step 4: Compare the first half and reversed second half
    ListNode* firstHalfPtr = head;
    ListNode* secondHalfPtr = secondHalfHead;

    while (secondHalfPtr != nullptr) {

        if (firstHalfPtr->val != secondHalfPtr->val) {

            // Restore original list before returning
            reverseList(secondHalfHead);
            return false;
        }

        firstHalfPtr = firstHalfPtr->next;
        secondHalfPtr = secondHalfPtr->next;
    }

    // Step 5: Restore the original list structure
    reverseList(secondHalfHead);

    return true;
}
```

### Find the intersection of point Y in Linked List
```cpp
// Finds the intersection node of two singly linked lists
ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {

    // If either list is empty, an intersection is impossible
    if (headA == nullptr || headB == nullptr)
        return nullptr;

    // Traversal pointers for both lists
    ListNode* currentA = headA;
    ListNode* currentB = headB;

    /*
        Traverse both lists simultaneously.

        When currentA reaches the end of list A,
        redirect it to the head of list B.

        When currentB reaches the end of list B,
        redirect it to the head of list A.

        This ensures both pointers travel the same total distance:
            lengthA + lengthB

        If an intersection exists, they will meet there.
        If no intersection exists, both will eventually become nullptr.
    */
    while (currentA != currentB) {

        currentA = (currentA == nullptr) ? headB : currentA->next;
        currentB = (currentB == nullptr) ? headA : currentB->next;
    }

    // Either the intersection node or nullptr
    return currentA;
}
// TC: O(m+n) SC: O(1)
```

### Detect a loop in a Linked List
```cpp
// Detect whether a linked list contains a cycle
bool hasCycle(ListNode* head) {

    // slow moves one step, fast moves two steps
    ListNode* slow = head;
    ListNode* fast = head;

    /*
        Traverse while fast can move two steps.
        If a cycle exists, fast will eventually
        catch up to slow inside the loop.
    */
    while (fast != nullptr && fast->next != nullptr) {

        slow = slow->next;           // move 1 step
        fast = fast->next->next;     // move 2 steps

        // If both pointers meet, a cycle exists
        if (slow == fast)
            return true;
    }

    // If fast reaches nullptr, no cycle exists
    return false;
}
```

### Find the starting point of a loop in Linked List
```cpp
// Returns the node where the cycle begins (or nullptr if no cycle)
ListNode* detectCycleStart(ListNode* head) {

    ListNode* slow = head;
    ListNode* fast = head;

    // Step 1: Detect if a cycle exists
    while (fast != nullptr && fast->next != nullptr) {

        slow = slow->next;
        fast = fast->next->next;

        if (slow == fast) {

            /*
                Step 2: Move one pointer to head.
                Move both one step at a time.
                They will meet at the start of the cycle.
            */
            slow = head;

            while (slow != fast) {
                slow = slow->next;
                fast = fast->next;
            }

            return slow;  // cycle start node
        }
    }

    // No cycle
    return nullptr;
}
```
```cpp
// Remove a cycle from a singly linked list if one exists
void removeCycle(ListNode* head) {

    // Empty list cannot contain a cycle
    if (head == nullptr)
        return;

    // Two pointers used for Floyd's cycle detection
    // slow moves 1 step at a time
    // fast moves 2 steps at a time
    ListNode* slow = head;
    ListNode* fast = head;

    /*
        Phase 1: Detect whether a cycle exists.

        If the list contains a loop, the fast pointer will
        eventually meet the slow pointer inside the cycle.
        If fast reaches nullptr, the list has no cycle.
    */
    while (fast != nullptr && fast->next != nullptr) {

        slow = slow->next;          // move 1 step
        fast = fast->next->next;    // move 2 steps

        if (slow == fast)
            break;  // meeting point inside the cycle
    }

    // If fast reached the end, there is no cycle
    if (fast == nullptr || fast->next == nullptr)
        return;

    /*
        Phase 2: Locate the node where the cycle begins.

        Move slow back to the head.
        Keep fast at the meeting point.

        If we move both pointers one step at a time,
        they will meet at the start of the cycle.

        However, to remove the cycle we actually want
        the node *just before* the cycle start.
    */
    slow = head;

    // Special case: cycle begins at the head node
    if (slow == fast) {

        // Move fast until it reaches the last node in the cycle
        while (fast->next != slow)
            fast = fast->next;

    } else {

        /*
            Move both pointers together until their
            next pointers match.

            At this moment:
            slow->next == fast->next

            This node is the start of the cycle,
            and fast is the node just before it.
        */
        while (slow->next != fast->next) {
            slow = slow->next;
            fast = fast->next;
        }
    }

    /*
        Phase 3: Break the cycle.

        fast currently points to the last node in the cycle.
        Setting its next pointer to nullptr restores
        the linked list to a proper linear structure.
    */
    fast->next = nullptr;
}
```


### Length of a loop in a Linked List
```cpp
// Returns the length of the cycle in the linked list
// If no cycle exists, returns 0
int findLengthOfLoop(ListNode *head) {

    ListNode* slow = head;
    ListNode* fast = head;

    /*
        Step 1: Detect whether a cycle exists
        using Floyd's Tortoise and Hare algorithm
    */
    while (fast != nullptr && fast->next != nullptr) {

        slow = slow->next;           // move 1 step
        fast = fast->next->next;     // move 2 steps

        // Cycle detected
        if (slow == fast) {

            /*
                Step 2: Count the number of nodes
                in the cycle
            */
            int loopLength = 1;
            ListNode* current = slow->next;

            while (current != slow) {
                loopLength++;
                current = current->next;
            }

            return loopLength;
        }
    }

    // No cycle present
    return 0;
}
```

## Hard

### Reverse Linked List in a group of given size K
```cpp

// Reverse nodes from start up to (but not including) end
ListNode* reverseSegment(ListNode* start, ListNode* end) {

    ListNode* prev = end;

    while (start != end) {

        // Save next node before reversing pointer
        ListNode* nextNode = start->next;

        // Reverse pointer
        start->next = prev;

        prev = start;
        start = nextNode;
    }

    return prev;  // new head of reversed segment
}


// Reverse nodes of the linked list in groups of size k
ListNode* reverseKGroup(ListNode* head, int k) {

    // Dummy node helps simplify head manipulation
    ListNode* dummy = new ListNode(0);
    dummy->next = head;

    // Points to the node before the current group
    ListNode* prevGroup = dummy;

    while (true) {

        // Step 1: Find the k-th node from prevGroup
        ListNode* kthNode = prevGroup;

        for (int i = 0; i < k && kthNode != nullptr; i++) {
            kthNode = kthNode->next;
        }

        // If fewer than k nodes remain, stop
        if (kthNode == nullptr)
            break;

        // Step 2: Identify the start of the next group
        ListNode* nextGroupHead = kthNode->next;

        // Step 3: Current group's first node
        ListNode* groupStart = prevGroup->next;

        // Step 4: Reverse current group
        prevGroup->next = reverseSegment(groupStart, nextGroupHead);

        // Step 5: Move prevGroup to the end of the reversed group
        prevGroup = groupStart;
    }

    return dummy->next;
}
```

### Rotate a Linked List to right by K
```cpp
ListNode* rotateRight(ListNode* head, int k) {

    // Edge cases:
    // If list is empty, has one node, or rotation is 0
    if (!head || !head->next || k == 0)
        return head;

    // Step 1: Find the length of the list and the tail node
    int n = 1;
    ListNode* tail = head;

    while (tail->next) {
        tail = tail->next;
        n++;
    }

    // Step 2: Reduce unnecessary rotations
    // Rotating n times gives the same list
    k %= n;

    if (k == 0) return head;

    // Step 3: Make the list circular
    // Example:
    // 1 → 2 → 3 → 4 → 5
    // ↑               ↓
    // ← ← ← ← ← ← ← ←
    tail->next = head;

    /*
        Step 4: Find the new tail

        Rotating right by k means the last k nodes move to the front.

        Example:
        1 → 2 → 3 → 4 → 5
        k = 2

        Result should be:
        4 → 5 → 1 → 2 → 3

        New head = node at position (n - k)
        New tail = node before it

        So:
        newTail index = (n - k) - 1
                      = n - k - 1
    */
    ListNode* newTail = head;

    // for rotate left by K => for (int i = 0; i < k - 1; i++)
    for (int i = 0; i < n - k - 1; i++)
        newTail = newTail->next;

    // The node after newTail becomes the new head
    ListNode* newHead = newTail->next;

    // Step 5: Break the circular list
    newTail->next = nullptr;

    return newHead;
}
```

### Merge Two Sorted Linked List
```cpp
ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {

    // Dummy node simplifies handling the head of the merged list
    ListNode* dummy = new ListNode(-1);

    // Pointer used to build the merged list
    ListNode* temp = dummy;

    /*
        Traverse both lists simultaneously.

        At each step, attach the smaller node
        to the merged list and advance that list's pointer.
    */
    while (list1 != NULL && list2 != NULL) {

        if (list1->val <= list2->val) {

            // Attach node from list1
            temp->next = list1;

            // Move list1 forward
            list1 = list1->next;

        } else {

            // Attach node from list2
            temp->next = list2;

            // Move list2 forward
            list2 = list2->next;
        }

        // Move the merged list pointer forward
        temp = temp->next;
    }

    /*
        One of the lists may still contain remaining nodes.
        Attach the remaining portion directly since it is already sorted.
    */
    if (list1 != NULL)
        temp->next = list1;
    else
        temp->next = list2;

    // The merged list starts after the dummy node
    return dummy->next;
}
```

### Flatten a Linked List
```cpp
// Find the middle of the horizontal list
ListNode* findMid(ListNode* head) {

    ListNode* slow = head;
    ListNode* fast = head->next;

    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }

    return slow;
}

// Merge two sorted lists connected using the 'child' pointer
ListNode* merge(ListNode* list1, ListNode* list2) {

    // Create a dummy node on the heap to simplify list construction
    ListNode* dummyNode = new ListNode(-1);

    // Tail pointer used to build the merged list
    ListNode* tail = dummyNode;

    /*
        Traverse both lists simultaneously.
        Always attach the smaller node to the merged list.
        The merged list is formed using the 'child' pointer.
    */
    while (list1 && list2) {

        if (list1->val < list2->val) {

            // Attach node from list1
            tail->child = list1;

            // Move list1 down its vertical chain
            list1 = list1->child;

        } else {

            // Attach node from list2
            tail->child = list2;

            // Move list2 down its vertical chain
            list2 = list2->child;
        }

        // Move the tail pointer forward
        tail = tail->child;

        // Ensure horizontal links are removed
        // The flattened list should only use 'child'
        tail->next = NULL;
    }

    // Attach remaining nodes from whichever list is not empty
    tail->child = (list1) ? list1 : list2;

    // The merged list starts after the dummy node
    return dummyNode->child;
}

// Flatten the multi-level linked list
// TC: O(N * M) in worst case
ListNode* flattenLinkedList1(ListNode* head) {

    // Base case: empty list or only one column
    if (!head || !head->next)
        return head;

    /*
        Step 1:
        Recursively flatten the lists to the right.
        This ensures that when merging,
        both lists are already flattened.
    */
    head->next = flattenLinkedList1(head->next);

    /*
        Step 2:
        Merge the current vertical list with the
        already-flattened list on the right.
    */
    return merge(head, head->next);
}

// Divide and conquer flatten
// TC: O(N Log N)
ListNode* flattenLinkedList(ListNode* head) {

    if (!head || !head->next)
        return head;

    // Step 1: Split the horizontal list
    ListNode* mid = findMid(head);
    ListNode* right = mid->next;
    mid->next = NULL;

    // Step 2: Flatten both halves
    ListNode* leftFlat = flattenLinkedList(head);
    ListNode* rightFlat = flattenLinkedList(right);

    // Step 3: Merge the two flattened lists
    return merge(leftFlat, rightFlat);
}
```

### Sort a Linked List
```cpp
// Find the middle node of the linked list
ListNode* findMid(ListNode* head) {

    ListNode* slow = head;
    ListNode* fast = head->next;

    /*
        Fast moves 2 steps and slow moves 1 step.
        When fast reaches the end, slow will be at the middle.
    */
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }

    return slow;
}

// Merge two sorted linked lists
ListNode* merge(ListNode* list1, ListNode* list2) {

    // Dummy node simplifies list construction
    ListNode* dummy = new ListNode(-1);
    ListNode* tail = dummy;

    /*
        Traverse both lists and attach the smaller node
        to the merged list.
    */
    while (list1 && list2) {

        if (list1->val < list2->val) {
            tail->next = list1;
            list1 = list1->next;
        } else {
            tail->next = list2;
            list2 = list2->next;
        }

        tail = tail->next;
    }

    // Attach remaining nodes
    tail->next = list1 ? list1 : list2;

    return dummy->next;
}

// Sort linked list using merge sort
ListNode* sortList(ListNode* head) {

    // Base case: empty list or single node
    if (head == NULL || head->next == NULL)
        return head;

    // Step 1: Find middle and split the list
    ListNode* mid = findMid(head);

    ListNode* right = mid->next;
    mid->next = NULL;

    ListNode* left = head;

    // Step 2: Recursively sort both halves
    left = sortList(left);
    right = sortList(right);

    // Step 3: Merge the sorted halves
    return merge(left, right);
}
```