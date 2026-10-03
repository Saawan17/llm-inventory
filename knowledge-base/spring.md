# Spring Framework and Spring Boot

## Overview
The Spring Framework provides infrastructure for Java applications, including dependency injection, web development, transactions, and data access. Spring Boot simplifies application setup through auto-configuration, starter dependencies, and production-oriented features.

## Dependency injection and IoC
Inversion of Control means the framework manages object creation and wiring. Dependency Injection supplies an object's collaborators rather than requiring it to construct them itself.

Constructor injection is generally preferred:
```java
@Service
public class ProductService {
    private final ProductRepository repository;

    public ProductService(ProductRepository repository) {
        this.repository = repository;
    }
}
```
Spring detects components such as `@Component`, `@Service`, `@Repository`, and `@Controller` through component scanning when configured appropriately.

## Typical web request flow
A common Spring MVC flow is:
1. An HTTP request reaches the servlet container.
2. Spring's `DispatcherServlet` routes it to a matching controller.
3. The controller validates input and calls a service.
4. The service applies business logic and calls repositories or other services.
5. The controller returns a response, often serialized as JSON.

Keep controllers focused on HTTP concerns, services focused on business logic, and repositories focused on persistence.

## REST controllers
```java
@RestController
@RequestMapping("/api/products")
public class ProductController {
    private final ProductService service;

    public ProductController(ProductService service) {
        this.service = service;
    }

    @GetMapping("/{id}")
    public ProductDto getById(@PathVariable String id) {
        return service.getById(id);
    }
}
```
Use DTOs to define API request and response shapes rather than exposing persistence entities directly. Use appropriate HTTP methods and status codes, and validate request bodies with Bean Validation where suitable.

## Configuration
Spring Boot supports properties in `application.properties` or `application.yml`, environment variables, and externalized configuration. Keep secrets such as database passwords and API keys out of committed configuration files.

Example:
```properties
spring.datasource.url=${DB_URL}
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}
```

## Spring Data JPA
Spring Data JPA can generate repository implementations from interfaces:
```java
public interface ProductRepository extends JpaRepository<Product, String> {
    Optional<Product> findByName(String name);
}
```
Use entity relationships carefully. Bidirectional relationships can cause recursive JSON serialization; DTO mapping or deliberate Jackson annotations can prevent this. Define transaction boundaries at suitable service methods and understand lazy loading.

## Spring Security
Spring Security provides authentication and authorization. Authentication establishes who the caller is; authorization determines what that caller may do.

For stateless token-based APIs:
- Configure a `SecurityFilterChain`.
- Define which routes are public and which require authentication or roles.
- Validate tokens and their signature, issuer, audience, and expiry as appropriate.
- Enforce authorization on the server; never trust a role supplied only by the client.
- Use HTTPS in production.
- Store passwords using a dedicated password-hashing function such as BCrypt or Argon2. Passwords should not be reversibly encrypted.
- Protect login, registration, password-reset, and verification flows against abuse.

JWTs are signed tokens, not necessarily encrypted tokens. Do not put secrets or sensitive personal information in their claims.

## Transactions and errors
Use `@Transactional` for operations that must succeed or fail as a unit. Handle expected application errors with clear exception types and map them to consistent HTTP responses, for example with `@ControllerAdvice` and `@ExceptionHandler`. Do not expose stack traces or internal secrets to clients.

## Testing
- Unit-test service logic with JUnit and Mockito.
- Use Spring Boot test support for application-context and integration tests.
- Use MockMvc for many MVC endpoint tests.
- Test authentication, authorization, validation, and error responses—not only successful requests.

## Production considerations
- Use a supported Java and Spring Boot version.
- Configure database connection pools and health checks.
- Add structured logs, metrics, and tracing where appropriate.
- Externalize environment-specific configuration.
- Apply database migrations through a migration tool.
- Set timeouts and sensible retry policies for remote calls.
- Avoid retrying non-idempotent operations unless the operation is designed to tolerate retries.
- Review dependency vulnerabilities and keep dependencies maintained.
