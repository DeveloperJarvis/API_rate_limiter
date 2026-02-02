# API Rate Limiter – Public API

This document describes the **logical API contract** exposed by the
API Rate Limiter library.

The library is framework-agnostic and can be used in:

- API gateways
- Middleware layers
- Background services
- Internal microservices

---

## 1. Core Entry Point

### RateLimiterManager

The `RateLimiterManager` is the primary interface used by applications.

```python
decision = rate_limiter.allow_request(request)
```

---

## 2. Request Model

### Request

```python
Request(
    client_id: str,
    endpoint: str,
    api_key: Optional[str],
    user_id: Optional[str],
    ip_address: Optional[str],
    timestamp: Optional[float]
)
```

#### Fields

| Field      | Description                      |
| ---------- | -------------------------------- |
| client_id  | Canonical client identity        |
| endpoint   | API endpoint being accessed      |
| api_key    | Authenticated API key (optional) |
| user_id    | User identifier (optional)       |
| ip_address | Client IP address (optional)     |
| timestamp  | Request timestamp (optional)     |

> **Note:** Rate limiting decisions should be based on authenticated
> identity, not client-provided counters.

---

## 3. Response Model

### RateLimitDecision

```python
RateLimitDecision(
    allowed: bool,
    remaining: int,
    retry_after: Optional[float]
)
```

#### Fields

| Field       | Description                               |
| ----------- | ----------------------------------------- |
| allowed     | Whether the request is allowed            |
| remaining   | Remaining tokens or queue capacity        |
| retry_after | Seconds until next request may be allowed |

---

## 4. Algorithms Supported

### Token Bucket (Default)

- Allows burst traffic
- Tokens refill at fixed rate
- Best for public APIs

### Leaky Bucket

- Smooths traffic
- Fixed throughput
- Best for internal services

---

## 5. Configuration

### RateLimitConfig

```python
RateLimitConfig(
    capacity: int,
    refill_rate: float
)
```

| Field       | Meaning                            |
| ----------- | ---------------------------------- |
| capacity    | Max tokens / queued requests       |
| refill_rate | Tokens added or drained per second |

---

## 6. Error Handling

- Exceeded limits return logical **HTTP 429**
- `retry_after` is populated when applicable
- No exceptions are thrown for normal throttling

---

## 7. Thread Safety

- One logical bucket per client
- Per-client locking
- No global locks
- Deterministic behavior under concurrency

---

## 8. Extensibility

The system is designed for extension:

- New algorithms (Sliding Window, Fixed Window)
- Distributed repositories (Redis, DynamoDB)
- Custom identity extraction strategies

---

## 9. Observability

Exposed signals include:

- Allowed vs rejected requests
- Per-client usage patterns
- Throttling events

These are critical for production readiness.

---

## 10. Design Principles

- Explicit over implicit
- Deterministic over probabilistic
- Correctness over micro-optimizations
- Clean separation of concerns

---

## Summary

This API provides a **simple, deterministic, and concurrency-safe**
interface for enforcing rate limits in backend systems.
