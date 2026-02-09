## Sorting Algorithms

### Selection Sort

**Intuition**

The selection sort algorithm sorts an array by repeatedly finding the minimum element from the unsorted part and putting it at the beginning. The largest element will end up at the last index of the array.

**Approach**

1. Select the starting index of the unsorted part using a loop with i from 0 to n-1.
2. Find the smallest element in the range from i to n-1 using an inner loop.
3. Swap this smallest element with the element at index i.
4. Repeat the process for the next starting index.

**Code**

```cpp
vector<int> selectionSort(vector<int>& nums) {
    int n = nums.size();
    for (int i=0; i<n-1; i++) {
        int minIdx = i;
        for (int j= i+1; j<n; j++) {
            if (nums[j] < nums[minIdx]) {
                minIdx = j;
            }
        }
        swap(nums[i], nums[minIdx]);
    }
    return nums;
}
```

### Bubble Sort

**Intuition**

The bubble sort algorithm sorts an array by repeatedly swapping adjacent elements if they are in the wrong order. The largest elements "bubble" to the end of the array with each pass.

**Approach**

1. Run a loop from 0 to n-1.
2. Run a nested loop from j from 0 to n-i-1.
3. If arr[j] > arr[j+1], swap them.
4. Continue until the array is sorted.

**Code**

```cpp
vector<int> bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i=0; i<n; i++) {
        for (int j=0; j<n; j++) {
            if (arr[i] < arr[j]) {
                swap(arr[i], arr[j]);
            }
        }
    }
    return arr;
}
```

### Insertion Sort

**Intuition**

Insertion sort builds a sorted array one element at a time by repeatedly picking the next element and inserting it into its correct position within the already sorted part of the array.

**Approach**

1. In each iteration, select an element from the unsorted part of the array using an outer loop.
2. Place this element in its correct position within the sorted part of the array.
3. Use an inner loop to shift the remaining elements as necessary to accommodate the selected element. This involves swapping elements until the selected element is in its correct position.
4. Continue this process until the entire array is sorted.

**Code**

```cpp
vector<int> insertionSort(vector<int>& nums) {
    for (int i=0; i<nums.size(); i++) {
        int j = i;
        while (j>0 && nums[j-1] > nums [j]) {
            swap(nums[j-1], nums[j]);
            j--;
        }
    }
    return nums;
}
```

### Merge Sort

**Intuition**

Merge Sort is a powerful sorting algorithm that follows the divide-and-conquer approach. The array is divided into two equal halves until each sub-array contains only one element. Each pair of smaller sorted arrays is then merged into a larger sorted array.

The algorithm consists of two main functions:
- `merge()`: This function merges the two halves of the array, assuming both parts are already sorted.
- `mergeSort()`: This function divides the array into 2 parts: low to mid and mid+1 to high where, low is the leftmost index of the array, high is the rightmost index of the array, and mid is the middle index of the array.

By repeating these steps recursively, Merge Sort efficiently sorts the entire array.

**Approach**

**mergeSort(arr[], low, high)**

1. Divide the Array: Split the given array into two halves by splitting the range. For any range from low to high, the splits will be low to mid and mid+1 to high, where mid = (low + high) / 2. This process continues until the range size is 1.
2. Recursive Division: In mergeSort(), divide the array around the middle index by making recursive calls: mergeSort(arr, low, mid) for the left half and mergeSort(arr, mid+1, high) for the right half. Here, low is the leftmost index, high is the rightmost index, and mid is the middle index of the array.
3. Base Case: To complete the recursive function, define the base case. The recursion ends when the array has only one element left, meaning low and high are the same, pointing to a single element. If low >= high, the function returns.

**merge(arr[], low, mid, high)**

1. Use a temporary array to store the elements of the two sorted halves after merging. The range of the left half is from low to mid and the range of the right half is from mid+1 to high.
2. Use two pointers, left starting from low and right starting from mid+1. Using a while loop (while left <= mid && right <= high), compare the elements from each half and insert the smaller one into the temporary array. After the loop, any leftover elements in both halves are copied into the temporary array.
3. Transfer the elements from the temporary array back to the original array in the range low to high.

**Code**

```cpp
void merge(vector<int>&arr, int low, int mid, int high) {
    vector<int> temp(high-low+1);
    int left = low, right = mid + 1;
    int k=0;
    while(left <= mid && right <= high) {
        if (arr[left]<=arr[right]) {
            temp[k++] = arr[left++];
        } else {
            temp[k++] = arr[right++];
        }
    }
    while(left<=mid) {
        temp[k++] = arr[left++];
    }
    while(right<=high) {
        temp[k++] = arr[right++];
    }
    for(int i=low; i<=high; i++) {
        arr[i] = temp[i-low];
    }
}

void ms(vector<int>&arr, int low, int high) {
    if (low>=high) return;
    int mid = (low+high)/2;
    ms(arr, low, mid);
    ms(arr, mid+1, high);
    merge(arr, low, mid, high);
}

vector<int> mergeSort(vector<int>& nums) {
    ms(nums, 0, nums.size()-1);
    return nums;
}
```


### Quick Sort

**Intuition**

Quick Sort is a divide-and-conquer algorithm like Merge Sort. However, unlike Merge Sort, Quick Sort does not use an extra array for sorting (though it uses an auxiliary stack space). This makes Quick Sort slightly better than Merge Sort from a space perspective.

This algorithm follows two simple steps repeatedly:
1. Pick a pivot and place it in its correct position in the sorted array.
2. Move smaller elements (i.e., smaller than the pivot) to the left of the pivot and larger ones to the right.

**Approach**

To implement Quick Sort, we will create two functions:

**quickSort(arr[], low, high)**

Initial Setup: The low pointer points to the first index, and the high pointer points to the last index of the array.

1. Partitioning: Use the partition() function to get the index where the pivot should be placed after sorting. This index, called the partition index, separates the left and right unsorted subarrays.
2. Recursive Calls: After placing the pivot at the partition index, recursively call quickSort() for the left and right subarrays. The range of the left subarray will be [low to partition index - 1] and the range of the right subarray will be [partition index + 1 to high].
3. Base Case: The recursion continues until the range becomes 1.

**partition(arr[], low, high)**

1. Select pivot (e.g., arr[low]).
2. Use pointers i (low) and j (high).
3. Move i forward to find element > pivot, and j backward to find element < pivot. Ensure i <= high - 1 and j >= low + 1.
4. If i < j, swap arr[i] and arr[j].
5. Continue until j < i.
6. Swap pivot (arr[low]) with arr[j] and return j as partition index.

This approach ensures that Quick Sort efficiently sorts the array using the divide-and-conquer strategy.

**Code**

```cpp
int partition(vector<int>& arr, int low, int high) {
    int ele = arr[low];
    int i = low;
    int j = high;

    while (i < j) {
        while (arr[i] <= ele && i <= high) i++;
        while (arr[j] > ele && j >= low) j--;
        if (i < j) swap(arr[i], arr[j]);
    }
    swap(arr[low], arr[j]);
    return j;
}

void qs(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pivot = partition(arr, low, high);
        qs(arr, low, pivot-1);
        qs(arr, pivot+1, high);
    }
}

vector<int> quickSort(vector<int>& nums) {
    qs(nums, 0, nums.size()-1);
    return nums;
}
```
