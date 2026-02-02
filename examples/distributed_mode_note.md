# Distributed Rate Limiting – Design Notes

This document outlines how the rate limiter behaves in
**multi-instance / distributed deployments**.

---

## 1. Problem Statement

In distributed systems:

- Multiple API servers handle requests concurrently
- Rate limit state must be shared
- In-memory buckets are insufficient

---

## 2. Centralized Store Strategy

### Approach

- Store bucket state in a shared data store (e.g., Redis)
- Each request performs:
  - Fetch
  - Atomic update
  - Save

### Benefits

- Strong consistency
- Accurate rate enforcement

### Drawbacks

- Higher latency
- Store becomes a bottleneck
- Requires careful atomicity

---

## 3. Atomicity Guarantees

Bucket updates must be atomic.

Common approaches:

- Redis Lua scripts
- Compare-and-swap (CAS)
- Database transactions

---

## 4. Hybrid Strategy

### Approach

- Local in-memory buckets per instance
- Periodic sync with central store
- Soft enforcement

### Benefits

- Low latency
- High throughput

### Tradeoffs

- Approximate limits
- Short-lived inconsistencies

---

## 5. Failure Handling

| Scenario          | Recommended Behavior            |
| ----------------- | ------------------------------- |
| Store unavailable | Fail-open (public APIs)         |
| Store unavailable | Fail-closed (internal services) |
| Clock skew        | Use monotonic clocks            |
| State corruption  | Reset bucket                    |

---

## 6. Clock Considerations

- Use a shared, monotonic time source
- Avoid system clock jumps
- Prefer server-side timestamps

---

## 7. Sharding Strategy

- Hash client ID → shard
- Co-locate hot keys
- Avoid uneven distribution

---

## 8. Security Concerns

- Do not trust client timestamps
- Protect against key-spamming
- Rate limit unauthenticated traffic separately

---

## 9. When NOT to Use Distributed Limiting

- Single-instance services
- Low-traffic internal tools
- Non-critical endpoints

---

## 10. Summary

Distributed rate limiting is a **tradeoff**:

- Accuracy vs latency
- Consistency vs availability

This library is designed to make those tradeoffs **explicit and configurable**.
