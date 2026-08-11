# Java Core Library — Chapter 1
## Basics of Java Programming — Interview Study & Revision Notes

> **Source:** `04-core-library.pdf` — Chapter 1, Q1–Q40.
>
> **Study goal:** Do not memorize 40 isolated answers. Build one mental model, then use the follow-ups as active-recall checks.
>
> The source organizes every question as: question → 30-second answer → thought process → edge cases → what NOT to say → common follow-up.

---

# 1. Master Mental Model

```text
Java
│
├── Types
│   ├── Primitive: byte short int long float double char boolean
│   └── Reference: classes, interfaces, arrays, enums, String
│
├── Expressions
│   ├── promotion
│   ├── casting
│   ├── arithmetic
│   ├── logical / bitwise
│   └── precedence
│
├── Control flow
│   ├── if / switch
│   ├── for / enhanced-for
│   ├── while / do-while
│   ├── break / continue
│   └── instanceof
│
├── Class semantics
│   ├── final
│   ├── static
│   ├── enum
│   └── packages / imports
│
├── Runtime
│   ├── .java
│   ├── javac
│   ├── .class bytecode
│   ├── JVM
│   └── interpreter + JIT
│
└── Precision / identity
    ├── String pool
    ├── == vs equals
    ├── integer overflow
    ├── double / IEEE 754
    └── BigDecimal
```

---

# Q1 — Primitive vs Reference Types

### Question

What's the difference between primitive types and reference types? Walk me through what's happening in memory.

### Interview answer

Java has **8 primitive types**. A primitive variable represents the primitive value directly. A reference variable holds a reference to an object.

The common stack/heap model is useful, but don't say primitives are *always* on the stack: a primitive field can live inside an object.

Java is **always pass-by-value**. With an object, the value being copied is the reference. Therefore a method can mutate the referenced object, but reassigning its parameter does not change the caller's reference.

### Example

```java
void change(List<Integer> list) {
    list.add(10);              // caller sees the mutation
}

void reassign(List<Integer> list) {
    list = new ArrayList<>();  // caller's reference unchanged
}
```

### Edge cases

- Arrays are reference types even when they contain primitives.
- `null` applies to references, not primitives.
- Primitive fields get defaults; local primitive variables do not.

### What NOT to say

> "Java is pass-by-reference for objects."

Wrong.

> "Primitives always live on the stack."

Too simplistic.

### Common follow-up

**If Java is pass-by-value, how can a method modify the contents of a List I passed in?**

**Answer:** The method receives a copy of the reference. Both the caller and callee references point to the same List object, so mutations through either reference affect that same object. Reassigning the callee's reference only changes the local copy.

### Memory hook

**Primitive = value. Reference = reference to object. Java always passes by value.**

---

# Q2 — The 8 Primitive Types

### Question

Name all primitive types with their sizes and defaults.

| Type | Size | Default |
|---|---:|---|
| `byte` | 8-bit | `0` |
| `short` | 16-bit | `0` |
| `int` | 32-bit | `0` |
| `long` | 64-bit | `0L` |
| `float` | 32-bit | `0.0f` |
| `double` | 64-bit | `0.0d` |
| `char` | 16-bit | `'\u0000'` |
| `boolean` | JVM-dependent | `false` |

### Important

- `int`, `long`, etc. have language-defined widths.
- `char` is a 16-bit UTF-16 code unit.
- The Java specification does **not** mandate a storage size for `boolean`.

### Edge cases

```java
long x = 10_000_000_000L;
float f = 3.14f;
char c = 65;       // 'A'
```

### Common follow-up

**What happens if you assign an integer literal larger than `int` range without `L`?**

**Answer:** Integer literals are `int` by default. If the literal itself is outside the `int` range, the compiler rejects it. Use an `L` suffix to make it a `long` literal.

### Memory hook

**4 integer + 2 floating + char + boolean = 8.**

---

# Q3 — Autoboxing and Unboxing

### Question

What are autoboxing and unboxing?

### Answer

```text
int → Integer     boxing
Integer → int     unboxing
```

The compiler inserts the wrapper conversion automatically.

```java
Integer x = 10;   // boxing
int y = x;        // unboxing
```

### NPE trap

```java
Integer balance = null;
int amount = balance; // NullPointerException
```

Conceptually:

```java
int amount = balance.intValue();
```

### Common follow-up

**Why can unboxing a null wrapper throw NPE?**

**Answer:** Unboxing requires obtaining the primitive value from the wrapper. A null wrapper has no object/value to unwrap, so the compiler-generated unboxing call dereferences `null`.

### Memory hook

**Boxing wraps. Unboxing unwraps. Null + unboxing = NPE.**

