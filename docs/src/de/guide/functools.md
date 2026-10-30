# Funktions-API

Das Modul `pyfplib.functools` bietet kleine, kombinierbare Helfer für Sequenzen. Die meisten werden auch aus dem übergeordneten Paket `pyfplib` re-exportiert; `first`, `split_first` und `split_last` müssen aus `pyfplib.functools` importiert werden.

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
from pyfplib.functools import first, split_first, split_last
```

Viele Helfer akzeptieren Callbacks mit einem, zwei oder drei Parametern. Die zusätzlichen Parameter erhalten den Elementindex und die vollständige Sequenz.

---

## Iteration

### `for_each(function: Callable[..., None], sequence: Sequence[T]) -> None`

Wendet `function` auf jedes Element an, um Nebenwirkungen auszuführen. Der Callback kann `(value)`, `(value, index)` oder `(value, index, sequence)` akzeptieren.

```python
from pyfplib import for_each

def print_item(value: int) -> None:
    print(value)

def print_indexed(value: str, index: int) -> None:
    print(index, value)

for_each(print_item, [1, 2])        # prints 1, then 2
for_each(print_indexed, ["a", "b"]) # prints "0 a", then "1 b"
```

---

## Prädikate

### `any_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Gibt `True` zurück, wenn mindestens ein Element `predicate` erfüllt; für eine leere Sequenz `False`. Der Callback kann `(value)`, `(value, index)` oder `(value, index, sequence)` akzeptieren.

```python
from pyfplib import any_of

def greater_than_two(value: int) -> bool:
    return value > 2

numbers: list[int] = [1, 2, 3]

print(any_of(greater_than_two, numbers))         # True
print(any_of(lambda value: value > 10, numbers)) # False
print(any_of(lambda value: True, []))            # False
```

### `all_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Gibt `True` zurück, wenn jedes Element `predicate` erfüllt; für eine leere Sequenz `True`. Der Callback kann `(value)`, `(value, index)` oder `(value, index, sequence)` akzeptieren.

```python
from pyfplib import all_of

def is_positive(value: int) -> bool:
    return value > 0

print(all_of(is_positive, [1, 2, 3]))  # True
print(all_of(is_positive, [1, -1, 2])) # False
print(all_of(lambda value: False, [])) # True
```

### `none_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Gibt `True` zurück, wenn kein Element `predicate` erfüllt; für eine leere Sequenz `True`. Der Callback kann `(value)`, `(value, index)` oder `(value, index, sequence)` akzeptieren.

```python
from pyfplib import none_of

def is_negative(value: int) -> bool:
    return value < 0

print(none_of(is_negative, [1, 2, 3]))              # True
print(none_of(lambda value: value > 2, [1, 2, 3]))  # False
print(none_of(lambda value: True, []))              # True
```

---

## Falten

### `fold(function: Callable[[Option[R], T], R] | Callable[[Option[R], T, int], R], sequence: Sequence[T], initial: R | None = None) -> Option[R]`

Reduziert eine Sequenz auf `Option[R]`. Der Callback erhält den Akkumulator als `Option[R]` und das aktuelle Element, optional mit dem Elementindex. Ohne Anfangswert beginnt der Akkumulator als `Nothing`; das Falten einer leeren Sequenz ohne Anfangswert gibt `Nothing()` zurück.

```python
from pyfplib import Option, fold

def add(accumulator: Option[int], value: int) -> int:
    return accumulator.unwrap_or(0) + value

def add_with_index(accumulator: Option[int], value: int, index: int) -> int:
    return accumulator.unwrap_or(0) + value + index

numbers: list[int] = [1, 2, 3]

print(fold(add, numbers, 0))         # Some(6)
print(fold(add_with_index, numbers)) # Some(9)
```

```python
from pyfplib import Option, fold

def add(accumulator: Option[int], value: int) -> int:
    return accumulator.unwrap_or(0) + value

print(fold(add, []))     # Nothing()
print(fold(add, [], 10)) # Some(10)
```

