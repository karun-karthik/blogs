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

# Q12 · Fail-Fast vs Fail-Safe Iterators

### Fail-Fast

A **fail-fast iterator** attempts to detect structural modifications to a collection that happen outside the iterator while iteration is in progress.

If detected, it may throw:

```java
ConcurrentModificationException
```

Example:

```java
List<Integer> list = new ArrayList<>();

list.add(1);
list.add(2);
list.add(3);

for (Integer value : list) {
    if (value == 2) {
        list.remove(value);
    }
}
```

`ArrayList` uses a **fail-fast iterator**.

### Important

Fail-fast is **best-effort**, not guaranteed.

Therefore, don't say:

> "Modifying an `ArrayList` during iteration always throws `ConcurrentModificationException`."

For example, removing the element that causes the iterator to reach the end can result in no exception because another `next()` call may never occur.

---

### `Iterator.remove()`

This is the correct way to remove the current element while iterating an `ArrayList`:

```java
Iterator<Integer> iterator = list.iterator();

while (iterator.hasNext()) {
    Integer value = iterator.next();

    if (value == 2) {
        iterator.remove();
    }
}
```

Result:

```text
[1, 3]
```

The iterator knows about its own modification and can maintain its internal state.

---

### Fail-Safe / Snapshot-Based

"Fail-safe" is common interview terminology, but it isn't an official Java API classification.

A better description for `CopyOnWriteArrayList` is:

> **Snapshot-based iterator**

```java
CopyOnWriteArrayList<Integer> list =
        new CopyOnWriteArrayList<>();

list.add(1);
list.add(2);
list.add(3);

for (Integer value : list) {
    if (value == 2) {
        list.remove(value);
    }
}
```

The iteration can continue without `ConcurrentModificationException`.

Conceptually:

```text
Iterator created
      ↓
Snapshot = [1, 2, 3]

list.remove(2)

Actual list = [1, 3]
Iterator    = [1, 2, 3]
```

The iterator continues over its original snapshot.

---

### CopyOnWriteArrayList — Key Properties

### Reads

Cheap and safe.

### Writes

Expensive because a structural modification creates a new underlying array.

```text
add/remove
    ↓
copy array
    ↓
modify new array
```

Therefore:

> **Good for read-heavy, write-rare workloads.**

### Iterator

Snapshot-based.

```text
Iterator created
      ↓
Snapshot captured
      ↓
Later modifications
      ↓
Existing iterator doesn't see them
```

### `iterator.remove()`

Not supported:

```java
iterator.remove();
```

throws:

```text
UnsupportedOperationException
```

Even though:

```java
list.remove(value);
```

is supported.

---

### ConcurrentHashMap

`ConcurrentHashMap` uses **weakly consistent iterators**.

Example:

```java
ConcurrentHashMap<Integer, String> map =
        new ConcurrentHashMap<>();

map.put(1, "A");
map.put(2, "B");

for (Integer key : map.keySet()) {
    map.put(3, "C");
}
```

The iteration can continue without:

```text
ConcurrentModificationException
```

### Weakly consistent means

* Concurrent modifications are allowed.
* No `ConcurrentModificationException` due to those modifications.
* The iterator may reflect some modifications.
* It does **not** provide a snapshot.
* It does **not** guarantee that every modification will be observed.

---

### Three Iterator Models

| Collection             | Iterator behavior     | Key idea                        |
| ---------------------- | --------------------- | ------------------------------- |
| `ArrayList`            | **Fail-fast**         | Modification may cause CME      |
| `CopyOnWriteArrayList` | **Snapshot-based**    | Iterates over captured snapshot |
| `ConcurrentHashMap`    | **Weakly consistent** | Allows concurrent modifications |

### Memorize this

```text
ArrayList
→ Fail-fast

CopyOnWriteArrayList
→ Snapshot-based

ConcurrentHashMap
→ Weakly consistent
```

---

### Fail-Fast vs Snapshot vs Weakly Consistent

```text
                    Iterator
                       │
       ┌───────────────┼────────────────┐
       │               │                │
   ArrayList       CopyOnWrite      ConcurrentHashMap
       │               │                │
   Fail-fast       Snapshot       Weakly consistent
       │               │                │
   May throw       Stable view     Allows concurrent
      CME          of old state       modification
```

---

### Important Interview Traps

### 1. CME does NOT mean multiple threads

This can happen in a single thread:

```java
for (Integer x : list) {
    list.remove(x);
}
```

`ConcurrentModificationException` is about **unexpected structural modification during iteration**, not necessarily concurrency.

---

### 2. Fail-fast ≠ guaranteed exception

Fail-fast detection is **best-effort**.

Don't use `ConcurrentModificationException` as a correctness mechanism.

---

### 3. CopyOnWriteArrayList ≠ live iterator

If:

```java
Iterator<Integer> iterator = list.iterator();

list.add(4);
```

the existing iterator generally **does not see `4`**.

It sees the snapshot captured when it was created.

---

### 4. ConcurrentHashMap ≠ snapshot

Its iterator is **weakly consistent**, not snapshot-based.

It may observe some modifications made after iteration begins.

---

### 5. CopyOnWriteArrayList writes are expensive

```text
Many reads + few writes
        ↓
CopyOnWriteArrayList ✅

Many writes + few reads
        ↓
CopyOnWriteArrayList generally ❌
```

---

### Final Interview Answer

> **"A fail-fast iterator, such as the one used by ArrayList, attempts to detect structural modifications made outside the iterator and may throw ConcurrentModificationException. CopyOnWriteArrayList uses snapshot-based iterators, so modifications don't affect an existing iterator, but every structural write requires copying the underlying array. ConcurrentHashMap provides weakly consistent iterators that tolerate concurrent modifications without throwing ConcurrentModificationException and may reflect some of those modifications."**

### 10-Second Revision

```text
Fail-fast
→ ArrayList
→ CME may occur
→ Best-effort detection

Snapshot
→ CopyOnWriteArrayList
→ Iterator sees old snapshot
→ Writes are expensive
→ Read-heavy workloads

Weakly consistent
→ ConcurrentHashMap
→ Concurrent modifications allowed
→ No CME
→ May see some modifications
```

# Q13 · `CopyOnWriteArrayList` — When Is It the Right Pick?

### What is `CopyOnWriteArrayList`?

`CopyOnWriteArrayList` is a **thread-safe List implementation** designed primarily for:

> **Read-heavy, write-rare workloads where safe, stable iteration is important.**

The core idea is:

```text
Read
→ use the existing array

Write
→ copy the underlying array
→ apply the modification
→ publish the new array
```

---

### Why Is It Called Copy-On-Write?

Suppose:

```java
CopyOnWriteArrayList<Integer> list =
        new CopyOnWriteArrayList<>();

list.add(1);
list.add(2);
list.add(3);
```

Conceptually:

```text
Current array
[1, 2, 3]

list.add(4)
      ↓
copy array
      ↓
New array
[1, 2, 3, 4]
```

Therefore:

```text
Reads / iteration → cheap
Writes             → expensive
```

---

### When Should You Choose It?

The most important rule is:

```text
READS >>>>>>>>>>> WRITES
```

For example:

```text
100,000 reads/sec
        +
2 writes/sec
```

This is a **read-heavy workload**, so `CopyOnWriteArrayList` can be a good fit.

### Why?

* Many threads can read concurrently.
* Iteration uses a stable snapshot.
* Readers don't need to coordinate with every write.
* Writes are rare enough that the array-copy cost may be acceptable.

---

### The Classic Use Case — Listener Registry

Suppose you maintain:

```java
List<EventListener> listeners;
```

Listeners are:

* registered rarely,
* removed rarely,
* iterated over whenever an event occurs.

Conceptually:

```text
Register listener
      ↓
   rare write

Publish event
      ↓
iterate listeners
      ↓
frequent reads
```

This is an excellent `CopyOnWriteArrayList` use case.

Other examples:

* Event listener registries
* Subscriber lists
* Read-mostly configuration
* Frequently iterated metadata

---

### The Main Trade-off

The entire design revolves around this trade-off:

```text
                    CopyOnWriteArrayList
                            │
                 ┌──────────┴──────────┐
                 │                     │
               READ                  WRITE
                 │                     │
              Cheap                Expensive
                 │                     │
          Stable snapshot       Copy underlying
                                  array
```

Therefore:

```text
Many reads + few writes
        ↓
       ✅
```

while:

```text
Many writes
        ↓
       ❌
```

---

### Iterator Behavior

This is one of the most important interview concepts.

Consider:

```java
CopyOnWriteArrayList<Integer> list =
        new CopyOnWriteArrayList<>();

list.add(1);
list.add(2);
list.add(3);

Iterator<Integer> iterator = list.iterator();

list.add(4);
```

Now:

```java
while (iterator.hasNext()) {
    System.out.println(iterator.next());
}
```

prints:

```text
1
2
3
```

not:

```text
1
2
3
4
```

### Why?

The iterator was created when the list was:

```text
[1, 2, 3]
```

So it operates on that snapshot:

```text
Actual list:
[1, 2, 3, 4]

Existing iterator:
[1, 2, 3]
```

### Key rule

> **An existing `CopyOnWriteArrayList` iterator does not see modifications made after the iterator was created.**

---

### Modification During Iteration

Consider:

```java
for (Integer value : list) {
    if (value == 2) {
        list.remove(value);
    }

    System.out.println(value);
}
```

With `CopyOnWriteArrayList`, the iteration can continue safely.

The iterator has:

```text
Snapshot:
[1, 2, 3]
```

while the actual list becomes:

```text
Actual list:
[1, 3]
```

Therefore the iteration prints:

```text
1
2
3
```

and the final list is:

```text
[1, 3]
```

---

### `iterator.remove()` Is Different

This is a common interview trap.

With:

```java
Iterator<Integer> iterator = list.iterator();
```

calling:

```java
iterator.remove();
```

throws:

```text
UnsupportedOperationException
```

### Why?

The iterator is **snapshot-based** and does not support mutation.

Therefore:

```java
list.remove(value);
```

✅ Supported

but:

```java
iterator.remove();
```

❌ Unsupported

---

### "Fail-Safe" Terminology

You may hear:

> "`CopyOnWriteArrayList` is fail-safe."

This is common interview terminology, but **"fail-safe" is not an official Java API classification**.

For a technically precise answer, say:

> **"`CopyOnWriteArrayList` provides snapshot-based iterators."**

This is preferable to simply calling it fail-safe.

---

### Why Is Write-Heavy Workload Bad?

Suppose:

```text
10,000 writes/sec
100 reads/sec
```

Every structural write can require copying the underlying array.

Conceptually:

```text
10,000 writes
      ↓
10,000 array copies
      ↓
CPU + memory allocation
      ↓
potential GC pressure
```

Therefore, `CopyOnWriteArrayList` is generally a **poor choice for write-heavy workloads**.

---

### List Size Also Matters

The cost of a write depends heavily on the size of the underlying array.

Suppose:

```text
List size = 1,000,000
```

and:

```java
list.set(500_000, newValue);
```

The important consideration is that the copy-on-write mechanism can require copying the underlying array rather than simply modifying one element in place.

Conceptually:

```text
1,000,000-element array
        ↓
      COPY
        ↓
new 1,000,000-element array
        ↓
modify element
```

Therefore, even **infrequent writes** can become expensive if the list is extremely large.

---

### Read-Heavy vs Write-Heavy

### Read-heavy

```text
100,000 reads/sec
2 writes/sec
```

✅ Potentially excellent fit.

### Write-heavy

```text
10,000 writes/sec
100 reads/sec
```

❌ Generally poor fit.

### The important point

Don't think:

> "There are writes, so I cannot use `CopyOnWriteArrayList`."

Instead ask:

> **"Are writes rare enough, and is the cost of copying the entire array acceptable?"**

---

### `CopyOnWriteArrayList` vs `ArrayList`

|                                    | `ArrayList`                | `CopyOnWriteArrayList`         |
| ---------------------------------- | -------------------------- | ------------------------------ |
| Thread-safe                        | ❌                          | ✅                              |
| Iterator                           | Fail-fast, best-effort     | Snapshot-based                 |
| Concurrent structural modification | May cause CME              | Existing iterator remains safe |
| Read-heavy concurrent workload     | Not inherently thread-safe | Good fit                       |
| Write cost                         | Relatively cheap           | Expensive                      |
| Writes                             | In-place                   | Copy-on-write                  |

### Important

Don't choose `CopyOnWriteArrayList` **just because it is thread-safe**.

The workload matters.

---

### `CopyOnWriteArrayList` vs `ConcurrentHashMap`

These solve different problems.

### `CopyOnWriteArrayList`

```text
List
↓
Read-heavy
↓
Snapshot-based iterator
```

