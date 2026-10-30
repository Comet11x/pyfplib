# Getting Started

## Installation

```bash
pip install -U pyfplib
```

pyfplib has no runtime dependencies and supports Python 3.12 and newer.

## Option

Use `Option` when a value may be absent. `Some` wraps a value and `Nothing` represents its absence.

```python
from pyfplib import Nothing, Some

user = Some({"name": "Ada", "email": "ada@example.com"})

email = user.map(lambda u: u.get("email")).unwrap_or("unknown")
print(email)  # ada@example.com

missing = Nothing()
print(missing.unwrap_or("unknown"))  # unknown
```

## Result

Use `Result` to model operations that can fail without raising exceptions across your API boundary.

```python
from pyfplib import Err, Ok, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

print(divide(10, 2).unwrap())                 # 5.0
print(divide(10, 0).unwrap_or(float("nan")))  # nan

# Convert exceptions into an Err value
parsed = Result.try_call(int, "not a number")
print(parsed.is_err())  # True
```

## Functional Helpers

The `functools` module contains small helpers for common sequence operations.

```python
from pyfplib import all_of, any_of, find, fold, head, tail
from pyfplib import Nothing, Some

numbers = [1, 2, 3, 4, 5]

print(head(numbers))                       # Some(1)
print(tail(numbers))                       # [2, 3, 4, 5]
print(any_of(lambda n: n > 4, numbers))    # True
print(all_of(lambda n: n > 0, numbers))    # True
print(find(lambda n: Some(n) if n % 2 == 0 else Nothing(), numbers))  # Some(2)

total = fold(lambda acc, n: acc.unwrap_or(0) + n, numbers, 0)
print(total)  # Some(15)
```

## What's Next?

- [Option API](/guide/option) — full reference for `Some`, `Nothing`, and `Option`
- [Result API](/guide/result) — full reference for `Ok`, `Err`, and `Result`
- [Functions API](/guide/functools) — full reference for the sequence helpers
