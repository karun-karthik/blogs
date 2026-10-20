# Meeting Room Booking Management — LLD Interview Guide

> **Purpose:** A practical, interview-oriented guide for solving a Meeting Room Booking Management LLD problem from first principles. Use it to structure a 45–60 minute interview, explain design decisions, and handle likely follow-ups.
>
> **Scope:** In-memory, single-office baseline. Users can discover/book rooms, cancel bookings, and view bookings. A room cannot have overlapping active bookings. Optional room capabilities are supported. Production/distributed concerns are discussed separately.

---

## 1. Problem Summary

Design a system that allows users to reserve meeting rooms for a time interval while respecting room availability and room requirements.

Core use cases:

1. Create/register a room.
2. Find a suitable room.
3. Book a room for a time interval.
4. Check availability.
5. Cancel a booking.
6. View existing bookings or a user's bookings.

The central invariant is:

> **A room must not have two active overlapping bookings.**

State this early. It drives availability checks, booking creation, cancellation, and concurrency handling.

---

## 2. Clarify Requirements Before Designing

### Functional requirements

- A room has an ID, capacity, and a set of capabilities.
- A user can request a room for a start/end interval.
- A user may specify required capabilities such as projector, whiteboard, or video conferencing.
- The system rejects invalid intervals.
- The system rejects overlapping active bookings for the same room.
- A user can cancel their booking, subject to the agreed cancellation policy.
- A user can view their bookings.
- A user can inspect available/suitable rooms for an interval.

### Non-functional / design concerns

- Correctness of the no-overlap invariant.
- Clear responsibility assignment and encapsulation.
- Concurrency safety.
- Testability and maintainability.
- Avoiding unnecessary abstractions and patterns.

### Ask or state assumptions

- Is the system single-office and single-time-zone?
- Are intervals half-open, `[start, end)`?
- Can users book multiple rooms for the same time?
- Can a user cancel another user's booking?
- Are past bookings cancellable?
- Do bookings require approval?
- Are recurring bookings required?
- Is the system in-memory, or must it support multiple server instances?

If time is limited, state reasonable assumptions and move forward. Do not design unrequested features.

---

## 3. Core Domain Model

A reasonable baseline model:

```text
User
Room
Booking
TimeInterval
RoomCapability
BookingManagementService
RoomRepository
BookingRepository
```

### Responsibility map

| Type | Owns | Does not own |
|---|---|---|
| `User` | User identity and user-related data | Global availability |
| `Room` | Room identity, capacity, capabilities, capability matching | All bookings, persistence |
| `Booking` | One reservation, owner, room, interval, lifecycle | Searching all bookings |
| `TimeInterval` | Start/end validation and overlap behavior | Booking persistence |
| `BookingManagementService` | Booking/cancellation workflows and coordination | Low-level storage mechanics |
| `RoomRepository` | Room retrieval/storage | Booking policy |
| `BookingRepository` | Booking retrieval/storage and query support | UI or request orchestration |

Only introduce a separate `User` class if it carries meaningful domain behavior or data. A `userId` on `Booking` may be sufficient for a small interview implementation.

---

## 4. Room and Capability Modeling

A room owns its capabilities and should answer whether it satisfies a requirement:

```java
room.supports(requiredCapabilities)
```

Prefer a set of capabilities over one boolean field per capability:

```java
public enum RoomCapability {
    PROJECTOR,
    WHITEBOARD,
    VIDEO_CONFERENCE
}
```

```java
public final class Room {
    private final String id;
    private final int capacity;
    private final Set<RoomCapability> capabilities;

    public Room(String id, int capacity, Set<RoomCapability> capabilities) {
        this.id = Objects.requireNonNull(id);
        if (capacity <= 0) {
            throw new IllegalArgumentException("Capacity must be positive");
        }
        this.capacity = capacity;
        this.capabilities = Set.copyOf(
            Objects.requireNonNull(capabilities)
        );
    }

    public String getId() {
        return id;
    }

    public int getCapacity() {
        return capacity;
    }

    public boolean supports(Set<RoomCapability> required) {
        return capabilities.containsAll(required);
    }
}
```

### Why composition instead of inheritance?

Capabilities are independently combinable properties. If every combination becomes a subtype (`ProjectorRoom`, `WhiteboardRoom`, `ProjectorWhiteboardRoom`, etc.), the subtype hierarchy grows combinatorially.

Use:

```text
Room
 └── capabilities: Set<RoomCapability>
```

instead of a growing hierarchy of capability-specific room subclasses.

**Interview explanation:** “Capabilities are properties that can be combined independently, not mutually exclusive room types. A set models combinations directly and lets us add a capability without creating new subclasses.”

---

## 5. TimeInterval: Validation and Overlap

Represent the interval as a value object. Use immutable timestamps, such as `Instant`, and validate that start precedes end.

Assume half-open intervals: `[start, end)`. Thus `10:00–11:00` and `11:00–12:00` are adjacent and do not overlap.

Two intervals overlap iff:

```text
startA < endB AND startB < endA
```

Java implementation:

```java
public final class TimeInterval {
    private final Instant start;
    private final Instant end;

    public TimeInterval(Instant start, Instant end) {
        this.start = Objects.requireNonNull(start);
        this.end = Objects.requireNonNull(end);

        if (!start.isBefore(end)) {
            throw new IllegalArgumentException("Start must be before end");
        }
    }

    public Instant getStart() {
        return start;
    }

    public Instant getEnd() {
        return end;
    }

    public boolean overlaps(TimeInterval other) {
        Objects.requireNonNull(other);
        return start.isBefore(other.end)
            && other.start.isBefore(end);
    }
}
```

Keep this object immutable. Otherwise a booking's interval could change unexpectedly after creation.

---

## 6. Booking: Reservation and Lifecycle

A booking represents one reservation and protects its own lifecycle.

A minimal status model is:

```java
public enum BookingStatus {
    ACTIVE,
    CANCELLED
}
```

Illustrative implementation:

```java
public final class Booking {
    private final String id;
    private final String userId;
    private final String roomId;
    private final TimeInterval interval;
    private BookingStatus status = BookingStatus.ACTIVE;

    public Booking(String id, String userId, String roomId,
                   TimeInterval interval) {
        this.id = Objects.requireNonNull(id);
        this.userId = Objects.requireNonNull(userId);
        this.roomId = Objects.requireNonNull(roomId);
        this.interval = Objects.requireNonNull(interval);
    }

    public boolean isActive() {
        return status == BookingStatus.ACTIVE;
    }

    public boolean overlaps(TimeInterval requested) {
        return isActive() && interval.overlaps(requested);
    }

    public void cancel() {
        if (status == BookingStatus.CANCELLED) {
            throw new IllegalStateException("Booking is already cancelled");
        }
        status = BookingStatus.CANCELLED;
    }

    public String getId() {
        return id;
    }

    public String getUserId() {
        return userId;
    }

    public String getRoomId() {
        return roomId;
    }

    public TimeInterval getInterval() {
        return interval;
    }
}
```

Important: the exact cancellation policy belongs in the requirements. If users may only cancel their own bookings or may not cancel past bookings, the application service should enforce those checks before invoking `booking.cancel()`.

Do not store duplicate state such as both `active` and `status`; they can contradict each other.

---

## 7. Repositories: Isolate Storage When Useful

Repository interfaces keep business policy independent of the storage mechanism.

```java
public interface RoomRepository {
    Optional<Room> findById(String roomId);
    List<Room> findAll();
}
```

```java
public interface BookingRepository {
    List<Booking> findByRoomId(String roomId);
    Optional<Booking> findById(String bookingId);
    List<Booking> findByUserId(String userId);
    void save(Booking booking);
}
```

For a minimal in-memory implementation, these can be backed by maps/lists. You do not need a repository interface for every object automatically; add an abstraction when it isolates a real dependency or makes testing/implementation changes easier.

### Where should overlap logic live?

A good interview boundary is:

- `TimeInterval` knows how to compare two intervals.
- `Booking` knows whether it is active and exposes its interval behavior.
- The service applies the booking policy across multiple bookings.
- The repository retrieves the relevant bookings.

For example, the service can call `findByRoomId(roomId)` and scan active bookings. Alternatively, a repository can expose a query such as `findConflicts(roomId, interval)` if the storage/query layer needs to optimize it. Explain the trade-off rather than treating one API as universally correct.

---

## 8. BookingManagementService: Orchestrate the Workflow

The service coordinates multiple objects and repository operations. It should not duplicate the room's capability logic or the interval's overlap formula.

A simplified example:

```java
public final class BookingManagementService {
    private final RoomRepository roomRepository;
    private final BookingRepository bookingRepository;

    public BookingManagementService(RoomRepository roomRepository,
                                    BookingRepository bookingRepository) {
        this.roomRepository = Objects.requireNonNull(roomRepository);
        this.bookingRepository = Objects.requireNonNull(bookingRepository);
    }

    public Booking bookRoom(String userId, String roomId,
                            TimeInterval interval,
                            Set<RoomCapability> requiredCapabilities) {
        Room room = roomRepository.findById(roomId)
            .orElseThrow(() -> new IllegalArgumentException("Room not found"));

        if (!room.supports(requiredCapabilities)) {
            throw new IllegalArgumentException(
                "Room does not satisfy required capabilities");
        }

        boolean conflict = bookingRepository.findByRoomId(roomId).stream()
            .filter(Booking::isActive)
            .anyMatch(b -> b.getInterval().overlaps(interval));

        if (conflict) {
            throw new IllegalStateException("Room is already booked");
        }

        Booking booking = new Booking(
            UUID.randomUUID().toString(), userId, roomId, interval
        );
        bookingRepository.save(booking);
        return booking;
    }

    public void cancelBooking(String userId, String bookingId) {
        Booking booking = bookingRepository.findById(bookingId)
            .orElseThrow(() -> new IllegalArgumentException("Booking not found"));

        if (!booking.getUserId().equals(userId)) {
            throw new SecurityException("Cannot cancel another user's booking");
        }

        booking.cancel();
        bookingRepository.save(booking);
    }

    public List<Booking> getBookingsForUser(String userId) {
        return bookingRepository.findByUserId(userId);
    }
}
```

This is illustrative interview code, not a complete production implementation. The basic version assumes the availability check and save are protected by the same atomicity mechanism when concurrent requests are possible. Without that, the example contains a race condition (covered below).

### Why a service?

Booking requires coordinating a room, existing bookings, a new booking, and persistence. No single `Booking` has all the information required to perform the collection-level operation. Putting the whole workflow on `Room` would couple the room to repositories and application concerns.

---

## 9. Booking Workflow

```text
Caller
  |
  v
BookingManagementService
  |
  +--> RoomRepository.findById(roomId)
  |
  +--> Room.supports(requiredCapabilities)
  |
  +--> BookingRepository.findByRoomId(roomId)
  |       |
  |       +--> reject if an active booking overlaps
  |
  +--> create Booking
  |
  +--> BookingRepository.save(booking)
  |
  v
Return booking
```

Narration:

> “The service retrieves the room, asks the room whether it supports the requested capabilities, checks existing active bookings for an interval conflict, creates and stores the booking only if the checks pass, and returns the booking.”

---

## 10. Availability and Complexity

A straightforward in-memory check:

```java
public boolean isAvailable(String roomId, TimeInterval requested) {
    return bookingRepository.findByRoomId(roomId).stream()
        .filter(Booking::isActive)
        .noneMatch(b -> b.getInterval().overlaps(requested));
}
```

If the room has `n` relevant bookings, a linear scan is `O(n)`.

This is generally appropriate for a basic LLD interview. Start with a simple correct design; introduce indexes or interval-oriented data structures only if scale or query requirements justify the complexity.

When searching for a suitable room, filter by capability/capacity and availability. If the problem asks the system to *choose* among multiple suitable rooms, clarify the selection rule (for example, smallest suitable room) before introducing a strategy abstraction.

---

## 11. Cancellation

Cancellation has two layers:

1. **Service/application checks:** booking exists; caller is permitted to cancel; any time-based policy is satisfied.
2. **Booking lifecycle transition:** `booking.cancel()` enforces the transition from `ACTIVE` to `CANCELLED`.

Persist the changed booking afterward.

A cancelled booking must not block a time slot. Deleting the record is simpler but loses history; cancellation preserves lifecycle information. Choose based on the stated requirements.

---

## 12. Concurrency and Double Booking

### The race

Two requests may execute:

```text
A: check availability -> available
B: check availability -> available
A: save booking
B: save booking
```

Both bookings can then exist, violating the central invariant.

### Required guarantee

The **availability check + booking creation** must be atomic with respect to competing bookings for the same room.

For a single-process in-memory exercise, a simple lock per room is easier to reason about than locking by exact requested interval. Different intervals can overlap even if their start/end pairs are not identical. The lock must cover the full conflict-check-and-create critical section.

