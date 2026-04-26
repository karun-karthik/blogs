## Fundamentals

### Decimal to Binary Conversion
```cpp
string decimalToBinary(int n) {
    if (n == 0) return "0";
    string binary = "";
    while (n > 0) {
        binary = (n % 2 == 0 ? "0" : "1") + binary;
        n /= 2;
    }
    return binary;
}
// TC: O(log n)
// SC: O(log n)
```

### Binary to Decimal Conversion
```cpp
int binaryToDecimal(string binary) {
    int decimal = 0;
    int power = 1;
    for (int i = binary.length() - 1; i >= 0; i--) {
        if (binary[i] == '1') {
            decimal += power;
        }
        power *= 2;
    }
    return decimal;
}
// TC: O(log n)
// SC: O(1)
```

### 1's Complement
```cpp
int onesComplement(int n) {
    int mask = 1;
    while (mask < n) {
        mask = (mask << 1) | 1;
    }
    return n ^ mask;
}
// TC: O(log n)
// SC: O(1)
```

### 2's Complement
```cpp
int twosComplement(int n) {
    int mask = 1;
    while (mask < n) {
        mask = (mask << 1) | 1;
    }
    return n ^ mask + 1;
}
// TC: O(log n)
// SC: O(1)
```

### Bitwise AND
```cpp
int bitwiseAnd(int a, int b) {
    return a & b;
}
// TC: O(1)
// SC: O(1)
```

### Bitwise OR
```cpp
int bitwiseOr(int a, int b) {
    return a | b;
}
// TC: O(1)
// SC: O(1)
```

### Bitwise XOR
```cpp
int bitwiseXor(int a, int b) {
    return a ^ b;
}
// TC: O(1)
// SC: O(1)
```

### Bitwise NOT
```cpp
int bitwiseNot(int a) {
    return ~a;
}
// TC: O(1)
// SC: O(1)
```

### Bitwise Left Shift
```cpp
int bitwiseLeftShift(int a, int b) {
    return a << b;
}
// TC: O(1)
// SC: O(1)
// If b is 1, it's equivalent to multiplying a by 2
```

### Bitwise Right Shift
```cpp
int bitwiseRightShift(int a, int b) {
    return a >> b;
}
// TC: O(1)
// SC: O(1)
// If b is 1, it's equivalent to dividing a by 2
```

## Algorithms

### Swap two numbers without using a temporary variable
```cpp
void swap(int& a, int& b) {
    a = a ^ b;
    b = a ^ b;
    a = a ^ b;
}
// TC: O(1)
// SC: O(1)
```

### Check if ith bit is set
```cpp
bool isSet(int n, int i) {
    return (n >> i) & 1;
}
// TC: O(1)
// SC: O(1)
```

### Set ith bit
```cpp
void setBit(int& n, int i) {
    n |= (1 << i);
}
// TC: O(1)
// SC: O(1)
```

### Clear ith bit
```cpp
void clearBit(int& n, int i) {
    n &= ~(1 << i);
}
// TC: O(1)
// SC: O(1)
```

### Toggle ith bit
```cpp
void toggleBit(int& n, int i) {
    n ^= (1 << i);
}
// TC: O(1)
// SC: O(1)
```

### Removing the last set bit
```cpp
int removeLastSetBit(int n) {
    return n & (n - 1);
}
// TC: O(1)
// SC: O(1)
```

### Count Set Bits
```cpp
int countSetBits(int n) {
    int count = 0;
    while (n > 0) {
        n &= (n - 1);
        count++;
    }
    return count;
}
// TC: O(log n)
// SC: O(1)
```

### Check if a number is power of 2
```cpp
bool isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
// TC: O(1)
// SC: O(1)
```

## FAQs

### Minimum number of bits to flip to convert a number to another number
```cpp
int minBitsToFlip(int a, int b) {
    int n = a ^ b; // has all the bits set where a and b have different bits
    int count = 0;
    while (n) {
        count++;
        n = n & (n-1);
    }
    return count;
}
// TC : O(k) where k is the number of set bits
// SC : O(1)
```

### Unique Number i (Every number appear twice except one)
```cpp
int uniqueNumber(vector<int>& nums) {
    int unique = 0;
    for (int num : nums) {
        unique ^= num;
    }
    return unique;
}
// TC : O(n)
// SC : O(1)
```

