# Result API

`Result[T, E]` represents either success (`Ok`) or failure (`Err`). It lives in `pyfplib.result` and is re-exported from the top-level `pyfplib` package.

```python
from pyfplib import Err, Ok, Result
```

---

## Constructors

### `Ok(value)`

Creates a successful result.

```python
>>> Ok(42).is_ok()
True
>>> Ok(42).unwrap()
42
```

### `Err(error)`

Creates a failed result.

```python
>>> Err("boom").is_err()
True
>>> Err("boom").unwrap_err()
'boom'
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
>>> bool(Ok(1)), bool(Err("e"))
(True, False)
>>> Ok(1).ok()
Some(1)
>>> Err("e").ok()
Nothing()
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
>>> Ok(1).unwrap_or(0)
1
>>> Err("e").unwrap_or(0)
0
>>> Err("e").unwrap_or_else(lambda e: len(e))
1
```

---

## Transformation

### `map(fn) -> Result[U, E]`

Applies `fn` to the `Ok` value. `Err` is returned unchanged.

```python
>>> Ok(2).map(lambda v: v * 3)
Ok(6)
>>> Err("e").map(lambda v: v * 3)
Err('e')
```

### `map_or(default, fn) -> Result[U, E]`

Applies `fn` to the `Ok` value or uses `default`. The result is always `Ok`.

```python
>>> Ok(2).map_or(0, lambda v: v * 3)
Ok(6)
>>> Err("e").map_or(0, lambda v: v * 3)
Ok(0)
```

### `map_or_else(default, fn) -> U`

Applies `fn` to the `Ok` value, or calls `default(error)` on `Err`.

```python
>>> Ok(2).map_or_else(lambda e: 0, lambda v: v * 3)
6
>>> Err("e").map_or_else(lambda e: len(e), lambda v: v * 3)
3
```

### `map_err(fn) -> Result[T, U]`

Applies `fn` to the `Err` value. `Ok` is returned unchanged.

```python
>>> Err("boom").map_err(str.upper)
Err('BOOM')
>>> Ok(1).map_err(str.upper)
Ok(1)
```

### `flatten() -> Result[T, E]`

Collapses one level of nesting.

```python
>>> Ok(Ok(1)).flatten()
Ok(1)
>>> Ok(1).flatten()
Ok(1)
```

### `flatten_all() -> Result[T, E]`

Collapses every level of nesting.

```python
>>> Ok(Ok(Ok(1))).flatten_all()
Ok(1)
```

---

## Combining

### `and_then(fn) -> Result[T, E]`

Runs `fn` only when the result is `Ok`; otherwise returns the `Err` unchanged.

```python
>>> Ok(2).and_then(lambda v: Ok(v + 1))
Ok(3)
>>> Err("e").and_then(lambda v: Ok(v + 1))
Err('e')
```

### `or_else(fn) -> Result[T, E]`

Runs `fn` only when the result is `Err`; otherwise returns the original `Ok`.

```python
>>> Err("e").or_else(lambda e: Ok(0))
Ok(0)
>>> Ok(1).or_else(lambda e: Ok(0))
Ok(1)
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
>>> Ok(1) & Ok(2)
Ok(2)
>>> Err("e") & Ok(2)
Err('e')
>>> Err("e") | Ok(2)
Ok(2)
```

---

## Exception Handling

### `Result.try_call(fn, *args, **kwargs) -> Result[R, Exception]` *(static)*

Calls `fn` and converts any raised exception into an `Err`.

```python
>>> Result.try_call(int, "42")
Ok(42)
>>> Result.try_call(int, "oops").is_err()
True
```

---

## Errors

- `UnwrapError` — raised by `unwrap()` and `unwrap_err()` when the wrong variant is present.
- `ExpectedError` — raised by `expect()` and `expect_err()` with the supplied message.

```python
from pyfplib import Err
from pyfplib.errors import UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)
```
