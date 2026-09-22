# Q1 — HashMap Internals

> **“Walk me through what happens internally when you call** `put("key", "value")` **on a** `HashMap`**.”**

### 30-Second Interview Answer

When `put(key, value)` is called, `HashMap` first obtains the key's `hashCode()` and performs additional hash spreading. It uses the processed hash and the table capacity to calculate a bucket index using `(capacity - 1) & hash`.

If the bucket is empty, a new node is inserted. If it is occupied, HashMap compares the stored hash and key equality to determine whether the key already exists; if it does, the value is replaced, otherwise the new entry is added to the collision structure.

In Java 8+, a heavily-collided bucket can be converted from a linked list into a red-black tree when the bucket reaches the treeification threshold and the table capacity is at least 64. The map also resizes when its size exceeds `capacity × loadFactor`, with the default load factor being `0.75`.

---



### Core Mental Model

Think of HashMap as:

```text
key
 ↓
hashCode()
 ↓
hash spreading
 ↓
bucket index
 ↓
table[index]
 ↓
┌───────────────────────────────┐
│ Empty?                        │
│                               │
│ YES → create Node             │
│                               │
│ NO  → inspect existing nodes  │
└───────────────────────────────┘
              ↓
       same key?
        /      \
      YES       NO
       ↓         ↓
 replace      collision
 value           ↓
             list/tree
```

The most important distinction:

```text
hashCode() → helps determine WHERE to look
equals()   → determines WHETHER the key is equal
```

---



### What Is HashMap Actually Trying to Solve?

Suppose we store:

```text
Alice → 25
Bob   → 30
Charlie → 35
```

A sequential data structure might require:

```text
search Alice
 ↓
check Bob
 ↓
check Charlie
 ↓
...
```

which can become `O(n)`.

A hash table tries to turn the key into a bucket location:

```text
"Alice"
   ↓
hashCode()
   ↓
processed hash
   ↓
bucket index
   ↓
table[index]
```

Under normal conditions, this allows approximately `O(1)` average lookup/insertion.

---



### Important: `hashCode()` Does NOT Mean Uniqueness

A common interview mistake is:

> "`hashCode()` uniquely identifies a key."

❌ Incorrect.

Two different keys can have the same hash:

```text
key A → hash 12345
key B → hash 12345
```

This is a **hash collision**.

Therefore:

```text
hashCode() ≠ unique identifier
```

HashMap handles collisions using additional key comparisons.

---



### Internal Structure

Conceptually, HashMap has a backing array:

```java
Node<K,V>[] table;
```

Think:

```text
table
 │
 ├── [0] → Node
 ├── [1] → null
 ├── [2] → Node → Node
 ├── [3] → null
 ├── ...
 └── [15] → Node
```

Each entry is represented conceptually by a node containing:

```text
Node
├── hash
├── key
├── value
└── next
```

`next` allows multiple entries to exist in the same bucket when collisions occur.

---



### What Happens During put()?

Suppose:

```java
HashMap<String, Integer> map = new HashMap<>();

map.put("Alice", 25);
```

The conceptual call chain is:

```text
put()
 ↓
hash(key)
 ↓
putVal()
 ↓
initialize/resize table if necessary
 ↓
calculate bucket
 ↓
inspect bucket
 ↓
insert / replace / collision handling
 ↓
possibly resize
```

---



### Step 1 — Calculate the Hash

The public `put()` path first calculates a HashMap-specific hash:

```java
put(K key, V value) {
    return putVal(hash(key), key, value, false, true);
}
```

The internal `hash()` performs approximately:

```java
static final int hash(Object key) {
    int h;
    return (key == null)
        ? 0
        : (h = key.hashCode()) ^ (h >>> 16);
}
```

So:

```text
"Alice"
   ↓
hashCode()
   ↓
h
   ↓
h ^ (h >>> 16)
   ↓
HashMap's processed hash
```



### Why does HashMap mix the hash?

The additional bit mixing helps distribute hash information across the bits used for bucket selection.

For interview purposes:

> HashMap does not simply use the raw `hashCode()`; it performs additional bit spreading before bucket selection.

---



### Step 2 — Initialize the Table If Necessary

A newly created default HashMap does **not necessarily allocate the backing array immediately**.

Conceptually:

```text
new HashMap<>()
      ↓
table not allocated yet
      ↓
first put()
      ↓
resize()
      ↓
allocate initial table
```

The default configuration includes:

```text
DEFAULT_INITIAL_CAPACITY = 16
DEFAULT_LOAD_FACTOR = 0.75
```

The actual backing table is allocated lazily during the first insertion.

### Interview Answer

If asked:

> Does `new HashMap<>()` immediately create 16 buckets?

Say:

> **No. HashMap uses lazy initialization. The default initial capacity is 16, but the backing table is allocated when the map first needs it, during insertion.**

---



### Step 3 — Determine the Bucket

Suppose:

```text
table length = 16
```

HashMap calculates:

```java
int i = (n - 1) & hash;
```

where:

```text
n = table.length
i = bucket index
```

Therefore:

```text
bucket = (capacity - 1) & hash
```

For capacity 16:

```text
capacity - 1 = 15
```

so:

```text
bucket = hash & 15
```

The result is between:

```text
0 and 15
```



### Important Terminology

Do not say:

> "`i` is the index of the element."

Say:

> **"**`i` **is the index of the bucket in the backing table."**

Inside that bucket there can be one or multiple nodes.

---



### Why `(n - 1) & hash`?

HashMap maintains table capacities as powers of two.

For example:

```text
16
32
64
128
256
```

For:

```text
n = 16
```

we get:

```text
n - 1 = 15
```

Binary:

```text
16 = 10000
15 = 01111
```

Therefore:

```text
hash & 01111
```

selects the lower bits needed to produce an index from:

```text
0 ... 15
```

This is closely related to:

```text
hash % 16
```

but the bitwise operation is used because the capacity is a power of two.

---



### Step 4 — Is the Bucket Empty?

The implementation effectively checks:

```java
if ((p = tab[i]) == null)
```

Here:

```text
p = tab[i]
```

means:

> Get the first `Node` stored in bucket `i`.

It does **not** mean an integer equality check.

For example:

```text
table[5]
    ↓
Node("Bob", 30)
```

then:

```java
p = table[5];
```

means:

```text
p
 ↓
Node("Bob", 30)
```

If:

```java
p == null
```

then the bucket is empty.

---



### Step 5 — Empty Bucket

If the bucket is empty:

```java
tab[i] = newNode(hash, key, value, null);
```

Conceptually:

```text
Before:

table[5] → null


After:

table[5]
    ↓
Node
├── hash
├── key = "Alice"
├── value = 25
└── next = null
```

This is the simplest `put()` path.

---



### Step 6 — What If the Bucket Is Occupied?

Suppose:

```text
table[5]
    ↓
Bob → 30
```

and we execute:

```java
map.put("Alice", 25);
```

HashMap needs to determine:

> Is the existing node actually the same key?

It considers the stored hash and key equality.

Conceptually:

```java
p.hash == hash
```

followed by key identity/equality checks.

The important idea is:

```text
same bucket
    ↓
compare hash
    ↓
compare key
    ↓
same key?
```

---



### Collision

Suppose:

```text
Alice.hashCode() == Bob.hashCode()
```

but:

```text
!Alice.equals(Bob)
```

Then they are still different keys.

They can coexist:

```text
Bucket 5

Alice → 25
   ↓
Bob → 30
```

This is a **collision**.

### Remember

```text
same hash ≠ same key
```

Two keys are considered equal only when they satisfy the equality rules.

---



### `hashCode()` and `equals()` Contract

For objects used as HashMap keys:

> If `a.equals(b)` is `true`, then `a.hashCode()` must equal `b.hashCode()`.

Formally:

```text
a.equals(b) == true
        ↓
a.hashCode() == b.hashCode()
```

The reverse is **not required**:

```text
a.hashCode() == b.hashCode()
        ⇏
a.equals(b)
```

That is exactly why collisions are possible.

### Interview Trap

Wrong:

> Different objects must have different hash codes.

Correct:

> Different objects can have the same hash code; equal objects must have the same hash code.

---



### Step 7 — Existing Key

Suppose:

```java
map.put("Alice", 25);
map.put("Alice", 30);
```

The second `put()` finds the existing key.

Therefore:

```text
Before:

Alice → 25


After:

Alice → 30
```

It does **not** create a second mapping.

The size remains:

```java
map.size() == 1
```

This is because HashMap maps each distinct key to one value.

---



### Collision Chain

Suppose many different keys map to the same bucket:

```text
Bucket 5

Alice
  ↓
Bob
  ↓
Charlie
  ↓
David
```

A lookup may have to inspect multiple nodes.

Therefore, with a linked-list collision structure:

```text
Average under good distribution → approximately O(1)
Worst-case bucket traversal     → O(n)
```

The `n` here refers to entries involved in that bucket's collision structure, not necessarily every entry in the HashMap.

---



### Java 8+ Treeification

Java 8+ can convert a heavily-collided bucket from a linked list into a **red-black tree**.

The source document identifies the important conditions:

```text
bucket reaches treeification threshold
AND
table capacity >= 64
```

Otherwise HashMap may resize instead.

Conceptually:

```text
Linked list:

A → B → C → D → E → F → G → H
```

can become:

```text
          D
        /   \
       B     F
      / \   / \
     A   C E   G
                 \
                  H
```

The actual structure is a **red-black tree**.

### Why treeify?

A long linked-list collision structure can result in:

```text
O(n)
```

search within that bucket.

A balanced tree provides approximately:

```text
O(log n)
```

search behavior.

---



### Why Threshold 8?

The threshold is a trade-off.

For a small collision chain:

```text
A → B → C
```

a linked list is simple and has low memory/structural overhead.

A tree requires additional structure such as:

```text
parent
left
right
color
```

So HashMap doesn't immediately turn every bucket into a tree.

Conceptually:

```text
small bucket
    ↓
linked list is sufficient

large bucket
    ↓
tree may be worthwhile
```

The source specifies the threshold of 8 for treeification.

---



### Why Capacity 64?

This is a **table-level condition**, while 8 is a **bucket-level condition**.

```text
8  → number of entries in one bucket

64 → capacity of the entire table
```

If the table is still relatively small:

```text
capacity < 64
```

HashMap prefers to consider **resizing first**.

Why?

A long collision chain in a small table can simply be a consequence of having too few buckets.

Increasing:

```text
16 → 32 → 64
```

can distribute entries across more buckets.

If the table is already at least 64 and one bucket still has many entries, treeification becomes more appropriate.

### Interview Answer

> **"The bucket threshold detects excessive collisions, while the 64 capacity threshold prevents premature treeification. For a relatively small table, resizing may distribute the entries more effectively; once the table is sufficiently large, a persistent large collision chain is a stronger reason to treeify."**

---



### Resize

HashMap also needs to resize as the number of entries grows.

The resize threshold is approximately:

```text
threshold = capacity × loadFactor
```

With the default:

```text
capacity = 16
loadFactor = 0.75
```

we get:

```text
threshold = 16 × 0.75
          = 12
```

So the map eventually grows:

```text
16 → 32 → 64 → 128 → ...
```

The source document describes this as resizing when the size exceeds `capacity × 0.75`.

---



### Why Load Factor?

Load factor controls the trade-off between memory usage and collision probability.

### Higher load factor

```text
more entries per table capacity
        ↓
less memory
        ↓
potentially more collisions
```



### Lower load factor

```text
more buckets
        ↓
more memory
        ↓
potentially fewer collisions
```

The default is:

```text
0.75
```

---



### What Happens During Resize?

Suppose:

```text
old capacity = 16
new capacity = 32
```

An important implementation detail:

> HashMap does not need to call `hashCode()` again on every key.

The node already stores the processed hash.

Conceptually:

```text
Node
├── hash   ← already available
├── key
├── value
└── next
```

During resize, existing nodes are redistributed into the new table using their stored hashes.

So don't casually say:

> "HashMap recalculates every hash during resize."

A more precise answer is:

> **"During resize, existing entries are redistributed using their stored hash values because the bucket calculation changes with the new table capacity."**

---



### Why Do Some Entries Stay and Others Move?

Suppose:

```text
16 → 32
```

Old bucket:

```java
hash & 15
```

New bucket:

```java
hash & 31
```

Because the capacity doubled, one additional bit becomes relevant.

An entry from old bucket `5` can therefore:

```text
stay at:

5
```

or move to:

```text
5 + 16 = 21
```

So:

```text
Old bucket 5
     │
     ├── stays → bucket 5
     │
     └── moves → bucket 21
```

