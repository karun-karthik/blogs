Absolutely. Rather than memorizing these as isolated tricks, it's much easier to remember them by grouping them into **"Bit Operations"**, **"Bit Tricks"**, and **"Bitmasking"**. Here's a compact cheatsheet designed for quick interview revision.

---

## 🚀 Bit Manipulation Cheatsheet

### 1️⃣ Shift Operators

| Operation | Meaning   | Mnemonic              |
| --------- | --------- | --------------------- |
| `x << k`  | `x × 2^k` | Shift Left → Multiply |
| `x >> k`  | `x / 2^k` | Shift Right → Divide  |

```cpp
5 << 1 = 10
5 << 2 = 20

20 >> 1 = 10
20 >> 2 = 5
```

> 💡 Works exactly for powers of 2 (integer division for right shift).

---

### 2️⃣ Odd / Even

```cpp
if (n & 1)
```

```text
Last Bit

0 → Even
1 → Odd
```

Mnemonic

```text
Odd numbers always end with binary 1.
```

---

### 3️⃣ Multiply / Divide by 2

```cpp
n << 1      // n * 2
n >> 1      // n / 2
```

---

### 4️⃣ Check Power of Two ⭐

```cpp
n > 0 && (n & (n-1)) == 0
```

#### Why?

```text
8

1000

8-1

0111

1000
0111
----
0000
```

Only powers of two have **exactly one set bit**.

Mnemonic

```text
Power of 2
=
Exactly ONE set bit
```

---

### 5️⃣ Remove Lowest Set Bit ⭐⭐⭐

```cpp
n &= (n-1)
```

Example

```text
12

1100

11

1011

1100
1011
----
1000
```

Removed the rightmost 1.

Mnemonic

```text
Subtract 1
↓

Flips everything after the last set bit.

AND removes that last set bit.
```

---

### 6️⃣ Get Lowest Set Bit ⭐⭐⭐

```cpp
n & (-n)
```

Example

```text
12

1100

-12

0100

1100
0100
----
0100
```

Returns

```text
4
```

Mnemonic

```text
Extract the rightmost 1.
```

---

### 7️⃣ Count Set Bits ⭐⭐⭐

```cpp
int count = 0;

while (n) {
    n &= (n-1);
    count++;
}
```

Why?

```text
Every iteration removes exactly one set bit.
```

Time

```text
O(number of set bits)
```

---

### 8️⃣ Toggle a Bit

```cpp
n ^= (1 << i)
```

Here, `i` means the bit position we want to change. It is zero-based, so `i = 0` means the first bit (rightmost bit), and `i = 1` means the second bit.

Example

```text
10 ^ 2 = 8
1010
0010
----
1000
```

```
0 → 1
1 → 0
```

Mnemonic

```text
XOR flips.
```

---

### 9️⃣ Set a Bit

```cpp
n |= (1 << i)
```

Here, `i` means the bit position we want to set. It is zero-based, so `i = 0` means the first bit (rightmost bit), and `i = 1` means the second bit.

Example

```text
8 | 2 = 10
1000
0010
----
1010
```

```
0 → 1
1 → 1
```

Mnemonic

```text
OR only turns ON.
```

---

### 🔟 Clear a Bit

```cpp
n &= ~(1 << i)
```

Here, `i` means the bit position we want to clear. It is zero-based, so `i = 0` means the first bit (rightmost bit), and `i = 1` means the second bit.

Example

```text
n = 13 (1101), i = 2
13 & ~4 = 9
```

```
1 → 0
0 → 0
```

Mnemonic

```text
NOT creates a mask
AND clears.
```

---

### 1️⃣1️⃣ Check if ith Bit is Set

```cpp
if (n & (1 << i))
```

Returns

```text
true → ith bit is 1

false → ith bit is 0
```

---

### 1️⃣2️⃣ Binary Representation

```cpp
1 << i
```

Examples

```text
i=0

0001

i=1

0010

i=2

0100

i=3

1000
```

Mnemonic

```text
1 shifted by i
=
2^i
```

---

### 1️⃣3️⃣ Subsets using Bitmask ⭐⭐⭐⭐⭐

For

```text
n elements
```

there are

```text
2^n subsets
```

Template

```cpp
for (int mask = 0; mask < (1 << n); mask++) {

    vector<int> subset;

    for (int i = 0; i < n; i++) {

        if (mask & (1 << i))
            subset.push_back(nums[i]);
    }
}
```

