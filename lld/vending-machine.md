# Vending Machine --- LLD Interview Revision Guide

A practical, interview-ready guide for a 45--60 minute low-level design
interview. The focus is not on memorizing classes; it is on explaining
requirements, ownership, invariants, workflows, failure handling, and
trade-offs.

------------------------------------------------------------------------

## 1. Problem Summary

Design the software for a vending machine that sells items from finite
inventory, accepts payment, dispenses a selected item, and returns
change when applicable.

The machine interacts with physical components---such as a cash
acceptor, coin/bill return mechanism, and dispenser---through software
interfaces. Those components can fail, time out, or return ambiguous
results.

The central correctness challenge is **coordinating inventory, payment,
and physical dispensing without losing money, dispensing twice, or
corrupting stock state**.

For an interview, begin with a deliberately small scope: one machine,
one purchase at a time, one currency, one item per purchase, and
hardware represented by interfaces. Then explain how concurrency and
ambiguous hardware outcomes affect the design.

## 2. Clarify Requirements Before Designing

Do not begin with classes. Clarify the behavior and state your
assumptions when the interviewer does not specify details.

### Functional requirements

-   Display or look up products and their prices.
-   Accept a product selection.
-   Check that the selected product exists and is available.
-   Accept cash and determine whether enough money has been inserted.
-   Dispense the selected item after payment is sufficient.
-   Return change after a successful purchase.
-   Refund payment when a purchase is known to have failed before
    dispensing.
-   Allow an operator to restock inventory.
-   Expose a transaction result or status.

### Important failure cases

-   Product does not exist.
-   Product is out of stock.
-   Payment is insufficient.
-   Cash acceptance fails or its result is unknown.
-   Dispensing is confirmed successful.
-   Dispensing is confirmed unsuccessful.
-   Dispenser times out and the physical outcome is unknown.
-   Refund or change return fails or times out.
-   A request is retried or delivered twice.
-   Two requests compete for the last unit.
-   The process restarts during a purchase.

### Non-functional / design concerns

-   Preserve inventory and money invariants.
-   Avoid duplicate dispensing, refunds, and change payouts.
-   Keep business workflow independent of specific hardware vendors.
-   Make failures diagnosable and recoverable.
-   Keep the interview design small enough to explain and implement.

### Ask or state assumptions

1.  Is payment cash-only, or must cards/mobile payments be supported?
2.  Is the currency fixed?
3.  Can a purchase contain multiple products, or exactly one item?
4.  Is restocking in scope?
5.  Can multiple users operate the machine concurrently?
6.  What does "dispense failed" mean: confirmed no item delivered, or a
    timeout with unknown outcome?
7.  If change cannot be returned, should the purchase remain completed
    with change owed?
8.  Is persistence and crash recovery expected, or is an in-memory
    interview implementation enough?

**Reasonable baseline:** one currency, one item per purchase,
cash-payment interface, restocking supported, and hardware abstracted.
Model `DISPENSED`, `NOT_DISPENSED`, and `UNKNOWN` as distinct outcomes.
Do not assume that a timeout proves the item was not delivered.

## 3. Core Domain Model

A useful strong-interview design has these concepts:

  -----------------------------------------------------------------------
  Type                                Responsibility
  ----------------------------------- -----------------------------------
  `Item`                              Product identity, description, and
                                      price

  `InventoryEntry`                    One item's available and reserved
                                      quantities

  `Inventory`                         Lookup, atomic reservation, commit,
                                      release, and restock

  `PurchaseTransaction`               One purchase's identity, state,
                                      item, payment, and reservation
                                      references

  `PaymentProcessor`                  Accept payment, refund, and return
                                      change through payment hardware

  `Dispenser`                         Request physical dispensing and
                                      report the outcome

  `VendingMachine`                    Coordinate the purchase workflow
                                      and recovery decisions

  `TransactionRepository`             Store and retrieve transaction
                                      state
  -----------------------------------------------------------------------

Do not turn every noun into a class. Keep a type only if it has
meaningful data, behavior, lifecycle, or an abstraction boundary.

### Responsibility map

