## Fundamentals

### Linear Search

```cpp
int linearSearch(vector<int>& nums, int target) {
    for (int i=0; i< nums.size(); i++) {
        if (nums[i] == target) 
            return i;
    }
    return -1;
}
```

### Largest Element

```cpp
int largestElement(vector<int>& nums) {
    int maxRes = INT_MIN;
    for (auto i:nums) {
        maxRes = max(maxRes, i);
    }
    return maxRes;
}
```

### Second Largest Element

```cpp
int secondLargestElement(vector<int>& nums) {
    int fmax = INT_MIN;
    int smax = INT_MIN;
    for (auto i: nums) {
        if (i > fmax) {
            smax = fmax;
            fmax = i;
        } else if (i > smax && i != fmax) {
            smax = i;
        }
    }
    return smax != INT_MIN ? smax : -1;
}
```

### Maximum Consecutive Ones

```cpp
int findMaxConsecutiveOnes(vector<int>& nums) {
    int oneCount = 0, maxRes = 0;
    for (auto i: nums) {
        if (i==1) {
            oneCount++;
            maxRes = max(maxRes, oneCount);
        } else {
            oneCount = 0;
        }
    }
    return maxRes;
}
```

### Left Rotate Array By One

```cpp
void rotateArrayByOne(vector<int>& nums) {
    int n = nums.size();
    int temp = nums[0];
    for (int i = 1; i < n; i++) {
        nums[i-1] = nums[i];
    }
    nums[n-1] = temp;
}
```

### Left Rotate Array By K

Shift to left by K

```cpp
void rotateArray(vector<int>& nums, int k) {
    int n = nums.size();
    k = k % n;
    reverse(nums.begin(), nums.begin() + k);
    reverse(nums.begin() + k, nums.end());
    reverse(nums.begin(), nums.end());
}
```

Shift to right by K
```cpp
void rotateArray(vector<int>& nums, int k) {
    int n = nums.size();
    k = k % n;
    reverse(nums.begin(), nums.end());
    reverse(nums.begin(), nums.begin() + k);
    reverse(nums.begin() + k, nums.end());
}
```

## Logic Building

### Moves Zeros to the End

```cpp
void moveZeroes(vector<int>& nums) {
    int n = nums.size();
    int i = 0, j = 0;
    while (i < n && j < n) {
        if (nums[i] != 0) {
            swap(nums[i], nums[j]);
            j++;
        }
        i++;
    }
}
```

### Remove Duplicates from Sorted Array

```cpp
int removeDuplicates(vector<int>& nums) {
    int i = 0, j = 0;
    int n = nums.size();
    while (i < n) {
        if (nums[i] != nums[j]) {
            j++;
            nums[j] = nums[i];
        }
        i++;
    }
    return j+1;
}
```

### Find missing number

```cpp
int missingNumber(vector<int>& nums) {
    int n = nums.size();
    int totalSum = 0;
    for (auto i: nums) totalSum += i;
    return (n*(n+1)/2) - totalSum;
}
```

### Union of 2 Sorted Arrays

```cpp
vector<int> unionArray(vector<int>& nums1, vector<int>& nums2) {
    int i = 0, j = 0;
    vector<int> res;
    while (i < nums1.size() && j < nums2.size()) {
        if (nums1[i] == nums2[j]) {
            if (res.empty() || res.back() != nums1[i]) res.push_back(nums1[i]);
            i++;
            j++;
        } else if (nums1[i] < nums2[j]) {
            if (res.empty() || res.back() != nums1[i]) res.push_back(nums1[i]);
            i++;
        } else {
            if (res.empty() || res.back() != nums2[j]) res.push_back(nums2[j]);
            j++;
        }
    }
    while (i < nums1.size()) {
        if (res.empty() || res.back() != nums1[i]) res.push_back(nums1[i]);
        i++;
    }
    while (j < nums2.size()) {
        if (res.empty() || res.back() != nums2[j]) res.push_back(nums2[j]);
        j++;
    }
    return res;
}
```