This is an important reason the actual JDK implementation can redistribute efficiently.

---



### Why Does Capacity Double?

Instead of:

```text
16 → 17 → 18 → 19 → 20 ...
```

HashMap grows geometrically:

```text
16
 ↓
32
 ↓
64
 ↓
128
 ↓
256
```

This prevents frequent resizing and preserves the power-of-two property needed for efficient bucket indexing.

---



### Null Key

Another common follow-up:

> What happens if the key is `null`?

HashMap permits one `null` key.

Conceptually:

```java
map.put(null, 100);
```

For a null key, HashMap's hash calculation returns:

```text
0
```

so the null key is handled in bucket 0.

The source document explicitly identifies the null-key behavior as an edge case.

---



### Why Can HashMap Have Only One Null Key?

Because:

```java
map.put(null, 100);
map.put(null, 200);
```

uses the same key:

```text
null → 100
```

then:

```text
null → 200
```

So the second operation updates the existing mapping.

```java
map.size() == 1
```

---



### Complete `put()` Flow

This is the diagram I recommend memorizing:

```text
                    put(key, value)
                           │
                           ▼
                      hash(key)
                           │
                 ┌─────────┴─────────┐
                 │                   │
             key.hashCode()      bit mixing
                 │                   │
                 └─────────┬─────────┘
                           ▼
                    processed hash
                           │
                           ▼
                 table initialized?
                     │           │
                    NO          YES
                     │           │
                     ▼           │
                   resize()      │
                     │           │
                     └─────┬─────┘
                           ▼
                 i = (n - 1) & hash
                           │
                           ▼
                      table[i]
                           │
                  ┌────────┴────────┐
                  │                 │
                null             non-null
                  │                 │
                  ▼                 ▼
               new Node        compare existing
                                    │
                              ┌─────┴─────┐
                              │           │
                         same key      different
                              │           │
                              ▼           ▼
                        replace value   collision
                                            │
                                      ┌─────┴─────┐
                                      │           │
                                  list small   list large
                                      │           │
                                      ▼           ▼
                                    list      capacity?
                                                │
                                          ┌─────┴─────┐
                                          │           │
                                        < 64        ≥ 64
                                          │           │
                                          ▼           ▼
                                       resize      treeify
```

---



### Complexity



### Average Case

Assuming a good hash distribution:

```text
put() → O(1)
get() → O(1)
remove() → O(1)
```



### Collision Chain

With a linked-list bucket:

```text
O(n)
```

in the number of entries in that bucket.

### Treeified Bucket

Approximately:

```text
O(log n)
```

for tree operations within that bucket.

### Resize

A resize requires redistributing existing entries, so it costs work proportional to the number of entries being moved.

However, resizing isn't performed on every insertion because capacity grows geometrically.

---



### Critical Interview Follow-Ups



### "Does HashMap guarantee O(1) lookup?"

**No.**

Say:

> "HashMap provides expected average O(1) lookup under a reasonable hash distribution, but collisions can degrade performance."

---



### "Does same hashCode mean same key?"

**No.**

```text
same hashCode
    ≠
same key
```

`equals()` determines equality.

---



### "If two keys have the same hashCode, can both exist?"

**Yes**, provided they aren't equal.

```text
hash(A) == hash(B)
A.equals(B) == false

→ both can exist
```

---



### "If `equals()` is true, must hashCode be the same?"

**Yes.**

```text
a.equals(b)
    ↓
a.hashCode() == b.hashCode()
```

This is part of the `equals()`/`hashCode()` contract.

---



### "What happens if you override equals but not hashCode?"

You can violate the contract.

Two logically equal objects may have different hashes and therefore be placed into different buckets.

That can cause HashMap lookups to fail unexpectedly.

---



### "What happens when you put the same key twice?"

The existing value is replaced.

```java
map.put("A", 10);
map.put("A", 20);
```

results in:

```text
A → 20
```

not:

```text
A → 10
A → 20
```

---



### "Can HashMap have null keys?"

Yes.

It supports one `null` key.

---



### "Why is capacity a power of two?"

Because HashMap uses:

```java
(hash & (capacity - 1))
```

for bucket selection, and powers of two make this bitwise indexing work efficiently.

---



### "Why doesn't HashMap treeify every bucket?"

Because a tree has additional memory and structural overhead. For small collision chains, a linked list is simpler and sufficient.

---



### "Why resize before treeification when capacity < 64?"

Because the collision may be caused by the table being too small. Increasing the number of buckets may spread those entries out without paying the cost of treeification.

---



### "Does resize call hashCode() again?"

A precise answer:

> **No, not necessarily. The node already stores the processed hash, so HashMap can redistribute entries using the stored hash when the table capacity changes.**

---



### "Does every entry move during resize?"

**No.**

When the capacity doubles, an entry can remain in the same bucket or move to the corresponding old-index-plus-old-capacity bucket.

---



### Common Interview Mistakes



### ❌ "HashMap uses hashCode to uniquely identify keys."

Correct:

> Hash code helps locate the bucket; equality determines key equality.



### ❌ "Collision means two keys are equal."

Correct:

> Collision means different keys produce the same relevant bucket/hash location.



### ❌ "HashMap always gives O(1)."

Correct:

> Expected average O(1), with collision-dependent degradation.



### ❌ "HashMap immediately allocates 16 buckets."

Correct:

> Default initial capacity is 16, but table allocation is lazy.



### ❌ "Resize means recomputing every key's hashCode."

Correct:

> Existing nodes store the processed hash and can be redistributed using it.



### ❌ "8 means eight buckets."

Correct:

> The treeification threshold concerns entries/nodes in **one bucket**.



### ❌ "64 is required because 8 entries mathematically need 64 buckets."

Correct:

> 64 is an implementation threshold used to prefer resizing before treeification when the table is still relatively small.

---



### Interview-Ready Answer

If the interviewer asks you to explain the whole thing, say:

> **"HashMap stores entries in an internal array of buckets. When I call** `put(key, value)`**, HashMap obtains the key's** `hashCode()` **and performs additional bit spreading. It then calculates the bucket using** `(capacity - 1) & hash`**.**
>
> **If the bucket is empty, it creates a new node. If the bucket is occupied, it checks the stored hash and key equality. If the key already exists, its value is replaced; otherwise, the new key is added to the collision structure.**
>
> **In Java 8+, if a bucket becomes sufficiently crowded, HashMap can convert the collision structure from a linked list into a red-black tree. Treeification requires the bucket threshold to be reached and the table capacity to be at least 64; otherwise resizing is preferred.**
>
> **HashMap also resizes when its size crosses the load-factor threshold, which by default is approximately** `capacity × 0.75`**. During resizing, the table grows, typically doubles, and existing nodes are redistributed using their stored hashes."**

---



### 30-Second Revision

```text
HashMap.put(key, value)

1. key.hashCode()
2. HashMap spreads/mixes the hash
3. Calculate bucket:
      (capacity - 1) & hash
4. Check table[bucket]
5. Empty?
      → create Node
6. Occupied?
      → compare hash + key equality
7. Same key?
      → replace value
8. Different key?
      → collision → linked list/tree
9. Bucket gets sufficiently large?
      → treeify if capacity >= 64
      → otherwise resize
10. Size crosses threshold?
      → resize
```



### The 5 things to never forget

```text
hashCode() → WHERE
equals()   → WHICH KEY
bucket     → WHERE ENTRY LIVES
collision  → DIFFERENT KEYS, SAME BUCKET
loadFactor → WHEN TABLE GROWS
```

And the three numbers:

```text
16  → default initial capacity
0.75 → default load factor
8   → treeification threshold

64  → minimum table capacity for treeification
```

The uploaded source explicitly frames Q1 around `put()`, bucket selection, collision handling, Java 8+ treeification, and resizing, including the 8/64 conditions and `0.75` load factor.

# Q2 — Why Is String Immutable in Java?

> **“Why is** `String` **immutable in Java?”**



### 30-Second Interview Answer

`String` is immutable, meaning once a `String` object is created, its contents cannot be changed. Any operation that appears to modify a String actually creates another String object and changes the reference to point to it.

Immutability provides several important properties: Strings can safely be shared through the String Pool, their hash code remains stable when used as keys in `HashMap`, and their contents cannot unexpectedly change when shared between components or threads. It also provides security benefits because a String's contents cannot change between validation and use.

---



### What Does Immutable Mean?

An immutable object is an object whose **state cannot be changed after construction**.

For:

```java
String s = "hello";
```

the String object representing:

```text
hello
```

cannot later become:

```text
world
```

through mutation.

The reference can change:

```java
s = "world";
```

but the original `"hello"` object itself was not modified.

### Key distinction

```text
Object immutability
    ↓
object's state cannot change

Reference reassignment
    ↓
variable points to another object
```

These are different concepts.

---



### Example: String Concatenation

Consider:

```java
String s = "hello";

s = s + " world";
```

It may look like `"hello"` is being modified.

It isn't.

Conceptually:

```text
Before:

"hello"
   ↑
   s


After:

"hello"

"hello world"
       ↑
       s
```

A new String representing `"hello world"` is created and `s` is updated to reference it.

The original `"hello"` remains unchanged.

---



### Why Does Java Make String Immutable?

There are several important consequences.

### 1. String Pool / Safe Sharing

Java can reuse identical String literals.

```java
String a = "hello";
String b = "hello";
```

Conceptually:

```text
String Pool

        "hello"
        /     \
       a       b
```

Both references can point to the same String object.

This is safe because neither `a` nor `b` can modify the shared String.

If Strings were mutable:

```text
        "hello"
        /     \
       a       b
```

and `a` could modify the object, `b` would unexpectedly observe the modification.

Immutability makes shared String objects safe to reuse.

---



### 2. HashMap Keys Remain Safe

This is one of the most important interview connections.

Consider:

```java
HashMap<String, Integer> map = new HashMap<>();

String key = "Alice";

map.put(key, 100);
```

HashMap uses the key's hash to determine the bucket.

Conceptually:

```text
"Alice"
   ↓
hashCode()
   ↓
bucket 5
```

Now imagine Strings were mutable.

If the key changed:

```text
"Alice" → "Bob"
```

its hash could change:

```text
hash("Alice") != hash("Bob")
```

The entry, however, was originally placed using the hash of `"Alice"`.

You could end up with:

```text
Entry physically stored:

bucket 5
   ↓
"Bob" → 100
```

while:

```text
hash("Bob")
    ↓
bucket 12
```

A subsequent lookup could search bucket 12 and fail to find the entry sitting in bucket 5.

Therefore:

> **An immutable String has a stable value and therefore a stable hash code, making it safe to use as a HashMap key.**

This connects directly to Q1's `hashCode()`/`equals()` discussion.

---



### 3. Security

Strings are frequently used to represent security-sensitive information such as:

```text
file paths
URLs
class names
configuration values
usernames
connection information
```

Imagine:

```text
validate(path)
     ↓
path is considered safe
     ↓
use(path)
```

If the String could be modified between validation and use:

```text
validate(path)
     ↓
path changes
     ↓
use(path)
```

the validated value and the used value could differ.

With an immutable String:

```text
validate(path)
     ↓
same contents
     ↓
use(path)
```

the contents cannot silently change.

So immutability provides an important security property around values that are validated and subsequently used.

---



### 4. Safe Sharing

Strings are frequently shared between different parts of an application.

Because they cannot change:

```text
Component A ──┐
              ├──► "hello"
Component B ──┤
              │
Component C ──┘
```

all components can safely read the same String.

No component can modify the object underneath the others.

---



### 5. Thread Safety

Immutable objects are inherently easier to share between threads because their state cannot be changed after construction.

For example:

```text
Thread 1 ──┐
Thread 2 ──┼──► "hello"
Thread 3 ──┘
```

All threads can read the same String without one thread modifying the String's state.

Important:

> **String's immutability means its own state cannot be modified; this does not mean every operation involving Strings is automatically thread-safe.**

---



### String Pool

String literals are commonly stored/reused through the JVM's String Pool.

For:

```java
String a = "hello";
String b = "hello";
```

the literals can refer to the same pooled String:

```text
       String Pool

          "hello"
          /     \
         /       \
        a         b
```

Therefore:

```java
a == b
```

can be:

```text
true
```

because both references can refer to the same object.

And:

```java
a.equals(b)
```

is also:

```text
true
```

because their contents are equal.

---



### `new String(...)`

Consider:

```java
String a = new String("hello");
String b = new String("hello");
```

Each `new String(...)` creates a distinct String object.

Conceptually:

```text
Heap:

String object #1
     "hello"
        ↑
        a


String object #2
     "hello"
        ↑
        b
```

Therefore:

```java
a == b
```

is:

```text
false
```

because the references point to different objects.

But:

```java
a.equals(b)
```

is:

```text
true
```

because the String contents are equal.

### Important

Do not say:

> "`new String()` creates the String on the stack."

Correct:

> **The String objects are heap objects; local references may live in stack frames/registers depending on JVM implementation and optimization.**

---



### `==` vs `equals()` for Strings

```java
String a = "hello";
String b = "hello";

System.out.println(a == b);
System.out.println(a.equals(b));
```

Potential result:

```text
true
true
```

because the literals can share the pooled object.

But:

```java
String a = new String("hello");
String b = new String("hello");
```

gives:

```text
a == b        → false
a.equals(b)   → true
```

because there are two distinct objects containing equal characters.

### Interview rule

For comparing String contents:

```java
a.equals(b)
```

not:

```java
a == b
```

---



### `final` Does NOT Mean Immutable

This is a classic interview question.

Consider:

```java
final StringBuilder sb = new StringBuilder("hello");

sb.append(" world");
```

This is valid.

Why?

Because:

```text
final
 ↓
reference cannot be reassigned
```

but:

```text
mutable object
 ↓
state can still change
```

So:

```text
final reference
        ≠
immutable object
```

For example:

```java
final StringBuilder sb = new StringBuilder("hello");

sb = new StringBuilder("world");  // ❌
sb.append(" world");              // ✅
```

The reference cannot change, but the StringBuilder's internal state can.

---



### String vs StringBuilder

This is a common follow-up.

### String

```java
String s = "hello";
s += " world";
```

Immutable.

Conceptually:

```text
old String
    ↓
new String
```



### StringBuilder

```java
StringBuilder sb = new StringBuilder("hello");

sb.append(" world");
```

Mutable.

Conceptually:

```text
same StringBuilder
       ↓
internal state changes
```

Therefore:

```text
String        → immutable
StringBuilder → mutable
```

For repeated modifications, `StringBuilder` is generally more appropriate than repeatedly creating Strings.

---



### Why Doesn't `s += "world"` Violate Immutability?

This is a classic follow-up.

```java
String s = "hello";

s += " world";
```

doesn't mutate `"hello"`.

Conceptually:

```text
s
 ↓
"hello"

        +

" world"

        ↓

"hello world"
      ↑
      s
```

The reference `s` is reassigned to another String.

Therefore:

```text
Object:
"hello"
    ↓
unchanged

Reference:
s
    ↓
changed
```

This is completely compatible with String immutability.

---



### Why Is Immutability Important for HashMap?

This is worth memorizing as an interview explanation:

```text
HashMap key
    ↓
hashCode()
    ↓
bucket
```

If the key's state changes after insertion:

```text
old state
   ↓
old hash
   ↓
old bucket
```

but after mutation:

```text
new state
   ↓
new hash
   ↓
new bucket
```

the object can physically remain in the old bucket while lookup searches the new bucket.

Immutable keys avoid this problem.

### General Rule

Objects used as HashMap keys should have stable fields participating in:

```java
equals()
hashCode()
```

String naturally satisfies this because it is immutable.

---



### Interview Follow-Ups



### Why is String immutable?

> String is immutable so its value cannot change after creation. This enables safe String Pool sharing, keeps its hash code stable for use as HashMap keys, simplifies sharing between threads/components, and provides useful security properties for validated values.



### Why is String Pool possible because of immutability?

> Multiple references can safely share the same String object because none of them can modify the object's contents.



### Why is String a good HashMap key?

> Its contents and therefore its hash code remain stable after insertion, so the key doesn't move logically to a different bucket while the entry remains physically stored in the original bucket.



### What happens when you concatenate Strings?

> A new String is produced; the existing String isn't modified.



### Is `String` immutable because it is `final`?

> No. `final` prevents reassignment of a reference; immutability prevents modification of an object's state. They are different concepts.



### Why not use `StringBuilder` everywhere?

> StringBuilder is mutable and is useful when repeatedly constructing/modifying text. String is preferable when you want an immutable value that can be safely shared and used as a key.



### `==` vs `equals()`?

> `==` compares object references, while `String.equals()` compares String contents.



### What happens with `new String("hello")`?

> A new String object is created on the heap even though `"hello"` may already exist in the String Pool.

---



### Common Interview Mistakes

```text
❌ String is immutable because it is final.

✅ final reference ≠ immutable object
```

```text
❌ hashCode() uniquely identifies a String.

✅ Equal Strings must have equal hash codes, but different Strings can collide.
```

```text
❌ String concatenation modifies the original String.

✅ A new String is created and the reference is updated.
```

```text
❌ new String("hello") creates the object on the stack.

✅ The String object is a heap object.
```

```text
❌ == compares String values.

✅ == compares references; equals() compares contents.
```

---



### Interview-Ready Answer

> **"String is immutable, meaning once a String object is created, its contents cannot be changed. Operations like concatenation create a new String rather than modifying the existing object.**
>
> **This immutability is important because Java can safely reuse String objects through the String Pool—multiple references can point to the same object without one reference being able to modify it. It also makes String safe and predictable as a HashMap key because its value and hash code cannot change after insertion.**
>
> **Immutability also makes Strings easier to safely share between components and threads and provides useful security properties when Strings are validated and subsequently used.**
>
> **It's important not to confuse** `final` **with immutability:** `final` **prevents a reference from being reassigned, while immutability prevents the object's state from changing."**

---



### 30-Second Revision

```text
String = immutable

Immutable means:
→ object's state cannot change after creation

s = s + "world"
→ doesn't modify old String
→ creates another String
→ s points to new String

Why immutable?

1. String Pool
   → safe sharing

2. HashMap
   → stable value/hashCode
   → safe key

3. Security
   → value can't change between validation/use

4. Sharing
   → components/threads can safely read it

5. Simpler concurrency
   → no mutable String state

Remember:

final reference ≠ immutable object

String:
→ immutable

StringBuilder:
→ mutable

String literals:
→ can be pooled/shared

new String("hello"):
→ new heap object

==:
→ reference identity

equals():
→ content equality
```



# Q3 — ArrayList vs LinkedList: Internals, Complexity & Interview Follow-ups



### What’s the difference between `ArrayList` and `LinkedList`? When would you use one over the other?

**Source question:** “What’s the difference between `ArrayList` and `LinkedList`? When would you use one over the other?”

---



### 30-Second Interview Answer

`ArrayList` is backed by a **resizable array**, while `LinkedList` is implemented as a **doubly linked list**.

`ArrayList` provides **O(1) random access** because it can directly access an array index, whereas `LinkedList` requires traversal, making indexed access **O(n)**.

Appending to the end is **O(1) amortized** for `ArrayList` and **O(1)** for `LinkedList`.

Insertion/removal in the middle is **O(n)** for both when using an index:

- `ArrayList` needs to shift elements.
- `LinkedList` needs to traverse to the position first, although the actual node insertion/removal is O(1) once the node is known.

`LinkedList` also has higher memory overhead because every node stores `prev`, `next`, and the element reference.

For most general-purpose list workloads involving **random access and iteration**, I would choose `ArrayList`. `LinkedList` is useful when frequent insertion/removal is performed through an already-positioned iterator/node.

---



### Internal Data Structures



### ArrayList

Conceptually:

```java
class ArrayList<E> {
    Object[] elementData;
    int size;
}
```

The backing storage is an `Object[]`.

For:

```java
ArrayList<Integer> list = new ArrayList<>();
list.add(10);
list.add(20);
list.add(30);
```

conceptually:

```text
ArrayList
   |
   v
Object[]
+----+----+----+
| 10 | 20 | 30 |
+----+----+----+
```

The array contains **references** to objects.

For `ArrayList<Integer>`, the elements are `Integer` objects rather than primitive `int` values.

### LinkedList

`LinkedList` is a **doubly linked list**.

Each node conceptually contains:

```text
Node<E>

+----------+----------+----------+
|  prev    |  item    |  next   |
+----------+----------+----------+
```

The list looks like:

```text
first
  |
  v
[A] <-> [B] <-> [C] <-> [D]
                           ^
                           |
                          last
```

This is why `LinkedList` can efficiently manipulate neighboring nodes once the required position is known.

---



### ArrayList — Size vs Capacity



### Size

Number of elements currently stored.

### Capacity

Number of elements the current backing array can hold before another resize is required.

Example:

```text
capacity = 10
size     = 7
```

means 7 elements are currently stored in an array capable of holding 10 references.

---



### ArrayList — Does `new ArrayList<>()` Immediately Create an Array?

With the modern JDK implementation, the default constructor does not immediately allocate a full backing array.

```java
ArrayList<Integer> list = new ArrayList<>();
```

Actual storage is allocated when elements are added.

By contrast:

```java
new ArrayList<>(10)
```

explicitly requests an initial capacity of 10.

---



### ArrayList — Adding at the End

For:

```java
list.add(value);
```

if there is available capacity, the element is placed at the next available position.

Therefore:

```text
add(element) → O(1)
```

for the normal case.

### What happens when the array is full?

Suppose:

```text
size     = 10
capacity = 10
```

and:

```java
list.add(10);
```

Conceptually:

```text
add()
  |
  v
check capacity
  |
  +-- enough space? → insert
  |
  +-- no space?
         |
         v
       grow
         |
         v
  allocate larger array
         |
         v
  copy existing references
         |
         v
      insert element
```

So the backing array is grown **before** the new element is inserted.

The old backing array becomes unreachable and therefore **eligible for garbage collection**.

The existing references are copied into the new array. The objects themselves are not duplicated merely because the array grows.

---



### ArrayList Growth

A common misconception is:

> “ArrayList always doubles its capacity.”

Do not treat that as the Java implementation rule.

Current OpenJDK implementations grow the backing array by approximately **1.5×** when more capacity is required.

Conceptually:

```text
10 → 15 → 22 → 33 → 49 → ...
```

The exact implementation details can vary by JDK version.

For interviews:

> “ArrayList grows its backing array geometrically; current OpenJDK growth is approximately 1.5×.”

---



### Why Is `ArrayList.add()` O(1) Amortized?

A single append that triggers resizing is expensive.

If the current capacity is `n`, resizing requires copying approximately `n` references:

```text
resize → O(n)
```

Therefore:

```text
One particular add() that triggers resize → O(n)
```

But most `add()` operations do not trigger resizing.

Across many insertions, the total resizing work is linear because capacity grows geometrically.

```text
n normal insertions     → O(n)
total resizing/copying  → O(n)
--------------------------------
total                   → O(n)
```

Therefore:

```text
O(n) / n = O(1) amortized
```



### Interview distinction


| Operation                        | Complexity         |
| -------------------------------- | ------------------ |
| Append when capacity exists      | O(1)               |
| Particular append causing resize | O(n)               |
| Many appends overall             | **O(1) amortized** |


---



### ArrayList — Resize vs Insertion Shift

Do not confuse these two operations.

### Resize

Creates a larger backing array and **copies references**:

```text
Old:

[A][B][C][D]

       copy

New:

[A][B][C][D][ ][ ][ ]
```



### Middle insertion

Existing elements are **shifted within the array**:

```text
Before:

[A][B][C][D][E]
       ^
      index 2

After:

[A][B][X][C][D][E]
```

Here `C`, `D`, and `E` move one position to the right.

---



### ArrayList — Middle Insertion

For:

```java
list.add(2, X);
```

given:

```text
[A][B][C][D][E]
```

the result is:

```text
[A][B][X][C][D][E]
```

The elements after index `2` must move.

Conceptually, Java uses optimized array-copy machinery such as:

```java
System.arraycopy(
    elementData,
    index,
    elementData,
    index + 1,
    size - index
);
```

Then:

```java
elementData[index] = element;
```

If `k` elements must be moved:

```text
copy k elements → O(k)
```

Worst case:

```text
ArrayList.add(index, value) → O(n)
```

---



### LinkedList — Random Access

Consider:

```java
list.get(500_000);
```

A `LinkedList` cannot directly jump to node 500,000.

It must traverse nodes.

Java optimizes traversal by choosing the closer end:

```java
if (index < size / 2)
    // traverse from first
else
    // traverse from last
```

Therefore:

```text
LinkedList.get(index) → O(n)
```

Even though it may traverse approximately `n/2` nodes:

```text
O(n / 2) = O(n)
```

---



### LinkedList — Indexed Insertion

Consider:

```java
linkedList.add(500_000, value);
```

There are two conceptual operations:

```text
1. Find the position → O(n)

2. Insert the node → O(1)
```

Therefore:

```text
O(n) + O(1)
= O(n)
```



### Interview phrasing