For production or multiple application instances, an in-process lock is insufficient. Use a shared database/coordination mechanism appropriate to the persistence system, such as transactions with suitable locking/isolation, optimistic concurrency where appropriate, or a database-level constraint/model that prevents overlapping reservations.

Do not claim one mechanism is universally correct. The correct choice depends on database capabilities, deployment topology, contention, and consistency requirements.

---

## 13. Invariants to State Explicitly

1. `TimeInterval.start < TimeInterval.end`.
2. A room cannot have two active overlapping bookings.
3. Only active bookings participate in availability checks.
4. A cancelled booking cannot be cancelled again, unless the API explicitly chooses idempotent cancellation.
5. A booking references a valid room and user identifier.
6. If authorization is in scope, a user can only cancel bookings they are permitted to cancel.

The first two are core correctness rules; others depend on the scope and policy.

---

## 14. Common Wrong Designs

### Putting everything in the service

**Symptom:** the service validates time intervals, compares raw timestamps, inspects room capabilities, mutates booking status, and implements storage.

**Problem:** it accumulates domain knowledge that belongs in smaller objects. Keep workflow orchestration in the service and local invariants/behavior with the relevant domain objects.

### Putting everything in `Room`

**Symptom:** `room.book()`, `room.findBookings()`, `room.saveBooking()`.

**Problem:** a room should not need to know repositories or coordinate the whole application workflow.

### Inheritance for room capabilities

**Problem:** independently combinable properties create many subtype combinations. Model capabilities as a set.

### Boolean field explosion

Many `hasProjector`, `hasWhiteboard`, `hasVideoConference` fields make the model grow every time a capability is added. A set/enum is a better fit for the stated requirement.

### Pattern-first design

Do not add Factory, Abstract Factory, Strategy, State, Observer, Singleton, event buses, or microservices just because they are familiar. First identify what varies independently and what complexity the abstraction removes.

---

## 15. Patterns and Abstractions: When Are They Justified?

- **Repository:** useful when you want business policy independent of in-memory/SQL/other storage or want a test seam.
- **Strategy:** not required for one fixed room-selection rule. Consider it when multiple selection algorithms must vary independently.
- **State pattern:** not required for a simple `ACTIVE`/`CANCELLED` enum. Consider it only if state-specific behavior and transitions become substantially more complex.
- **Factory:** not necessary if booking creation is straightforward. Add one only if creation has meaningful complexity or variation.
- **Lock/transaction:** not a design-pattern decoration; it is a correctness mechanism needed to protect the invariant under concurrent mutation.

For every abstraction, be able to answer: **What changes independently, and what dependency does this isolate?**

---

## 16. Trade-Offs to Discuss

| Choice | Simple option | When to evolve |
|---|---|---|
| Availability | Scan room bookings, `O(n)` | Index/query optimization when justified |
| Capabilities | `Set<RoomCapability>` | Rich capability metadata only if needed |
| Lifecycle | Enum with `ACTIVE`/`CANCELLED` | Richer lifecycle if approvals/expiry/etc. arrive |
| Persistence | In-memory repository | Database when persistence/concurrency requirements arrive |
| Room selection | Inline rule | Strategy if multiple algorithms vary independently |
| Concurrency | Per-room lock for single process | Database/shared coordination for multiple instances |
| Cancellation | Status transition | Hard delete only if history is irrelevant |

A strong interview candidate explains why the simplest option satisfies current requirements and what new pressure would justify the next step.

---

## 17. Minimum Viable vs. Strong Interview Design

### Minimum viable

- `Room`
- `Booking`
- `TimeInterval`
- `BookingManagementService`
- in-memory storage
- interval overlap check
- reject conflicts
- cancel booking

### Strong interview design

Add where useful:

- `RoomCapability` as an enum and capability set on `Room`
- immutable `TimeInterval`
- explicit booking lifecycle
- repository abstractions if storage isolation/testing matters
- explicit invariants and edge cases
- concurrency/race-condition explanation
- test cases for overlap, adjacency, cancellation, and capability matching

### Avoid until asked

- distributed locks
- complex scheduling engines
- microservices
- event bus/message queue
- complex state hierarchy
- specialized interval indexes
- recurrence rules
- notifications and approval workflows

---

## 18. Testing Strategy

### Interval tests

- `10:00–11:00` vs `11:00–12:00` → no overlap.
- `10:00–11:00` vs `10:30–11:30` → overlap.
- `10:00–11:00` vs `09:00–10:00` → no overlap.
- `10:00–11:00` vs `09:30–11:30` → overlap.
- Equal start/end or end before start → rejected.