### Intersection of 2 Sorted Arrays

```cpp
vector<int> intersectionArray(vector<int>& nums1, vector<int>& nums2) {
    vector<int> res;
    int i=0, j=0;
    while (i < nums1.size() && j < nums2.size()) {
        if (nums1[i] == nums2[j]) {
            res.push_back(nums1[i]);
            i++; j++;
        } else if (nums1[i] < nums2[j]) {
            i++;
        } else {
            j++;
        }
    }
    return res;
}
```

## FAQ - Medium

### Leaders in an Array

Given an integer array nums, return a list of all the leaders in the array.
A leader in an array is an element whose value is strictly greater than all elements to its right in the given array. The rightmost element is always a leader. The elements in the leader array must appear in the order they appear in the nums array.

```cpp
vector<int> leaders(vector<int>& nums) {
    vector<int> res;
    int n = nums.size();
    int j = n-1;
    res.push_back(nums[j]);
    int val = nums[j];
    while (j > 0) {
        j--;
        if (nums[j] > val) {
            val = nums[j];
            res.push_back(val);
        }
    }
    reverse(res.begin(), res.end());
    return res;
}
```

### Rearrange Array elements by Sign

```cpp
vector<int> rearrangeArray(vector<int>& nums) {
    vector<int> pos, neg;
    for (auto i: nums) {
        if (i > 0) pos.push_back(i);
        else neg.push_back(i);
    }
    vector<int> res;
    int j=0,k=0;
    for (int i = 0; i< nums.size(); i++) {
        if (i%2 == 0) {
            res.push_back(pos[j++]);
        } else {
            res.push_back(neg[k++]);
        }
    }
    return res;
}
```

### Print the matrix in spiral manner - clockwise

```cpp
vector<int> spiralOrder(vector<vector<int>>& matrix) {
    vector<int> ans;
    int n = matrix.size();
    int m = matrix[0].size();
    int top = 0, left = 0;
    int bottom = n - 1, right = m - 1;
    while (top <= bottom && left <= right) {
        for (int i = left; i <= right; ++i) {
            ans.push_back(matrix[top][i]);
        }
        top++;
        for (int i = top; i <= bottom; ++i) {
            ans.push_back(matrix[i][right]);
        }
        right--;
        if (top <= bottom) {
            for (int i = right; i >= left; --i) {
                ans.push_back(matrix[bottom][i]);
            }
            bottom--;
        }
        if (left <= right) {
            for (int i = bottom; i >= top; --i) {
                ans.push_back(matrix[i][left]);
            }
            left++;
        }
    }
    return ans;
}
```

### Pascal's Triangle (I)

Given two integers r and c, return the value at the rth row and cth column (1-indexed) in a Pascal's Triangle.

```cpp
int nCr(int n, int r) {
    if(r > n-r) r = n-r;
    if(r == 1) return n;
    int res = 1;
    // Calculate nCr using iterative method avoiding overflow
    for (int i = 0; i < r; i++) {
        res = res * (n-i);
        res = res / (i+1);
    }
    return res;
}
int pascalTriangleI(int r, int c) {
    return nCr(r-1, c-1);
}
```

### Pascal's Triangle (II)

Given an integer r, return all the values in the rth row (1-indexed) in Pascal's Triangle in correct order.

```cpp
vector<int> pascalTriangleII(int r) {
    vector<int> res(r);
    res[0] = 1;
    for (int i = 1; i < r; i++) {
        res[i] = (res[i-1] * (r-i))/i;
    }
    return res;
}
```

### Pascal's Triangle (III)

Given an integer n, return the first n (1-Indexed) rows of Pascal's triangle.