---

# Q4 — Type Promotion

### Question

Why does `byte + byte` become `int`?

### Answer

In arithmetic, `byte`, `short`, and `char` are generally promoted to `int`.

```java
byte a = 10;
byte b = 20;

var x = a + b;  // x is int
```

Therefore:

```java
byte c = a + b; // compile error
```

unless explicitly cast.

### Common follow-up

**Why does `int total = 2_000_000_000 * 3` produce a negative number?**

**Answer:** Both operands are `int`, so multiplication happens using 32-bit integer arithmetic. The result overflows before assignment to `total`. The assignment cannot recover information already lost.

Use:

```java
long total = 2_000_000_000L * 3;
```

### Memory hook

**byte/short/char arithmetic → int.**

---

# Q5 — Widening vs Narrowing Casting

### Answer

**Widening** goes from a smaller range/type to a larger one and is usually implicit.

```java
int x = 10;
long y = x;
```

**Narrowing** can lose range/precision and requires an explicit cast.

```java
double price = 99.95;
int x = (int) price; // 99
```

Casting `double` to `int` **truncates toward zero**; it does not round.

Reference casts work similarly:

```text
Cat → Animal      upcast, implicit
Animal → Cat      downcast, explicit
```

A bad downcast can throw `ClassCastException`.

### Common follow-up

**How would you safely check before downcasting?**

```java
if (animal instanceof Cat cat) {
    cat.purr();
}
```

Pattern matching performs the check and binding together.

### Memory hook

**Widening = automatic. Narrowing = explicit and potentially lossy.**

---

# Q6 — Arithmetic Operators

### Answer

Java arithmetic operators:

```text
+  -  *  /  %
```

Important:

```java
7 / 2   // 3
7.0 / 2 // 3.5
7 % 2   // 1
```

Integer division truncates toward zero.

### Common follow-up

**Why does integer division not produce a fractional result?**

**Answer:** The result type is determined by operand types. `int / int` performs integer division, so the fractional part is discarded. At least one operand must be floating-point to get a floating result.

### Edge case

```java
-7 / 3  // -2
-7 % 3  // -1
```

### Memory hook

**`/` divides; `%` gives remainder; int/int stays int.**

---

# Q7 — `&&` vs `&`, `||` vs `|`

### Answer

```text
&& → logical AND + short-circuit
|| → logical OR  + short-circuit

&  → bitwise AND for integers; evaluates both boolean operands
|  → bitwise OR  for integers; evaluates both boolean operands
```

Example:

```java
if (user != null && user.isActive()) {
}
```

If `user == null`, `user.isActive()` is never evaluated.

### Common follow-up

**Why is short-circuiting important?**

**Answer:** It avoids unnecessary work and can prevent errors by not evaluating the second operand when the result is already known.

### Memory hook

**Double symbol = short circuit. Single symbol = evaluate both.**

---

# Q8 — Bitwise Operators

### Operators

```text
&   AND
|   OR
^   XOR
~   complement
<<  left shift
>>  signed right shift
>>> unsigned right shift
```

### Key distinction

```text
>>  preserves the sign bit
>>> fills from the left with zeroes
```

Example:

```java
-1 >> 1   // -1
-1 >>> 1  // 2147483647
```

### Common use

Bit masks:

```java
if ((flags & READ) != 0) {
    ...
}
```

### Memory hook

**`>>` keeps sign; `>>>` zero-fills.**

---

# Q9 — `if-else` vs `switch`

### Answer

Use `switch` when comparing one expression against a set of discrete alternatives.

Use `if-else` when conditions involve ranges or more complex boolean logic.

Modern Java supports switch expressions:

```java
String result = switch (status) {
    case "PAID" -> "Done";
    case "PENDING" -> "Wait";
    default -> "Unknown";
};
```

### Follow-up drill

**Why is switch expression useful?**

**Answer:** It directly produces a value, reduces accidental fall-through with arrow cases, and can make branching logic more declarative.

### Memory hook

**Discrete alternatives → switch. Complex/range conditions → if.**

---

# Q10 — Classic `for` vs Enhanced `for`

### Answer

Classic `for` is best when you need an index or precise iteration control.

```java
for (int i = 0; i < list.size(); i++) {
    ...
}
```

Enhanced `for` is best when you simply need each element.

```java
for (Item item : list) {
    ...
}
```

For arrays, enhanced `for` is implemented as indexed access rather than an `Iterator`.

### Common follow-up

**How do you safely remove elements from a List during iteration?**

Use:

```java
list.removeIf(predicate);
```

or an explicit `Iterator` and its `remove()` method.

Don't structurally modify a normal list directly inside an enhanced-for loop.

