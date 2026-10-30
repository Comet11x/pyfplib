# API de Funções

O módulo `pyfplib.functools` fornece pequenos auxiliares combináveis para sequências. A maioria também é reexportada do pacote de nível superior `pyfplib`; `first`, `split_first` e `split_last` devem ser importados de `pyfplib.functools`.

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

Muitos auxiliares aceitam callbacks com um, dois ou três parâmetros. Os parâmetros extras recebem o índice do elemento e a sequência completa.

---

## Iteração

### `for_each(function: Callable[..., None], sequence: Sequence[T]) -> None`

Aplica `function` a cada elemento para seus efeitos colaterais. O callback pode aceitar `(value)`, `(value, index)` ou `(value, index, sequence)`.

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

Retorna `True` quando pelo menos um elemento satisfaz `predicate`; retorna `False` para uma sequência vazia. O callback pode aceitar `(value)`, `(value, index)` ou `(value, index, sequence)`.

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

Retorna `True` quando cada elemento satisfaz `predicate`; retorna `True` para uma sequência vazia. O callback pode aceitar `(value)`, `(value, index)` ou `(value, index, sequence)`.

```python
from pyfplib import all_of

def is_positive(value: int) -> bool:
    return value > 0

print(all_of(is_positive, [1, 2, 3]))  # True
print(all_of(is_positive, [1, -1, 2])) # False
print(all_of(lambda value: False, [])) # True
```

### `none_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Retorna `True` quando nenhum elemento satisfaz `predicate`; retorna `True` para uma sequência vazia. O callback pode aceitar `(value)`, `(value, index)` ou `(value, index, sequence)`.

```python
from pyfplib import none_of

def is_negative(value: int) -> bool:
    return value < 0

print(none_of(is_negative, [1, 2, 3]))              # True
print(none_of(lambda value: value > 2, [1, 2, 3]))  # False
print(none_of(lambda value: True, []))              # True
```

---

## Dobra

### `fold(function: Callable[[Option[R], T], R] | Callable[[Option[R], T, int], R], sequence: Sequence[T], initial: R | None = None) -> Option[R]`

Reduz uma sequência a `Option[R]`. O callback recebe o acumulador como `Option[R]` e o elemento atual, opcionalmente com o índice do elemento. Sem um valor inicial, o acumulador começa como `Nothing`; dobrar uma sequência vazia sem valor inicial retorna `Nothing()`.

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

## Acesso a elementos

### `head(iterable: Iterable[T]) -> Option[T]`

Retorna o primeiro elemento, ou `Nothing` quando o iterável está vazio. Aceita qualquer iterável.

```python
from pyfplib import head

print(head([10, 20])) # Some(10)
print(head([]))       # Nothing()
print(head("abc"))    # Some('a')
```

### `first(iterable: Iterable[T]) -> Option[T]`

Retorna o primeiro elemento de qualquer iterável. Comporta-se como `head`.

```python
from pyfplib.functools import first

print(first("abc")) # Some('a')
print(first([]))    # Nothing()
```

### `last(sequence: Sequence[T]) -> Option[T]`

Retorna o último elemento, ou `Nothing` quando a sequência está vazia.

```python
from pyfplib import last

print(last([10, 20])) # Some(20)
print(last([]))       # Nothing()
```

### `tail(sequence: Sequence[T]) -> Sequence[T]`

Retorna a sequência sem seu primeiro elemento. Sequências vazias são retornadas inalteradas.

```python
from pyfplib import tail

print(tail([1, 2, 3])) # [2, 3]
print(tail([]))        # []
```

### `split_first(sequence: Sequence[T]) -> tuple[Option[T], Sequence[T]]`

Divide uma sequência em seu primeiro elemento e na cauda restante. Uma sequência vazia retorna `(Nothing(), sequence)`.

```python
from pyfplib.functools import split_first

print(split_first([1, 2, 3])) # (Some(1), [2, 3])
print(split_first([]))        # (Nothing(), [])
```

### `split_last(sequence: Sequence[T]) -> tuple[Sequence[T], Option[T]]`

Divide uma sequência em sua parte inicial e seu último elemento. Uma sequência vazia retorna `(sequence, Nothing())`.

```python
from pyfplib.functools import split_last

print(split_last([1, 2, 3])) # ([1, 2], Some(3))
print(split_last([]))        # ([], Nothing())
```

---

## Busca

### `index(predicate: Callable[..., bool | Option[Any]] | T, sequence: Sequence[T]) -> Option[int]`

Retorna o índice do primeiro elemento correspondente. `predicate` pode ser um valor ou um callable; callables podem aceitar `(value)`, `(value, index)` ou `(value, index, sequence)`. Retorna `Nothing()` quando nenhum elemento corresponde.

```python
from pyfplib import index

numbers: list[int] = [1, 2, 3, 4]

print(index(3, numbers))                        # Some(2)
print(index(lambda value: value > 2, numbers))  # Some(2)
print(index(10, numbers))                       # Nothing()
```

### `find(callback: Callable[[T], Option[T] | bool], sequence: Sequence[T]) -> Option[T]`

Retorna o primeiro elemento para o qual `callback` retorna um `Option` não vazio ou qualquer valor verdadeiro. Retorna `Nothing()` quando nenhum elemento corresponde.

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

## Verificações de tamanho

### `is_empty(iterable: Sized) -> bool`

Retorna `True` quando `len(iterable) == 0`.

```python
from pyfplib import is_empty

print(is_empty([]))  # True
print(is_empty([1])) # False
```

### `is_not_empty(value: Sized) -> bool`

Retorna `True` quando `len(value) != 0`.

```python
from pyfplib import is_not_empty

print(is_not_empty([1])) # True
print(is_not_empty([]))  # False
```
