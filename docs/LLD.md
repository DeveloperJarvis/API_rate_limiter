# 📉 Low-Level Design (LLD): API Rate Limiter

**Algorithm:** Token Bucket / Leaky Bucket
**Language Context:** Python (conceptual, no code)

---

## 1. Problem Statement

Design an **API Rate Limiter** that controls the number of requests a client can make within a given time window.

### Goals

- Prevent abuse and overload
- Ensure fair usage across clients
- Support concurrent requests
- Be accurate under high load

---

## 2. Functional Requirements

- Limit requests **per client** (API key / user / IP)
- Allow **bursty traffic** within configured limits
- Reject or delay requests exceeding limits
- Work correctly under **concurrent access**
- Support dynamic configuration (per endpoint / per user tier)

---

## 3. Non-Functional Requirements

- Low latency
- Thread-safe
- Horizontally scalable
- Deterministic behavior
- Minimal memory overhead

---

## 4. High-Level Architecture

```
Client Request
      ↓
API Gateway / Middleware
      ↓
Rate Limiter
      ↓
Allowed → Forward to API
Denied  → 429 Too Many Requests
```

The **Rate Limiter** runs as:

- In-process middleware (single instance), or
- Distributed service (shared state store)

---

## 5. Core Concepts

### Rate Limit Definition

Example:

- **Capacity:** 100 tokens
- **Refill rate:** 10 tokens / second

---

## 6. Token Bucket Algorithm (Primary)

### Concept

- Each client has a **bucket of tokens**
- Tokens are added at a fixed rate
- Each request consumes one token
- If no tokens → request is rejected

---

## 7. Data Model

### RateLimitConfig

- capacity
- refill_rate (tokens/sec)
- burst_allowed (implicit via capacity)

### TokenBucket

- current_tokens
- last_refill_timestamp
- capacity
- refill_rate
- lock / synchronization primitive

### ClientRateState

- client_id
- bucket reference
- metadata (tier, endpoint rules)

---

## 8. Request Flow (Token Bucket)

1. Incoming request arrives
2. Identify client (API key / IP / user ID)
3. Fetch client’s TokenBucket
4. Refill tokens based on elapsed time
5. Check token availability
6. If token exists:
   - Consume 1 token
   - Allow request

7. Else:
   - Reject with HTTP 429

---

## 9. Refill Logic (Conceptual)

- Calculate `elapsed_time = now - last_refill_time`
- Compute `new_tokens = elapsed_time × refill_rate`
- Update:
  - `current_tokens = min(capacity, current_tokens + new_tokens)`
  - `last_refill_time = now`

---

## 10. Concurrency & Thread Safety

### Challenges

- Multiple requests from same client simultaneously
- Race conditions on token updates

### Solutions

- Per-client lock
- Atomic updates
- Serialized access via event queue
- Compare-and-swap in shared store

### Design Choice

> **One lock per bucket**, not global lock (prevents contention)

---

## 11. Leaky Bucket Algorithm (Alternative)

### Concept

- Requests enter a bucket (queue)
- Bucket leaks requests at a constant rate
- If bucket overflows → request rejected

### Differences vs Token Bucket

| Feature       | Token Bucket | Leaky Bucket    |
| ------------- | ------------ | --------------- |
| Burst support | Yes          | No              |
| Smoothing     | No           | Yes             |
| Complexity    | Medium       | Simple          |
| Use case      | APIs         | Traffic shaping |

---

## 12. When to Choose Which

### Token Bucket

- Public APIs
- Bursty traffic allowed
- User-facing services

### Leaky Bucket

- Internal services
- Strict throughput control
- Smoothing traffic spikes

---

## 13. Distributed Rate Limiting

### Problem

Multiple API servers must share rate state.

### Solutions

#### Central Store

- Redis / Memcached
- Bucket state stored per client
- Atomic operations for token updates

#### Hybrid

- Local in-memory buckets
- Periodic sync to central store
- Approximate enforcement

---

## 14. Failure Handling

- Store unavailable → fail open or fail closed
- Clock skew handling
- Bucket reset on corruption
- Graceful degradation

---

## 15. API Design (Logical)

### Input

- client_id
- endpoint
- timestamp

### Output

- allowed (boolean)
- retry_after (seconds)
- remaining_tokens

---

## 16. Configuration Strategy

- Global defaults
- Per endpoint overrides
- Per user tier limits
- Runtime reloadable configs

---

## 17. Observability

- Metrics:
  - Allowed vs rejected requests
  - Per-client usage
  - Token refill rate

- Logs:
  - Throttled requests

- Alerts:
  - High rejection rate

---

## 18. Edge Cases

- Clock jumps
- Long idle periods
- Token overflow
- Client identity spoofing

---

## 19. Security Considerations

- Authenticated client identity
- Rate limit by API key, not IP alone
- Prevent bucket flooding via fake clients

---

## 20. Tradeoffs

| Decision          | Tradeoff                  |
| ----------------- | ------------------------- |
| In-memory buckets | Fast but not shared       |
| Distributed store | Accurate but slower       |
| Token bucket      | Flexible but more complex |
| Leaky bucket      | Simple but restrictive    |

---

## 21. Summary

This design:

- Enforces fair API usage
- Handles concurrency safely
- Supports bursty workloads
- Scales horizontally
- Uses deterministic algorithms

**Token Bucket** is preferred for most API rate limiting use cases.