### `ConcurrentHashMap`

```text
Map
↓
Concurrent map operations
↓
Weakly consistent iterator
```

The iterator behavior is especially important:

```text
CopyOnWriteArrayList
→ snapshot
→ doesn't see later modifications
```

versus:

```text
ConcurrentHashMap
→ weakly consistent
→ may observe some modifications
```

---

### Common Interview Scenarios

### Scenario 1

```text
100,000 reads/sec
2 writes/sec
```

**Good candidate?**

✅ Yes, assuming the list size and memory/copy cost are acceptable.

---

### Scenario 2

```text
10,000 writes/sec
100 reads/sec
```

**Good candidate?**

❌ Generally no.

Every write can involve copying the array.

---

### Scenario 3

```text
Event listeners:
Register/remove → rare
Notify → extremely frequent
```

**Good candidate?**

✅ Yes.

Classic use case.

---

### Scenario 4

```text
Shopping cart:
add/remove → frequent
```

**Good candidate?**

❌ No.

---

### Scenario 5

```text
Existing iterator must see modifications
made after iterator creation
```

**Good candidate?**

❌ No.

`CopyOnWriteArrayList` iterators are snapshot-based.

---

### Scenario 6

```text
Readers need a stable view while another
thread modifies the list
```

**Good candidate?**

✅ Yes.

The iterator operates on its snapshot.

---

### Important Interview Traps

### 1. "CopyOnWriteArrayList is always better for concurrency."

❌ False.

It's specifically optimized for **read-heavy, write-rare** workloads.

---

### 2. "CopyOnWriteArrayList makes writes cheap."

❌ False.

Writes are expensive because of the copy-on-write mechanism.

---

### 3. "The iterator sees newly added elements."

❌ False.

An existing iterator operates on its snapshot.

---

### 4. "`iterator.remove()` works."

❌ False.

It throws:

```text
UnsupportedOperationException
```

---

### 5. "`CopyOnWriteArrayList` is fail-safe."

⚠️ Common interview terminology, but technically prefer:

> **Snapshot-based iterator.**

---

### 6. "COW is bad if there are any writes."

❌ False.

A workload like:

```text
100,000 reads/sec
2 writes/sec
```

can still be an excellent fit.

The question is whether the **write frequency × list size** makes copying expensive.

---

### Interview Decision Framework

When asked:

> **"Would you use `CopyOnWriteArrayList`?"**

Ask yourself:

### 1. Are reads much more frequent than writes?

```text
Reads >>> Writes
```

If yes → ✅

### 2. Are writes relatively rare?

If yes → ✅

### 3. Is frequent iteration required?

If yes → ✅

### 4. Do readers need a stable view?

If yes → ✅

### 5. Is copying the entire array on writes acceptable?

If yes → ✅

If not → consider another collection/design.

---

### Final Interview Answer

> **"`CopyOnWriteArrayList` is a good choice for read-heavy, write-rare workloads where safe, stable iteration is important. Its iterators operate on a snapshot, so concurrent modifications don't cause `ConcurrentModificationException` for the existing iterator. The trade-off is that structural writes are expensive because the underlying array is copied, so it is generally unsuitable for write-heavy workloads or very large lists with frequent updates."**

---

### 10-Second Revision

```text
CopyOnWriteArrayList
→ Thread-safe List
→ Read-heavy / write-rare

READ
→ Cheap
→ Safe concurrent access
→ Iterator uses snapshot

WRITE
→ Expensive
→ Copies underlying array
→ Cost increases with list size

ITERATOR
→ Snapshot-based
→ Doesn't see later modifications
→ No CME from concurrent modifications
→ iterator.remove() unsupported

BEST FOR
→ Listener registries
→ Subscriber lists
→ Read-mostly configuration
→ Frequently iterated, rarely modified lists

BAD FOR
→ Shopping carts
→ Real-time order books
→ Queues
→ Write-heavy workloads

MEMORIZE
→ "Many reads, few writes, stable iteration."
```

# Q14 · TreeMap and Red-Black Trees

> **"What's the underlying data structure of TreeMap, and what guarantees does it give you over HashMap?"**

### What is TreeMap?

`TreeMap` is a `Map` implementation backed by a **self-balancing red-black tree**.

Unlike `HashMap`, which is optimized for fast key lookup using hashing, `TreeMap` keeps its keys **sorted**.

```java
TreeMap<Integer, String> map = new TreeMap<>();

map.put(30, "C");
map.put(10, "A");
map.put(20, "B");
```

Iteration gives:

```text
10
20
30
```

The key trade-off is:

```text
HashMap → O(1) average lookup
TreeMap → O(log n) operations + sorted keys
```

TreeMap is useful when you need **ordering, navigation, or range queries**.

### Underlying Data Structure

TreeMap uses a **red-black tree**, which is a self-balancing Binary Search Tree.

```text
TreeMap
   ↓
Red-Black Tree
   ↓
Self-Balancing BST
   ↓
Sorted keys
+
O(log n) operations
```

Because it is a BST:

```text
left subtree < current node < right subtree
```

TreeMap uses **key comparison**, not hashing.

The keys are ordered using:

* `Comparable` → natural ordering
* `Comparator` → custom ordering

### Why Does TreeMap Need Balancing?

A normal BST can become skewed.

For example, inserting:

```text
10 → 20 → 30 → 40 → 50
```

can produce:

```text
10
  \
   20
     \
      30
        \
         40
           \
            50
```

This effectively behaves like a linked list.

Searching can therefore degrade to:

```text
O(n)
```

A red-black tree maintains balancing invariants so that its height remains:

```text
O(log n)
```

Therefore:

```text
get()    → O(log n)
put()    → O(log n)
remove() → O(log n)
```

### Red-Black Tree

Each node is either:

```text
🔴 RED
⚫ BLACK
```

Important invariants:

### 1. No red node has a red parent

Invalid:

```text
    20⚫
    /
  10🔴
  /
 5🔴
```

because `5` has a red parent.

### 2. Every root-to-null path has the same number of black nodes

This prevents paths from becoming arbitrarily unbalanced.

Together, these rules keep the tree approximately balanced.

### How Does Balancing Happen?

When insertion or deletion violates a red-black invariant, the tree can repair itself using:

* **Recoloring**
* **Rotations**

### Recoloring

Changes node colors:

```text
🔴 → ⚫
⚫ → 🔴
```

For example, when a red parent and red uncle cause a violation, recoloring can restore the local invariant and push the balancing problem upward.

### Rotation

A rotation changes the **shape** of the tree while preserving BST ordering.

Example:

```text
Before:

    20
   /
 10
 /
5
```

Right rotation around `20`:

```text
    10
   /  \
  5   20
```

The ordering is still:

```text
5 < 10 < 20
```

Remember:

```text
Recoloring → changes colors
Rotation   → changes tree shape
```

### TreeMap vs HashMap

|                        | HashMap                   | TreeMap                     |
| ---------------------- | ------------------------- | --------------------------- |
| Data structure         | Hash table                | Red-black tree              |
| Key mechanism          | `hashCode()` + `equals()` | `Comparable` / `Comparator` |
| Average lookup         | O(1)                      | O(log n)                    |
| Ordering               | No ordering guarantee     | Sorted                      |
| Range queries          | Not naturally supported   | Supported                   |
| Nearest-key operations | No                        | Yes                         |
| `floorKey()`           | No                        | Yes                         |
| `ceilingKey()`         | No                        | Yes                         |
| `subMap()`             | No                        | Yes                         |

**Important:** Don't say TreeMap is simply "faster" than HashMap.

The distinction is:

```text
HashMap
→ faster average plain lookup

TreeMap
→ sorted keys
→ navigation
→ range queries
→ O(log n) operations
```

### Comparable vs Comparator

TreeMap needs to know how keys should be ordered.

### Natural ordering

```java
TreeMap<Integer, String> map = new TreeMap<>();
```

`Integer` provides its natural ordering through `Comparable`.

### Custom ordering

```java
TreeMap<String, Integer> map =
    new TreeMap<>(Comparator.reverseOrder());
```

Here the supplied `Comparator` determines the ordering.

### Navigation Methods

### `firstKey()`

Returns the smallest key.

```java
map.firstKey();
```

### `lastKey()`

Returns the largest key.

```java
map.lastKey();
```

### `floorKey(k)`

Returns the **largest key ≤ k**.

```java
map.floorKey(35);
```

For:

```text
10 20 30 40 50
```

result:

```text
30
```

### `ceilingKey(k)`

Returns the **smallest key ≥ k**.

```java
map.ceilingKey(35);
```

Result:

```text
40
```

### Range Operations

### `headMap(k)`

Returns entries with keys `< k`.

```java
map.headMap(40);
```

### `tailMap(k)`

Returns entries with keys `>= k`.

```java
map.tailMap(40);
```

### `subMap(...)`

Returns entries within a key range.

For an inclusive range from `20` through `40`:

```java
map.subMap(20, true, 40, true);
```

Signature:

```text
subMap(fromKey, includeFrom, toKey, includeTo)
```

### Common Use Cases

Use TreeMap when you need:

* Sorted iteration
* Range queries
* Closest/nearest key lookup
* `floorKey()`
* `ceilingKey()`
* `firstKey()` / `lastKey()`
* `headMap()`
* `tailMap()`
* `subMap()`

### Common Interview Follow-Ups

### Why use TreeMap if HashMap has O(1) average lookup?

Because the requirement may be **ordering or navigation**, not just lookup.

For example:

```java
floorKey()
ceilingKey()
firstKey()
lastKey()
subMap()
headMap()
tailMap()
```

### How would you find all entries between X and Y?

For an inclusive range:

```java
map.subMap(X, true, Y, true);
```

### What happens if a normal BST is used instead?

It can become skewed:

```text
10
  \
   20
     \
      30
```

and operations can degrade to:

```text
O(n)
```

The red-black tree's balancing maintains logarithmic height.

### What happens during red-black balancing?

### Red parent + red uncle

Typically handled through **recoloring**, pushing the balancing problem upward.

### Red parent + no red uncle / shape imbalance

May require **rotation + recoloring**.

Example of an LL configuration:

```text
    20
   /
 10
 /
5
```

Right rotation:

```text
   10
  /  \
 5   20
```

### Edge Cases

### Null Keys

TreeMap does not allow null keys because keys participate in ordering/comparison.

TreeMap allows null values.

### Duplicate Keys

Like any `Map`, keys are unique.

Putting an existing key replaces its value:

```java
map.put(10, "A");
map.put(10, "B");
```

Result:

```text
10 → B
```

### Comparator

If a custom `Comparator` is supplied, **that comparator controls the ordering of the tree**.

### Concurrent Equivalent

For a concurrent sorted map:

```java
ConcurrentSkipListMap
```

It provides a concurrent sorted-map structure with `O(log n)` operations.

### Common Interview Traps

### Trap 1 — "TreeMap uses hashing"

❌ Wrong.

TreeMap uses:

```text
Comparable / Comparator
```

### Trap 2 — "TreeMap is faster than HashMap"

❌ Too broad.

HashMap has average `O(1)` lookup.

TreeMap has `O(log n)` operations but provides sorted ordering and navigation.

### Trap 3 — "TreeMap is a B-tree"

❌ Wrong.

TreeMap uses a **red-black tree**.

### Trap 4 — "Red-black trees are perfectly balanced"

❌ Wrong.

Say:

> **Red-black trees are self-balancing and maintain invariants that guarantee logarithmic height.**

### Trap 5 — "Rotation changes BST ordering"

❌ Wrong.

Rotation changes the **shape** while preserving BST ordering.

### Trap 6 — "TreeMap prevents all imbalance"

Avoid this wording.

Better:

> **The red-black invariants prevent the tree from degenerating into a linear-height tree and guarantee O(log n) height.**

### Decision Framework

```text
Need only fast key lookup?
        ↓
     HashMap

Need sorted keys?
        ↓
     TreeMap

Need nearest key?
        ↓
     TreeMap
 floorKey / ceilingKey

Need key range?
        ↓
     TreeMap
 headMap / tailMap / subMap

Need concurrent + sorted map?
        ↓
 ConcurrentSkipListMap
```

### Final Interview Answer

> **"TreeMap is backed by a self-balancing red-black tree. It maintains keys in sorted order using their natural ordering or a Comparator, giving O(log n) `get`, `put`, and `remove` operations. Compared with HashMap's average O(1) lookup, TreeMap trades some lookup performance for ordered iteration and useful navigation and range operations such as `floorKey`, `ceilingKey`, and `subMap`. I'd use TreeMap when sorted data, nearest-key lookup, or range queries are required."**

### 10-Second Revision