> “The actual node insertion is O(1) once the node or iterator position is known. But indexed insertion is O(n) because finding that position requires traversal.”

---



### LinkedList — Actual Node Insertion

Suppose:

```text
A <-> B <-> C
```

We want to insert `X` between `B` and `C`:

```text
A <-> B <-> X <-> C
```

Only a constant number of references need to change:

```java
X.prev = B;
X.next = C;

B.next = X;
C.prev = X;
```

Therefore:

```text
Actual pointer manipulation → O(1)
```

---



### LinkedList — Memory Overhead

Each node needs:

```text
object header
prev reference
item reference
next reference
```

So compared with `ArrayList`, it has significantly more per-element overhead.

```text
LinkedList → higher memory overhead
ArrayList  → lower per-element overhead
```

---



### Cache Locality

`ArrayList` stores references contiguously in an array:

```text
[A][B][C][D][E][F]
```

This provides good **spatial locality** and is generally cache-friendly.

`LinkedList` nodes may be scattered around the heap:

```text
[Node A]          [Node D]

       [Node B]

                    [Node C]
```

Therefore sequential `ArrayList` traversal can be faster in practice even when both operations are theoretically O(n).

Big-O describes asymptotic growth; it does not capture all hardware-level performance effects.

---



### LinkedList Iteration Trap

Consider:

```java
for (int i = 0; i < list.size(); i++) {
    System.out.println(list.get(i));
}
```

with a `LinkedList`.

Each `get(i)` requires traversal.

Therefore:

```text
n iterations
×
O(n) indexed lookup
=
O(n²)
```

So:

```text
LinkedList + get(i) loop → O(n²)
```



### ArrayList version

For `ArrayList`:

```java
for (int i = 0; i < list.size(); i++) {
    System.out.println(list.get(i));
}
```

each `get(i)` is O(1):

```text
n × O(1) = O(n)
```

Therefore:

```text
ArrayList  → O(n)
LinkedList → O(n²)
```

---



### Iterating Over LinkedList

Prefer:

```java
for (Integer value : list) {
    System.out.println(value);
}
```

or:

```java
Iterator<Integer> iterator = list.iterator();

while (iterator.hasNext()) {
    System.out.println(iterator.next());
}
```

The iterator maintains its current position and moves node-to-node instead of repeatedly searching for each index.

Therefore:

```text
LinkedList sequential iteration → O(n)
```

---



### Interview Follow-ups



### Follow-up 1 — Does `new ArrayList<>()` immediately create an array?

**Answer:** No, with the modern JDK implementation, the default constructor starts with an empty/default backing array. Actual storage is allocated when elements are added.

---



### Follow-up 2 — Where are `ArrayList` elements stored?

**Answer:** In an internal `Object[]` backing array.

```java
ArrayList<Integer> list = new ArrayList<>();
list.add(10);
```

Conceptually:

```text
ArrayList
   |
   v
Object[]
+----+----+----+
| 10 |    |    |
+----+----+----+
```

The array contains references to `Integer` objects.

---



### Follow-up 3 — What happens when an `ArrayList` becomes full?

**Answer:**

1. Check capacity.
2. Grow the backing array if necessary.
3. Allocate a larger `Object[]`.
4. Copy existing references.
5. Insert the new element.
6. The old array becomes eligible for GC once unreachable.

---



### Follow-up 4 — Is the resize-triggering `add()` O(1)?

**Answer:** No.

That particular operation is **O(n)** because existing references must be copied.

However, repeated appends are **O(1) amortized**.

---



### Follow-up 5 — Why is `ArrayList.add()` O(1) amortized?

**Answer:** Because the backing array grows geometrically. Expensive O(n) resizes happen infrequently, so the total resizing work across n insertions is O(n).

Thus:

```text
O(n) total work / n insertions = O(1) amortized
```

---



### Follow-up 6 — What happens during `ArrayList` middle insertion?

For:

```java
list.add(2, 100);
```

given:

```text
[A][B][C][D][E]
```

result:

```text
[A][B][100][C][D][E]
```

`C`, `D`, and `E` shift right.

This is O(n) in the worst case.

---



### Follow-up 7 — What is the internal structure of `LinkedList`?

**Answer:** A doubly linked list.

Each node contains:

```text
prev
item
next
```

The list maintains references to the first and last nodes.

---



### Follow-up 8 — How does `LinkedList.get(index)` find an element?

It traverses from the closer end:

```text
index < size / 2 → start from first
index >= size / 2 → start from last
```

Overall complexity:

```text
O(n)
```

---



### Follow-up 9 — Is insertion into `LinkedList` O(1)?

**Answer:** The actual node insertion is O(1) if the position/node is already known.

But:

```java
list.add(index, value);
```

is O(n) because locating the indexed position requires traversal.

---



### Follow-up 10 — Why does `LinkedList` use more memory?

Every node requires:

- object header
- `prev`
- `item`
- `next`

Therefore it has substantially more per-element overhead than an `ArrayList`.

---



### Follow-up 11 — Why can `ArrayList` be faster even when both are O(n)?

**Answer:** Cache locality.

`ArrayList` stores references contiguously, while linked-list nodes can be scattered across the heap.

---



### Follow-up 12 — Why can `LinkedList.get(i)` in a loop become O(n²)?

Because each indexed `get()` is O(n), and the loop performs n such operations:

```text
n × O(n) = O(n²)
```

---



### Follow-up 13 — How can you iterate through a `LinkedList` in O(n)?

Use an iterator or enhanced `for` loop:

```java
for (Integer value : list) {
    // ...
}
```

The iterator advances node-by-node.

---



### Follow-up 14 — What is the difference between `size` and `capacity`?

**Size:** number of elements currently stored.

**Capacity:** number of elements the current backing array can hold before it needs to grow.

Example:

```text
capacity = 10
size     = 7
```

---



### Follow-up 15 — Why not create a new array for every `add()`?

If we allocated a new array every time:

```text
add 1 → copy 0
add 2 → copy 1
add 3 → copy 2
add 4 → copy 3
...
```

Total copying would become:

```text
1 + 2 + 3 + ... + n = O(n²)
```

Geometric growth avoids this and provides O(1) amortized append.

---



### Complexity Cheat Sheet


| Operation                                | ArrayList          | LinkedList |
| ---------------------------------------- | ------------------ | ---------- |
| `get(index)`                             | **O(1)**           | **O(n)**   |
| `set(index, value)`                      | **O(1)**           | **O(n)**   |
| `add(value)` at end                      | **O(1) amortized** | **O(1)**   |
| `add(0, value)`                          | **O(n)**           | **O(1)**   |
| `add(index, value)`                      | **O(n)**           | **O(n)**   |
| `remove(index)`                          | **O(n)**           | **O(n)**   |
| Remove with known node/iterator position | —                  | **O(1)**   |
| Sequential iteration                     | **O(n)**           | **O(n)**   |
| Indexed `get(i)` loop                    | **O(n)**           | **O(n²)**  |
| Memory overhead                          | Lower              | Higher     |


---



### Interview Traps



### Trap 1 — “ArrayList insertion is always O(n)”

Not exactly.

```text
append with capacity → O(1)
append with resize   → O(n)
append amortized     → O(1)
middle insertion     → O(n)
```



### Trap 2 — “LinkedList insertion is O(1)”

Incomplete.

Correct:

```text
Known node/iterator position
        ↓
actual insertion → O(1)
```

But:

```text
add(index, value)
        ↓
find position → O(n)
        ↓
insert → O(1)
        ↓
overall → O(n)
```



### Trap 3 — “LinkedList is better for insertion”

Only when the position/node is already known.

### Trap 4 — “ArrayList always doubles”

Do not state this as a Java guarantee. Current OpenJDK growth is approximately 1.5×.

### Trap 5 — “One resize is O(1) because add() is O(1)”

No.

```text
Individual resize-triggering add → O(n)
Repeated appends → O(1) amortized
```



### Trap 6 — “LinkedList iteration is O(n²)”

Not generally.

This is O(n):

```java
for (Integer x : linkedList) {
    // ...
}
```

This can be O(n²):

```java
for (int i = 0; i < linkedList.size(); i++) {
    linkedList.get(i);
}
```

---



### Final Interview Answer

> "`ArrayList` is backed by a dynamically growing array, while `LinkedList` is a doubly linked list. `ArrayList` provides O(1) indexed access because it can directly access an array position, whereas `LinkedList` needs to traverse nodes, so indexed access is O(n).
>
> Appending to an `ArrayList` is O(1) amortized. Occasionally the backing array becomes full, causing a resize and O(n) copying operation. `LinkedList` can append at the end in O(1) because it maintains a reference to the last node.
>
> For middle insertion, `ArrayList` has to shift subsequent elements, making it O(n). `LinkedList` performs the actual node insertion in O(1), but finding the indexed position is O(n), so `add(index, value)` is also O(n).
>
> `LinkedList` has higher memory overhead because every node stores the element plus previous and next references, and its nodes have additional object overhead. `ArrayList` also generally has better cache locality.
>
> For most general-purpose workloads involving indexed access, iteration, and appending, I'd choose `ArrayList`. I'd consider `LinkedList` when I specifically need frequent insertion/removal through an already-positioned iterator or node and don't need random access."



# Q4 · == vs equals() vs the hashCode contract



### Exact question from the PDF

**“Explain the difference between** `==` **and** `.equals()`**. Then explain the hashCode contract.”**

### 30-second interview answer

- `==` on objects compares **identity/reference equality** — whether both references refer to the same object.
- `.equals()` compares **logical equality** when a class overrides it. `Object.equals()` defaults to identity-style comparison, while classes such as `String` and `Integer` override it for value/content equality.
- The `hashCode` contract says: **if** `a.equals(b)` **is** `true`**, then** `a.hashCode() == b.hashCode()` **must always be true.**
- The reverse is **not** required: two unequal objects can have the same hash code because hash collisions are allowed.
- Breaking the contract can cause incorrect behavior in `HashMap`, `HashSet`, and other hash-based collections.



### 1. `==` vs `.equals()`



### `==` with objects

For object references:

```java
String a = new String("hello");
String b = new String("hello");

System.out.println(a == b); // false
```

`a` and `b` refer to two different `String` objects.

So:

```text
== → identity/reference comparison
```

It does not compare the contents of the objects.

### `.equals()`

```java
String a = new String("hello");
String b = new String("hello");

System.out.println(a.equals(b)); // true
```

`String` overrides `equals()` to compare its character contents.

Important distinction:

```text
Object.equals()
    → defaults to identity-style equality

Overridden equals()
    → can define logical/value equality
```



### 2. String pool example

```java
String a = "hello";
String b = "hello";

System.out.println(a == b);      // true
System.out.println(a.equals(b)); // true
```

Both references point to the same pooled string object.

The important interview point is **not** that `==` compares values for strings. `==` is still comparing references; it happens to be `true` because both references refer to the same object.

### 3. What happens when `equals()` is not overridden?

```java
class User {
    int id;

    User(int id) {
        this.id = id;
    }
}

User u1 = new User(10);
User u2 = new User(10);

System.out.println(u1 == u2);      // false
System.out.println(u1.equals(u2)); // false
```

`u1` and `u2` are different objects.

Because `User` does not override `equals()`, it inherits `Object.equals()`, which performs identity-style equality.

### 4. The hashCode contract

The central rule is:

```text
a.equals(b) == true
        ↓
a.hashCode() == b.hashCode()
```

This **must** hold.

The reverse does not have to hold:

```text
a.hashCode() == b.hashCode()
        ↓
a.equals(b) may be true OR false
```

Unequal objects can have the same hash code. This is a **hash collision**.

### 5. Example of a valid collision

Suppose:

```java
User u1 = new User(10, "Alice");
User u2 = new User(10, "Bob");
```

and `equals()` uses both `id` and `name`.

Then:

```java
u1.equals(u2); // false
```

But it is completely legal for:

```java
u1.hashCode() == u2.hashCode(); // true
```

A hash collision does not violate the contract.

### 6. Why overriding `equals()` without `hashCode()` is dangerous

Consider:

```java
class User {
    int id;

    User(int id) {
        this.id = id;
    }

    @Override
    public boolean equals(Object obj) {
        User other = (User) obj;
        return this.id == other.id;
    }
}
```

Here:

```java
User u1 = new User(10);
User u2 = new User(10);

u1.equals(u2); // true
```

But `hashCode()` was not overridden.

The objects therefore inherit the default `Object.hashCode()` behavior, which can produce different hash codes for these distinct objects.

That violates the contract:

```text
equals() == true
but
hashCode() != same
```



### 7. How this breaks HashMap

