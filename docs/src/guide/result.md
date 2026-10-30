# Result API

`Result[T, E]` represents either success (`Ok`) or failure (`Err`). It lives in `pyfplib.result` and is re-exported from the top-level `pyfplib` package.

```python
from pyfplib import Err, Ok, Result
```

---

## Constructors

### `Ok(value: T)`

Creates a successful result.

```python
from pyfplib import Ok, Result

result: Result[int, str] = Ok(42)
print(result.is_ok())  # True
print(result.unwrap()) # 42
```

### `Err(error: E)`

Creates a failed result.

```python
from pyfplib import Err, Result

result: Result[int, str] = Err("boom")
print(result.is_err())           # True
print(repr(result.unwrap_err())) # 'boom'
```

---

## Inspection

| Method | Returns | Description |
|---|---|---|
| `is_ok()` | `bool` | `True` when the result is `Ok`. |
| `is_err()` | `bool` | `True` when the result is `Err`. |
| `value` | `T \| E` | The contained value or error. |
| `__bool__()` | `bool` | Truthy for `Ok`, falsy for `Err`. |
| `inspect(fn)` | `Result[T, E]` | Calls `fn` with the `Ok` value, returns `self`. |
| `inspect_err(fn)` | `Result[T, E]` | Calls `fn` with the `Err` value, returns `self`. |
| `ok()` | `Option[T]` | `Some(value)` for `Ok`, otherwise `Nothing()`. |
| `err()` | `Option[E]` | `Some(error)` for `Err`, otherwise `Nothing()`. |

```python
from pyfplib import Err, Ok, Result

ok_result: Result[int, str] = Ok(1)
err_result: Result[int, str] = Err("e")

print(bool(ok_result), bool(err_result))  # (True, False)
print(ok_result.ok())                     # Some(1)
print(err_result.ok())                    # Nothing()
print(err_result.err())                   # Some('e')
print(ok_result.err())                    # Nothing()

returned = ok_result.inspect(lambda value: print(f"ok: {value}"))
print(returned)  # Ok(1)

returned_err = err_result.inspect_err(lambda error: print(f"err: {error}"))
print(returned_err)  # Err('e')
```

---

## Extraction

| Method | Returns | Raises | Description |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Returns the `Ok` value or raises on `Err`. |
| `unwrap_err()` | `E` | `UnwrapError` | Returns the `Err` value or raises on `Ok`. |
| `expect(message)` | `T` | `ExpectedError` | Returns the `Ok` value or raises with `message`. |
| `expect_err(message)` | `E` | `ExpectedError` | Returns the `Err` value or raises with `message`. |
| `unwrap_or(default)` | `T` | — | Returns the `Ok` value or `default`. |
| `unwrap_or_else(fn)` | `T` | — | Returns the `Ok` value or `fn(error)`. |
| `unwrap_err_or(default)` | `E` | — | Returns the `Err` value or `default`. |

```python
from pyfplib import Err, Ok

def error_length(error: str) -> int:
    return len(error)

print(Ok(1).unwrap_or(0))                        # 1
print(Err("e").unwrap_or(0))                     # 0
print(Err("e").unwrap_or_else(error_length))     # 1
print(repr(Err("e").unwrap_err_or("fallback")))  # 'e'
print(repr(Ok(1).unwrap_err_or("fallback")))     # 'fallback'
```

---

## Pattern Matching

`Result` supports Python's structural pattern matching. Use `Ok(value)` to bind a successful value and `Err(error)` to bind the error, without calling `is_ok()` first.

```python
from pyfplib import Err, Ok, Result

def describe(result: Result[int, str]) -> str:
    match result:
        case Ok(value):
            return f"ok: {value}"
        case Err(error):
            return f"error: {error}"

print(describe(Ok(42)))      # ok: 42
print(describe(Err("boom"))) # error: boom
```

---

## Transformation

### `map(fn: Callable[[T], U]) -> Result[U, E]`

Applies `fn` to the `Ok` value. `Err` is returned unchanged.

```python
from pyfplib import Err, Ok

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map(triple))    # Ok(6)
print(Err("e").map(triple)) # Err('e')
```

### `map_or(default: T, fn: Callable[[T], U]) -> Result[U, E]`

Applies `fn` to the `Ok` value or to `default` when the result is `Err`. The result is always `Ok`. Use `map_or_else` when you need the plain value.