### Memory hook

**Need index/control → classic `for`; need values → enhanced `for`.**

---

# Q11 — `while` vs `do-while`

### Answer

```text
while:
check → execute

do-while:
execute → check
```

Therefore:

```text
while    → 0 or more executions
do-while → 1 or more executions
```

### Best use case

Input validation or retry logic where the first attempt is mandatory.

### Common follow-up

**How would you break out of two nested loops at once?**

Use a labeled `break`:

```java
outer:
for (...) {
    for (...) {
        if (...) {
            break outer;
        }
    }
}
```

Alternatively, extract the nested logic into a method and use `return`.

### Memory hook

**`do-while` means "do it once before deciding."**

---

# Q12 — `var`

### Answer

`var` is **local-variable type inference**, introduced in Java 10.

```java
var name = "Java"; // inferred as String
var list = new ArrayList<String>();
```

It is not dynamic typing.

### Cannot use

```java
var x;
var x = null;
```

Also not for:

- fields
- method parameters
- method return types

### Common follow-up

**How is Java `var` different from JavaScript `var`?**

**Answer:** Java `var` is compile-time type inference. Once inferred, the variable has a fixed static type. JavaScript `var` is a runtime/dynamic-language variable declaration with different semantics.

### Memory hook

**`var` hides the type declaration, not the type itself.**

---

# Q13 — `final`

### Three meanings

```text
final variable → cannot be reassigned
final method   → cannot be overridden
final class    → cannot be extended
```

### Critical trap

```java
final List<String> list = new ArrayList<>();

list.add("Java"); // valid
```

`final` freezes the **reference**, not necessarily the object.

### Common follow-up

**Does `final` make an object immutable?**

**Answer:** No. It only prevents reassignment of the variable. Object immutability is a property of the object's class/design.

### Memory hook

**final reference ≠ immutable object.**

---

# Q14 — Constants

Typical form:

```java
public static final int MAX_RETRIES = 3;
```

Use:

```text
UPPER_SNAKE_CASE
```

Java has no usable `const` declaration keyword.

### Compile-time constants

Certain primitive/String `static final` fields initialized with constant expressions may be inlined into client bytecode.

### Follow-up drill

**Why can changing a public compile-time constant require recompiling dependent code?**

**Answer:** Because clients may have the old constant value inlined into their bytecode. Recompiling the library alone may not update those already-compiled clients.

### Memory hook

**Constant = typically `static final`.**

---

# Q15 — Enums

### Answer

A Java enum is a special class with a fixed set of instances.

```java
enum OrderStatus {
    PENDING,
    SHIPPED,
    DELIVERED
}
```

Unlike C-style integer enums, Java enum constants are full objects.

They can have:

- fields
- constructors
- methods
- per-constant behavior
- interface implementations

Enums integrate naturally with `switch`, `EnumSet`, and `EnumMap`.

### Important

Every enum implicitly extends `java.lang.Enum`.

It cannot extend another class, but it can implement interfaces.

### Common follow-up

**Why is enum a recommended way to implement a singleton?**

**Answer:** The JVM controls enum instance creation. Enum serialization preserves enum identity, cloning is prevented, and the usual reflection-based constructor attacks don't create additional enum instances. This gives a concise, robust singleton implementation.

### Memory hook

**Enum = fixed set of real, type-safe objects.**

---

# Q16 — `static`

### Answer

`static` means the member is associated with the class rather than an individual instance.

```text
static field        → shared class-level field
static method       → no implicit this
static block        → class initialization
static nested class → no implicit outer-instance reference
```

### Static method

Cannot directly access instance state because there is no `this`.

### Static methods

They are **hidden**, not overridden.

### Common follow-up

**What's the difference between hiding a static method and overriding an instance method?**

**Answer:** Static method selection is based on the reference/class at compile time; it does not participate in runtime polymorphic dispatch. Instance method overriding uses dynamic dispatch based on the runtime object's class.

### Memory hook

**Object member → instance. Class member → static.**

---

# Q17 — Naming Conventions

| Element | Convention |
|---|---|
| Class/interface/enum | `PascalCase` |
| Method/field/variable/parameter | `camelCase` |
| Constant | `UPPER_SNAKE_CASE` |
| Package | `lowercase.dotted` |
| Generic type | `T`, `E`, `K`, `V`, `R` |

Examples:

```text
OrderService
processOrder()
totalAmount
MAX_RETRIES
com.company.billing
```

### Common follow-up

**Why use reverse-domain package names?**

**Answer:** They reduce naming collisions across organizations because a company controls a domain name and can use its reversed domain as a globally recognizable namespace.

### Memory hook

**Types Pascal; values camel; constants upper snake; packages lowercase.**