```java
Map<User, String> map = new HashMap<>();

User u1 = new User(10);
User u2 = new User(10);

map.put(u1, "Developer");

System.out.println(map.get(u2));
```

Even though:

```java
u1.equals(u2); // true
```

the lookup can fail because `u1` and `u2` can produce different hash codes.

Conceptually:

```text
put(u1)
  ↓
u1.hashCode()
  ↓
bucket X
  ↓
store entry

get(u2)
  ↓
u2.hashCode()
  ↓
bucket Y
  ↓
u1 is not searched
  ↓
lookup fails
```

The important point is that the problem is **not merely that** `u2` **was never inserted**. The real problem is that violating the equality/hash contract can cause a logically equal key to be looked up in a different bucket.

### 8. Correct `hashCode()` implementation

If equality is based only on `id`:

```java
@Override
public int hashCode() {
    return id;
}
```

This is contract-compatible because the same field determines equality.

For multiple equality fields, derive the hash from the same equality state:

```java
@Override
public int hashCode() {
    return Objects.hash(id, name);
}
```



### 9. Important nuance: can hashCode use fewer fields?

Suppose:

```java
@Override
public boolean equals(Object obj) {
    User other = (User) obj;
    return this.id == other.id &&
           this.name.equals(other.name);
}
```

This is technically contract-valid:

```java
@Override
public int hashCode() {
    return id;
}
```

because two equal objects necessarily have the same `id`, so equal objects will still have equal hash codes.

However, using both equality fields is generally better for hash distribution:

```java
@Override
public int hashCode() {
    return Objects.hash(id, name);
}
```

Interview-safe wording:

> “The hash code must be consistent with the equality definition. It is technically possible to use fewer fields as long as equal objects always produce the same hash, but using the equality fields generally gives better hash distribution.”



### 10. HashMap lookup: hashCode first, equals second

Consider:

```java
User u1 = new User(10, "Alice");
User u2 = new User(10, "Alice");

Map<User, String> map = new HashMap<>();

map.put(u1, "Developer");

System.out.println(map.get(u2)); // Developer
```

Conceptually, `HashMap` does:

```text
get(u2)
   ↓
calculate u2.hashCode()
   ↓
locate the appropriate bucket
   ↓
inspect candidate entries
   ↓
use equality comparison to identify the matching key
   ↓
u1.equals(u2) == true
   ↓
return "Developer"
```

A useful mental model:

```text
hashCode() → “Which bucket should I look in?”
equals()   → “Is this actually the key I am looking for?”
```

`hashCode()` alone cannot establish equality.

### 11. Hash collision inside HashMap/HashSet

Suppose:

```java
User u1 = new User(10, "Alice");
User u2 = new User(10, "Bob");
```

and both happen to have the same hash:

```java
u1.hashCode() == u2.hashCode(); // true
u1.equals(u2);                  // false
```

They can still coexist as different keys/elements.

The hash identifies a candidate bucket; equality distinguishes the actual keys.

### 12. Mutable fields and HashSet/HashMap

This is a classic interview trap.

```java
class User {
    int id;
    String name;

    @Override
    public boolean equals(Object obj) {
        User other = (User) obj;
        return id == other.id &&
               name.equals(other.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name);
    }
}
```

Now:

```java
User u = new User(10, "Alice");

Set<User> set = new HashSet<>();
set.add(u);

u.name = "Bob";

System.out.println(set.contains(u)); // false
```

Why?

When the object was inserted, its hash was based on:

```text
(10, "Alice")
```

After mutation, a lookup calculates the hash using the current state:

```text
(10, "Bob")
```

That can correspond to a different bucket.

Conceptually:

```text
Object stored according to:
    hash(10, "Alice")

Lookup performed using:
    hash(10, "Bob")
```

Therefore, avoid mutating fields used by `equals()`/`hashCode()` while the object is being used as a key in a hash-based collection.

### 13. `Objects.equals()` — null-safe equality

```java
String a = null;
String b = "hello";

a.equals(b);          // NullPointerException
Objects.equals(a, b); // false
```

`Objects.equals(a, b)` is null-safe.

Conceptually:

```text
Objects.equals(a, b)

a == b          → true
a == null       → false
b == null       → false
otherwise       → a.equals(b)
```

Therefore:

```java
Objects.equals(null, "hello"); // false
Objects.equals(null, null);    // true
```



### 14. Records

Java records automatically provide `equals()` and `hashCode()` based on their record components.

For example:

```java
record User(int id, String name) {}
```

The record's equality/hash behavior is derived from its components.

### 15. Diagnostic questions and answers



### Follow-up 1 — `==` with two String objects

```java
String a = new String("hello");
String b = new String("hello");
```

What is:

```java
a == b
a.equals(b)
```

**Answer:**

```text
a == b       → false
a.equals(b)  → true
```

Reason: two distinct objects, but `String.equals()` compares content.

### Follow-up 2 — String literals

```java
String a = "hello";
String b = "hello";
```

What is:

```java
a == b
a.equals(b)
```

**Answer:**

```text
a == b       → true
a.equals(b)  → true
```

Both references refer to the same pooled string object.

### Follow-up 3 — No equals override

```java
User u1 = new User(10);
User u2 = new User(10);
```

with no `equals()` override.

What happens?

**Answer:**

```text
u1 == u2       → false
u1.equals(u2)  → false
```

The references point to different objects and `User` inherits identity-style `Object.equals()`.

### Follow-up 4 — The contract

If:

```java
u1.equals(u2) == true
```

what **must** be true?

**Answer:**

```java
u1.hashCode() == u2.hashCode()
```

The reverse is not required.

### Follow-up 5 — Collision

Can this happen?

```java
u1.equals(u2) == false
u1.hashCode() == u2.hashCode()
```

**Answer: Yes.**

That is a valid hash collision.

### Follow-up 6 — HashMap lookup

Why can this fail if `equals()` is overridden but `hashCode()` is not?

**Answer:**

A logically equal lookup key can produce a different hash and therefore lead the hash table to a different bucket, so the stored key may never be considered.

### Follow-up 7 — `Objects.hash()`

If:

```java
equals() → id + name
```

a standard implementation is:

```java
@Override
public int hashCode() {
    return Objects.hash(id, name);
}
```

The key idea is to derive the hash from the same logical state used for equality.

### Follow-up 8 — HashSet mutation

```java
Set<User> set = new HashSet<>();
set.add(u);

u.name = "Bob";

set.contains(u);
```

Why can this return `false`?

**Answer:**

The object's current equality/hash state changed after insertion. The lookup can calculate a different hash and search a different bucket from the one where the object was placed.

### Follow-up 9 — Null safety

```java
String a = null;
String b = "hello";
```

What happens?

```java
a.equals(b);
Objects.equals(a, b);
```

**Answer:**

```text
a.equals(b)          → NullPointerException
Objects.equals(a,b)  → false
```



### Follow-up 10 — Can unequal objects have equal hashes?

Yes.

```text
equals() == false
hashCode() == same
```

is legal and expected to be possible because the hash space is finite and collisions can occur.

### Common interview traps



### Trap 1 — “`equals()` checks whether two objects are the same object.”

Too vague/wrong for modern Java interview framing.

Better:

> `==` checks reference identity. `equals()` checks logical equality when the class overrides it.



### Trap 2 — “If hash codes are equal, objects must be equal.”

Wrong.

Correct:

> Equal objects must have equal hash codes, but equal hash codes do not imply equality.



### Trap 3 — “Different objects must have different hash codes.”

Wrong.

Different objects may collide.

### Trap 4 — “HashMap uses only hashCode.”

Wrong.

It uses the hash to locate candidate entries and equality to identify the matching key.

### Trap 5 — “If I override equals(), Java automatically fixes hashCode().”

Wrong.

If you override `equals()`, you generally need a compatible `hashCode()` implementation.

### Trap 6 — “`==` compares String contents.”

Wrong.

`==` compares references. String literals can make `==` appear to compare values because of string pooling.

### Trap 7 — “Hash code is generated only once when inserted.”

Not the right model.

The hash used for lookup is based on the object's current state. Mutating equality/hash fields after insertion can make lookup fail.

### Final interview answer

> `==` and `equals()` serve different purposes for objects. `==` checks reference identity — whether two references point to the same object. `equals()` is intended for logical equality and can be overridden by a class; for example, `String.equals()` compares character content.
>
> The `hashCode()` contract is that whenever `a.equals(b)` is true, `a.hashCode()` and `b.hashCode()` must be equal. The reverse is not required, so unequal objects can have the same hash code due to collisions.
>
> This contract is critical for `HashMap` and `HashSet`: the hash code is used to locate the appropriate bucket, and equality is then used to identify the exact matching key or element. If `equals()` is overridden without a compatible `hashCode()`, logically equal objects can be placed/looked up in different buckets and hash-based collection operations can fail.
>
> A good implementation derives `hashCode()` from the same logical fields used by `equals()`, commonly with `Objects.hash(...)`. Also, fields used by `equals()`/`hashCode()` should not be mutated while the object is being used as a key in a hash-based collection.



### One-minute revision

```text
== 
→ reference/identity comparison

equals()
→ logical equality

Object.equals()
→ identity-style by default

String.equals()
→ content equality

hashCode contract:
equals(a,b) == true
        ↓
hashCode(a) == hashCode(b) MUST be true

Reverse:
same hash
        ↓
does NOT imply equals

HashMap / HashSet:
hashCode()
    ↓
find bucket
    ↓
equals()
    ↓
confirm exact key/element

Collision:
different objects
→ same hash is allowed

Mutable equality fields:
→ dangerous after insertion into HashMap/HashSet

Objects.equals(a,b):
→ null-safe equality
```



# Q5 · volatile vs synchronized vs atomic — when each?



### Exact question from the PDF

**“What's the difference between** `volatile`**,** `synchronized`**, and** `AtomicInteger`**? Give me a use case where each is the right pick.”**

### 30-second interview answer

- `volatile` = **visibility only**; it does not make compound operations atomic.
- `synchronized` = **mutual exclusion + visibility**; use it for compound actions and coordinated updates to shared state.
- `Atomic*` classes such as `AtomicInteger` = **lock-free atomic operations using CAS** for single variables, such as counters and flags with read-modify-write semantics.
- Decision rule:
  - shared status flag → `volatile`
  - simple atomic counter → `AtomicInteger`
  - check-then-act / multiple shared-state updates → `synchronized`

The PDF explicitly warns that `volatile int counter; counter++;` is still a race condition and highlights CAS-based atomic operations for `AtomicInteger`/`AtomicLong`. fileciteturn3file0

### 1. `volatile` — visibility

```java
class Worker {
    volatile boolean shutdownRequested = false;

    void shutdown() {
        shutdownRequested = true;
    }

    void work() {
        while (!shutdownRequested) {
            // keep working
        }
    }
}
```

`volatile` gives the shared flag the required visibility semantics so that another thread can observe the volatile write.

The PDF's mental model is:

```text
volatile
    ↓
visibility
```

A strong interview formulation is:

> "`volatile` is appropriate when threads need visibility of a shared variable and the access does not require a compound atomic operation."

The PDF specifically gives status flags read by many threads and written rarely, such as `shutdownRequested`, as a use case. fileciteturn3file0

### Important precision: don't overstate "main memory"

A common beginner explanation is:

> "`volatile` means every read/write goes directly to main memory instead of L1/L2 cache."

This is a useful mental model, but it is not the precise Java Memory Model explanation.

Prefer:

> "`volatile` provides Java Memory Model visibility and ordering guarantees."



### 2. `volatile` does NOT provide atomicity

```java
volatile int count = 0;

void increment() {
    count++;
}
```

`count++` is conceptually:

```text
read count
    ↓
add 1
    ↓
write count
```

Two threads can interleave:

```text
Thread A              Thread B
--------              --------
read 0
                      read 0
add 1
                      add 1
write 1
                      write 1
```

Two increments occurred, but the final value can be `1`.

Therefore:

```text
volatile
    → visibility ✅
    → atomicity  ❌
```

The PDF explicitly uses `volatile int counter; counter++;` as a race-condition example. fileciteturn3file0

### 3. `AtomicInteger` — atomic single-variable operations

```java
AtomicInteger count = new AtomicInteger(0);

void increment() {
    count.incrementAndGet();
}
```

`AtomicInteger` provides atomic read-modify-write operations.

The PDF describes `AtomicInteger`, `AtomicLong`, etc. as using **Compare-And-Swap (CAS)** hardware instructions and being lock-free, making them a natural fit for simple counters and flags. fileciteturn3file0

Conceptually:

```text
read current value
      ↓
calculate new value
      ↓
CAS: update only if value is still what I observed
      ↓
success → done
failure → retry
```



### 4. `synchronized` — mutual exclusion + visibility

Consider:

```java
if (balance >= amount) {
    balance -= amount;
}
```

This is a compound operation:

```text
check
  ↓
make decision
  ↓
update
```

Use synchronization to protect the entire critical section:

```java
synchronized (account) {
    if (balance >= amount) {
        balance -= amount;
    }
}
```

Now only one thread can execute that critical section at a time for that monitor.

The PDF's framing is:

```text
synchronized
    → mutual exclusion
    + visibility
```

It specifically recommends `synchronized` for compound operations such as check-then-act and multi-field updates. fileciteturn3file0

### 5. `synchronized` also provides visibility

```java
class Counter {
    int count = 0;

    synchronized void increment() {
        count++;
    }

    synchronized int getCount() {
        return count;
    }
}
```

Both methods synchronize on the same object's monitor.

The synchronization gives:

```text
mutual exclusion
+
visibility / memory-ordering guarantees
```

Important nuance:

```java
synchronized void increment() {
    count++;
}

int getCount() {
    return count;
}
```

Do not assume that synchronizing only the writer makes every unsynchronized reader safe. For synchronization-based visibility, accesses should participate in the appropriate synchronization protocol.

### 6. `AtomicInteger` does NOT automatically make a compound sequence atomic

```java
AtomicInteger balance = new AtomicInteger(100);

if (balance.get() >= 80) {
    balance.addAndGet(-80);
}
```

This is not automatically thread-safe as a whole.

The individual operations are atomic:

```text
get()
addAndGet()
```

but the sequence:

```text
get
 ↓
check
 ↓
update
```

is not one atomic transaction.

Two threads can both observe `100` and both pass the check.

### 7. CAS can express a complete atomic state transition

`AtomicInteger` can also be used with `compareAndSet()` when the complete state transition can be expressed as a CAS loop:

```java
int current;

do {
    current = balance.get();

    if (current < 80) {
        return;
    }
} while (!balance.compareAndSet(current, current - 80));
```

The idea is:

```text
read current
      ↓
calculate desired value
      ↓
CAS only if current is unchanged
      ↓
success → update happened atomically
failure → retry
```

For the basic interview question, remember:

```text
AtomicInteger
    → atomic operations on a single variable

synchronized
    → useful when several operations/state changes must be coordinated
```



### 8. `volatile` and happens-before

Consider:

```java
class Worker {
    private volatile boolean running;
    private int result;

    void stop() {
        result = 42;
        running = false;
    }

    void work() {
        while (running) {
            // work
        }

        System.out.println(result);
    }
}
```

If Thread B observes:

```java
running == false
```

the volatile write to `running` establishes the required happens-before relationship with the subsequent read of that same volatile variable.

Therefore the earlier:

```java
result = 42;
```

is visible to Thread B.

The intended result is:

```text
running == false
result == 42
```

This illustrates that `volatile` provides memory-ordering/visibility semantics beyond the flag itself. fileciteturn3file0

### 9. Double-checked locking and `volatile`

The PDF highlights double-checked locking:

```java
class Singleton {

    private static volatile Singleton instance;

    static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

Why `volatile`?

The `synchronized` block provides mutual exclusion during creation, while `volatile` provides the safe-publication and ordering semantics required by the pattern.

Without `volatile`, problematic reordering/visibility effects could allow another thread to observe a non-null reference without safely observing the fully initialized object.

Important correction:

> `volatile` is **not primarily needed to prevent two threads from creating two instances**. The synchronized block handles mutual exclusion during creation.

The PDF specifically warns that without `volatile`, JIT/compiler reordering can allow another thread to see a non-null reference to a not-yet-initialized object. fileciteturn3file0

### 10. Use-case decision table


| Requirement                               | Natural choice  | Why                                                                     |
| ----------------------------------------- | --------------- | ----------------------------------------------------------------------- |
| Shared shutdown/status flag               | `volatile`      | Visibility                                                              |
| Simple atomic counter                     | `AtomicInteger` | Atomic read-modify-write                                                |
| Atomic increment/decrement                | `AtomicInteger` | CAS-based atomic operation                                              |
| Check-then-act                            | `synchronized`  | Entire sequence needs protection                                        |
| Multiple fields updated consistently      | `synchronized`  | One critical section                                                    |
| Simple visibility + no compound operation | `volatile`      | No atomic RMW needed                                                    |
| Very-high-contention counter              | `LongAdder`     | PDF notes it can outperform `AtomicLong` through striped internal state |


The PDF specifically notes `LongAdder` for very-high-contention counters. fileciteturn3file0

### 11. Common interview traps



### Trap 1 — “volatile makes operations atomic.”

Wrong.

```java
volatile int count;
count++;
```

`count++` can still race.

### Trap 2 — “volatile means it always reads directly from RAM.”

Too simplistic.

Prefer:

> `volatile` provides Java Memory Model visibility and ordering guarantees.



### Trap 3 — “AtomicInteger makes any code involving the variable thread-safe.”

Wrong.

```java
if (balance.get() >= amount) {
    balance.addAndGet(-amount);
}
```

The complete business operation is still compound.

### Trap 4 — “synchronized is only for locking.”

Incomplete.

`synchronized` provides:

```text
mutual exclusion
+
visibility
```



### Trap 5 — “synchronized is always better because it is safer.”

Wrong as a blanket rule. Match the primitive to the concurrency requirement. fileciteturn3file0

### Trap 6 — “AtomicInteger and synchronized are interchangeable.”

They can sometimes solve the same simple counter problem, but:

```text
AtomicInteger
→ atomic operations on a variable

synchronized
→ mutual exclusion around a critical section
```



### Follow-up questions



### Follow-up 1 — Why isn't `volatile count++` safe?

Because `count++` is a read-modify-write sequence, not one indivisible operation.

`volatile` gives visibility, not atomicity.

### Follow-up 2 — Why is `AtomicInteger` suitable for a counter?

Because `incrementAndGet()` performs the increment atomically using CAS semantics.

### Follow-up 3 — Why not use `AtomicInteger` for everything?

Atomic operations on a single variable do not automatically make a multi-step business operation atomic.

For compound invariants, a critical section protected by `synchronized` can be clearer and safer.

### Follow-up 4 — Can `AtomicInteger` replace `synchronized`?

For some simple single-variable state transitions, yes.

For arbitrary compound state involving multiple variables or actions, no—not automatically.

### Follow-up 5 — Does `synchronized` provide visibility?

Yes.

Synchronization provides both:

```text
mutual exclusion
+
visibility
```



### Follow-up 6 — What if only the writer is synchronized?

Do not assume all unsynchronized readers automatically become safe.

For reliable synchronization-based visibility, accesses should participate in the appropriate synchronization protocol, typically using the same monitor.

### Follow-up 7 — Why does double-checked locking need `volatile`?

Because `volatile` provides the required visibility/order semantics for safely publishing the singleton reference and prevents problematic reordering around construction.

The synchronized block handles mutual exclusion during creation.

### Follow-up 8 — What is CAS?

**Compare-And-Swap** conceptually means:

> “Change this value only if it is still the value I previously observed.”

If another thread changed it, the CAS fails and the operation can retry.

### Follow-up 9 — What if contention is extremely high for a counter?

The PDF calls out `LongAdder` as an option that can outperform `AtomicLong` under very high contention because it uses striped internal state. fileciteturn3file0

### Follow-up 10 — Can volatile protect multiple variables?

`volatile` applies visibility semantics to the volatile variable; it does not turn a sequence involving several variables into one atomic transaction.

If several state changes must happen together, use an appropriate synchronization/atomic-state design.

### Follow-up 11 — Why doesn't `synchronized` just protect the variable?

`synchronized` protects a **critical section** associated with a monitor. It can therefore protect an entire sequence of reads, checks, writes, and method calls as one mutually exclusive operation.

### Follow-up 12 — Can `volatile` be used for a shutdown flag?

Yes. This is one of the PDF's explicit use cases:

```java
volatile boolean shutdownRequested;
```

Many threads can read it while another thread changes it.

### Diagnostic cases we covered



### Case 1 — shared shutdown flag

```java
volatile boolean shutdownRequested;
```

**Answer:** `volatile`

**Reason:** visibility of shared state.

### Case 2 — shared counter

```java
volatile int count;

void increment() {
    count++;
}
```

**Answer:** `volatile` is insufficient.

Use `AtomicInteger` or appropriate synchronization.

### Case 3 — atomic counter

```java
AtomicInteger count = new AtomicInteger();

count.incrementAndGet();
```

**Answer:** `AtomicInteger`

### Case 4 — account check-then-act

```java
if (balance >= amount) {
    balance -= amount;
}
```

**Answer:** `synchronized` or another design that atomically protects the complete state transition.

### Case 5 — AtomicInteger does not make a sequence atomic

```java
AtomicInteger balance = new AtomicInteger(100);

if (balance.get() >= 80) {
    balance.addAndGet(-80);
}
```

**Answer:** Not automatically thread-safe as a complete operation.

### Case 6 — volatile visibility of previous writes

```java
result = 42;
running = false; // volatile
```

If another thread observes `running == false`, the volatile happens-before relationship makes the earlier `result = 42` visible.

### Case 7 — double-checked locking

```java
private static volatile Singleton instance;
```

**Answer:** `volatile` provides safe-publication and ordering semantics; `synchronized` provides mutual exclusion during creation.

### Final interview answer

> `volatile`, `synchronized`, and the atomic classes solve different concurrency problems. `volatile` is primarily for visibility: when one thread changes a shared flag or state, other threads need to reliably observe it, but `volatile` does not make compound operations such as `count++` atomic.
>
> `synchronized` provides mutual exclusion as well as visibility, so I use it when I need to protect a critical section or a compound operation such as check-then-act or updating multiple related fields consistently.
>
> `AtomicInteger` provides atomic operations on a single variable using CAS. I would use it for things like a shared request counter where I need atomic increment/decrement without protecting a larger critical section.
>
> So my rule of thumb is: **visibility-only flag →** `volatile`**; atomic single-variable operation →** `AtomicInteger`**; compound critical section or shared-state invariant →** `synchronized`**.**



### One-minute revision

```text
volatile
    ↓
visibility + ordering
    ↓
NOT atomic
    ↓
good for shared flags/state

AtomicInteger
    ↓
CAS
    ↓
atomic single-variable operations
    ↓
good for counters / simple RMW operations

synchronized
    ↓
mutual exclusion
    +
visibility
    ↓
good for compound operations
and coordinated shared state

Critical trap:

volatile int count;
count++;

    ↓

NOT atomic

Another trap:

AtomicInteger balance;

get()
  ↓
check
  ↓
addAndGet()

    ↓

NOT automatically one atomic business operation

Mental model:

volatile
    → "I need other threads to see this."

AtomicInteger
    → "I need this single variable operation to be atomic."

synchronized
    → "I need this entire critical section to execute as one protected operation."
```



# Q6 · Checked vs unchecked exceptions — when to use which?



### Difference between checked and unchecked exceptions? When would you create a checked exception vs an unchecked one in your own code?



### 30-Second Interview Answer

**Checked exceptions** extend `Exception` but not `RuntimeException`. The compiler forces the caller to either catch them or declare them with `throws`.

**Unchecked exceptions** extend `RuntimeException`. The compiler does not force the caller to catch or declare them.

I would generally use a **checked exception** when the caller can reasonably recover from the condition and should explicitly handle or propagate it—for example, a file not being available or a temporary network failure.

I would use an **unchecked exception** for programming errors or invalid state/arguments—for example, passing `null` where it isn't allowed or calling an API in an invalid state.

Modern Java and Spring applications often favor unchecked exceptions to avoid excessive catch/propagate boilerplate and meaningless wrapping, but the choice is ultimately an API design decision.

### Exception Hierarchy

```text
Throwable
├── Error
│   ├── OutOfMemoryError
│   └── StackOverflowError
│
└── Exception
    ├── RuntimeException
    │   ├── NullPointerException
    │   ├── IllegalArgumentException
    │   └── IllegalStateException
    │
    └── Other Exceptions
        ├── IOException
        ├── SQLException
        └── ...
```

The important rule:

```text
Checked:
Exception subclasses that are NOT RuntimeException