-   `Item` should not know about the machine's inventory count.
-   `Inventory` owns the stock state and protects its local stock
    invariants.
-   `PurchaseTransaction` owns the state and facts of one purchase.
-   `PaymentProcessor` should not decide whether inventory is released.
-   `Dispenser` should not decide whether to refund the customer.
-   `VendingMachine` coordinates the workflow because the operation
    crosses inventory, payment, dispensing, and settlement.
-   Repositories handle persistence/querying; they should not own
    business policy.

## 4. Item and Inventory Modeling

### `Item`

Typical fields:

``` java
final class Item {
    private final String id;
    private final String name;
    private final Money price;
}
```

The product definition and the number of units currently in the machine
are different concepts. A product may exist even when no units are
available.

Use a `Money` value type rather than floating-point arithmetic for real
currency calculations. For an interview, a fixed currency and decimal
scale may be enough; a production design should represent the currency
explicitly and use an appropriate minor-unit or decimal representation.

### `InventoryEntry`

An inventory entry can track:

-   `itemId`
-   `availableQuantity`
-   `reservedQuantity` or equivalent reservation records

The exact representation depends on the implementation. The important
point is that a purchase may need to claim a unit before the hardware
outcome is known.

### Why reserve stock?

Suppose only one chocolate remains. Two purchase attempts both read
`availableQuantity = 1`. If both proceed to payment and dispensing, the
system may sell the same logical unit twice.

Reservation is a claim on a unit while the purchase is in progress. It
prevents another purchase from taking that unit before the first
purchase has a known outcome.

A simple conceptual API:

``` java
Optional<Reservation> reserve(String itemId, String transactionId);
void commitReservation(String reservationId);
void releaseReservation(String reservationId);
```

`reserve` must atomically check availability and claim the unit.
`commitReservation` makes the sale's stock deduction final.
`releaseReservation` returns the unit to availability when the design
has established that it is safe to do so.

### Why not keep only a list of items?

A `List<Item>` describes product definitions, not stock quantities or
reservations. It also makes it awkward to enforce the invariant that the
same physical/logical unit cannot be claimed by two purchases.

## 5. Inventory Invariants and Concurrency

State the invariant before discussing synchronization.

1.  Available quantity must never be negative.
2.  Reserved quantity must never be negative.
3.  A unit cannot be reserved by two active purchases.
4.  A reservation can be committed or released at most once.
5.  A purchase's stock reservation must not be released merely because a
    dispenser timed out.
6.  Restocking must not overwrite or accidentally erase active
    reservations.

### The race

``` text
Request A: read stock = 1
Request B: read stock = 1
Request A: decide item is available
Request B: decide item is available
Request A: dispense
Request B: dispense
```

A check followed by a separate update is not atomic. Put the
availability check and reservation in one atomic operation.

### What synchronization is appropriate?

-   **Single-process interview implementation:** a synchronized method
    or lock around the inventory reservation operation may be
    sufficient.
-   **Multiple application instances:** a process-local lock is not
    enough. Use a shared persistence/coordination mechanism, such as a
    transaction with suitable locking or optimistic concurrency.
-   **Physical hardware:** software locks alone do not prove what
    happened at the dispenser. Hardware outcome tracking and
    reconciliation are separate concerns.

Do not claim that `synchronized` solves distributed concurrency or
physical exactly-once delivery.

## 6. PurchaseTransaction: State and Lifecycle

A purchase is more than a method call. It has a lifecycle that can
outlive one request because payment, dispensing, refunds, or change may
fail.

Useful transaction facts include:

-   Stable transaction ID
-   Selected item ID
-   Agreed price
-   Inventory reservation ID
-   Amount accepted
-   Change due
-   Current purchase status
-   External operation IDs or references
-   Failure/reconciliation reason, where appropriate

Avoid copying the full `Item` object or every hardware detail into the
transaction unless the design needs a snapshot. For example, storing the
agreed price can matter if product prices can change while a purchase is
in progress.

### Example states

A practical state set might include:

``` text
CREATED
INVENTORY_RESERVED
PAYMENT_ACCEPTED
DISPENSING
RECONCILIATION_REQUIRED
REFUND_PENDING
CHANGE_PENDING
COMPLETED
FAILED
REFUNDED
```

These names are not sacred. Use the smallest set that can express the
required behavior without ambiguous states.

### State distinctions that matter

-   `FAILED` should mean the system knows the purchase failed under the
    defined policy.
-   `RECONCILIATION_REQUIRED` means the system cannot safely infer the
    physical or financial outcome.
-   `REFUND_PENDING` means the refund has not yet been confirmed.
-   `CHANGE_PENDING` means the item was dispensed, but the customer is
    still owed change.
-   `COMPLETED` should only be reached when the purchase's required
    success and settlement conditions have been met.

Do not mark a refund as completed merely because a refund request was
sent. Do not mark a dispense as failed merely because the response timed
out.

## 7. PaymentProcessor: Accepting, Refunding, and Returning Change

The payment boundary should abstract the physical or external payment
mechanism.

Possible operations:

``` java
PaymentResult acceptPayment(String transactionId, Money amount);
RefundResult refund(String operationId, String transactionId, Money amount);
ChangeResult returnChange(String operationId, String transactionId, Money amount);
```

The exact API depends on the hardware. A real cash acceptor may
accumulate inserted cash incrementally rather than accept one amount in
a single call. Keep the interview API aligned with the assumed hardware
model.

### Keep the amounts distinct

-   **Price:** amount due for the item.
-   **Accepted amount:** money the machine has actually accepted.
-   **Change due:** `acceptedAmount - price`, only when payment is
    sufficient and the purchase succeeds under the chosen policy.
-   **Refund amount:** amount that should be returned when the purchase
    is confirmed not to have delivered the item.

Example: item costs ₹30 and ₹50 has been accepted.

-   Confirmed successful dispense: return ₹20 change.
-   Confirmed non-dispense: refund ₹50.
-   Unknown dispense outcome: do not automatically refund ₹50 or retry
    dispensing until the outcome is reconciled.

### Why should the dispenser not return money?

Dispensing and money movement are different responsibilities, and they
have different hardware, failure modes, and operation identifiers. If
`Dispenser` also handles refunds, it becomes coupled to payment policy
and hardware.

### Payment failure is not always a simple boolean

A payment operation can be confirmed successful, confirmed unsuccessful,
or unknown after a timeout. If payment status is unknown, do not blindly
repeat an operation that might accept money twice. Model the uncertainty
or explain the assumed behavior explicitly.

## 8. Dispenser: Model the Physical Outcome Correctly

A small interface is enough to isolate hardware:

``` java
enum DispenseOutcome {
    DISPENSED,
    NOT_DISPENSED,
    UNKNOWN
}

interface Dispenser {
    DispenseResult dispense(String transactionId, String itemId);
    DispenseResult getOutcome(String transactionId);
}
```

`getOutcome` is optional in the minimum design, but it represents a
useful recovery capability when hardware supports status queries.

### Why three outcomes?

-   `DISPENSED`: the hardware confirms that the item was delivered.
-   `NOT_DISPENSED`: the hardware confirms that the item was not
    delivered.
-   `UNKNOWN`: the system cannot establish which physical outcome
    occurred.

A timeout is usually evidence of `UNKNOWN`, not necessarily
`NOT_DISPENSED`. The command may have reached the hardware and completed
even though the response was lost.

### Transaction ID and idempotency

Send a stable transaction ID with the dispense request. If the same
logical request is retried, hardware that supports deduplication should
recognize the ID and avoid dispensing a second item.

**Important limitation:** a transaction ID by itself does not guarantee
exactly-once physical delivery. The dispenser must persist/deduplicate
operation IDs or provide a reliable status/reconciliation mechanism. If
it cannot, the software must represent uncertainty and use an
operational recovery process rather than pretending the outcome is
known.

## 9. VendingMachine: Orchestrate, Do Not Own Every Detail

`VendingMachine` coordinates the purchase because the workflow crosses
several collaborators. It should not duplicate their internal
responsibilities.

Typical dependencies:

``` java
final class VendingMachine {
    private final Inventory inventory;
    private final PaymentProcessor paymentProcessor;
    private final Dispenser dispenser;
    private final TransactionRepository transactions;
}
```

Potential public operations:

``` java
PurchaseResult purchase(String itemId, Money offeredAmount);
PurchaseStatus getPurchaseStatus(String transactionId);
void restock(String itemId, int quantity);
```

These are illustrative signatures, not a required API. In a cash-input
device, `insertCash` and `selectItem` may be separate operations; a
single `purchase` call is a convenient abstraction for the interview
baseline.

### What the coordinator should do

-   Create or load a transaction.
-   Validate the product and reserve inventory.
-   Coordinate payment.
-   Request dispensing.
-   Commit or release the reservation according to the confirmed
    outcome.
-   Request change or refund when appropriate.
-   Persist state transitions.
-   Stop automatic progress when an outcome is unknown and arrange
    reconciliation.

### What it should not do

-   Implement the physical motor protocol.
-   Maintain its own duplicate stock count separate from `Inventory`.
-   Calculate hardware-specific cash acceptance behavior.
-   Let a timeout silently become success or failure.
-   Hide refund/change failures behind a generic boolean.

## 10. End-to-End Purchase Workflow

The sequence below is a strong interview baseline. Explain the invariant
at each boundary, not just the method calls.

### Happy path

1.  Create a purchase transaction with a stable ID.
2.  Validate that the item exists and its price is known.
3.  Atomically reserve one unit of inventory.
4.  Accept payment and confirm the accepted amount.
5.  If payment is insufficient, return accepted money and release the
    reservation according to the payment outcome.
6.  Request dispense using the stable transaction ID.
7.  If the item is confirmed dispensed, commit the inventory
    reservation.
8.  If change is due, request change using a stable operation ID.
9.  Mark the transaction `COMPLETED` only after required settlement is
    confirmed.

### Confirmed dispense failure

1.  The dispenser confirms `NOT_DISPENSED`.
2.  Do not commit the stock reservation as a sale.
3.  Request a refund of the accepted amount.
4.  Release the reservation only when the workflow has established it is
    safe to do so.
5.  Mark the transaction `REFUNDED` or `FAILED` according to the state
    model and confirmed refund result.

If the refund fails or its outcome is unknown, do not claim the customer
has been refunded. Keep a pending/reconciliation state.

### Unknown dispense outcome

1.  The dispenser times out or returns an ambiguous result.
2.  Mark the transaction `RECONCILIATION_REQUIRED`.
3.  Keep the stock reservation; do not make that unit available to
    another purchase prematurely.
4.  Do not automatically issue a full refund.
5.  Do not automatically retry dispensing unless the hardware's
    idempotency/outcome contract makes that retry safe.
6.  Query the hardware or route the transaction for operator
    reconciliation.
7.  Once the outcome is known, resume the appropriate branch.

### Dispense succeeds, change fails

The customer received the item, so do not release the stock or refund
the full purchase as if no item was delivered. Keep the sale committed
and track the unpaid change as `CHANGE_PENDING` until it is settled or
handled by the agreed policy.

## 11. Failure Matrix

  -----------------------------------------------------------------------
  Event                   What is known?          Safe response
  ----------------------- ----------------------- -----------------------
  Item missing            No valid product        Reject before accepting
                                                  payment

  Item out of stock       No unit can be reserved Reject before accepting
                                                  payment

  Payment confirmed       Accepted amount is      Return accepted money
  insufficient            below price             and release reservation
                                                  once safe

  Dispense confirmed      Item delivered          Commit reservation;
  successful                                      return change if due

  Dispense confirmed      Item not delivered      Refund accepted amount;
  unsuccessful                                    release reservation
                                                  when safe

  Dispense timeout        Physical outcome        Reconcile; do not
                          unknown                 blindly refund or retry

  Refund timeout          Refund outcome unknown  Keep refund pending;
                                                  query/reconcile by
                                                  operation ID

  Change timeout          Change outcome unknown  Keep change pending; do
                                                  not repeat blindly

  Process crashes after   Depends on hardware and Recover from
  dispense                durable records         transaction log and
                                                  hardware status; do not
                                                  assume rollback undoes
                                                  physical effects
  -----------------------------------------------------------------------