```text
TreeMap
   ↓
Red-Black Tree
   ↓
Self-balancing BST
   ↓
O(log n)
   ↓
Sorted keys
   ↓
floor / ceiling / first / last
   ↓
headMap / tailMap / subMap
```

**Memory hook:**

> **HashMap = fast lookup**
> **TreeMap = sorted lookup + navigation**


# Q15 — LinkedHashMap and LRU Cache

### Interview Question

**How would you implement an LRU cache in Java in 10 lines?**

### 30-Second Interview Answer

> I would use `LinkedHashMap` with `accessOrder=true` and override `removeEldestEntry()`. `LinkedHashMap` combines hash-table lookup with a doubly-linked ordering of entries. With access order enabled, every access moves the entry to the tail, making the head the least recently used entry. When the cache exceeds its capacity, `removeEldestEntry()` automatically removes the LRU entry. This gives O(1) average `get`, `put`, and eviction operations.

---

### What is `LinkedHashMap`?

`LinkedHashMap` combines:

1. **Hash-table lookup** → fast access by key.
2. **Doubly-linked entry ordering** → maintains a predictable iteration order.

By default, the ordering is **insertion order**.

```java
LinkedHashMap<Integer, String> map = new LinkedHashMap<>();

map.put(1, "A");
map.put(2, "B");
map.put(3, "C");
```

Iteration order:

```text
1 → 2 → 3
```

---

### Insertion Order vs Access Order

The constructor is:

```java
LinkedHashMap(
    int initialCapacity,
    float loadFactor,
    boolean accessOrder
)
```

The important parameter is:

```java
accessOrder
```

### `accessOrder = false`

Default behavior:

```text
Insertion order
```

```java
new LinkedHashMap<>(16, 0.75f, false);
```

### `accessOrder = true`

```text
Access order
```

```java
new LinkedHashMap<>(16, 0.75f, true);
```

Now accessing an entry moves it toward the **tail**.

---

### Why `accessOrder=true` Is Important for LRU

Suppose:

```java
LinkedHashMap<Integer, String> map =
    new LinkedHashMap<>(16, 0.75f, true);

map.put(1, "A");
map.put(2, "B");
map.put(3, "C");
```

Current order:

```text
1 → 2 → 3
```

Now:

```java
map.get(1);
```

The accessed entry moves to the tail:

```text
2 → 3 → 1
```

Therefore:

```text
Head = LRU
Tail = MRU
```

Where:

* **LRU** = Least Recently Used
* **MRU** = Most Recently Used

---

### Why Does `get()` Change the Map?

Normally, we think of `get()` as a read operation.

But with:

```java
accessOrder = true
```

a `get()` also updates the access ordering.

Example:

```text
Before:

2 → 3 → 1
↑         ↑
LRU       MRU
```

Execute:

```java
cache.get(2);
```

After:

```text
3 → 1 → 2
         ↑
        MRU
```

`2` became the most recently accessed entry, so it moves to the tail.

---

### How LRU Eviction Works

Assume:

```text
capacity = 3
```

Operations:

```java
put(1, "A");
put(2, "B");
put(3, "C");
```

Order:

```text
1 → 2 → 3
```

Access `1`:

```java
get(1);
```

Order becomes:

```text
2 → 3 → 1
```

Now insert `4`:

```java
put(4, "D");
```

Temporarily:

```text
2 → 3 → 1 → 4
↑
LRU
```

Capacity is `3`, but size is now `4`.

Therefore the eldest/LRU entry `2` is removed:

```text
3 → 1 → 4
```

Final entries:

```text
3, 1, 4
```

---

### `removeEldestEntry()`

`LinkedHashMap` provides:

```java
protected boolean removeEldestEntry(Map.Entry<K, V> eldest)
```

By default, it returns `false`.

For an LRU cache, override it:

```java
@Override
protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
    return size() > capacity;
}
```

The method is checked **after a `put`**.

---

### Why `size() > capacity` and Not `>=`?

Suppose:

```text
capacity = 3
```

We want:

```text
put(1) → size = 1 → keep
put(2) → size = 2 → keep
put(3) → size = 3 → keep
put(4) → size = 4 → evict
```

Therefore:

```java
return size() > capacity;
```

is correct.

If we used:

```java
return size() >= capacity;
```

then:

```text
put(3)
size = 3
```

would already trigger eviction.

The cache would never actually be allowed to contain `3` entries.

---

### Complete LRU Cache Implementation

```java
import java.util.LinkedHashMap;
import java.util.Map;

class LRUCache<K, V> extends LinkedHashMap<K, V> {

    private final int capacity;

    LRUCache(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
```

### Usage

```java
LRUCache<Integer, String> cache = new LRUCache<>(3);

cache.put(1, "A");
cache.put(2, "B");
cache.put(3, "C");

cache.get(1);

cache.put(4, "D");
```

The ordering evolves as:

```text
put(1)       → 1
put(2)       → 1 2
put(3)       → 1 2 3

get(1)       → 2 3 1

put(4)       → 2 3 1 4
                ↑
               LRU

evict(2)     → 3 1 4
```

---

### Why Is LRU O(1)?

An LRU cache needs two things:

### 1. Fast key lookup

The hash-table portion allows us to find an entry by key in:

```text
O(1) average
```

### 2. Fast ordering updates

The doubly-linked structure allows us to:

* Move an accessed entry to the tail.
* Remove the LRU entry from the head.

Both are:

```text
O(1)
```

Therefore:

| Operation         |   Complexity |
| ----------------- | -----------: |
| `get()`           | O(1) average |
| `put()`           | O(1) average |
| Move entry to MRU |         O(1) |
| Remove LRU        |         O(1) |

### Mental Model

```text
             Hash Table
                 │
                 ▼
              Entry
                 │
                 ▼
LRU ←──────── Doubly-linked ────────→ MRU
 ↑                                     ↑
Head                                  Tail
```

---

### Why Not `HashMap + LinkedList`?

You could implement an LRU cache using:

```text
HashMap + Doubly Linked List
```

The idea would be:

```text
HashMap
key → node

Doubly Linked List
LRU ← nodes → MRU
```

This works, but you would have to manually maintain both structures.

For example, every `get()` would need to:

1. Find the node in the `HashMap`.
2. Remove it from its current position.
3. Move it to the tail.
4. Keep the `HashMap` pointing to the same node.

`LinkedHashMap` already provides this mechanism.

For this interview question, `LinkedHashMap` is therefore the concise Java-specific solution.

---

### What Happens When `put()` Updates an Existing Key?

This is an important follow-up.

With:

```java
accessOrder = true
```

an access to an existing entry can update its position.

For example:

```text
Before:

1 → 2 → 3
```

Then:

```java
map.put(1, "Updated");
```

The existing entry `1` is treated as accessed and moves toward the tail:

```text
2 → 3 → 1
```

So don't think only `get()` matters when reasoning about access ordering.

---

### Thread Safety

`LinkedHashMap` is **not thread-safe by default**.

This is especially important for an LRU cache because:

```java
cache.get(key);
```

can modify the internal ordering when:

```java
accessOrder = true;
```

So a `get()` can itself cause a structural modification.

For simple synchronization, a synchronized map can be considered:

```java
Collections.synchronizedMap(...);
```

However, for a concurrent production cache, a dedicated caching library such as **Caffeine** is generally more appropriate.

---

### LRU vs TTL

LRU and TTL solve different problems.

| Mechanism     | Based on           |
| ------------- | ------------------ |
| **LRU**       | Recent usage       |
| **TTL**       | Time elapsed       |
| **LRU + TTL** | Usage + expiration |

### Why Do We Need TTL?

Suppose:

```text
Capacity = 100
```

An entry may remain in the cache for a very long time if the cache doesn't become full.

TTL allows an entry to expire after a configured amount of time.

For example:

```text
TTL = 10 minutes
```

An entry can expire after 10 minutes even if the cache still has plenty of capacity.

`LinkedHashMap` gives you the LRU mechanism, but it does **not** provide built-in TTL expiration.

For requirements involving both eviction and expiration, a dedicated cache implementation such as Caffeine is more suitable.

---

### Production Considerations

The `LinkedHashMap` implementation is excellent for:

* Interview implementations
* Simple in-memory caches
* Small/single-threaded use cases
* Understanding the LRU mechanism

For production caching, requirements may include:

* Concurrent access
* TTL expiration
* Maximum size
* Maximum weight
* Statistics
* Refresh
* More sophisticated eviction policies

A dedicated cache library such as **Caffeine** can handle these requirements.

The key interview distinction is:

```text
LinkedHashMap
    ↓
Simple LRU implementation

Caffeine
    ↓
Production-oriented caching
```

---

### Common Interview Traps

### Trap 1 — Forgetting `accessOrder=true`

```java
new LinkedHashMap<>(16, 0.75f, true);
```

The third parameter must be `true` for access-order behavior.

Without it:

```text
Insertion order
```

With it:

```text
Access order
```

---

### Trap 2 — Using `>=`

Wrong:

```java
return size() >= capacity;
```

Correct:

```java
return size() > capacity;
```

The cache should be allowed to reach its maximum capacity.

---

### Trap 3 — Saying `get()` is always read-only

With:

```java
accessOrder = true
```

`get()` changes the ordering.

---

### Trap 4 — Saying `LinkedHashMap` is thread-safe

It isn't.

---

### Trap 5 — Saying LRU provides TTL

It doesn't.

```text
LRU → usage-based eviction
TTL → time-based expiration
```

---

### Trap 6 — Saying "LinkedHashMap is just HashMap + LinkedList"

A better explanation is:

> `LinkedHashMap` combines hash-table lookup with linked entry ordering.

---

### Trap 7 — Saying "Just use Redis"

For this interview question, the interviewer is testing the **Java implementation of an LRU cache**. Redis is a separate distributed-cache discussion.

---

### Common Follow-Up Questions

### Why does `get()` move an entry?

Because `accessOrder=true` tracks recent accesses. The accessed entry becomes the MRU entry and moves to the tail.

### Which entry is evicted?

The **eldest entry**, which is the LRU entry when access-order mode is enabled.

### Why is eviction O(1)?

The LRU entry is at the head of the linked structure, so removing it is constant time.

### Why is lookup O(1)?

The hash-table portion provides O(1) average key lookup.

### Why use `LinkedHashMap` instead of `HashMap`?

`HashMap` provides lookup but doesn't maintain the access ordering required to identify the LRU entry efficiently.

### What if you need TTL?

Use a cache implementation that supports expiration, such as Caffeine.

### Is the implementation thread-safe?

No. `LinkedHashMap` is not thread-safe by default.

### What would you use in production?

For a concurrent cache with expiration and more advanced requirements, consider Caffeine.

### What if the interviewer says "don't use `LinkedHashMap`"?

Then implement the classic:

```text
HashMap<K, Node>
        +
Doubly Linked List
```

The `HashMap` gives O(1) lookup, while the doubly-linked list maintains LRU → MRU ordering.

---

### Alternative Interview Implementation: HashMap + Doubly Linked List

If the interviewer wants you to implement the data structure yourself, this is the standard approach.

```java
import java.util.HashMap;
import java.util.Map;

class LRUCache<K, V> {

    private static class Node<K, V> {
        K key;
        V value;
        Node<K, V> prev;
        Node<K, V> next;

        Node(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }

    private final int capacity;
    private final Map<K, Node<K, V>> map = new HashMap<>();

    // Dummy nodes
    private final Node<K, V> head = new Node<>(null, null);
    private final Node<K, V> tail = new Node<>(null, null);

    LRUCache(int capacity) {
        this.capacity = capacity;

        head.next = tail;
        tail.prev = head;
    }

    public V get(K key) {
        Node<K, V> node = map.get(key);

        if (node == null) {
            return null;
        }

        remove(node);
        addToTail(node);

        return node.value;
    }

    public void put(K key, V value) {
        if (map.containsKey(key)) {
            Node<K, V> node = map.get(key);

            node.value = value;

            remove(node);
            addToTail(node);

            return;
        }

        Node<K, V> node = new Node<>(key, value);

        map.put(key, node);
        addToTail(node);

        if (map.size() > capacity) {
            Node<K, V> lru = head.next;

            remove(lru);
            map.remove(lru.key);
        }
    }

    private void remove(Node<K, V> node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void addToTail(Node<K, V> node) {
        node.prev = tail.prev;
        node.next = tail;

        tail.prev.next = node;
        tail.prev = node;
    }
}
```

### Why this works

```text
HashMap
key → Node
```

gives:

```text
O(1) average lookup
```

The doubly-linked list gives:

```text
Head → LRU
Tail → MRU
```

Therefore:

```text
get()
  → HashMap lookup
  → remove node
  → add node to tail

put()
  → HashMap lookup/insert
  → move to tail
  → if capacity exceeded
       remove head
```

All core operations remain:

```text
O(1) average
```