Unchecked:
RuntimeException and its subclasses
Error and its subclasses
```



### Common Examples


| Exception                  | Checked / Unchecked | Reason                                      |
| -------------------------- | ------------------- | ------------------------------------------- |
| `IOException`              | Checked             | Extends `Exception`, not `RuntimeException` |
| `SQLException`             | Checked             | Extends `Exception`, not `RuntimeException` |
| `RuntimeException`         | Unchecked           | RuntimeException itself                     |
| `NullPointerException`     | Unchecked           | Extends `RuntimeException`                  |
| `IllegalArgumentException` | Unchecked           | Extends `RuntimeException`                  |
| `IllegalStateException`    | Unchecked           | Extends `RuntimeException`                  |
| `OutOfMemoryError`         | Unchecked           | Extends `Error`                             |
| `StackOverflowError`       | Unchecked           | Extends `Error`                             |




### What Makes an Exception Checked?

The compiler requires a checked exception to be **caught or declared**.

This does not compile:

```java
void readFile() {
    throw new IOException();
}
```

You must either catch it:

```java
void readFile() {
    try {
        throw new IOException();
    } catch (IOException e) {
        // handle
    }
}
```

or declare it:

```java
void readFile() throws IOException {
    throw new IOException();
}
```



### Unchecked Exceptions

This compiles without `try-catch` or `throws`:

```java
void process() {
    throw new IllegalArgumentException();
}
```

The important distinction is:

```text
Checked
→ compiler forces catch or declare

Unchecked
→ compiler does NOT force catch or declare
```

Unchecked does **not** mean that the exception cannot be caught.

For example:

```java
try {
    // ...
} catch (Exception e) {
    // catches RuntimeException subclasses too
}
```



### `==` Checked vs Unchecked Is Not Based on "Can It Happen at Runtime?"

A common misconception is:

> "Unchecked means the exception is handled during compile time."

Incorrect.

The distinction is about **compiler enforcement**.

`NullPointerException` happens at runtime, but it is unchecked because the compiler does not require:

```java
try {
    // ...
} catch (NullPointerException e) {
    // ...
}
```



### When Should I Create a Checked Exception?

Use a checked exception when the caller can **reasonably recover** and explicitly handling the condition is useful.

Examples:

```text
File doesn't exist
Network temporarily unavailable
External resource unavailable
Recoverable I/O problem
```

Example:

```java
class PaymentUnavailableException extends Exception {
}
```

The caller can then decide:

```java
try {
    paymentService.processPayment(payment);
} catch (PaymentUnavailableException e) {
    // retry
    // fallback
    // notify user
}
```

The important reasoning is not:

> "Only checked exceptions can trigger retry."

That is false.

You can implement retry logic for unchecked exceptions too.

The stronger reasoning is:

> "The caller can reasonably recover from this condition, and making it checked explicitly forces the caller to acknowledge or propagate it."



### When Should I Create an Unchecked Exception?

Use an unchecked exception when the problem represents:

- A programming error
- An invalid argument
- Invalid object state
- A violated method precondition
- Something the caller isn't reasonably expected to recover from

Example:

```java
void processPayment(Payment payment) {
    if (payment == null) {
        throw new IllegalArgumentException(
            "payment cannot be null"
        );
    }
}
```

The caller violated the API's precondition.

There is no need for every caller to write:

```java
try {
    processPayment(null);
} catch (InvalidPaymentException e) {
    // ...
}
```



### Practical Decision Rule

Think:

```text
Can the caller reasonably recover?
        │
   ┌────┴────┐
   │         │
  YES        NO
   │         │
Checked    Unchecked
   │         │
retry      programming
fallback   error
ask user   invalid argument
alternative invalid state
```

This is a **design guideline**, not an absolute law.

### Database Failure vs Invalid Argument

Consider:

```java
class UserService {

    User findUser(String id) {
        // ...
    }
}
```



### Database temporarily unavailable

A checked exception can be reasonable:

```java
class DatabaseUnavailableException extends Exception {
}
```

The caller might:

```text
retry
fallback
return a meaningful error
use another data source
```



### `id == null`

An unchecked exception is appropriate:

```java
if (id == null) {
    throw new IllegalArgumentException("id cannot be null");
}
```

This is a caller/programming error.

### Why Modern Java/Spring Often Uses Unchecked Exceptions

Modern Java and Spring code often favors unchecked exceptions because checked exceptions can produce significant boilerplate:

```java
try {
    repository.save(user);
} catch (DatabaseException e) {
    throw new ServiceException(e);
}
```

Every layer may end up catching, propagating, or wrapping the same exception even when it cannot meaningfully handle it.

An unchecked exception allows the exception to propagate until a layer actually knows what to do with it.

For example:

```java
class UserServiceException extends RuntimeException {