```cpp
vector<int> generateRow(int row) {
    long long ans = 1;
    vector<int> res;
    res.push_back(1);
    for (int col = 1; col < row; col++) {
        ans = ans * (row - col);
        ans = ans / col;
        res.push_back(ans);
    }
    return res;
}
vector<vector<int>> pascalTriangleIII(int n) {
    vector<vector<int>> pascalTriangle;
    for (int row = 1; row <= n; row++) {
        pascalTriangle.push_back(generateRow(row));
    }
    return pascalTriangle;
}
```

### Rotate Matrix by 90 degrees

Solution 1: New position is (j, n - i - 1); => rotated[j][n - i - 1] = matrix[i][j]

```cpp
void rotateMatrix(vector<vector<int>>& matrix) {
    int n = matrix.size();
    // Transpose the matrix
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            swap(matrix[i][j], matrix[j][i]);
        }
    }
    // Reverse each row of the matrix
    for (int i = 0; i < n; i++) {
        reverse(matrix[i].begin(), matrix[i].end());
    }
}
```

### 2 Sum

```cpp
vector<int> twoSum(vector<int>& nums, int target) {
    vector<int> res;
    unordered_map<int, int> mp;
    for (int i = 0; i < nums.size(); i++) {
        if (mp.find(target-nums[i]) != mp.end()) {
            res.push_back(i);
            res.push_back(mp[target-nums[i]]);
        } else {
            mp[nums[i]] = i;
        }
    }
    sort(res.begin(), res.end());
    return res;
}
```

### 3 Sum

```cpp
vector<vector<int>> threeSum(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    int n = nums.size();
    vector<vector<int>> res;
    for (int i=0; i<n; i++) {
        if (i>0 && nums[i]==nums[i-1]) continue;
        int j = i + 1;
        int k = n - 1;
        while (j<k) {
            int sum = nums[i] + nums[j] + nums[k];
            if (sum < 0) j++;
            else if (sum > 0) k--;
            else {
                res.push_back({nums[i], nums[j], nums[k]});
                j++; k--;
                while (j<k && nums[j]==nums[j-1]) j++;
                while (j<k && nums[k]==nums[k+1]) k--;
            }
        }
    }
    return res;
}
```

### 4 Sum

```cpp
vector<vector<int>> nSum(vector<int>& nums, int n, int start,
long long target) {
    vector<vector<int>> result;
    int size = nums.size();
    // Base case: 2-sum
    if (n == 2) {
        int left = start, right = size - 1;
        while (left < right) {
            long long sum = (long long)nums[left] + nums[right];
            if (sum == target) {
                result.push_back({nums[left], nums[right]});
                // Skip duplicate numbers
                while (left < right && nums[left] == nums[left + 1]) left++;
                while (left < right && nums[right] == nums[right - 1])
                right--;
                left++;
                right--;
            } else if (sum < target) {
                left++;
            } else {
                right--;
            }
        }
    } else {
        // Recursive case: n-sum
        for (int i = start; i < size - n + 1; i++) {
            // Skip duplicate numbers
            if (i > start && nums[i] == nums[i - 1]) continue;
            vector<vector<int>> subResult =
            nSum(nums, n - 1, i + 1, target - nums[i]);
            for (vector<int>& sub : subResult) {
                sub.push_back(nums[i]);
                result.push_back(sub);
            }
        }
    }
    return result;
}
vector<vector<int>> fourSum(vector<int>& nums, int target) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> result = nSum(nums, 4, 0, target);
    // Reorder the quadruplets so that the last element is at the beginning
    for (auto& quadruplet : result) {
        std::rotate(quadruplet.begin(), quadruplet.begin() + 3,
        quadruplet.end());
    }
    return result;
}
```

### Sort an array of 0, 1, 2

```cpp
void sortZeroOneTwo(vector<int>& arr) {
    int low = 0, mid = 0, high = arr.size()-1;
    while(mid <= high) {
        if (arr[mid]==0) {
            swap(arr[low], arr[mid]);
            low++; mid++;
        } else if (arr[mid]==1) {
            mid++;
        } else {
            swap(arr[mid], arr[high]);
            high--;
        }
    }
}
```