### Unique Number ii (Every number appear thrice except one)
```cpp
int singleNumber(vector<int>& nums, int k, int p) {

    int result = 0;

    for (int bit = 0; bit < 32; bit++) {
        int count = 0;
        // Count how many numbers have this bit set
        for (int num : nums) {
            if (num & (1 << bit))
                count++;
        }
        // Extract contribution of unique number
        if (count % k == p) {
            result |= (1 << bit);
        }
    }

    return result;
}
// K = 3, P = 1 for this use-case
// TC : O(n)
// SC : O(1)
```
```cpp
int singleNumber(vector<int>& nums) {

    // ones → holds bits that have appeared exactly once (mod 3)
    // twos → holds bits that have appeared exactly twice (mod 3)
    int ones = 0, twos = 0;

    for (int num : nums) {

        // Step 1:
        // Add current number's bits to 'ones' using XOR
        // (XOR toggles bits: adds if not present, removes if already present)
        // BUT remove any bits that are already in 'twos'
        // → ensures a bit doesn't exist in both 'ones' and 'twos'
        ones = (ones ^ num) & ~twos;

        // Step 2:
        // Add current number's bits to 'twos'
        // BUT remove any bits that are now in 'ones'
        // → ensures clean state transitions
        twos = (twos ^ num) & ~ones;
    }

    // After processing:
    // bits appearing 3 times are removed from both 'ones' and 'twos'
    // only bits appearing once remain in 'ones'
    return ones;
}
```

### Unique Number iii (Every number appear twice except two)
```cpp
vector<int> singleNumber(vector<int>& nums) {

    int xorAll = 0;

    // XOR all → cancels duplicates → xorAll = x ^ y
    // DRY: [1,2,1,3,2,5] → xorAll = 6 (110)
    for (int num : nums)
        xorAll ^= num;

    // Rightmost set bit → distinguishes x & y
    // DRY: diffBit = 6 & -6 = 2 (010)
    int diffBit = xorAll & -xorAll;

    int num1 = 0, num2 = 0;

    // Split into 2 groups using diffBit
    // DRY split:
    // num1: [2,3,2] → 3
    // num2: [1,1,5] → 5
    for (int num : nums) {
        if (num & diffBit)
            num1 ^= num;
        else
            num2 ^= num;
    }

    if (num1 > num2) swap(num1, num2);

    return {num1, num2}; // [3,5]
}
```

### Divide two integers without using multiplication, division and mod operator
```cpp
int divide(int dividend, int divisor) {
    // Handle overflow case
    if (dividend == INT_MIN && divisor == -1) return INT_MAX;

    // Determine sign
    bool negative = (dividend < 0) ^ (divisor < 0);

    // Convert to long to avoid overflow
    long a = labs(dividend);
    long b = labs(divisor);

    int result = 0;

    // Main logic
    while (a >= b) {
        long temp = b, multiple = 1;

        // Find largest shift
        while ((temp << 1) <= a) {
            temp <<= 1;
            multiple <<= 1;
        }

        a -= temp;
        result += multiple;
    }

    return negative ? -result : result;
}
```

### Power Set
```cpp
vector<vector<int>> subsets(vector<int>& nums) {
    int n = nums.size();
    vector<vector<int>> result;
    // DRY: nums = [1,2,3], n=3 → total = 8 (0 to 7)
    for (int i = 0; i < (1 << n); i++) {
        vector<int> subset;
        // Build subset using bits of i
        for (int j = 0; j < n; j++) {

            // Check j-th bit
            if ((i >> j) & 1) {
                subset.push_back(nums[j]);
            }
        }
        // DRY:
        // i=0 (000) -> []
        // i=1 (001) -> [1]
        // i=2 (010) -> [2]
        // i=3 (011) -> [1,2]
        // i=4 (100) -> [3]
        // i=5 (101) -> [1,3]
        // i=6 (110) -> [2,3]
        // i=7 (111) -> [1,2,3]
        result.push_back(subset);
    }
    return result;
}
```

### Range XOR
```cpp
int xorUpto(int n) {

    // XOR from 0 to n follows a repeating pattern (cycle of 4)
    // n % 4 == 0 → result = n
    // n % 4 == 1 → result = 1
    // n % 4 == 2 → result = n + 1
    // n % 4 == 3 → result = 0

    if (n % 4 == 0) return n;
    if (n % 4 == 1) return 1;
    if (n % 4 == 2) return n + 1;
    return 0;
}

int findRangeXOR(int l, int r) {

    // We cannot directly compute XOR(l → r) efficiently,
    // so we convert it into prefix XOR:

    // XOR(l → r) = XOR(0 → r) ^ XOR(0 → l-1)

    // Why this works:
    // Common part (0 → l-1) cancels out due to XOR property:
    // a ^ a = 0

    // DRY Example:
    // l = 3, r = 6
    // XOR(0→6) = 7
    // XOR(0→2) = 3
    // result = 7 ^ 3 = 4

    int xorR = xorUpto(r);       // XOR from 0 → r
    int xorL = xorUpto(l - 1);   // XOR from 0 → l-1

    return xorR ^ xorL;
}
```