---

### LinkedHashMap vs Manual LRU Implementation

|                                    | `LinkedHashMap`         | Manual implementation                  |
| ---------------------------------- | ----------------------- | -------------------------------------- |
| Lookup                             | O(1) average            | O(1) average                           |
| LRU ordering                       | Built in                | Implement yourself                     |
| Eviction                           | `removeEldestEntry()`   | Implement yourself                     |
| Code size                          | Very small              | Larger                                 |
| Interview "implement from scratch" | Usually not enough      | Appropriate                            |
| Risk of bugs                       | Low                     | Higher                                 |
| Best use                           | Java-specific interview | Data-structure/system-design follow-up |

---

### Final Interview Answer

> "For a simple Java LRU cache, I'd extend `LinkedHashMap` and enable access order with `accessOrder=true`. That gives me hash-table lookup plus a doubly-linked ordering of entries. Every access moves the entry to the tail, so the head represents the least recently used entry. I override `removeEldestEntry()` and return `size() > capacity`, which automatically evicts the LRU entry after an insertion exceeds capacity. `get`, `put`, and eviction are O(1) on average. The basic implementation isn't thread-safe, and if I need concurrency, TTL, or more advanced eviction behavior in production, I'd consider a dedicated cache such as Caffeine."

---

### 10-Second Revision

```text
LinkedHashMap
     +
accessOrder = true
     ↓
Head = LRU
Tail = MRU
     ↓
get() → move accessed entry to tail
     ↓
put() → if size > capacity
     ↓
remove eldest
     ↓
O(1) average get / put / eviction
```

### Code to Memorize

```java
class LRUCache<K, V> extends LinkedHashMap<K, V> {

    private final int capacity;

    LRUCache(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
```

### One-Line Memory Trick

> **`LinkedHashMap + accessOrder=true + removeEldestEntry(size > capacity) = simple O(1) LRU cache.`**

# Q16 · HashSet vs TreeSet vs LinkedHashSet

### Interview Question

> **Compare `HashSet`, `TreeSet`, and `LinkedHashSet`. When would you use each one?**

### 30-Second Interview Answer

> `HashSet` is backed by a `HashMap`, so it provides O(1) average `add`, `remove`, and `contains`, but does not guarantee iteration order.
>
> `LinkedHashSet` adds a linked structure to the hash-based implementation, maintaining **insertion order** while retaining O(1) average operations.
>
> `TreeSet` is backed by a `TreeMap` using a **red-black tree**. It maintains elements in sorted order and provides O(log n) `add`, `remove`, and `contains`.
>
> So I would use `HashSet` when I only need uniqueness, `LinkedHashSet` when I need uniqueness plus insertion order, and `TreeSet` when I need uniqueness plus sorted order or navigation operations.

---

### The Core Mental Model

Memorize this:

```text
HashSet
    ↓
HashMap
    ↓
Hash table
    ↓
hashCode() + equals()
    ↓
O(1) average
    ↓
No guaranteed order
```

```text
LinkedHashSet
    ↓
LinkedHashMap
    ↓
Hash table + linked structure
    ↓
hash-based lookup + insertion order
    ↓
O(1) average
```

```text
TreeSet
    ↓
TreeMap
    ↓
Red-black tree
    ↓
Comparable / Comparator
    ↓
O(log n)
    ↓
Sorted order + navigation
```

### Memory Trick

```text
HashSet       → Fast
LinkedHashSet → Fast + insertion order
TreeSet       → Sorted + navigation
```

---

### 1. HashSet

### What is it?

`HashSet` is a `Set` implementation that is implemented using a `HashMap`.

Conceptually:

```text
HashSet
    ↓
HashMap

element → dummy value
```

For example:

```java
Set<Integer> set = new HashSet<>();

set.add(10);
set.add(20);
set.add(30);
```

Conceptually:

```text
HashMap

key       value
----------------
10        PRESENT
20        PRESENT
30        PRESENT
```

The important point:

> The elements of the `HashSet` are used as keys in the underlying hash-based structure.

### HashSet Properties

| Property       | HashSet             |
| -------------- | ------------------- |
| Main structure | Hash table          |
| Backed by      | HashMap             |
| Ordering       | No guaranteed order |
| Duplicates     | Not allowed         |
| `add()`        | O(1) average        |
| `remove()`     | O(1) average        |
| `contains()`   | O(1) average        |
| Sorted         | No                  |
| `null`         | One `null` allowed  |
| Thread-safe    | No                  |

### Example

```java
Set<Integer> set = new HashSet<>();

set.add(30);
set.add(10);
set.add(20);
set.add(10);

System.out.println(set);
```

The second `10` is ignored because a `Set` cannot contain duplicates.

Do **not** write code that assumes a particular iteration order.

> Say **"no guaranteed iteration order"**, not "random order."

---

### How Does HashSet Prevent Duplicates?

This is one of the most important interview follow-ups.

When:

```java
set.add(object);
```

is called, the hash-based mechanism conceptually does:

```text
object
   ↓
hashCode()
   ↓
find candidate bucket
   ↓
compare candidate entries
   ↓
equals()
   ↓
duplicate?
   ├── yes → don't add
   └── no  → add
```

### Mental Model

```text
hashCode()
    ↓
"Where should I look?"
```

```text
equals()
    ↓
"Is this actually equal to an existing element?"
```

### Important Contract

If:

```java
a.equals(b) == true
```

then:

```java
a.hashCode() == b.hashCode()
```

must also be true.

But the reverse is **not** guaranteed:

```text
same hashCode
    ↓
does NOT mean
    ↓
equals() == true
```

Different objects can have the same hash code.

That's a **hash collision**.

---

### Custom Objects in HashSet

Consider:

```java
class User {
    private final int id;

    User(int id) {
        this.id = id;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof User other)) {
            return false;
        }

        return id == other.id;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(id);
    }
}
```

Now:

```java
Set<User> users = new HashSet<>();

users.add(new User(1));
users.add(new User(1));

System.out.println(users.size());
```

Output:

```text
1
```

Why?

```text
User(1)
   ↓
same hashCode
   ↓
same candidate bucket
   ↓
equals() returns true
   ↓
duplicate
   ↓
not inserted
```

### Without overriding `equals()` and `hashCode()`

```java
Set<User> users = new HashSet<>();

users.add(new User(1));
users.add(new User(1));

System.out.println(users.size());
```

The result is:

```text
2
```

because the two `User` objects are different object instances and `Object`'s default equality is identity-based.

---

### 2. LinkedHashSet

`LinkedHashSet` gives you:

```text
HashSet behavior
        +
Insertion order
```

Example:

```java
Set<Integer> set = new LinkedHashSet<>();

set.add(30);
set.add(10);
set.add(20);
set.add(10);
```

Iteration order:

```text
30 → 10 → 20
```

The duplicate `10` is still rejected.

### Important

`LinkedHashSet` does **not** mean:

```text
sorted order
```

It means:

```text
order in which elements were inserted/encountered
```

---

### How Does LinkedHashSet Maintain Order?

Conceptually:

```text
LinkedHashSet
      ↓
LinkedHashMap
      ↓
Hash table + linked structure
```

The two structures serve different purposes:

```text
Hash table
    ↓
Fast lookup
    ↓
O(1) average
```

```text
Linked structure
    ↓
Maintains encounter/insertion order
```

Conceptually:

```text
Hash table
   ↓
entries

Linked ordering:

30 → 10 → 20
```

So:

> `LinkedHashSet` does not use a separate `LinkedList` for retrieval. It maintains links between entries in addition to the hash-based structure.

### LinkedHashSet Properties

| Property       | LinkedHashSet                 |
| -------------- | ----------------------------- |
| Main structure | Hash table + linked structure |
| Backed by      | LinkedHashMap                 |
| Ordering       | Insertion order               |
| Duplicates     | Not allowed                   |
| `add()`        | O(1) average                  |
| `remove()`     | O(1) average                  |
| `contains()`   | O(1) average                  |
| Sorted         | No                            |
| `null`         | One `null` allowed            |
| Thread-safe    | No                            |
| Memory         | More than HashSet             |

### Why Use LinkedHashSet?

A very common use case:

> **Remove duplicates while preserving original order.**

```java
List<Integer> numbers =
        List.of(5, 2, 5, 1, 2, 3);

Set<Integer> unique =
        new LinkedHashSet<>(numbers);

System.out.println(unique);
```

Output:

```text
[5, 2, 1, 3]
```

You get:

```text
uniqueness
    +
original encounter order
```

---

### 3. TreeSet

`TreeSet` is different from the two hash-based sets.

It maintains elements in **sorted order**.

```java
Set<Integer> set = new TreeSet<>();

set.add(30);
set.add(10);
set.add(20);
```

Iteration:

```text
10 → 20 → 30
```

Conceptually:

```text
TreeSet
    ↓
TreeMap
    ↓
Red-black tree
```

### TreeSet Properties

| Property       | TreeSet                                       |
| -------------- | --------------------------------------------- |
| Main structure | Red-black tree                                |
| Backed by      | TreeMap                                       |
| Ordering       | Sorted                                        |
| Duplicates     | Not allowed                                   |
| `add()`        | O(log n)                                      |
| `remove()`     | O(log n)                                      |
| `contains()`   | O(log n)                                      |
| `null`         | Generally not supported with natural ordering |
| Thread-safe    | No                                            |
| Navigation     | Yes                                           |

A red-black tree is a self-balancing binary search tree whose height remains O(log n).

Therefore:

```text
search → O(log n)
insert → O(log n)
delete → O(log n)
```

TreeSet sacrifices average O(1) hash lookup in exchange for:

```text
sorted structure
+
efficient navigation
```

---

### TreeSet's Killer Feature: Navigation

`TreeSet` provides operations that a normal `HashSet` does not.

```java
TreeSet<Integer> set =
        new TreeSet<>(List.of(10, 20, 30, 40, 50));
```

You can ask:

```java
set.first();
set.last();

set.floor(25);
set.ceiling(25);

set.lower(30);
set.higher(30);
```

Results:

```text
first()      → 10
last()       → 50

floor(25)    → 20
ceiling(25)  → 30

lower(30)    → 20
higher(30)   → 40
```

### Navigation Cheat Sheet

```text
lower(x)
    largest element < x

floor(x)
    largest element <= x

ceiling(x)
    smallest element >= x

higher(x)
    smallest element > x
```

Memorize this:

```text
lower   → <
floor   → <=

ceiling → >=
higher  → >
```

### Why This Matters

If the problem asks:

> "Find the closest value less than or equal to X."

Think:

```java
treeSet.floor(x);
```

If it asks:

> "Find the smallest value greater than or equal to X."

Think:

```java
treeSet.ceiling(x);
```

This is extremely useful in coding interviews.

---

### TreeSet Range Operations

`TreeSet` also supports sorted range views:

```java
set.headSet(30);
set.tailSet(30);
set.subSet(20, 40);
```

Useful when working with:

* Sorted data
* Range queries
* Closest values
* Predecessor/successor
* Minimum/maximum
* Ordered iteration

---

### HashSet vs LinkedHashSet vs TreeSet

### Main Comparison

| Feature              | HashSet      | LinkedHashSet                 | TreeSet        |
| -------------------- | ------------ | ----------------------------- | -------------- |
| Underlying structure | Hash table   | Hash table + linked structure | Red-black tree |
| Backed by            | HashMap      | LinkedHashMap                 | TreeMap        |
| Order                | No guarantee | Insertion order               | Sorted order   |
| `add()`              | O(1) avg     | O(1) avg                      | O(log n)       |
| `remove()`           | O(1) avg     | O(1) avg                      | O(log n)       |
| `contains()`         | O(1) avg     | O(1) avg                      | O(log n)       |
| Duplicates           | No           | No                            | No             |
| `null`               | One allowed  | One allowed                   | Generally no   |
| Navigation           | No           | No                            | Yes            |
| Memory overhead      | Lower        | Higher                        | Higher         |
| Thread-safe          | No           | No                            | No             |

### The One Table to Memorize

```text
                  HashSet       LinkedHashSet       TreeSet

Structure         Hash table    Hash + linked      Red-black tree

Order             None          Insertion          Sorted

Add               O(1) avg      O(1) avg           O(log n)

Remove            O(1) avg      O(1) avg           O(log n)

Contains          O(1) avg      O(1) avg           O(log n)

Navigation        No            No                 Yes
```

---

### How to Choose

Always start with the **requirement**, not the collection name.

### Requirement 1

> "I only need unique elements."

```java
HashSet
```

Because:

```text
uniqueness
+
fast average operations
```

---

### Requirement 2

> "I need unique elements and want to preserve insertion order."

```java
LinkedHashSet
```

Because:

```text
uniqueness
+
insertion order
+
O(1) average operations
```