---

#### Example

```
nums = [A B C]
```

| Mask | Binary | Subset |
| ---- | ------ | ------ |
| 0    | 000    | {}     |
| 1    | 001    | A      |
| 2    | 010    | B      |
| 3    | 011    | A B    |
| 4    | 100    | C      |
| 5    | 101    | A C    |
| 6    | 110    | B C    |
| 7    | 111    | A B C  |

Mnemonic

```text
Every bit decides:

1 → Take

0 → Skip
```

---

### 🎯 Common Interview Tricks

| Trick                 | Code                               |           |
| --------------------- | ---------------------------------- | --------- |
| Odd / Even            | `n & 1`                            |           |
| Multiply by 2         | `n << 1`                           |           |
| Divide by 2           | `n >> 1`                           |           |
| Power of 2            | `(n > 0) && ((n & (n-1)) == 0)`    |           |
| Count Set Bits        | `while(n){ n &= (n-1); count++; }` |           |
| Remove Lowest Set Bit | `n &= (n-1)`                       |           |
| Get Lowest Set Bit    | `n & (-n)`                         |           |
| Check ith Bit         | `n & (1<<i)`                       |           |
| Set ith Bit           | `n \|= (1<<i)`                     |           |
| Clear ith Bit         | `n &= ~(1<<i)`                     |           |
| Toggle ith Bit        | `n ^= (1<<i)`                      |           |

---

### 🧠 Memory Story (The One I Recommend)

Instead of memorizing formulas, remember the **three personalities** of the bitwise operators:

| Operator | Personality | What it does |
| -------- | ----------- | ------------ |
| `&` | **Checker / Remover** | Checks bits, removes bits |
| `\|` | **Adder** | Turns bits ON, never OFF |
| `^` | **Flipper** | Toggles bits |
| `~` | **Inverter** | Flips every bit |
| `<<` | **Multiplier** | Moves left → ×2 |
| `>>` | **Divider** | Moves right → ÷2 |

Then the tricks become almost obvious:

```text
&  → Check, Count, Remove
|  → Set
^  → Toggle
~  → Invert
<< → Multiply
>> → Divide
```

This grouping is much easier to retain than memorizing each expression independently because every trick follows naturally from the operator's "personality."

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
Explanation: Converts a decimal number into binary by repeatedly dividing by 2 and collecting the remainders.

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
Explanation: Converts a binary string back into its decimal value by adding powers of 2 for each set bit.

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
Explanation: Flips every bit of the number, changing 0s to 1s and 1s to 0s.

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
Explanation: Finds the 2's complement by inverting the bits and then adding 1, which is commonly used for signed representations.

### Bitwise AND
```cpp
int bitwiseAnd(int a, int b) {
    return a & b;
}
// TC: O(1)
// SC: O(1)
```
Explanation: Performs a bitwise AND operation, keeping a bit only if it is set in both numbers.

### Bitwise OR
```cpp
int bitwiseOr(int a, int b) {
    return a | b;
}
// TC: O(1)
// SC: O(1)
```
Explanation: Performs a bitwise OR operation, keeping a bit if it is set in either number.

### Bitwise XOR
```cpp
int bitwiseXor(int a, int b) {
    return a ^ b;
}
// TC: O(1)
// SC: O(1)
```
Explanation: Performs a bitwise XOR operation, setting a bit when the two operands differ.

### Bitwise NOT
```cpp
int bitwiseNot(int a) {
    return ~a;
}
// TC: O(1)
// SC: O(1)
```
Explanation: Inverts every bit, effectively producing the bitwise complement of the number.

### Bitwise Left Shift
```cpp
int bitwiseLeftShift(int a, int b) {
    return a << b;
}
// TC: O(1)
// SC: O(1)
// If b is 1, it's equivalent to multiplying a by 2
```
Explanation: Shifts bits to the left, which multiplies the number by powers of 2.

### Bitwise Right Shift
```cpp
int bitwiseRightShift(int a, int b) {
    return a >> b;
}
// TC: O(1)
// SC: O(1)
// If b is 1, it's equivalent to dividing a by 2
```
Explanation: Shifts bits to the right, which divides the number by powers of 2.

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
Example: swap(4, 7) → a = 7, b = 4

### Check if ith bit is set
```cpp
bool isSet(int n, int i) {
    return (n >> i) & 1;
}
// TC: O(1)
// SC: O(1)
```
Example: isSet(13, 2) → true