### Capability tests

- A room supports a subset of its capabilities.
- A room supports all requested capabilities.
- A room missing one required capability is rejected.
- Empty required set is supported, if the requirements allow it.

### Booking tests

- Valid booking succeeds.
- Overlapping active booking is rejected.
- Adjacent booking succeeds.
- Cancelled booking no longer blocks the interval.
- Unknown room is rejected.
- Unauthorized cancellation is rejected if authorization is in scope.
- Concurrent conflicting requests cannot both succeed.

---

## 19. Follow-Up Requirements

### Capacity

Add `capacity` to `Room`; reject rooms with capacity below the requested attendee count.

### Location

Add a location field or value object only if location has enough structure/behavior to warrant it. Do not introduce inheritance for a room's location.

### Multiple room-selection policies

If rules such as “smallest suitable room,” “nearest room,” or “preferred room” need to be swapped independently, consider `RoomSelectionStrategy`.

### Approval

Add explicit states such as `PENDING`, `CONFIRMED`, `REJECTED`, and `CANCELLED` only if the approval workflow is required. Define valid transitions and who may trigger them.

### Recurring bookings

Introduce a recurrence rule and validate concrete occurrences; do not casually overload a one-off `TimeInterval`.

### Multiple server instances

A local lock no longer protects the invariant across instances. Move enforcement to a shared persistence or coordination mechanism.

### Atomic multi-room reservation

If booking several rooms must either fully succeed or fully fail, model a higher-level request/reservation and define transaction boundaries.

---

## 20. Your Interview Reasoning Framework

Use this sequence:

```text
Requirements
    ↓
Use cases
    ↓
Domain / entities
    ↓
Responsibilities
    ↓
Collaborations
    ↓
Abstractions
    ↓
Dependencies
    ↓
Patterns only if useful
    ↓
Code
```

For every important decision, ask:

1. What requirement or change creates the pressure?
2. What invariant must remain true?
3. Who owns the relevant data?
4. What behavior naturally needs that knowledge?
5. Does the operation involve one object or coordinate many?
6. What must depend on what?
7. What complexity does the abstraction remove, and what complexity does it add?
8. What happens under concurrent requests?

Avoid using “SRP,” “loose coupling,” or “SOLID” as the whole explanation. Explain the concrete reason first; use the principle as a summary.

---

## 21. Three-Minute Interview Explanation

> “The core domain types are `Room`, `Booking`, and `TimeInterval`. `Room` owns capacity and a composable set of capabilities, and answers whether it supports the requested capabilities. `TimeInterval` validates start/end and owns the overlap calculation. `Booking` represents one reservation and owns its lifecycle, including cancellation.
>
> `BookingManagementService` coordinates the workflow because creating a booking requires checking a room, comparing the requested interval with existing bookings, creating a reservation, and persisting it. Repositories can isolate persistence if that abstraction is useful for the implementation.
>
> The key invariant is that a room cannot have two active overlapping bookings. With half-open intervals, overlap is `startA < endB && startB < endA`, so adjacent meetings are allowed. A basic implementation can scan the room's active bookings.
>
> Under concurrency, checking availability and creating the booking must be atomic; otherwise two requests can both see the slot as available. A per-room lock may be enough for a single-process in-memory exercise, while production or multi-instance deployments need a shared database/coordination mechanism.
>
> I use composition for room capabilities because they are independently combinable properties. I would introduce Strategy only if room-selection algorithms need to vary independently, and I would avoid adding patterns until a concrete requirement justifies them.”

---

## 22. Final Cheat Sheet

Before coding, be able to state:

- **Invariant:** no overlapping active bookings for the same room.
- **Interval rule:** `startA < endB && startB < endA`.
- **Room:** capacity, capabilities, `supports(...)`.
- **TimeInterval:** immutable interval and `overlaps(...)`.
- **Booking:** one reservation and lifecycle; `cancel()`.
- **Service:** coordinates the multi-object workflow.
- **Repository:** isolates storage/query concerns when useful.
- **Concurrency:** check + create must be atomic.
- **Capabilities:** composition/set, not subclass combinations.
- **Patterns:** justify from change pressure, not familiarity.

**The central design principle:** put behavior where the required knowledge naturally lives, keep coordination explicit, preserve invariants, and use the simplest design that satisfies the stated requirements.