    UserServiceException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

The important interview answer is:

> "Modern Java/Spring often prefers unchecked exceptions because checked exceptions can introduce catch/propagate boilerplate and meaningless wrapping. But checked exceptions aren't inherently bad; the choice depends on the API and whether callers should be forced to acknowledge a recoverable condition."



### Spring Example

Spring commonly wraps lower-level checked database exceptions into unchecked exceptions such as `DataAccessException`.

The idea is that application/service layers don't necessarily need to explicitly propagate every low-level checked database exception.

### `Error` vs `Exception`

`Error` is different from normal application exceptions.

Examples:

```text
OutOfMemoryError
StackOverflowError
```

These generally indicate serious JVM/system-level problems.

You normally should **not use** `Error` **as normal application-control flow**.

You also generally should not write:

```java
catch (Error e) {
    // recover
}
```

as ordinary exception handling.

Specialized infrastructure may catch/log certain errors, but normal application code should not assume it can recover from JVM-level failures.

### Why Is `RuntimeException` Unchecked?

Because Java defines `RuntimeException` and its subclasses as unchecked.

Even though:

```text
RuntimeException extends Exception
```

the compiler treats it differently.

Therefore:

```java
void test() {
    throw new RuntimeException();
}
```

is valid without:

```java
throws RuntimeException
```

or:

```java
try/catch
```



### Does `catch (Exception)` Catch RuntimeException?

Yes.

Because:

```text
RuntimeException
        ↓
    Exception
```

Therefore:

```java
try {
    throw new NullPointerException();
} catch (Exception e) {
    // reached
}
```

works.

"Unchecked" does **not** mean "cannot be caught."

It means:

> The compiler doesn't force you to catch or declare it.



### Does `catch (Exception)` Catch `Error`?

No.

```java
try {
    // ...
} catch (Exception e) {
    // ...
}
```

does **not** catch:

```java
OutOfMemoryError
```

because:

```text
Exception
```

and:

```text
Error
```

are sibling subclasses of `Throwable`.

```text
Throwable
├── Exception
└── Error
```



### `catch (Exception)` Examples

```java
try {
    // ...
} catch (Exception e) {
}
```


| Thrown type                | Caught? | Why                                      |
| -------------------------- | ------- | ---------------------------------------- |
| `NullPointerException`     | Yes     | Extends `RuntimeException` → `Exception` |
| `IllegalArgumentException` | Yes     | Extends `RuntimeException` → `Exception` |
| `IOException`              | Yes     | Extends `Exception`                      |
| `SQLException`             | Yes     | Extends `Exception`                      |
| `OutOfMemoryError`         | No      | Extends `Error`, not `Exception`         |




### Try-With-Resources

Try-with-resources automatically closes resources that implement `AutoCloseable`.

```java
try (FileInputStream input =
         new FileInputStream("data.txt")) {

    // read file
}
```

`FileInputStream` implements `Closeable`, which extends `AutoCloseable`.

Conceptually:

```text
AutoCloseable
      ↑
  Closeable
      ↑
FileInputStream
```

The resource is closed when execution leaves the try-with-resources statement.

That includes both:

```text
normal completion
        OR
exceptional completion
```

Conceptually:

```text
enter try
    ↓
execute body
    ↓
body finishes
    OR
exception occurs
    ↓
resource.close()
    ↓
continue / propagate exception
```

This eliminates manual cleanup code such as:

```java
FileInputStream input = null;

try {
    input = new FileInputStream("data.txt");
    // read
} finally {
    if (input != null) {
        input.close();
    }
}
```



### Suppressed Exceptions

An important try-with-resources interview detail:

Suppose:

```java
try (SomeResource resource = ...) {
    // throws Exception A
}
```

and then:

```java
resource.close();
```

also throws **Exception B**.

Java preserves the exception from the body as the primary exception and records the close exception as a **suppressed exception**.

You can inspect it with:

```java
catch (Exception e) {
    Throwable[] suppressed = e.getSuppressed();
}
```

This prevents the cleanup exception from simply disappearing.

### Lambda / Streams Follow-Up

A common follow-up is:

> "Why doesn't `Stream.map()` let me throw checked exceptions easily?"

For example:

```java
files.stream()
     .map(file -> readFile(file))
```

If:

```java
String readFile(File file) throws IOException
```

then the standard `Function<T, R>` used by `map()` does not declare `throws IOException`.

Therefore the checked exception cannot simply propagate through the standard lambda signature.

This is one reason checked exceptions can become awkward when working with functional APIs.

Typical approaches include:

```text
handle the exception inside the lambda
wrap it in an unchecked exception
create a custom functional interface that allows checked exceptions
```



### Common Interview Traps



### Trap 1: "Checked exceptions are bad."

Too absolute.

Better:

> "Checked exceptions can be useful for recoverable conditions, but excessive use can introduce boilerplate. Modern Java/Spring applications often favor unchecked exceptions."



### Trap 2: "Unchecked exceptions cannot be caught."

False.

They can absolutely be caught:

```java
try {
    // ...
} catch (RuntimeException e) {
}
```



### Trap 3: "Unchecked means compile-time exception."

False.

Unchecked exceptions generally occur at runtime.

The term means:

> The compiler doesn't force catch-or-declare handling.



### Trap 4: "Error is a checked exception."

False.

`Error` is outside the checked-exception category.

```text
Throwable
├── Error        → unchecked
└── Exception
    ├── RuntimeException → unchecked
    └── others           → checked
```



### Trap 5: "Catch `Exception` everywhere."

Bad practice.

```java
try {
    // everything
} catch (Exception e) {
    // ignore
}
```

This can hide programming bugs and make failures difficult to diagnose.

Catch exceptions at a layer that can meaningfully handle them.

### Interview Decision Table


| Situation                       | Typical choice            | Reason                                         |
| ------------------------------- | ------------------------- | ---------------------------------------------- |
| File unavailable                | Checked                   | Caller may choose another file/recover         |
| Network temporarily unavailable | Checked can be reasonable | Retry/fallback may be possible                 |
| Database unavailable            | Checked can be reasonable | Caller may recover/retry                       |
| `null` argument                 | Unchecked                 | Caller/programming error                       |
| Invalid argument                | Unchecked                 | Violated API precondition                      |
| Invalid object state            | Unchecked                 | Programming/API usage error                    |
| Programming bug                 | Unchecked                 | Caller generally shouldn't be forced to handle |
| JVM out of memory               | `Error`                   | Serious JVM-level condition                    |




### Strong Final Interview Answer

> "Checked exceptions are subclasses of `Exception` other than `RuntimeException`, and the compiler forces us to catch or declare them. Unchecked exceptions are `RuntimeException` subclasses, where the compiler doesn't require catch-or-declare handling.
>
> I'd generally use checked exceptions when the caller can reasonably recover from the condition, such as a file or network resource being temporarily unavailable. I'd use unchecked exceptions for programming errors, invalid arguments, or invalid state—for example, passing `null` where it's not allowed.
>
> In modern Java and Spring, unchecked exceptions are commonly preferred because checked exceptions can create a lot of catch/propagate boilerplate and meaningless wrapping. But it's ultimately an API design decision rather than a rule that checked or unchecked is always better."



### One-Minute Revision

```text
CHECKED
→ Exception but NOT RuntimeException
→ compiler forces catch or declare
→ useful for recoverable conditions

UNCHECKED
→ RuntimeException + subclasses
→ compiler does NOT force catch/declare
→ programming errors / invalid args / invalid state

ERROR
→ separate branch of Throwable
→ JVM/system-level problems
→ generally don't catch for normal recovery

KEY RULE
→ Checked vs unchecked = compiler enforcement
→ NOT "can it happen at runtime?"

catch(Exception)
→ catches checked exceptions
→ catches RuntimeException subclasses
→ does NOT catch Error

TRY-WITH-RESOURCES
→ resource implements AutoCloseable
→ automatically calls close()
→ normal + exceptional flow
→ close exceptions can become suppressed exceptions

API DESIGN
→ caller can reasonably recover → checked can be appropriate
→ programming/API usage error → unchecked
→ modern Java/Spring often favors unchecked to reduce boilerplate
```



# Q11 — ConcurrentHashMap: How Is It Different from HashMap?

> **Exact question from the PDF:**  
> “How does ConcurrentHashMap differ from HashMap, and what changed between Java 7 and Java 8?”



### 30-Second Interview Answer

`HashMap` is not thread-safe for concurrent access. `ConcurrentHashMap` is designed for concurrent access.

In Java 7, `ConcurrentHashMap` used **segment-based locking** — by default, 16 segments, each independently locked.

In Java 8+, the segment design was removed. `ConcurrentHashMap` uses **CAS for insertion into empty buckets** and **synchronizes on the first node of a bucket when handling collisions**. This allows higher concurrency.

Reads are designed to proceed without locking.

### Core Concepts



### 1. Why is HashMap unsafe for concurrent writes?

`HashMap` is not designed for multiple threads concurrently modifying the same map.

Concurrent access can lead to:

- Lost updates.
- Inconsistent internal state.
- Structural corruption.
- Classic Java 7 resize-related problems.

The important interview point is that making individual operations look safe is not enough if a **compound operation** is performed without atomicity.

### 2. Java 7 ConcurrentHashMap — Segment-Based Locking

Java 7's `ConcurrentHashMap` divided the map into **segments**.

The source describes the default as:

```text
16 segments
```

Each segment had its own lock.

Conceptually:

```text
ConcurrentHashMap
│
├── Segment 0  → lock
├── Segment 1  → lock
├── Segment 2  → lock
├── ...
└── Segment 15 → lock
```

Instead of one global lock for the entire map, Java 7 used multiple independently locked segments.

### 3. Java 8+ ConcurrentHashMap — No Segments

Java 8 removed the segment-based design.

For an insertion into an **empty bucket**:

```text
Empty bucket
     │
     ▼
    CAS
```

For a **collision / non-empty bucket**:

```text
Non-empty bucket
       │
       ▼
synchronize on first node
```

This avoids having one large lock protecting the entire map.

### CAS — Compare-And-Swap



### What is CAS?

CAS means **Compare-And-Swap**.

Conceptually:

```text
CAS(location, expectedValue, newValue)
```

It replaces the value at `location` with `newValue` only if the current value is still `expectedValue`.

The operation is atomic.

`ConcurrentHashMap` uses CAS for certain updates, such as inserting into an empty bucket.

### How Java 8+ Handles a Put

Conceptually:

```text
put(key, value)
      │
      ▼
Determine bucket
      │
      ├── Bucket empty
      │       │
      │       └── CAS
      │
      └── Bucket non-empty
              │
              └── synchronize on first node
```

Different buckets can therefore have concurrent activity instead of all updates competing for one global lock.

### Reads

`ConcurrentHashMap` is designed so that reads can proceed **without locking**.

Therefore, a read in one bucket does not simply wait because another thread is updating a different bucket.

The source describes reads as completely lock-free in both the Java 7 and Java 8+ designs.

### `computeIfAbsent()` and the Check-Then-Act Race

Consider:

```java
if (!map.containsKey("A")) {
    map.put("A", 1);
}
```

This is a classic **check-then-act** race.

Two threads can execute:

```text
Thread 1                    Thread 2

containsKey("A")            containsKey("A")
       ↓                           ↓
     false                       false
       ↓                           ↓
   put("A", 1)                put("A", 1)
```

The problem is that `containsKey()` and `put()` are separate operations. Even if individual map operations are thread-safe, the **combination is not atomic**.

Use:

```java
map.computeIfAbsent("A", key -> 1);
```

This expresses the check + compute + insert as an atomic map operation.

`ConcurrentHashMap` provides compound operations such as:

```java
computeIfAbsent()
compute()
merge()
putIfAbsent()
```

These should be preferred when the operation itself needs to be atomic.

### Null Keys and Null Values

`HashMap` allows:

```java
HashMap<String, Integer> map = new HashMap<>();

map.put(null, 10);
map.put("A", null);
```

`ConcurrentHashMap` does not allow null keys or null values:

```java
ConcurrentHashMap<String, Integer> map =
    new ConcurrentHashMap<>();

map.put(null, 10);    // ❌
map.put("A", null);   // ❌
```



### Why?

A `null` result from:

```java
map.get("A");
```

could otherwise mean:

```text
1. "A" does not exist
2. "A" exists and its value is null
```

`ConcurrentHashMap` avoids this ambiguity by prohibiting null keys and values.

### Interview Answer

> `ConcurrentHashMap` does not allow null keys or values because null needs to remain an unambiguous indication that no mapping was found.



### Weakly Consistent Iterators

`ConcurrentHashMap` iterators are **weakly consistent**.

While one thread iterates:

```java
for (String key : map.keySet()) {
    // ...
}
```

another thread can modify the map.

The iterator:

- Does **not** throw `ConcurrentModificationException`.
- Does **not** stop immediately because of the modification.
- Does **not** provide a snapshot.
- May or may not observe modifications made after iteration begins.



### Remember

```text
Weakly consistent
        │
        ├── No ConcurrentModificationException
        ├── Can continue during concurrent modification
        ├── Not a snapshot
        └── May or may not see concurrent changes
```



### `size()` vs `mappingCount()`

Both concern the number of mappings.

```java
map.size();          // int
map.mappingCount();  // long
```

Do not confuse either one with internal table capacity.

```text
size()          → number of mappings, int
mappingCount()  → number of mappings, long
capacity        → number of internal buckets
```

For a highly concurrent map, the source highlights `mappingCount()` as preferable when the count may be very large.

### ConcurrentHashMap vs synchronizedMap

Compare:

```java
Collections.synchronizedMap(new HashMap<>());
```

with:

```java
new ConcurrentHashMap<>();
```

A synchronized wrapper uses a **common synchronization lock** around map operations.

Conceptually:

```text
Thread 1 ──┐
Thread 2 ──┼──► common lock ──► HashMap
Thread 3 ──┘
```

Java 8+ `ConcurrentHashMap` uses finer-grained concurrency:

```text
Empty bucket
    │
    └──► CAS

Non-empty bucket / collision
    │
    └──► synchronize on first node
```

Therefore, `ConcurrentHashMap` can provide substantially more concurrency than a single-lock synchronized map.

### Important Trap

Do **not** say:

> “ConcurrentHashMap is always faster than HashMap.”

`HashMap` is generally the simpler/faster choice when the map is thread-confined and concurrency is not required.

### Java 7 vs Java 8+ — Quick Comparison


| Area                   | Java 7 ConcurrentHashMap | Java 8+ ConcurrentHashMap                 |
| ---------------------- | ------------------------ | ----------------------------------------- |
| Main design            | Segments                 | No segments                               |
| Locking                | Segment-level            | Fine-grained bucket-level synchronization |
| Default segmentation   | 16 segments              | Removed                                   |
| Empty bucket insertion | Segment-based locking    | CAS                                       |
| Collision handling     | Segment lock             | Synchronize on first node                 |
| Reads                  | Lock-free                | Lock-free                                 |
| Concurrency            | Multiple segment locks   | Finer-grained concurrency                 |




### Follow-Up Questions and Answers



### Follow-up 1 — Two threads insert into different buckets

**Question:** If two threads perform `put()` operations into different buckets in Java 8+, do they necessarily wait for each other?

**Answer:** No. For an empty bucket, `ConcurrentHashMap` can use CAS, so operations involving different buckets can proceed concurrently.

### Follow-up 2 — What happens when two keys collide?

**Question:** What happens when two keys map to the same bucket?

**Answer:** The bucket is non-empty, so Java 8+ `ConcurrentHashMap` synchronizes on the first node of that bucket while handling the collision/update.

### Follow-up 3 — What is CAS?

**Question:** What does CAS mean?

**Answer:** CAS means **Compare-And-Swap**. It is an atomic read-modify-write primitive that changes a value only if it still matches an expected value.

```text
CAS(location, expected, newValue)
```

If the current value equals `expected`, it is replaced with `newValue`; otherwise, the operation fails.

### Follow-up 4 — Why is `containsKey()` + `put()` unsafe?

**Question:** Consider:

```java
if (!map.containsKey("A")) {
    map.put("A", 1);
}
```

How can this fail with two threads?

**Answer:** Both threads can observe the key as absent. The two operations are individually valid, but the **compound check-then-act operation is not atomic**.

Use:

```java
map.computeIfAbsent("A", key -> 1);
```

to express the operation atomically.

### Follow-up 5 — Why does ConcurrentHashMap reject null?

**Question:** Why can `HashMap` contain null while `ConcurrentHashMap` cannot?

**Answer:** A `null` result from `get()` would otherwise be ambiguous: the key might not exist, or it might exist with a null value. `ConcurrentHashMap` prohibits null keys and values to keep absence unambiguous.

### Follow-up 6 — What is a weakly consistent iterator?

**Question:** What happens if one thread iterates over a `ConcurrentHashMap` while another modifies it?

**Answer:** The iterator does not throw `ConcurrentModificationException`. It can continue while modifications happen concurrently, but it is not a snapshot. It may or may not observe modifications made after iteration begins.

### Follow-up 7 — `size()` vs `mappingCount()`

**Question:** What's the difference?

**Answer:**

```java
int size()
long mappingCount()
```

Both represent the number of mappings, but `mappingCount()` uses `long` and is preferable when dealing with potentially very large, highly concurrent maps. Neither represents internal bucket capacity.

### Follow-up 8 — Why not `Collections.synchronizedMap()`?

**Question:** Why use `ConcurrentHashMap` instead of `Collections.synchronizedMap(new HashMap<>())`?

**Answer:** A synchronized map uses a common synchronization lock, causing more contention. Java 8+ `ConcurrentHashMap` uses finer-grained concurrency: CAS for empty-bucket insertion, synchronization on the first node for collisions, and lock-free reads.

### Common Interview Traps



### Trap 1 — “ConcurrentHashMap locks the entire map”

Incorrect for Java 8+.

It does not use one global lock for normal map updates.

### Trap 2 — “ConcurrentHashMap uses segments in Java 8”

Incorrect.

The segment-based design was used in Java 7. Java 8 removed segments.

### Trap 3 — “CAS means there are no locks”

Incorrect.

Java 8+ `ConcurrentHashMap` uses CAS for certain operations, such as empty-bucket insertion, but also uses synchronization for collision handling.

### Trap 4 — “Every concurrent operation is completely lock-free”

Incorrect.

Reads are designed to be lock-free, but update operations can involve synchronization.

### Trap 5 — “computeIfAbsent is just containsKey + put internally”

Incorrect as an interview explanation.

The important property is that it provides an atomic compound operation so callers don't have to perform the check and insertion as separate operations.

### Trap 6 — “Weakly consistent means it always sees the latest data”

Incorrect.

A weakly consistent iterator may or may not observe concurrent modifications.

### Trap 7 — “HashMap doesn't allow null”

Incorrect.

`HashMap` allows null keys and null values. `ConcurrentHashMap` does not.

### Final Interview Answer

> `HashMap` is not thread-safe for concurrent modification, whereas `ConcurrentHashMap` is designed for concurrent access.
>
> In Java 7, `ConcurrentHashMap` used segment-based locking, with multiple independently locked segments. This allowed operations on different segments to proceed concurrently.
>
> In Java 8+, the segment design was removed. For insertion into an empty bucket, `ConcurrentHashMap` can use CAS, while collision handling synchronizes on the first node of the bucket. This provides finer-grained concurrency.
>
> Reads are designed to be lock-free. `ConcurrentHashMap` also provides atomic compound operations such as `computeIfAbsent()`, `compute()`, and `merge()`, which are important for avoiding check-then-act races.
>
> Unlike `HashMap`, `ConcurrentHashMap` does not allow null keys or null values because null would make it ambiguous whether a mapping is absent or explicitly mapped to null.
>
> Its iterators are weakly consistent: they don't throw `ConcurrentModificationException`, but they don't provide a snapshot and may or may not observe concurrent modifications.
>
> So the major evolution is: **Java 7 segment-based locking → Java 8+ finer-grained bucket-level concurrency using CAS and synchronization.**



### One-Minute Revision

```text
HashMap
  → Not thread-safe

ConcurrentHashMap
  → Thread-safe
  → No null keys/values
  → Lock-free reads
  → Weakly consistent iterators
  → Atomic compound operations

Java 7
  → Segments
  → Segment-level locks

Java 8+
  → No segments
  → Empty bucket → CAS
  → Collision → synchronize on first node
  → Finer-grained concurrency

Important APIs
  → computeIfAbsent()
  → compute()
  → merge()
  → putIfAbsent()

Important distinction
  → size() = int
  → mappingCount() = long

Key interview idea
  → Thread-safe individual operations
    ≠
    thread-safe compound operation

  → containsKey() + put()
    can race

  → computeIfAbsent()
    provides the atomic compound operation
```

