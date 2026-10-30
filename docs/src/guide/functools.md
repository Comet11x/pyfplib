# Functions API

The `pyfplib.functools` module provides small, composable helpers for sequences. Most are also re-exported from the top-level `pyfplib` package; `split_first` and `split_last` must be imported from `pyfplib.functools`.

```python
from pyfplib import (
    all_of,
    any_of,
    find,
    fold,
    for_each,
    head,
    index,
    is_empty,
    is_not_empty,
    last,
    none_of,
    tail,
)
from pyfplib.functools import split_first, split_last
```

Many helpers accept callbacks with one, two, or three parameters. The extra parameters receive the element index and the full sequence.

---

## Iteration

### `for_each(function, sequence) -> None`

Applies `function` to every element for its side effects.

```python
>>> for_each(lambda v: print(v), [1, 2])
1
2
>>> for_each(lambda v, i: print(i, v), ["a", "b"])
0 a
1 b
```

---

## Predicates

### `any_of(predicate, sequence) -> bool`

Returns `True` when at least one element satisfies `predicate`. Returns `False` for an empty sequence.

```python
>>> any_of(lambda v: v > 2, [1, 2, 3])
True
>>> any_of(lambda v: v > 10, [1, 2, 3])
False
```

### `all_of(predicate, sequence) -> bool`

Returns `True` when every element satisfies `predicate`. Returns `True` for an empty sequence.

```python
>>> all_of(lambda v: v > 0, [1, 2, 3])
True
>>> all_of(lambda v: v > 0, [1, -1])
False
```

### `none_of(predicate, sequence) -> bool`

Returns `True` when no element satisfies `predicate`.

```python
>>> none_of(lambda v: v > 10, [1, 2, 3])
True
>>> none_of(lambda v: v > 2, [1, 2, 3])
False
```

---

## Folding

### `fold(function, sequence, initial=None) -> Option[R]`

Reduces a sequence to a single value. The callback receives the accumulator and the current element, and optionally the element index.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [1, 2, 3], 0)
Some(6)
>>> fold(lambda acc, v, i: acc.unwrap_or(0) + v + i, [1, 2, 3])
Some(9)
```

Without an initial value the accumulator starts as `Nothing`; folding an empty sequence returns `Nothing()`.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [])
Nothing()
```

---

## Element Access

### `head(iterable) -> Option[T]`

Returns the first element, or `Nothing` when the iterable is empty. Accepts any iterable.

```python
>>> head([10, 20])
Some(10)
>>> head([])
Nothing()
```

### `first(iterable) -> Option[T]`

Alias-style helper that returns the first element of any iterable.

```python
>>> first("abc")
Some('a')
```

### `last(sequence) -> Option[T]`

Returns the last element, or `Nothing` when the sequence is empty.

```python
>>> last([10, 20])
Some(20)
>>> last([])
Nothing()
```

### `tail(sequence) -> Sequence[T]`

Returns the sequence without its first element. Empty sequences are returned unchanged.

```python
>>> tail([1, 2, 3])
[2, 3]
>>> tail([])
[]
```

### `split_first(sequence) -> tuple[Option[T], Sequence[T]]`

Splits a sequence into its first element and the remaining tail.

```python
>>> split_first([1, 2, 3])
(Some(1), [2, 3])
>>> split_first([])
(Nothing(), [])
```

### `split_last(sequence) -> tuple[Sequence[T], Option[T]]`

Splits a sequence into its initial part and its last element.

```python
>>> split_last([1, 2, 3])
([1, 2], Some(3))
>>> split_last([])
([], Nothing())
```

---

## Searching

### `index(predicate, sequence) -> Option[int]`

Returns the index of the first matching element. `predicate` may be a callable or a value to compare with.

```python
>>> index(3, [1, 2, 3, 4])
Some(2)
>>> index(lambda v: v > 2, [1, 2, 3, 4])
Some(2)
>>> index(10, [1, 2, 3])
Nothing()
```

### `find(callback, sequence) -> Option[T]`

Returns the first element for which `callback` returns a non-empty `Option` or any truthy value.

```python
>>> find(lambda v: Some(v) if v % 2 == 0 else Nothing(), [1, 2, 3])
Some(2)
>>> find(lambda v: v > 2, [1, 2, 3])
Some(3)
>>> find(lambda v: v > 10, [1, 2, 3])
Nothing()
```

---

## Size Checks

### `is_empty(iterable) -> bool`

Returns `True` when `len(iterable) == 0`.

```python
>>> is_empty([])
True
>>> is_empty([1])
False
```

### `is_not_empty(value) -> bool`

Returns `True` when `len(value) != 0`.

```python
>>> is_not_empty([1])
True
>>> is_not_empty([])
False
```
