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
