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
    int n = a ^ b; // gives exclusive bits
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