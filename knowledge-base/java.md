# Java

## Overview
Java is a statically typed, object-oriented programming language commonly used for backend services, enterprise applications, Android development, and distributed systems. Java source code is compiled to bytecode, which runs on a Java Virtual Machine (JVM).

## JDK, JRE, and JVM
- **JVM:** Executes Java bytecode and manages runtime services such as memory management and garbage collection.
- **JRE:** The runtime components needed to run Java applications (the exact packaging varies by distribution and Java version).
- **JDK:** Development tools, including the compiler and runtime components.

## Basic program
```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}
```
`main` is the conventional entry point for a simple Java application.

## Core language concepts
- **Variables and types:** Primitive types include `int`, `long`, `double`, `boolean`, and `char`. Reference types include classes, arrays, and interfaces.
- **Classes and objects:** A class defines state and behavior; an object is an instance of a class.
- **Encapsulation:** Keep internal state controlled through access modifiers and methods.
- **Inheritance:** A class can extend another class. Prefer composition when it models the relationship more clearly.
- **Interfaces:** Define contracts that classes can implement.
- **Polymorphism:** A reference to a supertype can refer to an instance of a subtype.
- **Generics:** Provide compile-time type safety for reusable classes and methods, such as `List<String>`.
- **Exceptions:** Use exceptions to represent exceptional conditions. Catch only when you can handle the problem or add useful context.

## Collections
Common interfaces and implementations:
- `List`: Ordered collection; common implementations include `ArrayList` and `LinkedList`.
- `Set`: Collection of unique elements; examples include `HashSet` and `TreeSet`.
- `Map`: Key-value associations; examples include `HashMap` and `TreeMap`.
- `Queue` and `Deque`: Useful for queue and double-ended queue operations.

Choose a collection based on required ordering, uniqueness, lookup behavior, and concurrency needs.

## Streams and lambdas
Streams support declarative processing of collections:
```java
List<String> names = List.of("Asha", "Ravi", "Anu");
List<String> longNames = names.stream()
    .filter(name -> name.length() > 3)
    .toList();
```
A stream pipeline generally consists of a source, intermediate operations, and a terminal operation. Avoid side effects inside stream operations where possible.

## Concurrency
Java supports concurrency through threads, executors, synchronization primitives, and higher-level concurrency APIs. Prefer managed executors and thread-safe designs over manually creating unbounded threads. Understand race conditions, visibility, deadlocks, and safe publication.

## Build tools
- **Gradle:** Uses build scripts such as `build.gradle` or `build.gradle.kts`.
- **Maven:** Uses `pom.xml`.
Build tools resolve dependencies, compile code, run tests, and package applications.

## Testing
JUnit is a common Java testing framework. Mockito can create test doubles for dependencies. Unit tests should verify behavior and edge cases; integration tests verify collaboration with real infrastructure or appropriately configured substitutes.

## Good practices
- Use meaningful names and small, cohesive methods.
- Prefer immutable values where practical.
- Program to interfaces when it improves flexibility.
- Use try-with-resources for `AutoCloseable` resources.
- Avoid catching and ignoring exceptions.
- Keep credentials outside source control.
- Validate input at system boundaries.
- Use dependency injection for service dependencies in application frameworks.
