# What is pyfplib?

**pyfplib** is a tiny, Rust-inspired functional programming library for Python. It provides explicit types for optional values and fallible operations, along with a set of composable helpers for working with sequences.

| Layer | Module | Purpose |
|---|---|---|
| **Option** | `pyfplib.option` | Represents a value that may be absent: `Some(value)` or `Nothing()` |
| **Result** | `pyfplib.result` | Represents success or failure: `Ok(value)` or `Err(error)` |
| **Functions** | `pyfplib.functools` | Sequence helpers such as `fold`, `find`, `any_of`, and `all_of` |

## Design Principles

- **Explicit over implicit** — absence and failure are values, not hidden `None` checks or scattered exceptions.
- **Composable** — `map`, `and_then`, `or_else`, and operator overloads let you build pipelines that read top to bottom.
- **Rust-inspired** — the API follows familiar `Option` and `Result` semantics from Rust, adapted to Python.
- **Dependency-free** — pure Python with no runtime dependencies, compatible with Python 3.12 and newer.

## Architecture

```
                 pyfplib
        ┌───────────┼───────────┐
        │           │           │
     Option       Result     functools
   Some/Nothing  Ok/Err     fold, find,
        │           │        any_of, ...
        └─────┬─────┘           │
              │                 │
              ▼                 ▼
      composable pipelines   sequence helpers
```

`Option` and `Result` share the same core implementation in `pyfplib._core` and are re-exported from `pyfplib.option` and `pyfplib.result`. Most users only need the top-level `pyfplib` package.

## Next Steps

- [Getting Started](/guide/getting-started) — install pyfplib and try your first pipeline
- [Option API](/guide/option) — full reference for `Some`, `Nothing`, and `Option`
- [Result API](/guide/result) — full reference for `Ok`, `Err`, and `Result`
- [Functions API](/guide/functools) — full reference for the sequence helpers
