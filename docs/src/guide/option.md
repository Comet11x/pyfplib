# Option API

`Option[T]` represents a value that may be present (`Some`) or absent (`Nothing`). It lives in `pyfplib.option` and is re-exported from the top-level `pyfplib` package.

```python
from pyfplib import Nothing, Option, Some
```

---

## Constructors

### `Some(value)`

Wraps a value in an `Option`. A `Some` always `is_some()`.

```python
>>> Some(42).is_some()
True
>>> Some(42).unwrap()
42
```

### `Nothing()`

Creates an empty `Option`. A `Nothing` always `is_none()`.

```python
>>> Nothing().is_none()
True
>>> Nothing().unwrap_or(0)
0
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
>>> bool(Some(1)), bool(Nothing())
(True, False)
>>> Some(1) == Some(1)
True
```

### `inspect(fn) -> Option[T]`

Calls `fn` with the contained value when `Some`, then returns the option unchanged.

```python
>>> Some(2).inspect(lambda v: print(v))
2
Some(2)
```

### `inspect_none(fn) -> Option[T]`

Calls `fn` with no arguments when `Nothing`, then returns the option unchanged.

```python
>>> Nothing().inspect_none(lambda: print("empty"))
empty
Nothing()
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
>>> Some(3).unwrap_or(0)
3
>>> Nothing().unwrap_or(0)
0
>>> Nothing().unwrap_or_else(lambda: 10)
10
```

---

## Transformation

### `map(fn) -> Option[U]`

Applies `fn` to the contained value, wrapping the result in `Some`. `Nothing` stays `Nothing`.

```python
>>> Some(3).map(lambda v: v * 2)
Some(6)
>>> Nothing().map(lambda v: v * 2)
Nothing()
```

### `map_or(default, fn) -> Option[U]`

Applies `fn` when `Some`, otherwise uses `default`. The result is always wrapped in `Some`.

```python
>>> Some(3).map_or(0, lambda v: v * 2)
Some(6)
>>> Nothing().map_or(0, lambda v: v * 2)
Some(0)
```

### `map_or_else(default, fn) -> U`

Applies `fn` when `Some`, otherwise calls `default()`.

```python
>>> Some(3).map_or_else(lambda: 0, lambda v: v * 2)
6
>>> Nothing().map_or_else(lambda: 0, lambda v: v * 2)
0
```

### `flatten() -> Option[T]`

Collapses one level of nesting.

```python
>>> Some(Some(1)).flatten()
Some(1)
>>> Some(1).flatten()
Some(1)
```

### `flatten_all() -> Option[T]`

Collapses every level of nesting.

```python
>>> Some(Some(Some(1))).flatten_all()
Some(1)
```

---

## Conversion

### `ok_or(err) -> Result[T, E]`

Converts an `Option` into a `Result`, using `err` when empty.

```python
>>> Some(1).ok_or("missing")
Ok(1)
>>> Nothing().ok_or("missing")
Err('missing')
```

### `ok_or_else(fn) -> Result[T, E]`

Like `ok_or`, but calls `fn()` to produce the error when empty.

```python
>>> Nothing().ok_or_else(lambda: "missing")
Err('missing')
```

### `from_optional(value) -> Option[T]` *(static)*

Builds an `Option` from a possibly-`None` value.

```python
>>> Option.from_optional(None)
Nothing()
>>> Option.from_optional(5)
Some(5)
```

---

## Combining

### `and_then(fn) -> Option[U]`

Runs `fn` only when `Some`; otherwise returns `Nothing`.

```python
>>> Some(2).and_then(lambda v: Some(v + 1))
Some(3)
>>> Nothing().and_then(lambda v: Some(v + 1))
Nothing()
```

### `or_else(fn) -> Option[T]`

Runs `fn` only when `Nothing`; otherwise returns the original option.

```python
>>> Nothing().or_else(lambda: Some(9))
Some(9)
>>> Some(1).or_else(lambda: Some(9))
Some(1)
```

### `xor(other) -> Option[T]`

Returns a value only when exactly one of the two options is `Some`.

```python
>>> Some(1).xor(Nothing())
Some(1)
>>> Some(1).xor(Some(2))
Nothing()
```

### `zip(other) -> Option[tuple[T, U]]`

Pairs the values when both options are `Some`.

```python
>>> Some(1).zip(Some("a"))
Some((1, 'a'))
```

### `zip_with(other, ctr) -> Option[R]`

Combines both values with `ctr` when both are `Some`.

```python
>>> Some(1).zip_with(Some(2), lambda a, b: a + b)
Some(3)
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
>>> Some(1) & Some(2)
Some(2)
>>> Nothing() & Some(2)
Nothing()
>>> Nothing() | Some(2)
Some(2)
```

---

## Mutation

### `push(value) -> T`

Stores `value` and returns the previously held value (or `value` when the option was empty).

```python
>>> opt = Some(1)
>>> opt.push(2)
1
>>> opt
Some(2)
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
    print(exc)
```
