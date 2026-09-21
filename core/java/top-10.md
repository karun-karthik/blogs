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

| Operation | Complexity |
|---|---:|
| Append when capacity exists | O(1) |
| Particular append causing resize | O(n) |
| Many appends overall | **O(1) amortized** |

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

| Operation | ArrayList | LinkedList |
|---|---:|---:|
| `get(index)` | **O(1)** | **O(n)** |
| `set(index, value)` | **O(1)** | **O(n)** |
| `add(value)` at end | **O(1) amortized** | **O(1)** |
| `add(0, value)` | **O(n)** | **O(1)** |
| `add(index, value)` | **O(n)** | **O(n)** |
| `remove(index)` | **O(n)** | **O(n)** |
| Remove with known node/iterator position | — | **O(1)** |
| Sequential iteration | **O(n)** | **O(n)** |
| Indexed `get(i)` loop | **O(n)** | **O(n²)** |
| Memory overhead | Lower | Higher |

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

**“Explain the difference between `==` and `.equals()`. Then explain the hashCode contract.”**

### 30-second interview answer

- `==` on objects compares **identity/reference equality** — whether both references refer to the same object.
- `.equals()` compares **logical equality** when a class overrides it. `Object.equals()` defaults to identity-style comparison, while classes such as `String` and `Integer` override it for value/content equality.
- The `hashCode` contract says: **if `a.equals(b)` is `true`, then `a.hashCode() == b.hashCode()` must always be true.**
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

The important point is that the problem is **not merely that `u2` was never inserted**. The real problem is that violating the equality/hash contract can cause a logically equal key to be looked up in a different bucket.

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

| Area | Java 7 ConcurrentHashMap | Java 8+ ConcurrentHashMap |
|---|---|---|
| Main design | Segments | No segments |
| Locking | Segment-level | Fine-grained bucket-level synchronization |
| Default segmentation | 16 segments | Removed |
| Empty bucket insertion | Segment-based locking | CAS |
| Collision handling | Segment lock | Synchronize on first node |
| Reads | Lock-free | Lock-free |
| Concurrency | Multiple segment locks | Finer-grained concurrency |

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
