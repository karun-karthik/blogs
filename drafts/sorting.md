## Sorting
```
#include <iostream>
#include <vector>
using namespace std;

void selectionSort(vector<int> &a) {
    int n = a.size();
    
    for (int i = 0; i < n; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (a[j] < a[minIdx]) {
                minIdx = j;
            }
        }
        if (minIdx != i) {
            swap(a[i], a[minIdx]);
        }
    }
}

void insertionSort(vector<int> &a) {
    int n = a.size();
    
    for (int i = 0; i < n; i++) {
        int j = i;
        
        while (j > 0 && a[j] < a[j-1]) {
            swap(a[j], a[j-1]);
            j--;
        }
    }
}

void merge(int low, int mid, int high, vector<int>&a) {
    vector<int> temp(high-low+1);
    int left = low, right = mid + 1;
    int k=0;
    
    while(left <= mid && right <= high) {
        if (a[left] <= a[right]) {
            temp[k++] = a[left++];
        } else {
            temp[k++] = a[right++];
        }
    }
    
    while (left <= mid) temp[k++] = a[left++];
    while (right <= high) temp[k++] = a[right++];
    
    for (int i = low; i<= high; i++) {
        a[i] = temp[i-low];
    }
}

void ms(int low, int high, vector<int>&a) {
    if (low >= high)    return;
    int mid = (low + high) / 2;
    ms(low, mid, a);
    ms(mid + 1, high, a);
    merge(low, mid, high, a);
}

void mergeSort(vector<int> &a) {
    int n = a.size();
    ms(0, n-1, a);
}

int partition(int low, int high, vector<int> &a) {
    int pivot = a[low];
    
    int i = low;
    int j = high;
    
    while (i < j) {
        while (i <= high && a[i] <= pivot)    i++;
        while (j >= low && a[j] > pivot)    j--;
        if (i < j)  swap(a[i], a[j]);
    }
    swap(a[low], a[j]);
    return j;
}

void qs(int low, int high, vector<int> &a) {
    if (low >= high)    return;
    int pivot = partition(low, high, a);
    qs(low, pivot-1, a);
    qs(pivot+1, high, a);
}

void quickSort(vector<int> &a) {
    int n = a.size();
    qs(0, n-1, a);
}

int main()
{
    std::vector<int> a = {3,56,23,51,2,-1};
    // selectionSort(a);
    // insertionSort(a);
    // mergeSort(a);
    quickSort(a);
    for (auto i: a) cout<<i<<" ,";
    return 0;
}
```