---

### Requirement 3

> "I need unique elements in sorted order."

```java
TreeSet
```

Because:

```text
uniqueness
+
sorted order
+
O(log n)
```

---

### Requirement 4

> "I need to find the closest element to X."

```java
TreeSet
```

because of:

```java
floor()
ceiling()
lower()
higher()
```

---

### Requirement 5

> "I need to remove duplicates from a List while preserving original order."

```java
LinkedHashSet
```

Example:

```java
List<Integer> result =
        new ArrayList<>(
                new LinkedHashSet<>(numbers)
        );
```

---

### The Most Important Internal Difference

This is one of the most common interview follow-ups.

### HashSet

Uses:

```text
hashCode()
    +
equals()
```

Mental model:

```text
hashCode()
    ↓
find candidate bucket
    ↓
equals()
    ↓
same logical element?
```

### TreeSet

Uses:

```text
Comparable.compareTo()
```

or:

```text
Comparator.compare()
```

Mental model:

```text
compare
    ↓
navigate through tree
    ↓
comparison == 0 ?
    ↓
already equivalent
```

Therefore:

> **HashSet determines membership through hashing + equality. TreeSet determines membership through ordering.**

---

### TreeSet and Comparator Equality — Critical Trap

Consider:

```java
TreeSet<String> set =
        new TreeSet<>(
                Comparator.comparingInt(String::length)
        );

set.add("cat");
set.add("dog");
set.add("elephant");

System.out.println(set);
System.out.println(set.size());
```

Lengths:

```text
cat      → 3
dog      → 3
elephant → 8
```

The comparator effectively does:

```text
compare("cat", "dog")
        ↓
3 - 3
        ↓
0
```

Therefore `TreeSet` considers `"cat"` and `"dog"` equivalent for set membership.

Output:

```text
[cat, elephant]
```

Size:

```text
2
```

### Important

It is possible for:

```text
a.equals(b) == false
```

while:

```text
comparator.compare(a, b) == 0
```

In a `TreeSet`, the latter means the elements are considered equivalent for the set's ordering.

Therefore:

> When using `TreeSet`, the ordering should generally be consistent with `equals()` to avoid surprising behavior.

---

### TreeSet With Custom Objects

Suppose:

```java
class Employee {
    int id;
    String name;
}
```

This will not work as expected unless `Employee` has a natural ordering or you provide a comparator:

```java
TreeSet<Employee> employees =
        new TreeSet<>();
```

### Comparator Approach

```java
TreeSet<Employee> employees =
        new TreeSet<>(
                Comparator.comparingInt(e -> e.id)
        );
```

Now employees are ordered by `id`.

### Important Trap

Suppose:

```text
Employee(10, "Alice")
Employee(10, "Bob")
```

and the comparator only compares `id`.

Then:

```text
compare(Alice, Bob)
        ↓
10 - 10
        ↓
0
```

So the `TreeSet` treats them as equivalent for set membership.

---

### Null Handling

### HashSet

Allows one `null`:

```java
Set<String> set = new HashSet<>();

set.add(null);
```

Valid.

### LinkedHashSet

Also allows one `null`:

```java
Set<String> set = new LinkedHashSet<>();

set.add(null);
```

Valid.

### TreeSet

With natural ordering, `null` is generally not supported:

```java
TreeSet<Integer> set = new TreeSet<>();

set.add(null);
```

This normally results in:

```text
NullPointerException
```

because the tree needs to compare elements.

A custom comparator can define special handling for `null`, but don't complicate a basic interview answer unless asked.

---

### Thread Safety

None of these are inherently thread-safe:

```text
HashSet
LinkedHashSet
TreeSet
```

For concurrent hash-based sets:

```java
Set<Integer> set =
        ConcurrentHashMap.newKeySet();
```

For concurrent sorted sets:

```java
NavigableSet<Integer> set =
        new ConcurrentSkipListSet<>();
```

Remember:

```text
Concurrent + hash-based
    ↓
ConcurrentHashMap.newKeySet()

Concurrent + sorted
    ↓
ConcurrentSkipListSet
```

---

### Memory Trade-off

Conceptually:

```text
HashSet
    ↓
Hash table
    ↓
Lower structural overhead
```

```text
LinkedHashSet
    ↓
Hash table
+
Linked ordering
    ↓
More memory
```

```text
TreeSet
    ↓
Tree nodes
+
tree pointers
    ↓
More structural overhead
```

So don't choose `LinkedHashSet` or `TreeSet` simply because they provide "more features."

Choose them when those features are required.

---

### Performance Notes

```text
                    HashSet     LinkedHashSet     TreeSet

add()               O(1)*       O(1)*             O(log n)

remove()            O(1)*       O(1)*             O(log n)

contains()          O(1)*       O(1)*             O(log n)

ordering            None        Insertion         Sorted
```

`*` means average-case complexity.

Hash-based collections can have collision-related degradation. Modern Java hash-map implementations can treeify sufficiently large collision chains, but the interview-level complexity remains:

```text
HashSet → O(1) average
```

---

### IDE Experiments

Don't just memorize this question. Run these.

### Experiment 1 — Ordering

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {

        Set<Integer> hash =
                new HashSet<>();

        Set<Integer> linked =
                new LinkedHashSet<>();

        Set<Integer> tree =
                new TreeSet<>();

        int[] values = {50, 10, 30, 20, 40};

        for (int x : values) {
            hash.add(x);
            linked.add(x);
            tree.add(x);
        }

        System.out.println("HashSet       : " + hash);
        System.out.println("LinkedHashSet : " + linked);
        System.out.println("TreeSet       : " + tree);
    }
}
```

Observe:

```text
HashSet
→ Don't rely on ordering

LinkedHashSet
→ 50 10 30 20 40

TreeSet
→ 10 20 30 40 50
```

Do not expect a particular `HashSet` order.

---

### Experiment 2 — Duplicate Removal

```java
List<Integer> numbers =
        List.of(5, 2, 5, 1, 2, 3, 1);

Set<Integer> hash =
        new HashSet<>(numbers);

Set<Integer> linked =
        new LinkedHashSet<>(numbers);

Set<Integer> tree =
        new TreeSet<>(numbers);

System.out.println(hash);
System.out.println(linked);
System.out.println(tree);
```

Understand the three behaviors:

```text
HashSet
→ unique

LinkedHashSet
→ unique + original order

TreeSet
→ unique + sorted
```

---

### Experiment 3 — TreeSet Navigation

```java
TreeSet<Integer> set =
        new TreeSet<>(
                List.of(10, 20, 30, 40, 50)
        );

System.out.println(set.lower(30));
System.out.println(set.floor(30));
System.out.println(set.ceiling(30));
System.out.println(set.higher(30));
```

Expected:

```text
20
30
30
40
```

Now try:

```java
System.out.println(set.floor(25));
System.out.println(set.ceiling(25));
```

Expected:

```text
20
30
```

This is worth practicing because `floor()` and `ceiling()` are extremely useful in coding interviews.

---

### Experiment 4 — Custom Comparator

```java
TreeSet<Integer> descending =
        new TreeSet<>(Comparator.reverseOrder());

descending.add(10);
descending.add(30);
descending.add(20);

System.out.println(descending);
```

Output:

```text
[30, 20, 10]
```

This demonstrates that `TreeSet` doesn't necessarily mean ascending order.

It means:

> **The set maintains the ordering defined by its natural ordering or supplied comparator.**

---

### Experiment 5 — TreeSet Comparator Equality

This is the most important advanced experiment.

```java
TreeSet<String> set =
        new TreeSet<>(
                Comparator.comparingInt(String::length)
        );

set.add("cat");
set.add("dog");
set.add("elephant");

System.out.println(set);
System.out.println(set.size());
```

Expected:

```text
[cat, elephant]
2
```

Why?

```text
"cat" → 3
"dog" → 3

compare("cat", "dog")
        ↓
0
        ↓
TreeSet considers them equivalent
```

This is an excellent interview example.

---

### Common Follow-Up Questions

### 1. What is the difference between HashSet and LinkedHashSet?

> Both provide O(1) average `add`, `remove`, and `contains`. `LinkedHashSet` additionally maintains insertion order, at the cost of additional memory for the linked structure.

---

### 2. What is the difference between HashSet and TreeSet?

> `HashSet` is hash-based and provides O(1) average operations without an ordering guarantee. `TreeSet` uses a red-black tree, provides O(log n) operations, and maintains sorted order.

---

### 3. Why is TreeSet O(log n)?

Because it uses a balanced red-black tree whose height remains O(log n).

```text
search → O(log n)
insert → O(log n)
delete → O(log n)
```

---

### 4. Why would you use LinkedHashSet?

When you need:

```text
uniqueness
+
predictable insertion order
```

Classic example:

> Remove duplicates from a list while preserving the order in which elements first appeared.

---

### 5. How does HashSet internally work?

Conceptually:

```text
HashSet
    ↓
HashMap
    ↓
element → dummy value
```

It uses hashing to locate candidate entries and `equals()` to determine equality.

---

### 6. How does TreeSet internally work?

Conceptually:

```text
TreeSet
    ↓
TreeMap
    ↓
Red-black tree
```

The tree is ordered using natural ordering or a supplied `Comparator`.

---

### 7. Does TreeSet use `hashCode()`?

No.

It uses:

```java
Comparable.compareTo()
```

or:

```java
Comparator.compare()
```

---

### 8. Does LinkedHashSet guarantee insertion order?

Yes.

Its iteration order follows insertion/encounter order.

It does **not** sort the elements.

```text
Inserted:

50 10 30

LinkedHashSet:

50 10 30
```

Not:

```text
10 30 50
```

---

### 9. Does HashSet maintain insertion order?

No.

If insertion order is required:

```java
LinkedHashSet
```

---

### 10. Can HashSet contain duplicates?

No.

That's part of the `Set` contract.

---

### 11. Can HashSet contain `null`?

Yes, one `null`.

---

### 12. Can LinkedHashSet contain `null`?

Yes, one `null`.

---

### 13. Can TreeSet contain `null`?

Normally not with natural ordering.

---

### 14. Which Set would you use for sorted unique elements?

```java
TreeSet
```

---

### 15. Which Set would you use for unique elements with insertion order?

```java
LinkedHashSet
```

---

### 16. Which Set would you choose by default?

Usually:

```java
HashSet
```

when you only need uniqueness and don't require ordering.

---

### What NOT to Say

### ❌ "TreeSet is faster because it's sorted."

Wrong.

```text
HashSet  → O(1) average
TreeSet  → O(log n)
```

TreeSet provides additional sorted/navigation capabilities.

---

### ❌ "LinkedHashSet allows duplicates."

Wrong.

All three are Sets:

```text
HashSet       → no duplicates
LinkedHashSet → no duplicates
TreeSet       → no duplicates
```

---

### ❌ "LinkedHashSet stores the elements in a LinkedList."

Too simplistic and potentially misleading.

Better:

> `LinkedHashSet` maintains a linked structure between entries in addition to its hash-based structure.

---

### ❌ "HashSet is randomly ordered."

Better:

> `HashSet` does not guarantee an iteration order, so application code should not depend on the order.

---

### ❌ "TreeSet uses HashMap."

Wrong.

```text
HashSet       → HashMap
LinkedHashSet → LinkedHashMap
TreeSet       → TreeMap
```

---

### ❌ "TreeSet uses equals() to determine duplicates."

Incomplete/wrong as an implementation explanation.

TreeSet uses:

```text
compareTo()
```

or:

```text
Comparator.compare()
```

If the comparison returns `0`, the elements are considered equivalent for set membership.

---

### Interview Decision Tree

```text
Need uniqueness?
       │
       ├── No
       │
       └── Yes
            │
            ▼
      Need ordering?
            │
       ┌────┴────┐
       │         │
      No        Yes
       │         │
       ▼         ▼
   HashSet    What type?
                 │
           ┌─────┴─────┐
           │           │
       Insertion     Sorted /
         order       navigation
           │           │
           ▼           ▼
    LinkedHashSet    TreeSet
```

---

### The Comparison You Should Memorize

```text
HashSet
    ↓
HashMap
    ↓
Hashing
    ↓
O(1) average
    ↓
No guaranteed order
```

```text
LinkedHashSet
    ↓
LinkedHashMap
    ↓
Hashing + linked ordering
    ↓
O(1) average
    ↓
Insertion order
```

```text
TreeSet
    ↓
TreeMap
    ↓
Red-black tree
    ↓
O(log n)
    ↓
Sorted order
    ↓