The key distinction is **confirmed failure versus unknown outcome**.
Many incorrect designs treat both as the same state.

## 12. Idempotency and Duplicate Requests

A client may retry after a timeout, or the machine controller may resend
a command. A retry must not accidentally become a second business
operation.

Use stable identifiers for:

-   Purchase transaction
-   Dispense operation
-   Refund operation
-   Change-return operation

For each external side effect, decide what happens if the same operation
ID is submitted again. The adapter should return the recorded result
where it can safely do so.

### What idempotency can and cannot do

-   It can prevent duplicate logical requests when the receiving
    component stores and checks operation IDs.
-   It can make status queries and retries safer.
-   It cannot reverse a physical item that already fell into the tray.
-   It cannot guarantee exactly-once behavior if the hardware has no
    deduplication or reliable outcome query.

Do not generate a new transaction ID on every retry of the same
purchase. That defeats deduplication.

## 13. Persistence and Crash Recovery

For a minimal coding interview, an in-memory repository may be
acceptable if stated as an assumption. For a strong design discussion,
identify where durability matters.

A crash can occur between any two steps:

``` text
Persist transaction
    → accept payment
    → persist payment result
    → request dispense
    → persist dispense result
    → commit stock
    → return change
    → persist completion
```

The exact order and recovery mechanism depend on hardware guarantees. A
database transaction cannot atomically roll back a physical dispense or
cash payout.

A durable implementation should record intent before an external side
effect, record confirmed results afterward, and reconcile incomplete
operations after restart. If the external device supports operation IDs
and status lookup, recovery can query the outcome. Otherwise, some cases
require operator intervention.

Do not imply that a repository alone makes the workflow transactional
across hardware.

## 14. Repositories and Dependency Boundaries

Potential abstractions:

``` java
interface TransactionRepository {
    void save(PurchaseTransaction transaction);
    Optional<PurchaseTransaction> findById(String transactionId);
}
```

`Inventory` may itself be a domain-facing abstraction, with an in-memory
or persistent implementation behind it.

### When repositories help

-   You need to swap in-memory storage for a database.
-   You want unit tests that control stored transactions.
-   The implementation has meaningful persistence/query behavior.
-   You need recovery after process restart.

### When not to overdo it

Do not create a repository interface for every small object merely to
show patterns. If the interview asks for a small in-memory design, a
concrete collection can be acceptable. Explain how the persistence
requirement would change that decision.

## 15. Invariants to State Explicitly

1.  Available stock cannot become negative.
2.  A unit cannot be reserved by two active purchases.
3.  A reservation is committed or released at most once.
4.  A purchase is not marked completed before confirmed dispense and
    required settlement.
5.  `UNKNOWN` is not equivalent to `NOT_DISPENSED`.
6.  An unknown dispense outcome must not trigger an unsafe retry or
    automatic refund.
7.  A refund is not considered complete until confirmed.
8.  A change payout is not considered complete until confirmed.
9.  A refund or change operation must not be duplicated by a retry.
10. The same transaction ID must refer to the same logical purchase.
11. Restocking must not erase or steal units reserved by active
    purchases.
12. Product price and transaction amount calculations must use exact
    monetary arithmetic.

The most important invariant is the coordination among **stock, physical
delivery, and money**. These are separate stateful systems, and no
ordinary in-memory method call makes them one atomic transaction.

## 16. Common Wrong Designs

### Decrementing stock before dispense is confirmed

**Problem:** if the dispenser confirms that no item was delivered, the
system may lose inventory unnecessarily.

**Better:** reserve stock before the operation; commit on confirmed
delivery; release only when the outcome permits it.

### Decrementing stock only after a timeout is resolved, without reserving

**Problem:** another purchase can claim the same final unit while the
first dispense is in progress.

**Better:** reserve first, then commit or release after the outcome is
known.

### Treating timeout as failure

**Problem:** the item may have been delivered and only the response was
lost. An automatic refund or retry may cause a free item or duplicate
dispense.

