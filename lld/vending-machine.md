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


---

# 25. Code Revision Appendix — Core Java Design

This appendix adds the code you should be able to explain and reproduce in an interview. It is intentionally organized around **ownership and invariants**, not around creating the maximum number of classes.

The snippets use Java 17. They illustrate the domain model and core workflow; hardware drivers, durable persistence, and complete recovery are intentionally left behind interfaces.

## 25.1 Money and Item

Use a value type for money rather than `double`, which can introduce binary floating-point rounding errors.

```java
import java.math.BigDecimal;
import java.util.Objects;

record Money(BigDecimal amount) {
    Money {
        Objects.requireNonNull(amount, "amount");
        if (amount.signum() < 0) {
            throw new IllegalArgumentException("Money cannot be negative");
        }
        amount = amount.setScale(2, java.math.RoundingMode.UNNECESSARY);
    }

    static Money of(String amount) {
        return new Money(new BigDecimal(amount));
    }

    Money plus(Money other) {
        return new Money(amount.add(other.amount));
    }

    Money minus(Money other) {
        if (amount.compareTo(other.amount) < 0) {
            throw new IllegalArgumentException("Result would be negative");
        }
        return new Money(amount.subtract(other.amount));
    }

    boolean isLessThan(Money other) {
        return amount.compareTo(other.amount) < 0;
    }

    boolean isZero() {
        return amount.signum() == 0;
    }
}

record Item(String id, String name, Money price) {
    Item {
        Objects.requireNonNull(id);
        Objects.requireNonNull(name);
        Objects.requireNonNull(price);
        if (id.isBlank() || name.isBlank()) {
            throw new IllegalArgumentException("Item id and name are required");
        }
    }
}
```

**Interview explanation:** `Item` describes a product; it does not own stock. `Money` centralizes monetary arithmetic and validation. This example assumes one currency and exactly two decimal places; multi-currency support requires an explicit currency code and defined rounding rules.

## 25.2 Inventory: Atomic Reservation

The key operation is not `isAvailable()` followed later by `decrement()`. That split creates a race. The check and reservation must be one atomic operation.

```java
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

record Reservation(String id, String transactionId, String itemId) {}

interface Inventory {
    Optional<Item> findItem(String itemId);

    Optional<Reservation> reserve(String itemId, String transactionId);

    void commit(String reservationId);

    void release(String reservationId);

    void restock(String itemId, int quantity);
}

final class InMemoryInventory implements Inventory {
    private static final class Entry {
        final Item item;
        int available;
        final Map<String, Reservation> activeByTransaction = new HashMap<>();

        Entry(Item item, int quantity) {
            this.item = item;
            this.available = quantity;
        }
    }

    private final Map<String, Entry> entries = new HashMap<>();
    private final Map<String, Reservation> reservations = new HashMap<>();
    private final Map<String, Boolean> completedReservations = new HashMap<>();

    public synchronized void addItem(Item item, int quantity) {
        if (quantity < 0) throw new IllegalArgumentException("Negative quantity");
        if (entries.containsKey(item.id())) {
            throw new IllegalArgumentException("Item already exists");
        }
        entries.put(item.id(), new Entry(item, quantity));
    }

    @Override
    public synchronized Optional<Item> findItem(String itemId) {
        Entry entry = entries.get(itemId);
        return entry == null ? Optional.empty() : Optional.of(entry.item);
    }

    @Override
    public synchronized Optional<Reservation> reserve(
            String itemId, String transactionId) {
        Entry entry = entries.get(itemId);
        if (entry == null) return Optional.empty();

        // A retry for the same transaction returns its existing reservation.
        Reservation existing = entry.activeByTransaction.get(transactionId);
        if (existing != null) return Optional.of(existing);

        if (entry.available == 0) return Optional.empty();

        entry.available--;
        Reservation reservation =
                new Reservation(java.util.UUID.randomUUID().toString(),
                                transactionId, itemId);
        entry.activeByTransaction.put(transactionId, reservation);
        reservations.put(reservation.id(), reservation);
        return Optional.of(reservation);
    }

    @Override
    public synchronized void commit(String reservationId) {
        Reservation reservation = reservations.remove(reservationId);
        if (reservation == null) {
            // Repeated commit is safe only if this reservation was already committed.
            if (Boolean.TRUE.equals(completedReservations.get(reservationId))) return;
            throw new IllegalArgumentException("Unknown reservation");
        }
        Entry entry = entries.get(reservation.itemId());
        entry.activeByTransaction.remove(reservation.transactionId());
        completedReservations.put(reservationId, true);
        // available was reduced at reserve time; commit finalizes the sale.
    }

    @Override
    public synchronized void release(String reservationId) {
        Reservation reservation = reservations.remove(reservationId);
        if (reservation == null) {
            // Repeated release after a prior release is harmless in this example.
            if (Boolean.FALSE.equals(completedReservations.get(reservationId))) return;
            throw new IllegalArgumentException("Unknown reservation");
        }
        Entry entry = entries.get(reservation.itemId());
        entry.available++;
        entry.activeByTransaction.remove(reservation.transactionId());
        completedReservations.put(reservationId, false);
    }

    @Override
    public synchronized void restock(String itemId, int quantity) {
        if (quantity <= 0) throw new IllegalArgumentException("Quantity must be positive");
        Entry entry = entries.get(itemId);
        if (entry == null) throw new IllegalArgumentException("Unknown item");
        entry.available += quantity;
    }

    public synchronized int availableQuantity(String itemId) {
        Entry entry = entries.get(itemId);
        if (entry == null) throw new IllegalArgumentException("Unknown item");
        return entry.available;
    }
}
```