floor / ceiling / lower / higher
```

---

### Interview-Ready Final Answer

If the interviewer asks:

> **"HashSet vs LinkedHashSet vs TreeSet?"**

Say:

> **"`HashSet`, `LinkedHashSet`, and `TreeSet` all enforce uniqueness, but they optimize for different requirements. `HashSet` is backed by a `HashMap` and gives O(1) average `add`, `remove`, and `contains`, with no ordering guarantee. `LinkedHashSet` adds a linked structure to maintain insertion order while retaining O(1) average operations. `TreeSet` is backed by a `TreeMap` using a red-black tree, so operations are O(log n), but elements remain sorted and I get navigation methods such as `floor`, `ceiling`, `lower`, and `higher`. So I'd choose HashSet for uniqueness, LinkedHashSet for uniqueness plus insertion order, and TreeSet for uniqueness plus sorted or range-based operations."**

---

### 10-Second Revision

```text
HashSet
→ HashMap
→ O(1) average
→ no guaranteed order
→ hashCode() + equals()


LinkedHashSet
→ LinkedHashMap
→ O(1) average
→ insertion order
→ hash-based + linked structure


TreeSet
→ TreeMap
→ Red-black tree
→ O(log n)
→ sorted order
→ compareTo() / Comparator
→ floor / ceiling / lower / higher
```

### One-Line Memory Trick

> **HashSet = Fast, LinkedHashSet = Fast + insertion order, TreeSet = Sorted + navigation.**

### Most Important Interview Trap

```text
HashSet
    → hashCode() + equals()

TreeSet
    → compareTo() / Comparator
```

And remember:

```text
HashSet       → no guaranteed order
LinkedHashSet → insertion order
TreeSet       → sorted order
```

> **All three enforce uniqueness.**

# Q17 · Comparable vs Comparator

### Question

**What's the difference between `Comparable` and `Comparator`? When would you use each?**

### 30-Second Interview Answer

`Comparable` is implemented **by the class itself** and defines its **natural/default ordering** using `compareTo()`.

`Comparator` is a **separate/external comparison strategy** that defines an ordering using `compare()`. It is useful when I don't own the class, or when I need **multiple different orderings** for the same class.

For example, `Student` could implement `Comparable<Student>` to define its natural ordering by age, while separate `Comparator<Student>` objects could sort students by name, marks, or age descending.

---

### Comparable

### What is Comparable?

`Comparable<T>` is an interface used when a class wants to define its **natural ordering**.

```java
public interface Comparable<T> {
    int compareTo(T other);
}
```

The class itself implements it:

```java
class Student implements Comparable<Student> {

    int age;

    @Override
    public int compareTo(Student other) {
        return Integer.compare(this.age, other.age);
    }
}
```

Here, age becomes the natural ordering of `Student`.

### `compareTo()` return value

`compareTo()` returns an `int`, not a `boolean`.

```text
negative → this comes before other
0        → this and other are equivalent according to the ordering
positive → this comes after other
```

Example:

```text
Student A → age = 20
Student B → age = 25

A.compareTo(B) → negative
B.compareTo(A) → positive
A.compareTo(A) → 0
```

The exact negative/positive number is not important. The **sign** is what matters.

---

### Comparator

### What is Comparator?

`Comparator<T>` is an external strategy for comparing two objects.

```java
public interface Comparator<T> {
    int compare(T a, T b);
}
```

Example:

```java
Comparator<Student> byAge = new Comparator<Student>() {
    @Override
    public int compare(Student a, Student b) {
        return Integer.compare(a.age, b.age);
    }
};
```

The comparison logic does not have to be inside `Student`.

### Modern Java

Java 8+ provides convenient factory and chaining methods:

```java
Comparator<Student> byAge =
        Comparator.comparingInt(s -> s.age);
```

---

### Comparable vs Comparator

| Feature             | Comparable                         | Comparator                      |
| ------------------- | ---------------------------------- | ------------------------------- |
| Package             | `java.lang`                        | `java.util`                     |
| Method              | `compareTo(T other)`               | `compare(T a, T b)`             |
| Defined by          | The class itself                   | External object                 |
| Purpose             | Natural/default ordering           | Alternative/custom ordering     |
| Number of orderings | One natural ordering               | Many possible orderings         |
| Modifies class?     | Yes                                | No                              |
| Useful when         | Class has an obvious natural order | Multiple orderings are required |
| Example             | Student by age                     | Student by name, marks, etc.    |

### Mental Model

```text
Comparable
    ↓
"What is the natural/default ordering of this object?"
    ↓
Defined by the class
    ↓
compareTo(other)
```

```text
Comparator
    ↓
"How do I want to order these objects for this use case?"
    ↓
Defined externally
    ↓
compare(a, b)
```

---

### When should I use Comparable?

Use `Comparable` when the class has a clear **natural/default ordering**.

For example:

```java
class Student implements Comparable<Student> {

    int age;

    @Override
    public int compareTo(Student other) {
        return Integer.compare(this.age, other.age);
    }
}
```

Now:

```java
Collections.sort(students);
```

uses:

```java
Student.compareTo()
```

The class itself owns the definition of its natural ordering.

---

### When should I use Comparator?

Use `Comparator` when:

### 1. You need multiple orderings

A `Student` might need to be sorted by:

* age
* name
* marks
* age descending
* name + marks

You don't want to change the `Student` class every time.

```java
Comparator<Student> byName =
        Comparator.comparing(s -> s.name);

Comparator<Student> byMarks =
        Comparator.comparingInt(s -> s.marks);

Comparator<Student> byAgeDescending =
        Comparator.comparingInt((Student s) -> s.age)
                  .reversed();
```

### 2. You don't own the class

For example, you cannot modify a third-party class to make it implement `Comparable`.

You can still define:

```java
Comparator<SomeThirdPartyClass> comparator = ...;
```

### 3. The ordering is specific to a particular operation

You may want one particular sort to use name while another uses marks.

```java
students.sort(byName);

students.sort(byMarks);
```

---

### Collections.sort()

If no Comparator is supplied:

```java
Collections.sort(students);
```

Java uses the elements' **natural ordering**:

```text
Collections.sort(students)
            ↓
Student.compareTo()
```

If a Comparator is supplied:

```java
Collections.sort(students, comparator);
```

Java uses:

```text
comparator.compare(student1, student2)
```

The supplied Comparator determines the ordering for that operation.

### Important

The Comparator takes precedence for that particular sort.

Even if:

```java
class Student implements Comparable<Student>
```

defines age as the natural ordering, this:

```java
Collections.sort(
    students,
    Comparator.comparing(s -> s.name)
);
```

sorts by name instead.

---

### One Comparable vs Many Comparators

A class can implement `Comparable` and also have many `Comparator` objects.

```java
class Student implements Comparable<Student> {

    @Override
    public int compareTo(Student other) {
        return Integer.compare(this.age, other.age);
    }
}
```

Natural ordering:

```java
Collections.sort(students);
```

uses age.

Alternative orderings:

```java
Comparator<Student> byName =
        Comparator.comparing(s -> s.name);

Comparator<Student> byMarks =
        Comparator.comparingInt(s -> s.marks);

Comparator<Student> byAgeDescending =
        Comparator.comparingInt((Student s) -> s.age)
                  .reversed();
```

### Mental model

```text
                    Student
                       │
             ┌─────────┴─────────┐
             │                   │
        Comparable          Comparators
             │                   │
       ONE natural          MANY strategies
        ordering                 │
             │              ┌────┼────┐
        compareTo()       name marks age...
```

---

### `compareTo() == 0` Does NOT Necessarily Mean `equals() == true`

This is a very important interview concept.

Suppose:

```java
class Student implements Comparable<Student> {

    int age;
    String name;

    @Override
    public int compareTo(Student other) {
        return Integer.compare(this.age, other.age);
    }
}
```

Consider:

```text
Student A → age = 20, name = "Alice"
Student B → age = 20, name = "Bob"
```

Then:

```java
A.compareTo(B) == 0
```

because both have age 20.

But they can still be different objects:

```java
A != B
```

and `equals()` could return:

```java
A.equals(B) == false
```

Therefore:

> `compareTo() == 0` means the objects are equivalent **according to that ordering**. It does not necessarily mean that they are the same object or that `equals()` returns `true`.

---

### TreeSet / TreeMap Trap

`TreeSet` and `TreeMap` use their ordering mechanism to determine element/key equivalence.

### TreeSet with Comparable

```java
TreeSet<Student> students = new TreeSet<>();

students.add(new Student(20, "Alice"));
students.add(new Student(20, "Bob"));
```

If `compareTo()` compares only age:

```text
Alice.compareTo(Bob)
        ↓
      20 vs 20
        ↓
        0
```

The `TreeSet` considers the second student equivalent for set purposes.

Therefore:

```java
students.size(); // 1
```

even though Alice and Bob are different objects.

### Important interview statement

> `TreeSet` determines uniqueness using its ordering mechanism (`compareTo()` or `Comparator.compare()`), not necessarily `equals()`.

The same principle applies to keys in `TreeMap`.

---

### Comparator and TreeSet

A class does **not** need to implement `Comparable` if the `TreeSet` receives a Comparator.

```java
class Student {
    int age;
    String name;
}
```

This is valid:

```java
TreeSet<Student> students =
    new TreeSet<>(
        Comparator.comparingInt(s -> s.age)
    );
```

The TreeSet now knows how to order Students through the supplied Comparator.

Conceptually:

```text
Student implements Comparable
        ↓
TreeSet can use compareTo()
```

or:

```text
Student doesn't implement Comparable
        ↓
TreeSet receives Comparator
        ↓
TreeSet uses Comparator.compare()
```

Without either:

```java
TreeSet<Student> students = new TreeSet<>();
```

Java has no ordering strategy for `Student`, so inserting a Student can result in a runtime failure.

---

### Comparator Chaining

Java provides methods for creating complex orderings.

Suppose:

```java
class Student {
    String name;
    int age;
    int marks;
}
```

Requirement:

1. Name ascending
2. If names are equal → marks descending
3. If marks are equal → age ascending

Use:

```java
Comparator<Student> comparator =
    Comparator.comparing((Student s) -> s.name)
        .thenComparing(
            Comparator.comparingInt((Student s) -> s.marks)
                      .reversed()
        )
        .thenComparingInt(s -> s.age);
```

### How the comparison works

```text
Compare names
    │
    ├── different → name ascending
    │
    └── same
         ↓
      Compare marks
         │
         ├── different → marks descending
         │
         └── same
              ↓
           Compare age
              ↓
           age ascending
```

---

### Important `reversed()` Trap

This:

```java
A.thenComparing(B).reversed()
```

reverses the **entire comparator built so far**.

Whereas:

```java
A.thenComparing(B.reversed())
```

keeps `A` unchanged and reverses only `B`.

Example:

```java
Comparator<Student> comparator =
    Comparator.comparing((Student s) -> s.name)
        .thenComparing(
            Comparator.comparingInt((Student s) -> s.marks)
                      .reversed()
        );
```

Here:

```text
name  → ascending
marks → descending
```

Only marks is reversed.

---

### Comparator Return Contract

Both `compareTo()` and `Comparator.compare()` follow the same basic sign convention.

```text
negative → first object comes before second
0        → equivalent according to ordering
positive → first object comes after second
```

For:

```java
Comparator<Student> byAge =
    Comparator.comparingInt(s -> s.age);
```

```text
A = 20, B = 25
compare(A, B) → negative

A = 25, B = 20
compare(A, B) → positive

A = 20, B = 20
compare(A, B) → 0
```

The exact magnitude is generally irrelevant.

---

### Don't Compare Using Subtraction

Avoid:

```java
return this.age - other.age;
```

Prefer:

```java
return Integer.compare(this.age, other.age);
```

### Why?

Subtraction can overflow.

For example, with values near the limits of `int`, the subtraction can produce an incorrect sign.

`Integer.compare()` safely expresses the intended comparison.

### Interview answer

> I avoid subtraction because integer overflow can produce an incorrect comparison result. `Integer.compare(a, b)` safely returns a negative value, zero, or a positive value.

---

### Anonymous Comparator vs Modern Comparator

### Traditional implementation

```java
Comparator<Student> byAge = new Comparator<Student>() {
    @Override
    public int compare(Student a, Student b) {
        return Integer.compare(a.age, b.age);
    }
};
```

### Modern Java

```java
Comparator<Student> byAge =
        Comparator.comparingInt(s -> s.age);
```

Modern Java also supports:

```java
Comparator<Student> byName =
        Comparator.comparing(s -> s.name);
```

```java
Comparator<Student> byAgeDescending =
        Comparator.comparingInt((Student s) -> s.age)
                  .reversed();