### Kadane's algorithm

Given an integer array nums, find the subarray with the largest sum and return the sum of the elements present in that subarray.

```cpp
int maxSubArray(vector<int>& nums) {
    int maxSum = INT_MIN, sum = 0;
    for (auto i: nums) {
        sum += i;
        maxSum = max(maxSum, sum);
        if (sum < 0) sum = 0;
    }
    return maxSum;
}
```

## FAQ - Hard


### Majority Element - 1 - Moore’s Voting Algorithm

Given an integer array nums of size n, return the majority element of the array.
The majority element of an array is an element that appears more than n/2 times in the array. The array is guaranteed to have a majority element.

```cpp
int majorityElement(vector<int>& nums) {
    int ele;
    int count = 0;
    for (int i: nums) {
        if (count == 0) {
            count = 1;
            ele = i;
        } else if (ele == i) {
            count++;
        } else {
            count--;
        }
    }
    return ele;
}
```

### Majority Element - 2

Given an integer array nums of size _n_. Return all elements which appear more than n/3 times in the array. The output can be returned in any order.

```cpp
vector<int> majorityElementTwo(vector<int>& nums) {
    vector<int> res;
    int ele1 = 0, ele2 = 0;
    int count1 = 0, count2 = 0;
    for (int i: nums) {
        if (count1 == 0 && i != ele2) {
            count1 = 1;
            ele1 = i;
        } else if (count2 == 0 && i != ele1) {
            count2 = 1;
            ele2 = i;
        } else if (ele1 == i) {
            count1++;
        } else if (ele2 == i) {
            count2++;
        } else {
            count1--;
            count2--;
        }
    }
    int n = nums.size();
    count1 = 0, count2 = 0;
    for(int i = 0; i < n; i++) {
        if(nums[i] == ele1) count1++;
        if(nums[i] == ele2) count2++;
    }
    int floor = n/3 + 1;
    if(count1 >= floor) res.push_back(ele1);
    if(count2 >= floor && ele1 != ele2) res.push_back(ele2);
    return res;
}
```

### Find the repeating element and missing element

```cpp
// A appears 2, B is missing -> [A, B]
vector<int> findMissingRepeatingNumbers(vector<int> nums) {
    int n = nums.size();
    int sum = (n*(n+1))/2;
    int total = 0;
    unordered_map<int, int> mp;
    vector<int> res;
    for (auto i: nums) {
        mp[i]++;
        total += i;
    }
    for (auto i: mp) {
        if (i.second > 1) {
            res.push_back(i.first);
        }
    }
    total = total - res[0];
    res.push_back(sum-total);
    return res;
}
```

### Count Inversions

Given an integer array nums. Return the number of inversions in the array.
Two elements a[i] and a[j] form an inversion if a[i] > a[j] and i < j.
- It indicates how close an array is to being sorted.
- A sorted array has an inversion count of 0.
- An array sorted in descending order has maximum inversion.

```cpp
long long int merge(vector<int>&arr, int low, int mid, int high) {
    vector<int> temp;
    int left = low, right = mid+1;
    int count = 0;
    while (left <= mid && right <= high) {
        if (arr[left] <= arr[right]) {
            temp.push_back(arr[left]);
            left++;
        } else {
            temp.push_back(arr[right]);
            right++;
            count += (mid-left+1); // main result
        }
    }
    while (left <= mid) {
        temp.push_back(arr[left]);
        left++;
    }
    while (right <= high) {
        temp.push_back(arr[right]);
        right++;
    }
    for (int i=low; i<=high; i++) {
        arr[i] = temp[i-low];
    }
    return count;
}
long long int mergeSort(vector<int>& arr, int low, int high) {
    long long int count = 0;
    if (low < high) {
        int mid = low + (high-low)/2;
        count += mergeSort(arr, low, mid);
        count += mergeSort(arr, mid+1, high);
        count += merge(arr, low, mid, high);
    }
    return count;
}
long long int numberOfInversions(vector<int> nums) {
    return mergeSort(nums, 0, nums.size()-1);
}
```

