# API Funzioni

Il modulo `pyfplib.functools` fornisce piccoli helper componibili per le sequenze. La maggior parte è anche riesportata dal pacchetto di livello superiore `pyfplib`; `first`, `split_first` e `split_last` devono essere importati da `pyfplib.functools`.

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

Molti helper accettano callback con uno, due o tre parametri. I parametri extra ricevono l'indice dell'elemento e l'intera sequenza.

---

## Iterazione

### `for_each(function: Callable[..., None], sequence: Sequence[T]) -> None`

Applica `function` a ogni elemento per i suoi effetti collaterali. La callback può accettare `(value)`, `(value, index)` o `(value, index, sequence)`.

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

## Predicati

### `any_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Restituisce `True` quando almeno un elemento soddisfa `predicate`; restituisce `False` per una sequenza vuota. La callback può accettare `(value)`, `(value, index)` o `(value, index, sequence)`.

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

Restituisce `True` quando ogni elemento soddisfa `predicate`; restituisce `True` per una sequenza vuota. La callback può accettare `(value)`, `(value, index)` o `(value, index, sequence)`.

```python
from pyfplib import all_of

def is_positive(value: int) -> bool:
    return value > 0

print(all_of(is_positive, [1, 2, 3]))  # True
print(all_of(is_positive, [1, -1, 2])) # False
print(all_of(lambda value: False, [])) # True
```

### `none_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Restituisce `True` quando nessun elemento soddisfa `predicate`; restituisce `True` per una sequenza vuota. La callback può accettare `(value)`, `(value, index)` o `(value, index, sequence)`.

```python
from pyfplib import none_of

def is_negative(value: int) -> bool:
    return value < 0

print(none_of(is_negative, [1, 2, 3]))              # True
print(none_of(lambda value: value > 2, [1, 2, 3]))  # False
print(none_of(lambda value: True, []))              # True
```

---

## Folding

### `fold(function: Callable[[Option[R], T], R] | Callable[[Option[R], T, int], R], sequence: Sequence[T], initial: R | None = None) -> Option[R]`

Riduce una sequenza a `Option[R]`. La callback riceve l'accumulatore come `Option[R]` e l'elemento corrente, facoltativamente con l'indice dell'elemento. Senza un valore iniziale, l'accumulatore parte da `Nothing`; piegare una sequenza vuota senza valore iniziale restituisce `Nothing()`.

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

## Accesso agli elementi

### `head(iterable: Iterable[T]) -> Option[T]`

Restituisce il primo elemento, o `Nothing` quando l'iterabile è vuoto. Accetta qualsiasi iterabile.

```python
from pyfplib import head

print(head([10, 20])) # Some(10)
print(head([]))       # Nothing()
print(head("abc"))    # Some('a')
```

### `first(iterable: Iterable[T]) -> Option[T]`

Restituisce il primo elemento di qualsiasi iterabile. Si comporta come `head`.

```python
from pyfplib.functools import first

print(first("abc")) # Some('a')
print(first([]))    # Nothing()
```

### `last(sequence: Sequence[T]) -> Option[T]`

Restituisce l'ultimo elemento, o `Nothing` quando la sequenza è vuota.

```python
from pyfplib import last

print(last([10, 20])) # Some(20)
print(last([]))       # Nothing()
```

### `tail(sequence: Sequence[T]) -> Sequence[T]`

Restituisce la sequenza senza il primo elemento. Le sequenze vuote vengono restituite invariate.

```python
from pyfplib import tail

print(tail([1, 2, 3])) # [2, 3]
print(tail([]))        # []
```

### `split_first(sequence: Sequence[T]) -> tuple[Option[T], Sequence[T]]`

Divide una sequenza nel suo primo elemento e nella coda rimanente. Una sequenza vuota restituisce `(Nothing(), sequence)`.

```python
from pyfplib.functools import split_first

print(split_first([1, 2, 3])) # (Some(1), [2, 3])
print(split_first([]))        # (Nothing(), [])
```

### `split_last(sequence: Sequence[T]) -> tuple[Sequence[T], Option[T]]`

Divide una sequenza nella sua parte iniziale e nel suo ultimo elemento. Una sequenza vuota restituisce `(sequence, Nothing())`.

```python
from pyfplib.functools import split_last

print(split_last([1, 2, 3])) # ([1, 2], Some(3))
print(split_last([]))        # ([], Nothing())
```

---

## Ricerca

### `index(predicate: Callable[..., bool | Option[Any]] | T, sequence: Sequence[T]) -> Option[int]`

Restituisce l'indice del primo elemento corrispondente. `predicate` può essere un valore o un callable; i callable possono accettare `(value)`, `(value, index)` o `(value, index, sequence)`. Restituisce `Nothing()` quando nessun elemento corrisponde.

```python
from pyfplib import index

numbers: list[int] = [1, 2, 3, 4]

print(index(3, numbers))                        # Some(2)
print(index(lambda value: value > 2, numbers))  # Some(2)
print(index(10, numbers))                       # Nothing()
```

### `find(callback: Callable[[T], Option[T] | bool], sequence: Sequence[T]) -> Option[T]`

Restituisce il primo elemento per cui `callback` restituisce un `Option` non vuoto o qualsiasi valore vero. Restituisce `Nothing()` quando nessun elemento corrisponde.

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

## Controlli di dimensione

### `is_empty(iterable: Sized) -> bool`

Restituisce `True` quando `len(iterable) == 0`.

```python
from pyfplib import is_empty

print(is_empty([]))  # True
print(is_empty([1])) # False
```

### `is_not_empty(value: Sized) -> bool`

Restituisce `True` quando `len(value) != 0`.

```python
from pyfplib import is_not_empty

print(is_not_empty([1])) # True
print(is_not_empty([]))  # False
```