```

---

### Common Interview Traps

### Trap 1 — `compareTo()` returns boolean

❌ Wrong:

```java
boolean compareTo(...)
```

✅ Correct:

```java
int compareTo(...)
```

---

### Trap 2 — Comparable supports multiple natural orderings

A class has **one natural ordering** through its single `compareTo()` implementation.

For multiple orderings, use multiple Comparators.

---

### Trap 3 — Comparator must be inside the class

❌ Not required.

Comparator is an external strategy.

---

### Trap 4 — `compareTo() == 0` means same object

❌ Wrong.

```java
a.compareTo(b) == 0
```

only means they are equivalent according to the ordering.

---

### Trap 5 — TreeSet always uses `equals()`

❌ Wrong.

`TreeSet` uses:

```text
Comparable.compareTo()
```

or:

```text
Comparator.compare()
```

to determine ordering/equivalence.

---

### Trap 6 — `reversed()` only reverses the last field

Not necessarily.

```java
A.thenComparing(B).reversed()
```

reverses the entire comparator constructed so far.

---

### Trap 7 — Subtract values to compare them

Avoid:

```java
return a.age - b.age;
```

Prefer:

```java
return Integer.compare(a.age, b.age);
```

---

### IDE Experiments

These are worth actually running because they make the behavior stick.

### Experiment 1 — Comparable natural ordering

```java
import java.util.*;

class Student implements Comparable<Student> {
    int age;
    String name;

    Student(int age, String name) {
        this.age = age;
        this.name = name;
    }

    @Override
    public int compareTo(Student other) {
        return Integer.compare(this.age, other.age);
    }

    @Override
    public String toString() {
        return name + " - " + age;
    }
}

public class Main {
    public static void main(String[] args) {

        List<Student> students = new ArrayList<>();

        students.add(new Student(25, "Alice"));
        students.add(new Student(20, "Bob"));
        students.add(new Student(22, "Charlie"));

        Collections.sort(students);

        System.out.println(students);
    }
}
```

Observe that `Collections.sort(students)` uses `compareTo()`.

---

### Experiment 2 — Comparator overrides natural ordering

Keep the same `Student` class.

```java
students.sort(
    Comparator.comparing(s -> s.name)
);
```

Now the list is sorted by name instead of age.

This demonstrates:

```text
Comparable → default ordering
Comparator → ordering for this particular operation
```

---

### Experiment 3 — TreeSet comparison trap

```java
TreeSet<Student> students = new TreeSet<>();

students.add(new Student(20, "Alice"));
students.add(new Student(20, "Bob"));
students.add(new Student(25, "Charlie"));

System.out.println(students);
System.out.println(students.size());
```

Expected size:

```text
2
```

Why?

```text
Alice(20)
Bob(20)      → compareTo() == 0 → treated as equivalent

Charlie(25)
```

---

### Experiment 4 — TreeSet with Comparator

```java
TreeSet<Student> students =
    new TreeSet<>(
        Comparator.comparing(s -> s.name)
    );

students.add(new Student(20, "Alice"));
students.add(new Student(20, "Bob"));
students.add(new Student(25, "Charlie"));

System.out.println(students);
```

Now the TreeSet's ordering is based on `name`.

---

### Experiment 5 — Comparator chaining

```java
Comparator<Student> comparator =
    Comparator.comparing((Student s) -> s.name)
        .thenComparing(
            Comparator.comparingInt((Student s) -> s.age)
                      .reversed()
        );

students.sort(comparator);
```

Create students with the same name but different ages and observe the secondary ordering.

---

### Quick Revision

```text
Comparable
    → implemented by the class
    → compareTo(T other)
    → one natural/default ordering

Comparator
    → external object
    → compare(T a, T b)
    → multiple/custom orderings

Collections.sort(list)
    → Comparable / compareTo()

Collections.sort(list, comparator)
    → Comparator / compare()

TreeSet / TreeMap
    → use compareTo() or Comparator
    → compare == 0 means equivalent for sorted collection purposes

Comparator.comparing(...)
    → convenient Java 8+ comparator creation

thenComparing(...)
    → secondary/tertiary ordering

reversed()
    → reverses the comparator it is called on

Integer.compare(a, b)
    → preferred over a - b
    → avoids integer overflow
```

### One-Line Memory Trick

> **Comparable = "I know my natural order."**
> **Comparator = "You tell me how you want me ordered."**


# Q18 · Queue vs Deque vs Stack

### Exact question from the source

**When would you use a Deque vs a Queue vs a Stack in Java? Are Stack and Vector still relevant?**

**Asked at:** Common in mid-level rounds
**Difficulty:** Medium
**Topic:** Collections

### 30-second interview answer

`Stack` and `Vector` are legacy Java classes. `Stack` extends `Vector` and has the older synchronized design.

For **LIFO / stack semantics**, prefer:

```java
Deque<Integer> stack = new ArrayDeque<>();
```

and use `push()`, `pop()`, and `peek()`.

For **FIFO / queue semantics**, use the `Queue` interface, commonly with:

```java
Queue<Integer> queue = new ArrayDeque<>();
```

For **concurrent producer-consumer systems**, use `BlockingQueue` implementations such as `ArrayBlockingQueue` or `LinkedBlockingQueue`.

For **non-blocking concurrent queues**, `ConcurrentLinkedQueue` is an option.

---

### Queue vs Deque vs Stack

### Queue

A `Queue` normally represents **FIFO** behavior:

```text
FIRST → 10 → 20 → 30 ← LAST

poll()
 ↓
10
```

Typical methods:

```java
offer()
poll()
peek()
```

Example:

```java
Queue<Integer> queue = new ArrayDeque<>();

queue.offer(10);
queue.offer(20);
queue.offer(30);

queue.poll(); // 10
```

Use a queue when elements should generally be processed in the order they were inserted.

Examples:

* BFS
* Work queues
* Request processing
* Task scheduling

---

### Deque

`Deque` means **double-ended queue**.

It supports insertion and removal from **both ends**:

```text
FIRST → [10] [20] [30] ← LAST
```

Common methods:

```java
addFirst()
addLast()

removeFirst()
removeLast()

peekFirst()
peekLast()
```

Example:

```java
Deque<Integer> deque = new ArrayDeque<>();

deque.addFirst(10);
deque.addLast(20);
deque.addLast(30);

deque.removeFirst(); // 10
deque.removeLast();  // 30
```

A `Deque` can also provide both **queue semantics** and **stack semantics**.

---

### Using Deque as a Stack

Modern Java code should generally prefer `Deque` over the legacy `Stack` class.

```java
Deque<Integer> stack = new ArrayDeque<>();

stack.push(10);
stack.push(20);
stack.push(30);

stack.pop();   // 30
stack.peek();  // 20
```

The behavior is LIFO:

```text
TOP
 ↓
30
20
10
```

Remember:

```text
push() → insert at stack top
pop()  → remove from stack top
peek() → inspect stack top
```

### Why is this LIFO?

The last element pushed is the first element popped:

```text
push(10)
push(20)
push(30)

pop() → 30
pop() → 20
pop() → 10
```

---

### Why Can ArrayDeque Be Both Queue and Stack?

The hierarchy is important:

```text
Queue
  ↑
Deque
  ↑
ArrayDeque implements Deque
```

More precisely:

```text
Deque extends Queue
ArrayDeque implements Deque
```

Therefore:

```java
Queue<Integer> q = new ArrayDeque<>();
```

can be used with queue operations:

```java
q.offer(10);
q.offer(20);
q.poll(); // 10
```

While:

```java
Deque<Integer> stack = new ArrayDeque<>();
```

can be used with stack operations:

```java
stack.push(10);
stack.push(20);
stack.pop(); // 20
```

The same underlying deque data structure can provide different semantics depending on the operations you choose.

### Important interview phrase

> "`ArrayDeque` implements `Deque`, and `Deque` extends `Queue`. Therefore an `ArrayDeque` can be used as either a FIFO queue or a LIFO stack."

---

### Queue API — add vs offer, remove vs poll, element vs peek

This is a common interview follow-up.

| Operation   | Successful behavior      | Failure / empty behavior |
| ----------- | ------------------------ | ------------------------ |
| `add(e)`    | Adds element             | Throws exception         |
| `offer(e)`  | Adds element             | Returns `false`          |
| `remove()`  | Removes and returns head | Throws exception         |
| `poll()`    | Removes and returns head | Returns `null`           |
| `element()` | Returns head             | Throws exception         |
| `peek()`    | Returns head             | Returns `null`           |

The easiest way to memorize it:

```text
                 Exception       Special value
                 ─────────        ─────────────
Insert           add()            offer()
Remove           remove()         poll()
Inspect          element()        peek()
```

### Example

```java
Queue<Integer> queue = new ArrayDeque<>();

queue.add(10);
queue.offer(20);

queue.remove();  // removes 10
queue.poll();    // removes 20
```

If the queue is empty:

```java
queue.remove();  // exception
queue.poll();    // null

queue.element(); // exception
queue.peek();    // null
```

---

### Why Does ArrayDeque Reject null?

```java
Queue<Integer> queue = new ArrayDeque<>();

queue.add(null); // NullPointerException
```

This is important because:

```java
queue.poll();
```

returns `null` when the queue is empty.

If `null` elements were allowed, we couldn't distinguish:

```text
poll() == null

Was the queue empty?
        OR
Was null actually stored?
```

By prohibiting `null`, `ArrayDeque` can safely use `null` as the "nothing available" result for methods such as `poll()` and `peek()`.

---

### ArrayDeque Internal Implementation

`ArrayDeque` is backed by a **resizable circular array**.

Conceptually:

```text
[ _ ][ _ ][ A ][ B ][ C ][ _ ]
        ↑           ↑
       head        tail
```

The important idea is that the elements don't have to be physically shifted whenever we remove from an end.

Remove `A`:

```text
[ _ ][ _ ][ _ ][ B ][ C ][ _ ]
              ↑       ↑
             head    tail
```

Add `D`:

```text
[ _ ][ _ ][ _ ][ B ][ C ][ D ]
              ↑           ↑
             head        tail
```

The logical boundaries move.

### Circular behavior

When the head or tail reaches the physical end of the array, it can wrap around to the beginning.

Conceptually:

```text
[ D ][ E ][ _ ][ _ ][ A ][ B ][ C ]
  ↑                       ↑
 tail                    head
```

This avoids repeatedly shifting every element.

---

### Why ArrayDeque Is Generally Faster Than LinkedList

Both can support deque operations at the ends in O(1), but their implementations differ.

### ArrayDeque

```text
Resizable circular array
        ↓
No per-element Node object
        ↓
Better memory locality
        ↓
Less pointer/reference chasing
```

### LinkedList

```text
Node ↔ Node ↔ Node ↔ Node
 ↓       ↓       ↓
data    data    data
```

Every element is represented by a linked node.

That introduces:

* Node allocation
* Additional references
* Pointer chasing
* Worse CPU cache locality

Therefore, `ArrayDeque` generally performs better for typical queue/stack/deque operations.

### Interview-ready answer

> "`ArrayDeque` is generally preferred over `LinkedList` because it uses a resizable circular array instead of allocating a node for every element. This reduces memory overhead and improves cache locality, so end operations generally have better performance in practice."

---

### Important: Array-Backed Does Not Mean Random Access

A common misconception:

> "ArrayDeque uses an array, so accessing the 5th element should be O(1)."

Not true.

`ArrayDeque` does **not** expose indexed access like:

```java
deque.get(5);
```

Unlike:

```java
ArrayList
```

which supports:

```java
list.get(5); // O(1)
```

For `ArrayDeque`, if you need to locate an arbitrary element, you generally have to traverse/iterate:

```text
ArrayDeque

head → A → B → C → D → E
             ↑
          traverse
```

So arbitrary positional access is not its purpose.

### Key interview phrase

> **Array-backed does not automatically mean random-access.**

`ArrayDeque` is optimized for **operations at the two ends**.

---

### ArrayDeque Complexity

Typical end operations:

| Operation       |     Complexity |
| --------------- | -------------: |
| `addFirst()`    | Amortized O(1) |
| `addLast()`     | Amortized O(1) |
| `removeFirst()` |           O(1) |
| `removeLast()`  |           O(1) |
| `peekFirst()`   |           O(1) |
| `peekLast()`    |           O(1) |

### Why amortized O(1)?

Most insertions are constant time:

```text
addLast()
   ↓
put element
move tail
   ↓
O(1)
```

Occasionally, the backing array must grow:

```text
old array
   ↓
allocate larger array
   ↓
copy elements
   ↓
O(n)
```

But resizing happens only occasionally, so insertion remains **amortized O(1)**.

### Interview trap

Don't say:

> "`addLast()` is always O(1)."

Prefer:

> "`addLast()` is amortized O(1); an individual operation can take O(n) if the backing array needs to resize."

---

### Stack vs Vector

`Stack` is a legacy Java class.

The relationship is:

```text
Stack extends Vector
```

Both originate from the early Java collections APIs.

The source describes them as legacy/synchronized and recommends `Deque` for modern stack semantics.

Instead of:

```java
Stack<Integer> stack = new Stack<>();
```

prefer:

```java
Deque<Integer> stack = new ArrayDeque<>();
```

Then:

```java
stack.push(10);
stack.push(20);

