# Q1 — HashMap Internals

> **“Walk me through what happens internally when you call `put("key", "value")` on a `HashMap`.”**

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

> **"`i` is the index of the bucket in the backing table."**

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

> **"HashMap stores entries in an internal array of buckets. When I call `put(key, value)`, HashMap obtains the key's `hashCode()` and performs additional bit spreading. It then calculates the bucket using `(capacity - 1) & hash`.**
>
> **If the bucket is empty, it creates a new node. If the bucket is occupied, it checks the stored hash and key equality. If the key already exists, its value is replaced; otherwise, the new key is added to the collision structure.**
>
> **In Java 8+, if a bucket becomes sufficiently crowded, HashMap can convert the collision structure from a linked list into a red-black tree. Treeification requires the bucket threshold to be reached and the table capacity to be at least 64; otherwise resizing is preferred.**
>
> **HashMap also resizes when its size crosses the load-factor threshold, which by default is approximately `capacity × 0.75`. During resizing, the table grows, typically doubles, and existing nodes are redistributed using their stored hashes."**

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

[New seciton]

# Q2 — Why Is String Immutable in Java?

> **“Why is `String` immutable in Java?”**

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
> **It's important not to confuse `final` with immutability: `final` prevents a reference from being reassigned, while immutability prevents the object's state from changing."**

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