---

## Elementzugriff

### `head(iterable: Iterable[T]) -> Option[T]`

Gibt das erste Element zurück oder `Nothing`, wenn das Iterable leer ist. Akzeptiert jedes Iterable.

```python
from pyfplib import head

print(head([10, 20])) # Some(10)
print(head([]))       # Nothing()
print(head("abc"))    # Some('a')
```

### `first(iterable: Iterable[T]) -> Option[T]`

Gibt das erste Element eines beliebigen Iterables zurück. Verhält sich wie `head`.

```python
from pyfplib.functools import first

print(first("abc")) # Some('a')
print(first([]))    # Nothing()
```

### `last(sequence: Sequence[T]) -> Option[T]`

Gibt das letzte Element zurück oder `Nothing`, wenn die Sequenz leer ist.

```python
from pyfplib import last

print(last([10, 20])) # Some(20)
print(last([]))       # Nothing()
```

### `tail(sequence: Sequence[T]) -> Sequence[T]`

Gibt die Sequenz ohne ihr erstes Element zurück. Leere Sequenzen werden unverändert zurückgegeben.

```python
from pyfplib import tail

print(tail([1, 2, 3])) # [2, 3]
print(tail([]))        # []
```

### `split_first(sequence: Sequence[T]) -> tuple[Option[T], Sequence[T]]`

Teilt eine Sequenz in ihr erstes Element und den verbleibenden Rest. Eine leere Sequenz gibt `(Nothing(), sequence)` zurück.

```python
from pyfplib.functools import split_first

print(split_first([1, 2, 3])) # (Some(1), [2, 3])
print(split_first([]))        # (Nothing(), [])
```

### `split_last(sequence: Sequence[T]) -> tuple[Sequence[T], Option[T]]`

Teilt eine Sequenz in ihren Anfangsteil und ihr letztes Element. Eine leere Sequenz gibt `(sequence, Nothing())` zurück.

```python
from pyfplib.functools import split_last

print(split_last([1, 2, 3])) # ([1, 2], Some(3))
print(split_last([]))        # ([], Nothing())
```

---

## Suchen

### `index(predicate: Callable[..., bool | Option[Any]] | T, sequence: Sequence[T]) -> Option[int]`

Gibt den Index des ersten passenden Elements zurück. `predicate` kann ein Wert oder ein Callable sein; Callables können `(value)`, `(value, index)` oder `(value, index, sequence)` akzeptieren. Gibt `Nothing()` zurück, wenn kein Element passt.

```python
from pyfplib import index

numbers: list[int] = [1, 2, 3, 4]

print(index(3, numbers))                        # Some(2)
print(index(lambda value: value > 2, numbers))  # Some(2)
print(index(10, numbers))                       # Nothing()
```

### `find(callback: Callable[[T], Option[T] | bool], sequence: Sequence[T]) -> Option[T]`

Gibt das erste Element zurück, für das `callback` ein nicht leeres `Option` oder einen beliebigen Wahrheitswert zurückgibt. Gibt `Nothing()` zurück, wenn kein Element passt.

```python
from pyfplib import Nothing, Option, Some, find

numbers: list[int] = [1, 2, 3]

def is_even(value: int) -> Option[int]:
    return Some(value) if value % 2 == 0 else Nothing()

print(find(is_even, numbers))                   # Some(2)
print(find(lambda value: value > 2, numbers))   # Some(3)
print(find(lambda value: value > 10, numbers))  # Nothing()
```

---

## Größenprüfungen

### `is_empty(iterable: Sized) -> bool`

Gibt `True` zurück, wenn `len(iterable) == 0`.

```python
from pyfplib import is_empty

print(is_empty([]))  # True
print(is_empty([1])) # False
```

### `is_not_empty(value: Sized) -> bool`

Gibt `True` zurück, wenn `len(value) != 0`.

```python
from pyfplib import is_not_empty

print(is_not_empty([1])) # True
print(is_not_empty([]))  # False
```