---

# Q18 — Packages and Imports

### Answer

A package is a namespace that groups related classes.

```java
package com.company.payment;
```

An import lets you use a simple name instead of repeatedly writing the fully qualified name.

```java
import java.util.List;
```

### Important

`import` does **not** copy or include the class's code.

The classpath/module path determines where classes are found.

`java.lang.*` is automatically available.

### Common follow-up

**What's the difference between an import and a Java 9 module export?**

**Answer:** An `import` is a source-level name-resolution convenience. A module `exports` declaration controls whether a package is accessible to other modules at the module-system level.

### Memory hook

**Package = namespace. Import = naming shortcut.**

---

# Q19 — `public static void main(String[] args)`

### Break it down

```text
public  → launcher can access it
static  → no object instance required
void    → no return value
main    → conventional entry-point name
String[] args → command-line arguments
```

Varargs is also accepted:

```java
public static void main(String... args)
```

because varargs are represented as an array at the method level.

### Common follow-up

**What happens if you change any part of the standard main signature?**

**Answer:** The class may still compile, but the Java launcher will not recognize the changed method as the standard entry point. You can overload `main`, but the recognized `String[]`/`String...` entry point must exist.

### Memory hook

**Public + static + void + main + String[].**

---

# Q20 — `String[] args`

Running:

```bash
java MyApp hello world
```

gives:

```text
args[0] = "hello"
args[1] = "world"
```

`args.length == 2`.

With no arguments, `args` is an empty array, not `null`.

### Common follow-up

**Is `args[0]` the program name like C's `argv[0]`?**

**Answer:** No. In Java, `args` contains the command-line arguments supplied after the class name. The launcher does not put the Java program/class name into `args[0]`.

### Memory hook

**Java `args[0]` = first user argument.**

---

# Q21 — Compilation vs Execution

```text
.java source
    │
    │ javac
    ↓
.class bytecode
    │
    │ java
    ↓
JVM
    │
    ├── class loading
    ├── verification
    ├── initialization
    └── execution
             │
             ├── interpreter
             └── JIT compiler → native machine code
```

### Answer

`javac` compiles Java source into JVM bytecode. The JVM loads and executes that bytecode. Frequently executed/hot code may be compiled to native machine code by the JIT.

### Common follow-up

**Why does Java need a JIT if `javac` already compiles the code?**

**Answer:** `javac` produces platform-independent JVM bytecode. The JIT can use runtime information about the actual workload and machine to optimize hot code specifically for that environment.

### Memory hook

**`javac` → bytecode; JVM → execution; JIT → hot native code.**

---

# Q22 — Classpath

### Answer

The classpath tells Java where classes and JAR files can be found.

Example:

```bash
java -cp lib/foo.jar:./classes MyApp
```

### Important distinction

```text
ClassNotFoundException
→ requested class cannot be found by the class loader

NoClassDefFoundError
→ a required class definition could not be loaded/initialized as expected at runtime
```

### Common follow-up

**Why can code compile successfully but fail with `NoClassDefFoundError` at runtime?**

**Answer:** The dependency may have been available on the compile-time classpath but missing, incompatible, or failed during initialization on the runtime classpath.

### Memory hook

**Classpath = runtime/compile-time search locations for classes and JARs.**

---

# Q23 — `Math`

Useful methods:

```text
abs
min / max
pow
sqrt
floor / ceil / round
random
PI / E
addExact / multiplyExact
```

All ordinary `Math` methods are static.

### Important traps

```java
Math.pow(2, 10) // 1024.0, a double
Math.sqrt(16)   // 4.0
Math.round(2.5) // 3
```

`Math.round` is not banker's rounding.

For concurrent random integer generation, `ThreadLocalRandom` is generally preferable to `Math.random()`.

### Common follow-up

**Why would you use `ThreadLocalRandom` instead of `Math.random()`?**

**Answer:** It is designed for concurrent use without the shared contention characteristics of `Math.random()`, and it directly provides bounded integer/long generation.

### Memory hook

**`Math` = static numeric utility methods.**

---

# Q24 — Why `0.1 + 0.2 != 0.3`

### Answer

`double` uses IEEE 754 binary floating point.

Many decimal fractions, including `0.1` and `0.2`, cannot be represented exactly in binary. Java therefore stores nearby approximations.

So:

```java
0.1 + 0.2
```

can produce:

```text
0.30000000000000004
```

### For comparisons

Use a tolerance where approximation is expected:

```java
Math.abs(a - b) < 1e-9
```

### For money

Use `BigDecimal`.

### Common follow-up

**Walk me through using BigDecimal for a simple price calculation.**