**Better:** use `UNKNOWN` and reconcile.

### Letting `Dispenser` refund money

**Problem:** dispensing hardware becomes coupled to payment policy and
money-return hardware.

**Better:** the dispenser reports the physical outcome; the workflow
coordinator selects the appropriate settlement action.

### Combining `Payment` and `PaymentProcessor` without a clear boundary

A `Payment` domain object may represent amounts and payment state.
`PaymentProcessor` is an adapter/service that interacts with cash
hardware. Keep both only if they represent distinct responsibilities;
otherwise avoid redundant classes.

### One giant `VendingMachine` class

**Problem:** product lookup, stock mutation, payment mechanics, motor
protocol, refund logic, persistence, and recovery all become tangled.

**Better:** the machine coordinates; inventory owns stock; payment and
dispenser adapters own hardware interaction; transaction owns purchase
state.

### Boolean-only result types

`true/false` cannot distinguish confirmed failure from unknown outcome
or expose a pending settlement.

**Better:** use explicit result types/enums for meaningful outcomes.

### Marking refund complete when requested

**Problem:** the refund command may have failed or timed out.

**Better:** represent pending/unknown refund state and reconcile by
stable operation ID.

### Pattern-first design

Do not add State, Strategy, Factory, Observer, Singleton, event buses,
or microservices just because they are familiar. Start with the
invariants and change pressures, then add abstractions only when they
reduce meaningful complexity.

## 17. Patterns and Abstractions: When Are They Justified?

-   **Adapter / interface boundary:** useful because physical payment
    and dispensing devices vary by vendor and should not leak device
    protocols into business logic.
-   **Repository:** useful when persistence and recovery matter or when
    storage needs to be replaced/tested independently.
-   **State pattern:** not required for a modest transaction state
    machine. An enum plus guarded transition methods is often enough.
    Consider State only if each state has substantial distinct behavior.
-   **Strategy:** not needed for one fixed product-selection or change
    policy. Consider it if multiple policies must vary independently.
-   **Factory:** not necessary if constructing the transaction is
    simple.
-   **Command / operation ID:** stable operation identities help retries
    and deduplication, but do not by themselves guarantee exactly-once
    physical action.
-   **Lock/transaction:** a correctness mechanism for protecting
    inventory state, not a pattern to add decoratively.

For every abstraction, answer: **what changes independently, and what
dependency does this boundary isolate?**

## 18. Trade-Offs to Discuss

  --------------------------------------------------------------------------
  Decision                Simple interview choice When to evolve
  ----------------------- ----------------------- --------------------------
  Stock representation    Quantity per item       Reservation records when
                                                  purchases can overlap or
                                                  remain uncertain

  Inventory concurrency   Synchronized atomic     Shared database
                          reserve                 transaction/coordination
                                                  across instances

  Transaction lifecycle   Enum with guarded       Richer state model if
                          transitions             workflows become
                                                  substantially more complex

  Hardware integration    Interfaces with         Vendor-specific adapters
                          simulated adapters      and protocol handling

  Result modeling         Explicit outcome        Richer error taxonomy if
                          enum/result object      operations need
                                                  differentiated recovery

  Persistence             In-memory repository    Durable storage when crash
                                                  recovery is required

  Retry safety            Stable operation IDs    Device-level deduplication
                                                  and reconciliation support

  Money                   Fixed-currency `Money`  Currency-aware accounting
                          value type              and explicit rounding
                                                  rules

  Refund/change           Synchronous request in  Durable pending operations
                          simple demo             and recovery worker in
                                                  production
  --------------------------------------------------------------------------

A strong candidate explains what the current design guarantees and what
it does **not** guarantee.

## 19. Minimum Viable vs. Strong Interview Design vs. Production Design

### Minimum viable interview design

-   `Item`
-   `Inventory`
-   `VendingMachine`
-   `PaymentProcessor` interface
-   `Dispenser` interface
-   One purchase flow
-   Stock check and payment validation
-   Dispense success/failure handling
-   Change/refund explanation

### Strong interview design

Add:

-   Atomic inventory reservation
-   `PurchaseTransaction` with explicit state
-   Separate confirmed failure from unknown outcome
-   Stable transaction and operation IDs
-   Idempotency discussion for dispense/refund/change
-   Explicit refund/change pending states
-   Transaction repository abstraction if persistence is relevant
-   Failure matrix and concurrency invariants
-   Tests for all important branches

### Production-grade concerns---do not implement all by default

-   Durable transaction log and restart recovery
-   Hardware-specific protocol details and device health
-   Operator reconciliation tooling
-   Audit trail and metrics/alerts
-   Cross-process inventory consistency
-   Robust cash denomination and change-availability modeling
-   Secure payment handling and compliance, if electronic payment is
    introduced
-   Operational policies for customer disputes and unpaid change

## 20. Testing Strategy

### Inventory tests

-   Reserving an available item succeeds.
-   Reserving an out-of-stock item fails.
-   Two concurrent requests for the last unit cannot both reserve it.
-   Committing a reservation decreases sellable stock exactly once.
-   Releasing a reservation makes the unit available exactly once.
-   Invalid quantities are rejected.
-   Restocking does not corrupt active reservations.

### Purchase happy-path tests

-   Valid product + sufficient payment + successful dispense completes.
-   Correct change is returned.
-   Inventory is committed once.
-   Repeating a transaction ID does not create a second purchase.

### Failure tests

-   Unknown product is rejected before payment.
-   Out-of-stock product is rejected before payment.
-   Insufficient payment returns accepted money and releases the
    reservation when safe.
-   Confirmed non-dispense triggers a refund.
-   Refund failure leaves a pending state.
-   Unknown dispense outcome enters reconciliation and does not
    refund/retry blindly.
-   Dispense success plus change failure leaves change pending rather
    than undoing the sale.
-   Unknown change outcome is not blindly repeated.
-   Crash/restart recovery does not duplicate dispense or refund when
    hardware supports operation IDs.

### State-machine tests

-   Invalid transitions are rejected.
-   `COMPLETED` cannot be reached before confirmed dispense and required
    settlement.
-   `REFUNDED` cannot be reached before refund confirmation.
-   A terminal transaction is not silently restarted as a new purchase.

## 21. Follow-Up Requirements

### Add card or mobile payment

Keep the purchase workflow dependent on a payment abstraction, but
define authorization/capture/refund semantics. Do not assume cash refund
and electronic refund have identical behavior. If payment can be
authorized before dispensing and captured afterward, discuss that
trade-off explicitly.

### Support multiple items in one purchase

Represent line items and quantities in the transaction. Reserve all
requested stock atomically or define partial-fulfillment policy.
Calculate the total using exact monetary arithmetic. Specify whether one
failed item aborts the whole purchase or allows partial completion.

### Support multiple currencies

Add currency identity to `Money`; define conversion source, rounding,
and when exchange rates are locked. Do not compare monetary values from
different currencies as if they were directly comparable.

### Machine runs out of change

Define policy: reject payment combinations that cannot be settled,
accept exact payment only, or track change owed. This is a business
requirement, not merely a `returnChange()` implementation detail.

### Restocking during a purchase

Restocking must update inventory through the same inventory owner and
must not overwrite reservations. Define whether restock operations can
happen concurrently with purchases and how operator authorization is
handled if in scope.

### Multiple machines

Each machine has its own stock and hardware identity. If central
management is added, distinguish machine-local physical inventory from
any central catalog. Avoid a global stock counter that ignores
individual machines.

### Multiple software instances control one machine

A local `synchronized` method no longer protects shared inventory or
device commands across processes. Use shared coordination and ensure the
hardware command path also deduplicates operations.

### Hardware supports no idempotency or status query

The system cannot always determine the outcome of a timed-out command.
Explain the residual uncertainty, avoid unsafe automatic
retries/refunds, and introduce an operator/manual reconciliation policy.
Do not promise exactly-once physical delivery.

### Customer walks away while money is inserted

This requires a session/timeout policy: how long selection and inserted
cash remain associated, whether idle cash is returned, and how session
cleanup interacts with in-flight dispense or refund operations.

