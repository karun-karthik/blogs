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