```java
BigDecimal price = new BigDecimal("19.99");
BigDecimal tax = new BigDecimal("0.18");

BigDecimal total = price.add(price.multiply(tax));
```

Use decimal strings for exact decimal construction.

### Memory hook

**Binary floating point ≠ exact decimal arithmetic.**

---

# Q25 — `BigDecimal` vs `double`

### Answer

Use `BigDecimal` for:

- money
- tax
- billing
- accounting
- audit-sensitive decimal calculations

`double` is appropriate for many scientific/engineering/statistical calculations where approximation is acceptable.

### Critical construction rule

```java
new BigDecimal("0.1") // correct decimal representation
new BigDecimal(0.1)   // captures the binary floating-point approximation
```

### Immutability

```java
BigDecimal total = BigDecimal.ZERO;
total.add(price); // does NOT change total
```

Correct:

```java
total = total.add(price);
```

### Equality trap

```java
new BigDecimal("1.0").equals(new BigDecimal("1.00"))      // false
new BigDecimal("1.0").compareTo(new BigDecimal("1.00"))  // 0
```

### Common follow-up

**Why shouldn't you use `new BigDecimal(0.1)`?**

**Answer:** `0.1` is already an inexact binary floating-point value. The constructor receives that approximation and represents it exactly, preserving the floating-point error. Passing `"0.1"` constructs the intended decimal value exactly.

### Memory hook

**Money → BigDecimal; construct from String; remember immutability.**

---

# Q26 — `i++` vs `++i`

### Answer

```text
i++ → use old value, then increment
++i → increment, then use new value
```

Example:

```java
int i = 5;
int x = i++; // x=5, i=6
```

```java
int i = 5;
int x = ++i; // x=6, i=6
```

In a normal `for` increment slot, the difference is irrelevant because the returned expression value is discarded.

### Common follow-up

**What does `int i = 5; i = i++;` produce?**

**Answer:** `i` remains `5`.

The postfix expression returns the old value `5`, increments the variable to `6`, and then the assignment writes the saved old value `5` back.

### Memory hook

**Postfix returns old. Prefix returns new.**

---

# Q27 — Ternary Operator

### Answer

```java
condition ? valueIfTrue : valueIfFalse
```

It is an expression that produces a value.

Good:

```java
String label = isPaid ? "Done" : "Pending";
```

Avoid deeply nested ternaries.

### Important

Only the selected branch is evaluated.

### Common follow-up

**How would you rewrite a deeply nested ternary cleanly?**

**Answer:** Prefer an `if-else` chain, a switch expression, or extract the decision into a named method. The goal is to make the business rule readable rather than compressing everything into one expression.

### Memory hook

**Ternary = short, value-producing conditional.**

---

# Q28 — `break`, `continue`, Labels

### Answer

```text
break    → exits current loop/switch
continue → skips to next iteration
label    → lets break/continue target an outer labeled statement
```

Example:

```java
outer:
for (...) {
    for (...) {
        if (...) {
            break outer;
        }
    }
}
```

### Common follow-up

**What's a cleaner alternative to a labeled break?**

**Answer:** Often extract the nested search into a separate method and use `return`. If the loop is part of a larger expression, restructuring the logic can also remove the need for labels.

### Memory hook

**break = leave. continue = next. label = choose which loop.**

---

# Q29 — `instanceof` and Pattern Matching

### Answer

Classic:

```java
if (animal instanceof Cat) {
    Cat cat = (Cat) animal;
    cat.purr();
}
```

Modern Java:

```java
if (animal instanceof Cat cat) {
    cat.purr();
}
```

Pattern matching combines:

```text
type check + cast + variable binding
```

`null instanceof Cat` is `false`.

### Common follow-up

**What did Java 16 change?**

**Answer:** Pattern matching for `instanceof` became a standard feature. It allows the type test and cast to be combined, with the pattern variable scoped only where the compiler knows the test succeeded.

### Memory hook

**`instanceof Cat cat` = check + cast + bind.**

---

# Q30 — String Concatenation

### Answer

Simple concatenation with `+` is fine.

Repeated concatenation inside a loop can create many intermediate Strings.

Prefer:

```java
StringBuilder sb = new StringBuilder();

for (String item : items) {
    sb.append(item);
}
```

Since Java 9, ordinary string concatenation is implemented through `invokedynamic` / `StringConcatFactory`, allowing the runtime to optimize it.

### Common follow-up

**Why can repeated `String +` in a loop become O(n²)?**

**Answer:** Strings are immutable. Each concatenation can require creating a new String containing the previous accumulated content plus the new value. As the accumulated string grows, repeated copying can produce quadratic total work. `StringBuilder` maintains mutable character data and avoids that repeated reconstruction.

