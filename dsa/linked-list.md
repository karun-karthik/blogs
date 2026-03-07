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
ListNode* reverseList(ListNode* head) {
    ListNode* newHead = NULL;

    while (head != NULL) {
        ListNode* next = head->next;
        head->next = newHead;
        newHead = head;
        head = next;
    }

    return newHead;
}

ListNode *addOne(ListNode *head) {
    ListNode* reversed = reverseList(head);
    ListNode* curr = reversed;
    int carry = 1;
    while (curr != NULL) {
        int res = (curr->val) + carry;
        carry = res/10;
        curr->val = (res % 10);
        curr = curr->next;
    }
    curr = reversed;
    while (curr->next != NULL) {
        curr = curr->next;
    }
    if (carry) {
        curr->next = new ListNode(1);
    }
    return reverseList(reversed);
}
```