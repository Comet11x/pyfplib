# Option API

`Option[T]` represents a value that may be present (`Some`) or absent (`Nothing`). It lives in `pyfplib.option` and is re-exported from the top-level `pyfplib` package.

```python
from pyfplib import Nothing, Option, Some
```

---

## Constructors

### `Some(value: T)`

Wraps a non-`None` value in an `Option`. Because `Option` uses `None` internally to represent absence, `Some(None)` behaves like `Nothing()`.

```python
from pyfplib import Some

print(Some(42).is_some())    # True
print(Some(42).unwrap())     # 42
print(Some(None).is_none())  # True
```

### `Nothing()`

Creates an empty `Option`. A `Nothing` always reports `is_none()`.

```python
from pyfplib import Nothing

print(Nothing().is_none())     # True
print(Nothing().unwrap_or(0))  # 0
```

---

## Inspection

| Method | Returns | Description |
|---|---|---|
| `is_some()` | `bool` | `True` when a value is present. |
| `is_none()` | `bool` | `True` when no value is present. |
| `value` | `T \| None` | The raw contained value (may be `None`). |
| `__bool__()` | `bool` | Truthy for `Some`, falsy for `Nothing`. |
| `__eq__(other)` | `bool` | Compares contained values when both are `Option`s. |
| `__hash__()` | `int` | Hashes the contained value. |

```python
from pyfplib import Nothing, Some

print(bool(Some(1)), bool(Nothing()))  # (True, False)
print(Some(1) == Some(1))              # True
```

### `inspect(fn: Callable[[T], None]) -> Option[T]`

Calls `fn` with the contained value when `Some`, then returns the same option for chaining.

```python
from pyfplib import Option, Some

option: Option[int] = Some(2)
returned = option.inspect(lambda value: print(f"inspected: {value}"))
print(returned)  # Some(2)
```

### `inspect_none(fn: Callable[[], None]) -> Option[T]`

Calls `fn` with no arguments when `Nothing`, then returns the same option for chaining.

```python
from pyfplib import Nothing

returned = Nothing().inspect_none(lambda: print("empty"))
print(returned)  # Nothing()
```

---

## Extraction

| Method | Returns | Raises | Description |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Returns the value or raises when empty. |
| `expect(message)` | `T` | `ExpectedError` | Returns the value or raises with `message`. |
| `unwrap_or(default)` | `T` | — | Returns the value or `default`. |
| `unwrap_or_else(fn)` | `T` | — | Returns the value or calls `fn()` for a fallback. |

```python
from pyfplib import Nothing, Some

def fallback() -> int:
    return 10

print(Some(3).unwrap_or(0))               # 3
print(Nothing().unwrap_or(0))             # 0
print(Some(3).unwrap_or_else(fallback))   # 3
print(Nothing().unwrap_or_else(fallback)) # 10
```

---

## Pattern Matching

`Option` supports Python's structural pattern matching. Use `Some(value)` to bind the contained value and `Nothing()` to match an empty option, without calling `is_some()` first.

```python
from pyfplib import Nothing, Option, Some

def describe(option: Option[int]) -> str:
    match option:
        case Some(value):
            return f"got {value}"
        case Nothing():
            return "nothing"

print(describe(Some(42)))   # got 42
print(describe(Nothing()))  # nothing
```

---

## Transformation

### `map(fn: Callable[[T], U]) -> Option[U]`

Applies `fn` to the contained value and wraps the result in `Some`. `Nothing` stays `Nothing`.

```python
from pyfplib import Nothing, Some

def double(value: int) -> int:
    return value * 2

print(Some(3).map(double))    # Some(6)
print(Nothing().map(double))  # Nothing()
```

### `map_or(default: U, fn: Callable[[T], U]) -> Option[U]`

Applies `fn` to a `Some` value or uses `default`, and always returns an `Option` (`Some`). Use `map_or_else` when you need the plain value.

```python
from pyfplib import Nothing, Option, Some

def double(value: int) -> int:
    return value * 2

present: Option[int] = Some(3)
empty: Option[int] = Nothing()

print(present.map_or(0, double))  # Some(6)
print(empty.map_or(0, double))    # Some(0)
```

### `map_or_else(default: Callable[[], U], fn: Callable[[T], U]) -> U`

Applies `fn` to a `Some` value, or calls `default()` when empty, returning the plain value.

```python
from pyfplib import Nothing, Some

def default() -> int:
    return 0

def double(value: int) -> int:
    return value * 2

print(Some(3).map_or_else(default, double))   # 6
print(Nothing().map_or_else(default, double)) # 0
```