### Memory hook

**String immutable; loop concatenation → StringBuilder.**

---

# Q31 — Field Defaults vs Local Variables

### Answer

Fields get automatic defaults:

```text
int      → 0
boolean  → false
reference → null
char     → '\u0000'
```

Local variables get **no default** and must be definitely assigned before use.

```java
int counter;
System.out.println(counter); // compile error
```

Arrays also initialize their elements to defaults.

### Common follow-up

**Why does Java not give local variables defaults like fields?**

**Answer:** Java's compiler performs definite-assignment analysis for locals. Requiring explicit initialization catches accidental use-before-assignment. Fields, by contrast, are part of object/class state and are initialized as part of object/class initialization.

### Memory hook

**Fields default. Locals must be assigned. Arrays default.**

---

# Q32 — Operator Precedence

Example:

```java
5 + 3 * 2 == 11
```

Evaluate:

```text
3 * 2 = 6
5 + 6 = 11
11 == 11 → true
```

### Simplified precedence

```text
unary
*
/
%
+
-
shifts
relational / instanceof
equality
&
^
|
&&
||
?:
assignment
```

### Important

Precedence determines grouping; evaluation order is a separate concept.

Use parentheses when the expression is non-obvious.

### Memory hook

**Unary → arithmetic → shifts → relational → equality → bitwise → logical → ternary → assignment.**

---

# Q33 — String Pool and `==`

### Answer

String literals are interned.

```java
String a = "hello";
String b = "hello";

a == b // true
```

They can point to the same pooled String.

But:

```java
String a = new String("hello");
String b = new String("hello");

a == b // false
```

`.equals()` compares content.

### Rule

```text
==       → reference identity
equals() → logical content
```

### Common follow-up

**When would you use `intern()`?**

**Answer:** `intern()` returns the canonical pooled representation of a string. It can be useful when explicit canonicalization/deduplication is justified, but careless interning can increase memory pressure because pooled strings have long-lived reachability.

### Memory hook

**Strings: content → `.equals()`, identity → `==`.**

---

# Q34 — Integer Overflow

### Answer

Java integer arithmetic normally wraps on overflow.

```java
int x = Integer.MAX_VALUE;
x++;
```

produces:

```text
Integer.MIN_VALUE
```

### Detect/prevent

```java
Math.addExact(a, b);
Math.subtractExact(a, b);
Math.multiplyExact(a, b);
```

These throw `ArithmeticException` on overflow.

For larger ranges use `long` or `BigInteger`.

### Classic binary-search bug

Bad:

```java
int mid = (low + high) / 2;
```

Safe:

```java
int mid = low + (high - low) / 2;
```

### Common follow-up

**Walk through the classic binary-search overflow bug.**

**Answer:** If `low` and `high` are both large positive integers, `low + high` can exceed `Integer.MAX_VALUE` and wrap negative. Subtracting first keeps the intermediate value within the range when `low <= high`.

### Memory hook

**Java int overflow wraps unless you use `Math.*Exact`.**

---

# Q35 — Enums With Behavior

### Answer

An enum constant can override an abstract method:

```java
enum Operation {
    ADD {
        public int apply(int a, int b) {
            return a + b;
        }
    },
    SUB {
        public int apply(int a, int b) {
            return a - b;
        }
    };

    public abstract int apply(int a, int b);
}
```

Each constant can provide its own behavior.

This can replace a large switch with polymorphic dispatch.

### Common follow-up

**Why can each enum constant override a method?**

**Answer:** Each constant-specific class body represents a specialized enum constant implementation. The enum's abstract method forces every constant to provide the required behavior.

### Memory hook

**Enums can encapsulate both data and behavior.**

---

# Q36 — `null`

### Answer

`null` belongs to the reference side of Java's type system.

Valid:

```java
String s = null;
Integer x = null;
```

Invalid:

```java
int x = null;
```

Also:

```java
null instanceof String // false
```

### Common follow-up

**Why does `Integer x = null; int y = x;` throw NPE?**

**Answer:** Assigning `x` to primitive `int` triggers unboxing. The compiler effectively calls `x.intValue()`, which dereferences null.

### Memory hook

**`null` is for references; unboxing null is dangerous.**

---

# Q37 — Static Blocks

### Answer

A static block executes during class initialization.

```java
class Config {
    static {
        // initialization
    }
}
```

Multiple static initializers execute in textual order along with static field initialization.

### Important

This is class initialization, not "once per object."

Initialization problems can result in `ExceptionInInitializerError`.

### Common follow-up

**When would you use a static block instead of a static field initializer?**

**Answer:** Use a static block when class-level initialization requires multiple statements, control flow, exception handling, or logic that doesn't fit naturally into a single expression.