### Reverse Pairs

Given an integer array nums. Return the number of reverse pairs in the array.
An index pair (i, j) is called a reverse pair if:
- 0 <= i < j < nums.length
- nums[i] > 2 * nums[j].

```cpp
void merge(vector<int>& arr, int start, int mid, int end) {
    vector<int> temp(end-start+1);
    int left = start;
    int right = mid+1;
    int k = 0;
    while (left <= mid && right <= end) {
        if (arr[left] < arr[right]) {
            temp[k++] = arr[left++];
        } else {
            temp[k++] = arr[right++];
        }
    }
    while (left <= mid) temp[k++] = arr[left++];
    while (right <= end) temp[k++] = arr[right++];
    for (int i=start; i<=end; i++) arr[i] = temp[i-start];
}
int countPairs(vector<int> &arr, int low, int mid, int high) {
    int right = mid + 1;
    int cnt = 0;
    for (int i = low; i <= mid; i++) {
        /*while right is less than equal to high
        and arr[i] is greater than 2 * arr[right]
        then increment right by 1*/
        while (right <= high && arr[i] > 2 * arr[right]) right++;
        cnt += (right - (mid + 1));
    }
    return cnt;
}
int mergeSort(vector<int>& nums, int start, int end) {
    int count = 0;
    if (start >= end) return count;
    int mid = start+(end-start)/2;
    count += mergeSort(nums, start, mid);
    count += mergeSort(nums, mid + 1, end);
    count += countPairs(nums, start, mid, end);
    merge(nums, start, mid, end);
    return count;
}
int reversePairs(vector<int>& nums) {
    return mergeSort(nums, 0, nums.size()-1);
}
```

### Maximum Product Subarray in an Array

Given an integer array nums. Find the subarray with the largest product, and return the product of the elements present in that subarray.
A subarray is a contiguous non-empty sequence of elements within an array.

```cpp
int maxProduct(vector<int>& arr) {
    int res = INT_MIN;
    int suffix = 1;
    int prefix = 1;
    int n = arr.size();
    for (int i = 0; i<arr.size(); i++) {
        if (prefix == 0) prefix = 1;
        if (suffix == 0) suffix = 1;
        prefix = prefix * arr[i];
        suffix = suffix * arr[n-i-1];
        res = max(res, max(suffix, prefix));
    }
    return res;
}
```

### Merge 2 sorted arrays without extra space

```cpp
void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
    int len = n + m;
    int gap = (len / 2) + (len % 2);
    while (gap > 0) {
        int left = 0;
        int right = left + gap;
        while (right < len) {
            // When left in nums1[] and right in nums2[]
            if (left < m && right >= m) {
                swapIfGreater(nums1, nums2, left, right - m);
            }
            // When both pointers in nums2[]
            else if (left >= m) {
                swapIfGreater(nums2, nums2, left - m, right - m);
            }
            // When both pointers in nums1[]
            else {
                swapIfGreater(nums1, nums1, left, right);
            }
            //Increment the pointers by 1 each
            left++, right++;
        }
        //If gap is equal break out of the loop
        if (gap == 1) break;
        gap = (gap / 2) + (gap % 2);
    }
    // Copy elements of nums2 into nums1
    for (int i = m; i < m + n; i++) {
        nums1[i] = nums2[i - m];
    }
}
void swapIfGreater(vector<int>& arr1, vector<int>& arr2, int idx1, int idx2) {
    if (arr1[idx1] > arr2[idx2]) {
        swap(arr1[idx1], arr2[idx2]);
    }
}
```