stack.pop();  // 20
stack.peek(); // 10
```

### Interview-ready answer

> "`Stack` is a legacy class that extends `Vector`. For modern stack semantics, I would use the `Deque` interface with an `ArrayDeque` implementation and use `push`, `pop`, and `peek`."

---

### BlockingQueue

`BlockingQueue` is useful for **producer-consumer systems**.

Conceptually:

```text
Producer Threads
       │
       ▼
┌─────────────────┐
│ BlockingQueue   │
└─────────────────┘
       │
       ▼
Consumer Threads
```

The important behavior is **blocking based on queue state**.

If the queue is full:

```text
producer
   ↓
put()
   ↓
WAIT
```

If the queue is empty:

```text
consumer
   ↓
take()
   ↓
WAIT
```

This allows producers and consumers to coordinate without manually implementing the waiting mechanism.

---

### BlockingQueue — put vs offer

For a bounded queue that is currently full:

```java
blockingQueue.put(10);
```

will **block until space becomes available**.

Whereas:

```java
blockingQueue.offer(10);
```

does **not wait** and returns:

```java
false
```

if the queue cannot accept the element.

There is also a timed version:

```java
blockingQueue.offer(
    10,
    5,
    TimeUnit.SECONDS
);
```

It waits up to five seconds for space and returns `false` if space does not become available.

### Remember

```text
Queue full:

put()              → WAIT
offer()             → false
offer(e, timeout)   → WAIT up to timeout
```

---

### BlockingQueue — take vs poll

For an empty queue:

```java
blockingQueue.take();
```

blocks until an element becomes available.

```java
blockingQueue.poll();
```

immediately returns `null`.

Timed:

```java
blockingQueue.poll(5, TimeUnit.SECONDS);
```

waits for up to five seconds.

### Remember

```text
Queue empty:

take()              → WAIT
poll()              → null
poll(timeout)       → WAIT up to timeout
```

---

### Backpressure

One of the most important real-world reasons to use a **bounded** `BlockingQueue` is **backpressure**.

Suppose:

```text
100 Producers
       ↓
Queue(capacity = 1000)
       ↓
20 Consumers
```

If producers generate work faster than consumers process it, the queue eventually fills.

```text
Queue fills
    ↓
Queue reaches capacity
    ↓
producer calls put()
    ↓
producer waits
    ↓
consumer removes work
    ↓
space becomes available
    ↓
producer continues
```

This prevents work from accumulating without bound.

### Why bounded instead of unbounded?

An unbounded queue can continuously accumulate work:

```text
Producers >>> Consumers

Queue
 ↓
 ↓
 ↓
 ↓
keeps growing
 ↓
memory pressure
 ↓
potential OOM
```

A bounded queue provides **backpressure**.

### Interview-ready answer

> "I would use a bounded `BlockingQueue` when producers can generate work faster than consumers can process it. Once the queue reaches capacity, producers are forced to wait, providing backpressure and preventing unbounded accumulation of work."

---

### ArrayBlockingQueue vs LinkedBlockingQueue

The source mentions both as `BlockingQueue` implementations.

### ArrayBlockingQueue

```java
BlockingQueue<Integer> q =
    new ArrayBlockingQueue<>(100);
```

* Array-backed
* Bounded
* Capacity specified at construction

### LinkedBlockingQueue

```java
BlockingQueue<Integer> q =
    new LinkedBlockingQueue<>(100);
```

* Linked-node-based
* Can be bounded by specifying capacity
* Implements blocking producer-consumer behavior

Important:

> `LinkedBlockingQueue` is not simply a `LinkedList`; it is a dedicated `BlockingQueue` implementation using linked nodes and concurrency controls.

---

### ConcurrentLinkedQueue

For concurrent access where you don't need blocking behavior:

```java
Queue<Integer> queue =
    new ConcurrentLinkedQueue<>();
```

It is designed for **thread-safe, non-blocking concurrent queue operations**.

Unlike a bounded `BlockingQueue`, it does not provide producer-consumer blocking/backpressure.

Conceptually:

```text
BlockingQueue

full  → producer may BLOCK
empty → consumer may BLOCK


ConcurrentLinkedQueue

empty → poll() returns null
no blocking
no bounded-capacity backpressure
```

### Comparison

|                     | `BlockingQueue`   | `ConcurrentLinkedQueue`       |
| ------------------- | ----------------- | ----------------------------- |
| Thread-safe         | Yes               | Yes                           |
| Blocking operations | Yes               | No                            |
| Bounded option      | Yes               | No                            |
| Backpressure        | Yes               | No                            |
| Empty `poll()`      | `null`            | `null`                        |
| Typical use         | Producer-consumer | Concurrent non-blocking queue |

---

### Concurrent Queue Trap: Check-Then-Act

Avoid:

```java
if (!queue.isEmpty()) {
    Integer value = queue.poll();
}
```

when multiple threads are consuming.

Why?

Because another thread can remove the element between `isEmpty()` and `poll()`.

```text
Queue: [10]

Thread A                 Thread B

isEmpty() → false
                         isEmpty() → false

                         poll() → 10

poll() → null
```

Therefore, the result of `isEmpty()` is not guaranteed to remain true/false by the time the next operation occurs.

Prefer:

```java
Integer value = queue.poll();

if (value != null) {
    // successfully consumed an element
}
```

For a `BlockingQueue`, if you actually want to wait for work:

```java
Integer value = blockingQueue.take();
```

### General concurrency principle

> **Avoid separate check-then-act operations when the check and action need to be atomic.**

---

### Choosing the Right Queue

### A. Single-threaded BFS

```java
Queue<Integer> queue = new ArrayDeque<>();
```

Why?

* FIFO
* No concurrency required
* Efficient end operations

### B. Producer-consumer + bounded capacity

```java
BlockingQueue<Integer> queue =
    new ArrayBlockingQueue<>(100);
```

Why?

* Thread-safe
* Blocking
* Bounded
* Backpressure

### C. Multiple threads + non-blocking queue

```java
Queue<Integer> queue =
    new ConcurrentLinkedQueue<>();
```

Why?

* Thread-safe
* Non-blocking
* Designed for concurrent access
* No blocking/backpressure requirement

---

### Common Interview Traps

### Trap 1 — Using Stack for modern LIFO

❌

```java
Stack<Integer> stack = new Stack<>();
```

Prefer:

```java
Deque<Integer> stack = new ArrayDeque<>();
```

---

### Trap 2 — Saying Queue always means FIFO

`Queue` is an abstraction; implementations can have different ordering behavior.

For example:

```java
PriorityQueue<Integer>
```

does **not** behave as a normal FIFO queue.

It is heap-based and orders elements according to their ordering/comparator.

---

### Trap 3 — Saying LinkedList is always the best Deque

Both:

```java
Deque<Integer> a = new ArrayDeque<>();
Deque<Integer> b = new LinkedList<>();
```

support deque operations.

But `ArrayDeque` is generally preferred for typical stack/queue usage because of better cache locality and lower per-element overhead.

---

### Trap 4 — Saying ArrayDeque provides indexed access

It doesn't behave like `ArrayList`.

```text
ArrayList → random access
ArrayDeque → efficient access at ends
```

---

### Trap 5 — Saying BlockingQueue locks the queue while processing

Incorrect mental model.

Blocking occurs because of **queue state**:

```text
full  → put() can wait
empty → take() can wait
```

It does not mean the queue is blocked while a consumer is processing an element.

---

### Trap 6 — Check then act

Avoid:

```java
if (!queue.isEmpty()) {
    queue.poll();
}
```

in concurrent consumer code.

Prefer:

```java
Integer value = queue.poll();
```

and inspect the result.

---

### Quick Revision Cheat Sheet

```text
┌─────────────────────────────────────────────────────┐
│ Queue                                               │
│ FIFO                                                │
│ offer / poll / peek                                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Deque                                               │
│ Double-ended queue                                  │
│ addFirst / addLast                                 │
│ removeFirst / removeLast                           │
│ Can implement Queue + Stack semantics              │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Stack                                               │
│ LIFO                                                │
│ Legacy                                              │
│ Prefer Deque + ArrayDeque                           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ ArrayDeque                                          │
│ Resizable circular array                            │
│ Efficient at both ends                              │
│ Amortized O(1) insertion at ends                    │
│ No null elements                                    │
│ Good default for Stack/Queue                        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ BlockingQueue                                       │
│ Thread-safe producer-consumer                      │
│ put()   → waits if full                            │
│ take()  → waits if empty                           │
│ Bounded queues → backpressure                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ ConcurrentLinkedQueue                               │
│ Thread-safe                                         │
│ Non-blocking                                        │
│ No backpressure                                     │
└─────────────────────────────────────────────────────┘
```

---

### Interview Decision Tree

```text
Need a queue/deque in a single-threaded context?
                │
                ▼
            ArrayDeque
                │
                ├── FIFO → Queue interface
                │
                └── LIFO → Deque interface


Need concurrent producer-consumer coordination?
                │
                ▼
          BlockingQueue
                │
                ├── Need fixed capacity?
                │       ↓
                │  ArrayBlockingQueue
                │
                └── Linked-node based?
                        ↓
                  LinkedBlockingQueue


Need concurrent + non-blocking?
                │
                ▼
       ConcurrentLinkedQueue
```

---

### IDE Experiments

These are worth running yourself because they make the API behavior much easier to retain.

### Experiment 1 — Queue vs Stack

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {

        // Queue → FIFO
        Queue<Integer> queue = new ArrayDeque<>();

        queue.offer(10);
        queue.offer(20);
        queue.offer(30);

        System.out.println(queue.poll()); // 10
        System.out.println(queue.peek()); // 20


        // Stack → LIFO
        Deque<Integer> stack = new ArrayDeque<>();

        stack.push(10);
        stack.push(20);
        stack.push(30);

        System.out.println(stack.pop());  // 30
        System.out.println(stack.peek()); // 20
    }
}
```

---

### Experiment 2 — All six Queue methods

```java
Queue<Integer> queue = new ArrayDeque<>();

System.out.println(queue.poll());   // null
System.out.println(queue.peek());   // null

// System.out.println(queue.remove());  // NoSuchElementException
// System.out.println(queue.element()); // NoSuchElementException

System.out.println(queue.offer(10)); // true
System.out.println(queue.add(20));   // true

System.out.println(queue.poll());    // 10
System.out.println(queue.remove());  // 20
```

---

### Experiment 3 — ArrayDeque rejects null

```java
Deque<Integer> deque = new ArrayDeque<>();

deque.add(10);

// Throws NullPointerException
deque.add(null);
```

Then ask yourself:

> Why does Java prohibit null here?

Because:

```java
deque.poll()
```

needs `null` to unambiguously mean:

```text
"No element available"
```

---

### Experiment 4 — BlockingQueue

```java
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args)
            throws InterruptedException {

        BlockingQueue<Integer> queue =
                new ArrayBlockingQueue<>(2);

        queue.put(10);
        queue.put(20);

        System.out.println(queue.poll()); // 10
        System.out.println(queue.poll()); // 20
        System.out.println(queue.poll()); // null
    }
}
```

To actually observe blocking, fill the queue and call `put()` from one thread while another thread eventually removes an element.

---

### Experiment 5 — ConcurrentLinkedQueue

```java
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) {

        Queue<Integer> queue =
                new ConcurrentLinkedQueue<>();

        queue.offer(10);
        queue.offer(20);
        queue.offer(30);

        System.out.println(queue.poll()); // 10
        System.out.println(queue.poll()); // 20
        System.out.println(queue.poll()); // 30
        System.out.println(queue.poll()); // null
    }
}
```

---

### Final Mental Model

If you remember only this:

```text
FIFO?
 ↓
Queue
 ↓
ArrayDeque


LIFO?
 ↓
Deque
 ↓
ArrayDeque


Both ends?
 ↓
Deque
 ↓
ArrayDeque


Producer-consumer + blocking/backpressure?
 ↓
BlockingQueue


Concurrent + non-blocking?
 ↓
ConcurrentLinkedQueue


Legacy Stack?
 ↓
Don't reach for it
 ↓
Deque + ArrayDeque
```

### One-line interview summary

> **"For normal FIFO or LIFO operations I generally use `ArrayDeque`; for producer-consumer coordination with blocking and backpressure I use `BlockingQueue`; for concurrent non-blocking queue operations I can use `ConcurrentLinkedQueue`; and I prefer `Deque` over the legacy `Stack` class."**
