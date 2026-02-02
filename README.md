# 🚦 API Rate Limiter Library

**Token Bucket & Leaky Bucket based API rate limiting system**
_Focus: algorithms, concurrency, API design_

---

## 📌 Overview

This project implements a **server-side API Rate Limiter** using well-known traffic control algorithms such as:

- **Token Bucket**
- **Leaky Bucket**

The library is designed to demonstrate **low-level system design concepts** relevant to backend engineering interviews and real-world API infrastructure.

It focuses on:

- Correctness under concurrency
- Deterministic request handling
- Clean separation of concerns
- Extensible, configuration-driven design

---

## 🎯 Goals

- Prevent API abuse and accidental overload
- Allow controlled burst traffic
- Enforce fair usage across clients
- Work correctly in concurrent environments
- Be adaptable to different deployment models

---

## 🧠 Core Concepts

### Token Bucket Algorithm

- Each client has a bucket of tokens
- Tokens refill at a fixed rate
- Requests consume tokens
- Bursts are allowed up to bucket capacity

### Leaky Bucket Algorithm

- Requests enter a queue-like bucket
- Requests leak at a constant rate
- Excess requests are dropped
- Smooths traffic instead of allowing bursts

---

## 🏗 High-Level Architecture

```
Client Request
      ↓
API Middleware / Gateway
      ↓
Rate Limiter
      ↓
Allowed → API Handler
Denied  → HTTP 429
```

The rate limiter can run as:

- In-process middleware
- Standalone service
- Distributed system backed by shared storage

---

## 🧩 Key Components

### Rate Limiter

- Entry point for request validation
- Applies configured rate limit rules
- Returns allow/deny decisions

### Bucket State

- Tracks current tokens or queue size
- Maintains timestamps for refill/drain logic
- Isolated per client or per key

### Configuration Manager

- Global defaults
- Per-endpoint limits
- Per-client or tier-based overrides

### Concurrency Control

- Ensures atomic updates to bucket state
- Prevents race conditions under parallel requests

---

## 🔄 Request Lifecycle

1. Incoming request arrives
2. Client identity is extracted (API key / IP / user ID)
3. Corresponding bucket state is retrieved
4. Bucket is updated based on elapsed time
5. Request is allowed or rejected
6. Response metadata is returned (remaining quota, retry-after)

---

## ⚙ Concurrency Model

- One logical bucket per client
- Bucket updates are serialized
- Avoids global locks
- Supports multi-threaded and async execution models

---

## 🌐 Distributed Rate Limiting

Supported deployment strategies:

- **Local-only** (in-memory, fastest)
- **Centralized store** (e.g., Redis)
- **Hybrid** (local cache + periodic sync)

Trade-offs between accuracy, latency, and scalability are explicitly considered.

---

## 📊 Observability

The system is designed to expose:

- Allowed vs rejected request counts
- Per-client usage metrics
- Refill and drain rates
- Throttling events

These metrics are critical for production readiness and capacity planning.

---

## 🔐 Security Considerations

- No trust in client-supplied counters
- Rate limiting based on authenticated identity
- Protection against key-spamming attacks
- Optional IP + API key enforcement

---

## 🧪 Intended Use Cases

- API gateways
- Backend services
- Microservices throttling
- Interview system design demonstrations
- Learning concurrency-safe algorithms

---

## 🚫 Non-Goals

- UI or dashboard
- Request authentication
- Billing or quota enforcement
- Network-level traffic shaping

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0 or later (GPL-3.0-or-later)**.

You are free to:

- Use
- Modify
- Redistribute

Under the terms of the GPL license.

See the LICENSE file or visit:
[https://www.gnu.org/licenses/](https://www.gnu.org/licenses/)

---

## 👤 Author

**Developer Jarvis** (Pen Name)
GitHub: [https://github.com/DeveloperJarvis](https://github.com/DeveloperJarvis)

---

## 🏁 Summary

This library demonstrates how to design and reason about an **API rate limiter** with:

- Strong algorithmic foundations
- Concurrency-safe state management
- Clear API boundaries
- Scalable architecture choices

It is ideal for **backend engineers**, **system design interviews**, and **learning how real rate limiters work internally**.