## 22. Interview Reasoning Framework

Use this sequence:

``` text
Requirements and assumptions
        ↓
Core workflows and failure cases
        ↓
Invariants: stock, money, delivery
        ↓
Domain concepts and ownership
        ↓
Purchase state machine
        ↓
Interfaces at hardware boundaries
        ↓
Concurrency and idempotency
        ↓
Persistence/recovery if required
        ↓
Patterns only where justified
        ↓
Code and tests
```

For every important design decision, ask:

1.  What requirement creates the pressure?
2.  What invariant must remain true?
3.  Who owns the data?
4.  Which object has the knowledge needed for this behavior?
5.  Is this a local operation or a workflow across several components?
6.  What if the operation fails after the external side effect already
    happened?
7.  What does a timeout prove---and what does it not prove?
8.  Can the operation be safely retried?
9.  What complexity does the abstraction remove, and what complexity
    does it add?
10. What changes when multiple requests or multiple application
    instances operate concurrently?

Avoid using "SRP," "loose coupling," or "SOLID" as the whole
explanation. Explain the concrete reason first, then name the principle
if it helps.

## 23. Three-Minute Interview Explanation

> "I would model product definitions separately from stock. `Item`
> contains product identity and price, while `Inventory` owns available
> quantities and reservations. The inventory reservation operation must
> atomically check and claim a unit so two purchases cannot both take
> the last item.
>
> Each purchase has a stable transaction ID and an explicit lifecycle
> represented by `PurchaseTransaction`. `VendingMachine` coordinates the
> workflow: reserve stock, accept sufficient payment, request
> dispensing, then commit or release the reservation and settle change
> or refund based on the confirmed outcome.
>
> I would isolate physical payment and dispensing behind interfaces
> because hardware protocols and failure modes can vary independently.
> The dispenser returns one of three outcomes: `DISPENSED`,
> `NOT_DISPENSED`, or `UNKNOWN`. A timeout is not proof that dispensing
> failed. For an unknown outcome, I would keep the reservation and enter
> reconciliation rather than automatically refunding or retrying.
>
> Refund and change operations also need stable operation IDs and
> explicit pending states, because a timeout can leave their outcomes
> unknown too. A transaction ID alone does not guarantee exactly-once
> physical delivery; the hardware must support deduplication or reliable
> outcome lookup.
>
> For a single-process interview implementation, an atomic synchronized
> inventory reservation and in-memory repositories may be sufficient.
> For production, I would add durable transaction records and restart
> recovery, shared coordination across instances, hardware-specific
> reconciliation, and operational monitoring. I would add patterns only
> where they isolate a real variation point."

## 24. Final Cheat Sheet

Before coding, be able to state:

-   **Core invariant:** a unit cannot be sold to two purchases, and the
    machine must not misrepresent whether the customer received the item
    or money.
-   **Inventory:** reserve first, then commit on confirmed delivery or
    release when safe.
-   **Transaction:** stable ID, explicit state, guarded transitions.
-   **Payment:** distinguish accepted amount, refund amount, and change
    due.
-   **Dispenser:** `DISPENSED`, `NOT_DISPENSED`, `UNKNOWN`.
-   **Timeout:** unknown outcome, not automatically failure.
-   **Retry safety:** stable operation IDs plus hardware-side
    deduplication/status support.
-   **Coordinator:** `VendingMachine` coordinates; collaborators own
    their local responsibilities.
-   **Failure policy:** refund only when non-delivery is confirmed; keep
    refunds/change pending until confirmed.
-   **Concurrency:** reserve stock atomically; process-local locks do
    not coordinate multiple instances.
-   **Persistence:** a database cannot roll back a physical dispense;
    recovery needs durable intent/results and reconciliation.
-   **Patterns:** adapter boundaries are justified by hardware
    variation; other patterns need a concrete reason.

**Central design principle:** preserve the relationship between
inventory, payment, and physical delivery. Reserve resources before
irreversible actions, distinguish confirmed outcomes from uncertainty,
and never claim an external side effect succeeded or failed without
evidence.