### What to explain—and what to improve in production

- `reserve()` checks and claims stock under the same lock, so two threads cannot reserve the last unit.
- Stock is made unavailable at reservation time, not only after dispensing.
- `commit()` does not subtract stock again because reservation already made the unit unavailable.
- `release()` makes the unit available again only when the workflow knows that releasing it is safe.
- The `synchronized` keyword protects only this in-memory object inside one process. It does not coordinate multiple application instances.
- A production repository should persist reservation state and transitions atomically. The in-memory idempotency maps disappear on restart.

For a shorter interview answer, present the interface and explain the atomicity requirement; implement the synchronized version only if time permits.

## 25.3 Hardware Boundaries and Explicit Outcomes

```java
enum DispenseOutcome {
    DISPENSED,
    NOT_DISPENSED,
    UNKNOWN
}

record DispenseResult(DispenseOutcome outcome, String detail) {}

interface Dispenser {
    DispenseResult dispense(String transactionId, String itemId);

    // Optional recovery operation if the device supports outcome lookup.
    DispenseResult getOutcome(String transactionId);
}

enum OperationStatus {
    SUCCEEDED,
    FAILED,
    UNKNOWN
}

record PaymentResult(OperationStatus status, Money acceptedAmount, String detail) {}
record RefundResult(OperationStatus status, String detail) {}
record ChangeResult(OperationStatus status, String detail) {}

interface PaymentProcessor {
    PaymentResult acceptPayment(String transactionId, Money amount);

    RefundResult refund(String operationId, String transactionId, Money amount);

    ChangeResult returnChange(String operationId, String transactionId, Money amount);
}
```

**Do not replace `UNKNOWN` with `false`.** A timeout can mean the command completed but its response was lost. Payment acceptance, refund, and change return can have the same ambiguity as dispensing.

Stable operation IDs allow an adapter/device that supports deduplication to recognize retries. The IDs alone do not provide exactly-once physical behavior.

## 25.4 Purchase State

```java
enum PurchaseStatus {
    CREATED,
    INVENTORY_RESERVED,
    PAYMENT_ACCEPTED,
    DISPENSING,
    RECONCILIATION_REQUIRED,
    REFUND_PENDING,
    CHANGE_PENDING,
    COMPLETED,
    FAILED,
    REFUNDED
}

final class PurchaseTransaction {
    private final String id;
    private final String itemId;
    private final Money price;

    private PurchaseStatus status = PurchaseStatus.CREATED;
    private String reservationId;
    private Money acceptedAmount = Money.of("0.00");
    private Money changeDue = Money.of("0.00");
    private String note = "";

    PurchaseTransaction(String id, String itemId, Money price) {
        this.id = Objects.requireNonNull(id);
        this.itemId = Objects.requireNonNull(itemId);
        this.price = Objects.requireNonNull(price);
    }

    String id() { return id; }
    String itemId() { return itemId; }
    Money price() { return price; }
    PurchaseStatus status() { return status; }
    String reservationId() { return reservationId; }
    Money acceptedAmount() { return acceptedAmount; }
    Money changeDue() { return changeDue; }
    String note() { return note; }

    void setReservationId(String id) { this.reservationId = id; }
    void setAcceptedAmount(Money amount) { this.acceptedAmount = amount; }
    void setChangeDue(Money amount) { this.changeDue = amount; }
    void setNote(String note) { this.note = note; }

    void transitionTo(PurchaseStatus next) {
        // Production code should validate allowed transitions explicitly.
        this.status = next;
    }
}
```

