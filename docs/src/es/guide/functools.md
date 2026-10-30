# API de Funciones

El módulo `pyfplib.functools` proporciona pequeños ayudantes componibles para secuencias. La mayoría también se reexporta desde el paquete de nivel superior `pyfplib`; `first`, `split_first` y `split_last` deben importarse desde `pyfplib.functools`.

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

Muchos ayudantes aceptan callbacks con uno, dos o tres parámetros. Los parámetros adicionales reciben el índice del elemento y la secuencia completa.

---

## Iteración

### `for_each(function: Callable[..., None], sequence: Sequence[T]) -> None`

Aplica `function` a cada elemento por sus efectos secundarios. La callback puede aceptar `(value)`, `(value, index)` o `(value, index, sequence)`.

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

## Predicados

### `any_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Devuelve `True` cuando al menos un elemento satisface `predicate`; devuelve `False` para una secuencia vacía. La callback puede aceptar `(value)`, `(value, index)` o `(value, index, sequence)`.

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

Devuelve `True` cuando cada elemento satisface `predicate`; devuelve `True` para una secuencia vacía. La callback puede aceptar `(value)`, `(value, index)` o `(value, index, sequence)`.

```python
from pyfplib import all_of

def is_positive(value: int) -> bool:
    return value > 0

print(all_of(is_positive, [1, 2, 3]))  # True
print(all_of(is_positive, [1, -1, 2])) # False
print(all_of(lambda value: False, [])) # True
```

### `none_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Devuelve `True` cuando ningún elemento satisface `predicate`; devuelve `True` para una secuencia vacía. La callback puede aceptar `(value)`, `(value, index)` o `(value, index, sequence)`.

```python
from pyfplib import none_of

def is_negative(value: int) -> bool:
    return value < 0

print(none_of(is_negative, [1, 2, 3]))              # True
print(none_of(lambda value: value > 2, [1, 2, 3]))  # False
print(none_of(lambda value: True, []))              # True
```

---

## Plegado

### `fold(function: Callable[[Option[R], T], R] | Callable[[Option[R], T, int], R], sequence: Sequence[T], initial: R | None = None) -> Option[R]`

Reduce una secuencia a `Option[R]`. La callback recibe el acumulador como `Option[R]` y el elemento actual, opcionalmente con el índice del elemento. Sin un valor inicial, el acumulador comienza como `Nothing`; plegar una secuencia vacía sin valor inicial devuelve `Nothing()`.

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

## Acceso a elementos

### `head(iterable: Iterable[T]) -> Option[T]`

Devuelve el primer elemento, o `Nothing` cuando el iterable está vacío. Acepta cualquier iterable.

```python
from pyfplib import head

print(head([10, 20])) # Some(10)
print(head([]))       # Nothing()
print(head("abc"))    # Some('a')
```

### `first(iterable: Iterable[T]) -> Option[T]`

Devuelve el primer elemento de cualquier iterable. Se comporta como `head`.

```python
from pyfplib.functools import first

print(first("abc")) # Some('a')
print(first([]))    # Nothing()
```

### `last(sequence: Sequence[T]) -> Option[T]`

Devuelve el último elemento, o `Nothing` cuando la secuencia está vacía.

```python
from pyfplib import last

print(last([10, 20])) # Some(20)
print(last([]))       # Nothing()
```

### `tail(sequence: Sequence[T]) -> Sequence[T]`

Devuelve la secuencia sin su primer elemento. Las secuencias vacías se devuelven sin cambios.

```python
from pyfplib import tail

print(tail([1, 2, 3])) # [2, 3]
print(tail([]))        # []
```

### `split_first(sequence: Sequence[T]) -> tuple[Option[T], Sequence[T]]`

Divide una secuencia en su primer elemento y la cola restante. Una secuencia vacía devuelve `(Nothing(), sequence)`.

```python
from pyfplib.functools import split_first

print(split_first([1, 2, 3])) # (Some(1), [2, 3])
print(split_first([]))        # (Nothing(), [])
```

### `split_last(sequence: Sequence[T]) -> tuple[Sequence[T], Option[T]]`

Divide una secuencia en su parte inicial y su último elemento. Una secuencia vacía devuelve `(sequence, Nothing())`.

```python
from pyfplib.functools import split_last

print(split_last([1, 2, 3])) # ([1, 2], Some(3))
print(split_last([]))        # ([], Nothing())
```

---

## Búsqueda

### `index(predicate: Callable[..., bool | Option[Any]] | T, sequence: Sequence[T]) -> Option[int]`

Devuelve el índice del primer elemento coincidente. `predicate` puede ser un valor o un callable; los callables pueden aceptar `(value)`, `(value, index)` o `(value, index, sequence)`. Devuelve `Nothing()` cuando ningún elemento coincide.

```python
from pyfplib import index

numbers: list[int] = [1, 2, 3, 4]

print(index(3, numbers))                        # Some(2)
print(index(lambda value: value > 2, numbers))  # Some(2)
print(index(10, numbers))                       # Nothing()
```

### `find(callback: Callable[[T], Option[T] | bool], sequence: Sequence[T]) -> Option[T]`

Devuelve el primer elemento para el que `callback` devuelve un `Option` no vacío o cualquier valor verdadero. Devuelve `Nothing()` cuando ningún elemento coincide.

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

## Comprobaciones de tamaño

### `is_empty(iterable: Sized) -> bool`

Devuelve `True` cuando `len(iterable) == 0`.

```python
from pyfplib import is_empty

print(is_empty([]))  # True
print(is_empty([1])) # False
```

### `is_not_empty(value: Sized) -> bool`

Devuelve `True` cuando `len(value) != 0`.

```python
from pyfplib import is_not_empty

print(is_not_empty([1])) # True
print(is_not_empty([]))  # False
```
