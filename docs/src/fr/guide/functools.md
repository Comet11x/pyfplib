# API Fonctions

Le module `pyfplib.functools` fournit de petits assistants composables pour les séquences. La plupart sont également réexportés depuis le paquet de niveau supérieur `pyfplib` ; `first`, `split_first` et `split_last` doivent être importés depuis `pyfplib.functools`.

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

De nombreux helpers acceptent des callbacks avec un, deux ou trois paramètres. Les paramètres supplémentaires reçoivent l'index de l'élément et la séquence complète.

---

## Itération

### `for_each(function: Callable[..., None], sequence: Sequence[T]) -> None`

Applique `function` à chaque élément pour ses effets de bord. Le callback peut accepter `(value)`, `(value, index)` ou `(value, index, sequence)`.

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

## Prédicats

### `any_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Renvoie `True` lorsqu'au moins un élément satisfait `predicate` ; renvoie `False` pour une séquence vide. Le callback peut accepter `(value)`, `(value, index)` ou `(value, index, sequence)`.

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

Renvoie `True` lorsque chaque élément satisfait `predicate` ; renvoie `True` pour une séquence vide. Le callback peut accepter `(value)`, `(value, index)` ou `(value, index, sequence)`.

```python
from pyfplib import all_of

def is_positive(value: int) -> bool:
    return value > 0

print(all_of(is_positive, [1, 2, 3]))  # True
print(all_of(is_positive, [1, -1, 2])) # False
print(all_of(lambda value: False, [])) # True
```

### `none_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Renvoie `True` lorsqu'aucun élément ne satisfait `predicate` ; renvoie `True` pour une séquence vide. Le callback peut accepter `(value)`, `(value, index)` ou `(value, index, sequence)`.

```python
from pyfplib import none_of

def is_negative(value: int) -> bool:
    return value < 0

print(none_of(is_negative, [1, 2, 3]))              # True
print(none_of(lambda value: value > 2, [1, 2, 3]))  # False
print(none_of(lambda value: True, []))              # True
```

---

## Réduction

### `fold(function: Callable[[Option[R], T], R] | Callable[[Option[R], T, int], R], sequence: Sequence[T], initial: R | None = None) -> Option[R]`

Réduit une séquence à `Option[R]`. Le callback reçoit l'accumulateur sous forme de `Option[R]` et l'élément courant, éventuellement avec l'index de l'élément. Sans valeur initiale, l'accumulateur commence à `Nothing` ; plier une séquence vide sans valeur initiale renvoie `Nothing()`.

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

## Accès aux éléments

### `head(iterable: Iterable[T]) -> Option[T]`

Renvoie le premier élément, ou `Nothing` lorsque l'itérable est vide. Accepte tout itérable.

```python
from pyfplib import head

print(head([10, 20])) # Some(10)
print(head([]))       # Nothing()
print(head("abc"))    # Some('a')
```

### `first(iterable: Iterable[T]) -> Option[T]`

Renvoie le premier élément de tout itérable. Se comporte comme `head`.

```python
from pyfplib.functools import first

print(first("abc")) # Some('a')
print(first([]))    # Nothing()
```

### `last(sequence: Sequence[T]) -> Option[T]`

Renvoie le dernier élément, ou `Nothing` lorsque la séquence est vide.

```python
from pyfplib import last

print(last([10, 20])) # Some(20)
print(last([]))       # Nothing()
```

### `tail(sequence: Sequence[T]) -> Sequence[T]`

Renvoie la séquence sans son premier élément. Les séquences vides sont renvoyées inchangées.

```python
from pyfplib import tail

print(tail([1, 2, 3])) # [2, 3]
print(tail([]))        # []
```

### `split_first(sequence: Sequence[T]) -> tuple[Option[T], Sequence[T]]`

Sépare une séquence en son premier élément et la queue restante. Une séquence vide renvoie `(Nothing(), sequence)`.

```python
from pyfplib.functools import split_first

print(split_first([1, 2, 3])) # (Some(1), [2, 3])
print(split_first([]))        # (Nothing(), [])
```

### `split_last(sequence: Sequence[T]) -> tuple[Sequence[T], Option[T]]`

Sépare une séquence en sa partie initiale et son dernier élément. Une séquence vide renvoie `(sequence, Nothing())`.

```python
from pyfplib.functools import split_last

print(split_last([1, 2, 3])) # ([1, 2], Some(3))
print(split_last([]))        # ([], Nothing())
```

---

## Recherche

### `index(predicate: Callable[..., bool | Option[Any]] | T, sequence: Sequence[T]) -> Option[int]`

Renvoie l'index du premier élément correspondant. `predicate` peut être une valeur ou un callable ; les callables peuvent accepter `(value)`, `(value, index)` ou `(value, index, sequence)`. Renvoie `Nothing()` lorsqu'aucun élément ne correspond.

```python
from pyfplib import index

numbers: list[int] = [1, 2, 3, 4]

print(index(3, numbers))                        # Some(2)
print(index(lambda value: value > 2, numbers))  # Some(2)
print(index(10, numbers))                       # Nothing()
```

### `find(callback: Callable[[T], Option[T] | bool], sequence: Sequence[T]) -> Option[T]`

Renvoie le premier élément pour lequel `callback` renvoie un `Option` non vide ou toute valeur véridique. Renvoie `Nothing()` lorsqu'aucun élément ne correspond.

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

## Vérifications de taille

### `is_empty(iterable: Sized) -> bool`

Renvoie `True` lorsque `len(iterable) == 0`.

```python
from pyfplib import is_empty

print(is_empty([]))  # True
print(is_empty([1])) # False
```

### `is_not_empty(value: Sized) -> bool`

Renvoie `True` lorsque `len(value) != 0`.

```python
from pyfplib import is_not_empty

print(is_not_empty([1])) # True
print(is_not_empty([]))  # False
```