This deliberately keeps state transitions simple for readability. In an interview, say that transition methods should guard invalid transitions—for example, a transaction must not move from `CREATED` directly to `COMPLETED`. A production implementation should persist every important transition.

## 25.5 Transaction Repository

```java
import java.util.Optional;

interface TransactionRepository {
    void save(PurchaseTransaction transaction);
    Optional<PurchaseTransaction> findById(String transactionId);
}
```

The repository abstraction is useful if the design needs durable recovery or replaceable storage. An in-memory implementation is enough for a simple demo, but it cannot recover transactions after process restart.

## 25.6 Purchase Coordinator: The Important Branches

The following is **workflow-oriented reference code**, not a complete production implementation. It focuses on the decision points that interviewers usually probe. The exact behavior of payment acceptance must match the chosen cash hardware contract.

```java
final class VendingMachine {
    private final Inventory inventory;
    private final PaymentProcessor payments;
    private final Dispenser dispenser;
    private final TransactionRepository transactions;

    VendingMachine(
            Inventory inventory,
            PaymentProcessor payments,
            Dispenser dispenser,
            TransactionRepository transactions) {
        this.inventory = inventory;
        this.payments = payments;
        this.dispenser = dispenser;
        this.transactions = transactions;
    }

    PurchaseTransaction purchase(String itemId, Money offeredAmount) {
        Item item = inventory.findItem(itemId)
                .orElseThrow(() -> new IllegalArgumentException("Unknown item"));

        String txId = java.util.UUID.randomUUID().toString();
        PurchaseTransaction tx = new PurchaseTransaction(txId, itemId, item.price());
        transactions.save(tx);

        // 1. Reserve before accepting payment.
        Reservation reservation = inventory.reserve(itemId, txId)
                .orElseThrow(() -> new IllegalStateException("Out of stock"));
        tx.setReservationId(reservation.id());
        tx.transitionTo(PurchaseStatus.INVENTORY_RESERVED);
        transactions.save(tx);

        // 2. Accept payment. This assumes the adapter returns the confirmed amount.
        PaymentResult payment = payments.acceptPayment(txId, offeredAmount);
        if (payment.status() == OperationStatus.UNKNOWN) {
            tx.transitionTo(PurchaseStatus.RECONCILIATION_REQUIRED);
            tx.setNote("Payment outcome unknown; query/reconcile payment device");
            transactions.save(tx);
            return tx;
        }
        if (payment.status() != OperationStatus.SUCCEEDED) {
            inventory.release(reservation.id());
            tx.transitionTo(PurchaseStatus.FAILED);
            tx.setNote("Payment was not accepted");
            transactions.save(tx);
            return tx;
        }

        Money accepted = payment.acceptedAmount();
        tx.setAcceptedAmount(accepted);
        tx.transitionTo(PurchaseStatus.PAYMENT_ACCEPTED);
        transactions.save(tx);

        if (accepted.isLessThan(item.price())) {
            refundAndRelease(tx, reservation.id(), accepted, "Insufficient payment");
            return tx;
        }

        tx.setChangeDue(accepted.minus(item.price()));
        tx.transitionTo(PurchaseStatus.DISPENSING);
        transactions.save(tx);

        // 3. Request dispense with the stable transaction ID.
        DispenseResult result = dispenser.dispense(txId, itemId);

        if (result.outcome() == DispenseOutcome.UNKNOWN) {
            tx.transitionTo(PurchaseStatus.RECONCILIATION_REQUIRED);
            tx.setNote("Dispense outcome unknown; do not blindly refund or retry");
            transactions.save(tx);
            return tx; // Keep reservation until outcome is resolved.
        }

        if (result.outcome() == DispenseOutcome.NOT_DISPENSED) {
            refundAndRelease(tx, reservation.id(), accepted, "Item not dispensed");
            return tx;
        }

        // 4. Confirmed delivery: commit stock exactly once.
        inventory.commit(reservation.id());

        // 5. Settle change if any. Use a stable operation ID for retry safety.
        if (!tx.changeDue().isZero()) {
            ChangeResult change = payments.returnChange(
                    txId + ":change", txId, tx.changeDue());

            if (change.status() != OperationStatus.SUCCEEDED) {
                tx.transitionTo(PurchaseStatus.CHANGE_PENDING);
                tx.setNote("Item dispensed; change settlement requires follow-up");
                transactions.save(tx);
                return tx;
            }
        }

        tx.transitionTo(PurchaseStatus.COMPLETED);
        transactions.save(tx);
        return tx;
    }

    private void refundAndRelease(
            PurchaseTransaction tx,
            String reservationId,
            Money refundAmount,
            String reason) {
        tx.transitionTo(PurchaseStatus.REFUND_PENDING);
        tx.setNote(reason);
        transactions.save(tx);

        RefundResult refund = payments.refund(
                tx.id() + ":refund", tx.id(), refundAmount);

        if (refund.status() == OperationStatus.SUCCEEDED) {
            inventory.release(reservationId);
            tx.transitionTo(PurchaseStatus.REFUNDED);
        } else {
            // Do not claim a refund happened when its outcome is failed/unknown.
            tx.transitionTo(PurchaseStatus.REFUND_PENDING);
            tx.setNote(reason + "; refund requires follow-up");
        }
        transactions.save(tx);
    }
}
```

