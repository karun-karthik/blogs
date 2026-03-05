# Linked List

### Traverse a linkedlist
```cpp
vector<int> LLTraversal(ListNode *head) {
    //Storing a copy of the linked list
    ListNode* temp = head;
    //To store the values 
    //Sequentially
    vector<int> ans;

    //Keep traversing
    //Until the nullptr 
    //Is not encountered
    while (temp != nullptr) {
        //Storing of the values
        ans.push_back(temp->data);
        //Storing the address of the next node
        temp = temp->next;
    }
    //Return answer 
    return ans;
}
```