### Set ith bit
```cpp
void setBit(int& n, int i) {
    n |= (1 << i);
}
// TC: O(1)
// SC: O(1)
```
Example: setBit(8, 1) → 10

### Clear ith bit
```cpp
void clearBit(int& n, int i) {
    n &= ~(1 << i);
}
// TC: O(1)
// SC: O(1)
```
Example: clearBit(13, 2) → 9

### Toggle ith bit
```cpp
void toggleBit(int& n, int i) {
    n ^= (1 << i);
}
// TC: O(1)
// SC: O(1)
```
Example: toggleBit(10, 1) → 8

### Removing the last set bit
```cpp
int removeLastSetBit(int n) {
    return n & (n - 1);
}
// TC: O(1)
// SC: O(1)
```
Example: removeLastSetBit(12) → 8

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
Example: countSetBits(13) → 3

### Check if a number is power of 2
```cpp
bool isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
// TC: O(1)
// SC: O(1)
```
Example: isPowerOfTwo(16) → true

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
Example: minBitsToFlip(14, 8) → 2

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
Example: uniqueNumber([2, 4, 2, 5, 4]) → 5

### Unique Number ii (Every number appear thrice except one)
```cpp
int singleNumber(vector<int>& nums, int k, int p) {

    // INTUITION:
    // Every bit contributed by numbers appearing 'k' times
    // becomes a multiple of k and disappears after modulo.
    //
    // The remaining bits belong to the number
    // appearing 'p' times.

    int result = 0;

    // Check every bit independently
    for (int bit = 0; bit < 32; bit++) {

        int count = 0;

        // Count how many numbers have the current bit set
        for (int num : nums) {
            if (num & (1 << bit))
                count++;
        }

        // If the remainder is 'p',
        // this bit belongs to the required number
        if (count % k == p) {
            // set the corresponding bit in 'result'.
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
Example: singleNumber([2, 2, 2, 4]) → 4

### Unique Number iii (Every number appear twice except two)
```
               XOR All

        unique1 ^ unique2

               │
               ▼

      Pick ANY set bit

               │
               ▼

      Split into 2 groups

      Bit = 0      Bit = 1

       │              │
Duplicates       Duplicates
cancel           cancel

       │              │
       ▼              ▼

   unique1        unique2
```

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
Example: singleNumber([1, 2, 1, 3, 2, 5]) → [3, 5]

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
Example: divide(10, 3) → 3

### Power Set
```cpp
vector<vector<int>> powerSet(vector<int>& nums) {
    int n = nums.size();
    vector<vector<int>> result;

    // Each bitmask represents one subset.
    // Bit i:
    //   1 -> include nums[i]
    //   0 -> exclude nums[i]
    for (int mask = 0; mask < (1 << n); mask++) {
        vector<int> subset;

        // Read every bit of the current mask.
        for (int i = 0; i < n; i++) {
            // If the ith bit is set, include nums[i].
            if (mask & (1 << i)) subset.push_back(nums[i]);
        }

        result.push_back(subset);
    }

    return result;
}
```
Example: subsets([1, 2, 3]) generates 8 subsets

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
Example: findRangeXOR(3, 6) → 4

## Contests

### Odd Subsets
Given an array of unique elements nums, return all subsets of nums whose elements sum up to an odd value.
A subset of an array is any selection of its elements, including the empty set. Answers can be returned in any order.

```
Input: nums = [1, 2, 3, 4]
Output: [[1], [1, 2], [1, 2, 4], [1, 4], [2, 3], [2, 3, 4], [3], [3, 4]]
Explanation: all these subsets have an odd sum value.
```

```cpp
vector<vector<int>> setsWithOddSum(vector<int> nums) {
    int n = nums.size();
    vector<vector<int>> res;
    for (int mask = 0; mask < (1 << n); mask++) {
        vector<int> sol;
        int sum = 0;
        for (int i = 0; i < n; i++) {
            if (mask & (1 << i)) {
                sol.push_back(nums[i]);
                sum += nums[i];
            }
        }

        if (sum & 1) {
            res.push_back(sol);
        }
    }
    return res;
}
```

### Count Set Cost
Given two integers n and k, return the cost of flipping all set bits in n. One flip operation costs k.
```cpp
int setBitCost(int n, int k) {
    int count = 0;
    while (n) {
        count++;
        n = n & (n-1);
    }
    return count * k;
}
```