### Memory hook

**Static block = class initialization logic.**

---

# Q38 — Method Overloading Resolution

### Answer

Overloading is resolved at **compile time**.

A simplified resolution order is:

```text
1. exact / strict fixed-arity match
2. widening
3. boxing/unboxing
4. varargs
```

Example:

```java
void m(int x) {}
void m(long x) {}

m(5); // m(int)
```

### Ambiguity

```java
void m(String x) {}
void m(Integer x) {}

m(null); // ambiguous
```

`null` can match both and neither is more specific.

### Generic erasure trap

These cannot coexist:

```java
void m(List<String> x)
void m(List<Integer> x)
```

because both erase to `m(List)`.

### Common follow-up

**How do you resolve `m(null)` ambiguity?**

Cast the argument:

```java
m((String) null);
```

Now the compiler selects the String overload.

### Memory hook

**Overloading = compile-time selection. Exact → widening → boxing → varargs.**

---

# Q39 — Real `do-while` Use Case

### Best examples

- input validation
- retry attempts
- operations where the first attempt is mandatory

```java
do {
    result = callService();
} while (!result.success() && attempts++ < 3);
```

### Common follow-up

**Why is `do-while` more expressive than `while` for retries?**

**Answer:** The first attempt is a required action. Only after that attempt can the program inspect the result and decide whether another attempt is necessary.

### Memory hook

**Mandatory first attempt → do-while.**

---

# Q40 — Integrated Code Walkthrough

```java
int[] amounts = {100, 200, 300};

int total = 0;

for (int amount : amounts) {
    total += amount;
}

System.out.println(total);
```

### Line by line

```text
int[] amounts = {100, 200, 300};
```

Creates an array object containing three ints. `amounts` is a reference to that array.

```text
int total = 0;
```

Local primitive with explicit initialization.

```text
for (int amount : amounts)
```

Enhanced-for over an array. Conceptually it performs indexed access.

```text
total += amount;
```

Equivalent here to:

```text
total = total + amount;
```

```text
System.out.println(total);
```

Prints:

```text
600
```

### Edge cases

- `amounts == null` → NPE during iteration.
- Sum can overflow `int`.
- For a very large sum, use `long`.
- Arrays do not use an `Iterator`; the compiler generates array-index access.

### Common follow-up

**Rewrite this using a Stream.**

```java
int total = Arrays.stream(amounts).sum();
```

For a long sum:

```java
long total = Arrays.stream(amounts).asLongStream().sum();
```

### Memory hook

**Array → reference; enhanced-for → elements; `+=` → accumulation; output → 600.**

---

# Chapter 1 — High-Value Follow-Up Drill

These are the follow-ups you should be able to answer without looking:

## Type system

### Q: Is Java pass-by-reference?

**No. Always pass-by-value. For objects, the copied value is the reference.**

### Q: Can a primitive field live inside a heap object?

**Yes. A primitive instance field is part of its containing object.**

### Q: Why does `byte + byte` become `int`?

**Binary numeric promotion promotes byte/short/char arithmetic to int.**

### Q: Why does `2_000_000_000 * 3` overflow before assignment to long?

**Because the multiplication is performed as int unless one operand is already long.**

### Q: Does casting `double` to `int` round?

**No. It truncates toward zero.**

---

## Operators

### Q: Why use `&&` instead of `&`?

**Short-circuiting: the right side may not execute, which can save work and prevent unsafe evaluation.**

### Q: Difference between `>>` and `>>>`?

**`>>` sign-extends; `>>>` zero-fills.**

### Q: Does integer overflow throw?

**Not normally. It wraps. Use `Math.*Exact` to detect overflow.**

### Q: Why is `mid = low + (high-low)/2` safer?

**It avoids the potentially overflowing `low + high` intermediate.**

---

## Variables / classes

### Q: Is `var` dynamic typing?

**No. It is compile-time local-variable type inference.**

### Q: Does final make an object immutable?

**No. It prevents reassignment of the variable/reference.**

### Q: Can a final List be modified?

**Yes, if the List itself is mutable.**

### Q: Can static methods be overridden?

**No. They are hidden, not dynamically overridden.**

### Q: Does static mean thread-safe?

**Absolutely not. A shared static mutable field can actually introduce concurrency problems.**

---

## Strings

### Q: Why can `"hello" == "hello"` be true?

**Identical literals are interned and may reference the same pooled String.**

### Q: Should you use `==` for String comparison?

**No. Use `.equals()` for content equality.**

### Q: Why use StringBuilder in loops?

**String is immutable; repeated concatenation can repeatedly copy accumulated content.**

---