### `flatten() -> Option[T]`

Collapses one level of nesting. A non-nested option is returned unchanged.

```python
from pyfplib import Some

print(Some(Some(1)).flatten())  # Some(1)
print(Some(1).flatten())        # Some(1)
```

### `flatten_all() -> Option[T]`

Collapses every level of nesting until the innermost non-option value is reached.

```python
from pyfplib import Some

print(Some(Some(Some(1))).flatten_all())  # Some(1)
```

---

## Conversion

### `ok_or(err: E) -> Result[T, E]`

Converts an `Option` into a `Result`, using `err` when empty.

```python
from pyfplib import Nothing, Some

print(Some(1).ok_or("missing"))   # Ok(1)
print(Nothing().ok_or("missing")) # Err('missing')
```

### `ok_or_else(fn: Callable[[], E]) -> Result[T, E]`

Like `ok_or`, but calls `fn()` to produce the error when empty.

```python
from pyfplib import Nothing

def missing_error() -> str:
    return "missing"

print(Nothing().ok_or_else(missing_error))  # Err('missing')
```

### `from_optional(value: T | None) -> Option[T]` *(static)*

Builds an `Option` from a possibly-`None` value: `None` becomes `Nothing`, and any other value becomes `Some`.

```python
from pyfplib import Option

value: int | None = None
print(Option.from_optional(value))  # Nothing()
print(Option.from_optional(5))      # Some(5)
```

---

## Combining

### `and_then(fn: Callable[[T], Option[U]]) -> Option[U]`

Runs `fn` only when `Some`; otherwise returns `Nothing`.

```python
from pyfplib import Nothing, Option, Some

def increment(value: int) -> Option[int]:
    return Some(value + 1)

print(Some(2).and_then(increment))   # Some(3)
print(Nothing().and_then(increment)) # Nothing()
```

### `or_else(fn: Callable[[], Option[T]]) -> Option[T]`

Runs `fn` only when `Nothing`; otherwise returns the original option.

```python
from pyfplib import Nothing, Option, Some

def recover() -> Option[int]:
    return Some(9)

print(Nothing().or_else(recover))  # Some(9)
print(Some(1).or_else(recover))    # Some(1)
```

### `xor(other: Option[T]) -> Option[T]`

Returns a value only when exactly one of the two options is `Some`.

```python
from pyfplib import Nothing, Some

print(Some(1).xor(Nothing()))  # Some(1)
print(Some(1).xor(Some(2)))    # Nothing()
```

### `zip(other: Option[U]) -> Option[tuple[T, U]]`

Pairs the values when both options are `Some`.

```python
from pyfplib import Some

print(Some(1).zip(Some("a")))  # Some((1, 'a'))
```

### `zip_with(other: Option[U], ctr: Callable[[T, U], R]) -> Option[R]`

Combines both values with `ctr` when both are `Some`.

```python
from pyfplib import Some

def add(left: int, right: int) -> int:
    return left + right

print(Some(1).zip_with(Some(2), add))  # Some(3)
```

---

## Operators

`Option` overloads `&` and `|` to mirror `and_then` and `or_else`.

| Expression | Equivalent | Description |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Returns `b` when `a` is `Some`, otherwise `Nothing`. |
| `a & fn` | `a.and_then(lambda _: fn())` | Calls `fn()` when `a` is `Some`. |
| `a \| b` | `a.or_else(lambda: b)` | Returns `a` when `Some`, otherwise `b`. |
| `a \| fn` | `a.or_else(fn)` | Calls `fn()` when `a` is `Nothing`. |

```python
from pyfplib import Nothing, Some

print(Some(1) & Some(2))    # Some(2)
print(Nothing() & Some(2))  # Nothing()
print(Nothing() | Some(2))  # Some(2)
```

---

## Mutation

### `push(value: T) -> T`

Mutates the option in place: stores `value` and returns the previously held value, or `value` itself when the option was empty.

```python
from pyfplib import Option, Some

option: Option[int] = Some(1)
previous = option.push(2)

print(previous)  # 1
print(option)    # Some(2)
```

---

## Errors

- `UnwrapError` — raised by `unwrap()` when the option is `Nothing`.
- `ExpectedError` — raised by `expect(message)` when the option is `Nothing`.

```python
from pyfplib import Nothing
from pyfplib.errors import ExpectedError, UnwrapError

try:
    Nothing().unwrap()
except UnwrapError as exc:
    print(exc)  # called `Option.unwrap()` on a `Nothing` value

try:
    Nothing().expect("value is required")
except ExpectedError as exc:
    print(exc)  # value is required
```