### Important caveats about this teaching flow

1. `acceptPayment()` is modeled as one operation for simplicity. Real cash hardware often accepts denominations incrementally; define the contract before coding.
2. This sample does not implement a complete reconciliation worker. For `UNKNOWN`, persist enough information to query the device later and resume the correct branch.
3. A real system should persist intent before every external side effect and record the confirmed result afterward. The sample shows save calls to communicate that intent, but a durable implementation needs transactional storage and crash-recovery rules.
4. The sample's repository must return the same transaction on duplicate client requests if those requests represent the same purchase. A new random ID on every incoming retry is not sufficient. In production, accept a client/request idempotency key or create the transaction before the request can be retried.
5. The adapter must define the meaning of `FAILED` versus `UNKNOWN`. Never infer “not dispensed” from a timeout alone.
6. If the change result is `UNKNOWN`, do not blindly submit a new payout with a new operation ID. Query/reconcile the original operation.
7. For brevity, state-transition validation and exception handling are omitted. They should be added if the interviewer asks for implementation-level completeness.

## 25.7 Purchase Flow in One View

```text
Create transaction
       |
       v
Reserve stock atomically
       |
       v
Accept payment
  | failed / unknown
  |--------------------> release only when safe / reconcile
       |
       v
Enough money?
  | no
  v
Refund accepted amount
  | confirmed -> release reservation -> REFUNDED
  | unknown  -> REFUND_PENDING
       |
       v yes
Request dispense with stable transaction ID
  | DISPENSED
  |     v
  |  Commit reservation
  |     v
  |  Return change if due
  |     | confirmed -> COMPLETED
  |     | unresolved -> CHANGE_PENDING
  |
  | NOT_DISPENSED
  |     v
  |  Refund accepted amount
  |     | confirmed -> release reservation -> REFUNDED
  |     | unresolved -> REFUND_PENDING
  |
  | UNKNOWN
  v
RECONCILIATION_REQUIRED
(keep reservation; do not blindly refund or retry)
```

## 25.8 Interview Coding Checklist

When writing the code on a whiteboard or in an editor, implement in this order:

1. `Money` and `Item`.
2. `Inventory` API and an atomic `reserve()` implementation.
3. `DispenseOutcome` with all three outcomes.
4. Payment and dispenser interfaces.
5. `PurchaseTransaction` and explicit states.
6. The happy path through `VendingMachine`.
7. Confirmed dispense failure and refund handling.
8. Unknown dispense outcome and reconciliation state.
9. Change-payout failure.
10. Tests for the last inventory unit, duplicate operations, and every outcome branch.

**Do not start by coding every class.** First explain the invariants and workflow; then implement the smallest set of classes that makes those invariants enforceable.