## Numbers

### Q: Why is `0.1 + 0.2` not exactly `0.3`?

**IEEE 754 binary floating point cannot exactly represent those decimal fractions.**

### Q: When should you use BigDecimal?

**Exact decimal arithmetic: money, tax, billing, accounting, audit-sensitive values.**

### Q: Why `new BigDecimal("0.1")` instead of `new BigDecimal(0.1)`?

**The String constructor represents the intended decimal exactly; the double constructor preserves the double's prior approximation.**

---

## Runtime

### Q: What does javac produce?

**JVM bytecode in `.class` files.**

### Q: What does the JIT do?

**Compiles hot bytecode into optimized native machine code at runtime.**

### Q: What is the classpath?

**A set of locations where Java tools/class loaders search for classes and JARs.**

### Q: Why can compilation succeed while runtime fails?

**A dependency can exist on the compile-time classpath but be missing or incompatible at runtime.**

---

# Final 15 Questions — Revision Test

Before considering Chapter 1 mastered, answer these from memory:

1. What are Java's 8 primitives?
2. Why is Java pass-by-value?
3. Why does `byte + byte` become `int`?
4. What is widening vs narrowing?
5. Why does `&&` differ from `&`?
6. What is the difference between `>>` and `>>>`?
7. Why isn't `var` dynamic typing?
8. Does `final` mean immutable?
9. What does `static` mean for fields/methods/classes?
10. Why should String content be compared with `.equals()`?
11. Why does `0.1 + 0.2` have precision issues?
12. When should you use `BigDecimal`?
13. What happens on integer overflow?
14. How does Java choose an overloaded method?
15. Explain `.java → .class → JVM → JIT`.

If you can answer these **without opening the notes**, Chapter 1 is in good shape.

---

# 2-Revision Plan

## Revision 1 — Understanding

Read the chapter once and make sure you can explain:

```text
types
→ promotion
→ casting
→ operators
→ control flow
→ var/final/static
→ String identity
→ numeric precision
→ compilation/JVM
```

## Revision 2 — Active Recall

Close the notes.

Explain the 15 revision questions aloud.

Then solve these mentally:

```java
byte a = 10;
byte b = 20;
var x = a + b;
```

**x = int**

```java
Integer x = null;
int y = x;
```

**NPE**

```java
System.out.println(7 / 2);
```

**3**

```java
System.out.println(7.0 / 2);
```

**3.5**

```java
int x = Integer.MAX_VALUE;
x++;
```

**Integer.MIN_VALUE**

```java
String a = "hello";
String b = "hello";
a == b
```

**true for the interned literals**

```java
int i = 5;
i = i++;
```

**5**

```java
System.out.println(-1 >> 1);
```

**-1**

```java
System.out.println(-1 >>> 1);
```

**2147483647**

---

# One-Page Memory Sheet

```text
8 PRIMITIVES
byte short int long
float double char boolean

JAVA
always pass-by-value

PROMOTION
byte/short/char → int

CASTING
widening → implicit
narrowing → explicit
double → int = truncate

ARITHMETIC
7/2 = 3
7.0/2 = 3.5
7%2 = 1
overflow = wrap

LOGICAL
&& / || = short circuit
& / | = evaluate both boolean operands

SHIFT
>>  = sign extension
>>> = zero fill

LOOPS
for = control/index
enhanced-for = values
while = 0+
do-while = 1+

var
= compile-time local type inference

final
variable = no reassignment
method = no override
class = no extension
final reference ≠ immutable object

static
field = class-level
method = no this
block = class initialization
nested class = no implicit outer reference

ENUM
fixed type-safe objects
can contain data + behavior

STRING
== = reference identity
equals = content
literal = pooled/interned
loop concatenation = StringBuilder

NULL
reference only
unboxing null = NPE

DOUBLE
IEEE 754
0.1 + 0.2 ≠ exact 0.3

MONEY
BigDecimal
construct from String
immutable
compareTo for numeric comparison

OVERFLOW
normal int arithmetic wraps
Math.*Exact → ArithmeticException

OVERLOADING
compile time
exact → widening → boxing → varargs

INSTANCEOF
check + cast
Java 16 pattern:
obj instanceof Cat cat

COMPILE
.java → javac → .class
.class → JVM
hot code → JIT → native

CLASSPATH
where classes/JARs are found
```

---

## Source note

This chapter is based on **Chapter 1 of `04-core-library.pdf` (Q1–Q40)**. The source explicitly includes a common-follow-up section for each interview question; where a follow-up is explicitly present in the retrieved source, it is incorporated above. The source's Q1–Q40 organization and examples are preserved rather than replacing them with an unrelated Java syllabus.