```python
from pyfplib import Err, Ok, Result

def triple(value: int) -> int:
    return value * 3

ok_result: Result[int, str] = Ok(2)
err_result: Result[int, str] = Err("e")

print(ok_result.map_or(1, triple))  # Ok(6)
print(err_result.map_or(1, triple)) # Ok(3)
```

### `map_or_else(default: Callable[[E], T], fn: Callable[[T], U]) -> U`

Applies `fn` to the `Ok` value, or calls `default(error)` on `Err` and applies `fn` to that fallback, returning the plain value.

```python
from pyfplib import Err, Ok

def error_length(error: str) -> int:
    return len(error)

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map_or_else(error_length, triple))    # 6
print(Err("e").map_or_else(error_length, triple)) # 3
```

### `map_err(fn: Callable[[E], U]) -> Result[T, U]`

Applies `fn` to the `Err` value. `Ok` is returned unchanged.

```python
from pyfplib import Err, Ok

print(Err("boom").map_err(str.upper))  # Err('BOOM')
print(Ok(1).map_err(str.upper))        # Ok(1)
```

### `flatten() -> Result[T, E]`

Collapses one level of nesting. A non-nested result is returned unchanged.

```python
from pyfplib import Ok

print(Ok(Ok(1)).flatten())  # Ok(1)
print(Ok(1).flatten())      # Ok(1)
```

### `flatten_all() -> Result[T, E]`

Collapses every level of nesting until the innermost non-result value is reached.

```python
from pyfplib import Ok

print(Ok(Ok(Ok(1))).flatten_all())  # Ok(1)
```

---

## Combining

### `and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]`

Runs `fn` only when the result is `Ok`; otherwise returns the `Err` unchanged.

```python
from pyfplib import Err, Ok, Result

def increment(value: int) -> Result[int, str]:
    return Ok(value + 1)

print(Ok(2).and_then(increment))    # Ok(3)
print(Err("e").and_then(increment)) # Err('e')
```

### `or_else(fn: Callable[[E], Result[T, E]]) -> Result[T, E]`

Runs `fn` only when the result is `Err`; otherwise returns the original `Ok`.

```python
from pyfplib import Err, Ok, Result

def recover(error: str) -> Result[int, str]:
    return Ok(0)

print(Err("e").or_else(recover))  # Ok(0)
print(Ok(1).or_else(recover))     # Ok(1)
```

---

## Operators

`Result` overloads `&` and `|` to mirror `and_then` and `or_else`.

| Expression | Equivalent | Description |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Returns `b` when `a` is `Ok`, otherwise the `Err`. |
| `a & fn` | `a.and_then(lambda v: fn(v))` | Calls `fn(value)` when `a` is `Ok`. |
| `a \| b` | `a.or_else(lambda _: b)` | Returns `a` when `Ok`, otherwise `b`. |
| `a \| fn` | `a.or_else(lambda e: fn(e))` | Calls `fn(error)` when `a` is `Err`. |

```python
from pyfplib import Err, Ok

print(Ok(1) & Ok(2))    # Ok(2)
print(Err("e") & Ok(2)) # Err('e')
print(Err("e") | Ok(2)) # Ok(2)
```

---

## Exception Handling

### `Result.try_call(fn: Callable[..., R], *args, **kwargs) -> Result[R, Exception]` *(static)*

Calls `fn` with the supplied arguments and converts any raised `Exception` into an `Err`.

```python
from pyfplib import Result

print(Result.try_call(int, "42"))            # Ok(42)
print(Result.try_call(int, "oops").is_err()) # True
```

---

## Errors

- `UnwrapError` — raised by `unwrap()` and `unwrap_err()` when the wrong variant is present.
- `ExpectedError` — raised by `expect()` and `expect_err()` with the supplied message.

```python
from pyfplib import Err, Ok
from pyfplib.errors import ExpectedError, UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)  # called `Result.unwrap()` on a `Err` value

try:
    Ok(1).unwrap_err()
except UnwrapError as exc:
    print(exc)  # called `Result.unwrap_err()` on a `Ok` value

try:
    Err("boom").expect("success required")
except ExpectedError as exc:
    print(exc)  # success required

try:
    Ok(1).expect_err("failure required")
except ExpectedError as exc:
    print(exc)  # failure required
```
