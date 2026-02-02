# 📁 Project Structure — API Rate Limiter Library

```
api_rate_limiter/
│
├── main.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py          # Global & per-endpoint rate limit configs
│   └── constants.py         # Defaults, enums, error codes
│
├── limiter/
│   ├── __init__.py
│   ├── base.py              # Abstract rate limiter interface
│   ├── token_bucket.py      # Token Bucket algorithm logic
│   ├── leaky_bucket.py      # Leaky Bucket algorithm logic
│   └── manager.py           # Chooses algorithm & applies policies
│
├── state/
│   ├── __init__.py
│   ├── bucket.py            # Per-client bucket state model
│   ├── repository.py        # State storage abstraction
│   └── memory_store.py      # In-memory state backend
│
├── concurrency/
│   ├── __init__.py
│   ├── locks.py             # Per-client locking strategy
│   └── clock.py             # Time abstraction (monotonic / mockable)
│
├── middleware/
│   ├── __init__.py
│   └── api_middleware.py    # Framework-agnostic request wrapper
│
├── protocol/
│   ├── __init__.py
│   ├── request.py           # Normalized request model
│   └── response.py          # Allow / deny response model
│
├── observability/
│   ├── __init__.py
│   ├── metrics.py           # Counters & gauges
│   └── logger.py            # Structured logging
│
├── utils/
│   ├── __init__.py
│   └── identifiers.py      # Client key extraction helpers
│
├── tests/
│   ├── unit/
│   │   ├── test_token_bucket.py
│   │   ├── test_leaky_bucket.py
│   │   ├── test_concurrency.py
│   │   └── test_repository.py
│   │
│   ├── integration/
│   │   ├── test_middleware_flow.py
│   │   └── test_multi_client_limits.py
│   │
│   └── load/
│       └── test_high_throughput.py
│
├── docs/
│   ├── design.md            # LLD & algorithm explanation
│   └── api.md               # Logical API contract
│
├── LICENSE
├── README.md
└── setup.py
```

---

## 🧠 Why This Structure Works

### 1. **Algorithm Isolation**

Each rate limiting algorithm lives in its own module:

- Easy comparison
- Easy extension
- No conditional spaghetti

---

### 2. **State vs Logic Separation**

- `limiter/` → **decision making**
- `state/` → **data ownership**
- Enables distributed backends later (Redis, etc.)

---

### 3. **Concurrency Explicitness**

Concurrency is **not hidden**:

- Locks
- Time sources
- Thread safety is intentional and visible

This is _exactly_ what interviewers look for.

---

### 4. **Framework-Agnostic Design**

No Flask/FastAPI hard dependency:

- Works as middleware
- Works as service
- Works in tests

---

### 5. **Production-Grade Testing**

- Unit tests → correctness
- Integration tests → flow
- Load tests → performance

---

## 🎯 Minimal Version (If You Want Simpler)

```
api_rate_limiter/
├── main.py
├── limiter/
├── state/
├── utils/
├── tests/
├── README.md
└── LICENSE
```

---

## 🏁 Interview Takeaway Line

> “I separated rate limiting **algorithms**, **state management**, and **concurrency control** so each concern scales independently.”
