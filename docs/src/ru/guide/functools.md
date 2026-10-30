# API функций

Модуль `pyfplib.functools` предоставляет небольшие композируемые помощники для последовательностей. Большинство из них также реэкспортируются из пакета `pyfplib` верхнего уровня; `first`, `split_first` и `split_last` нужно импортировать из `pyfplib.functools`.

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

Многие помощники принимают обратные вызовы с одним, двумя или тремя параметрами. Дополнительные параметры получают индекс элемента и всю последовательность.

---

## Итерация

### `for_each(function: Callable[..., None], sequence: Sequence[T]) -> None`

Применяет `function` к каждому элементу ради побочных эффектов. Обратный вызов может принимать `(value)`, `(value, index)` или `(value, index, sequence)`.

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

## Предикаты

### `any_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Возвращает `True`, когда хотя бы один элемент удовлетворяет `predicate`; для пустой последовательности возвращает `False`. Обратный вызов может принимать `(value)`, `(value, index)` или `(value, index, sequence)`.

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

Возвращает `True`, когда каждый элемент удовлетворяет `predicate`; для пустой последовательности возвращает `True`. Обратный вызов может принимать `(value)`, `(value, index)` или `(value, index, sequence)`.

```python
from pyfplib import all_of

def is_positive(value: int) -> bool:
    return value > 0

print(all_of(is_positive, [1, 2, 3]))  # True
print(all_of(is_positive, [1, -1, 2])) # False
print(all_of(lambda value: False, [])) # True
```

### `none_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

Возвращает `True`, когда ни один элемент не удовлетворяет `predicate`; для пустой последовательности возвращает `True`. Обратный вызов может принимать `(value)`, `(value, index)` или `(value, index, sequence)`.

```python
from pyfplib import none_of

def is_negative(value: int) -> bool:
    return value < 0

print(none_of(is_negative, [1, 2, 3]))              # True
print(none_of(lambda value: value > 2, [1, 2, 3]))  # False
print(none_of(lambda value: True, []))              # True
```

---

## Свёртка

### `fold(function: Callable[[Option[R], T], R] | Callable[[Option[R], T, int], R], sequence: Sequence[T], initial: R | None = None) -> Option[R]`

Сводит последовательность к `Option[R]`. Обратный вызов получает аккумулятор как `Option[R]` и текущий элемент, а также (необязательно) индекс элемента. Без начального значения аккумулятор начинается с `Nothing`; свёртка пустой последовательности без начального значения возвращает `Nothing()`.

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

## Доступ к элементам

### `head(iterable: Iterable[T]) -> Option[T]`

Возвращает первый элемент или `Nothing`, если итерируемый объект пуст. Принимает любой итерируемый объект.

```python
from pyfplib import head

print(head([10, 20])) # Some(10)
print(head([]))       # Nothing()
print(head("abc"))    # Some('a')
```

### `first(iterable: Iterable[T]) -> Option[T]`

Возвращает первый элемент любого итерируемого объекта. Работает так же, как `head`.

```python
from pyfplib.functools import first

print(first("abc")) # Some('a')
print(first([]))    # Nothing()
```

### `last(sequence: Sequence[T]) -> Option[T]`

Возвращает последний элемент или `Nothing`, если последовательность пуста.

```python
from pyfplib import last

print(last([10, 20])) # Some(20)
print(last([]))       # Nothing()
```

### `tail(sequence: Sequence[T]) -> Sequence[T]`

Возвращает последовательность без первого элемента. Пустые последовательности возвращаются без изменений.

```python
from pyfplib import tail

print(tail([1, 2, 3])) # [2, 3]
print(tail([]))        # []
```

### `split_first(sequence: Sequence[T]) -> tuple[Option[T], Sequence[T]]`

Разделяет последовательность на первый элемент и оставшийся хвост. Для пустой последовательности возвращает `(Nothing(), sequence)`.

```python
from pyfplib.functools import split_first

print(split_first([1, 2, 3])) # (Some(1), [2, 3])
print(split_first([]))        # (Nothing(), [])
```

### `split_last(sequence: Sequence[T]) -> tuple[Sequence[T], Option[T]]`

Разделяет последовательность на начальную часть и последний элемент. Для пустой последовательности возвращает `(sequence, Nothing())`.

```python
from pyfplib.functools import split_last

print(split_last([1, 2, 3])) # ([1, 2], Some(3))
print(split_last([]))        # ([], Nothing())
```

---

## Поиск

### `index(predicate: Callable[..., bool | Option[Any]] | T, sequence: Sequence[T]) -> Option[int]`

Возвращает индекс первого совпадающего элемента. `predicate` может быть значением или вызываемым объектом; вызываемые объекты могут принимать `(value)`, `(value, index)` или `(value, index, sequence)`. Возвращает `Nothing()`, если ни один элемент не совпал.

```python
from pyfplib import index

numbers: list[int] = [1, 2, 3, 4]

print(index(3, numbers))                        # Some(2)
print(index(lambda value: value > 2, numbers))  # Some(2)
print(index(10, numbers))                       # Nothing()
```

### `find(callback: Callable[[T], Option[T] | bool], sequence: Sequence[T]) -> Option[T]`

Возвращает первый элемент, для которого `callback` возвращает непустой `Option` или любое истинное значение. Возвращает `Nothing()`, если ни один элемент не совпал.

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

## Проверка размера

### `is_empty(iterable: Sized) -> bool`

Возвращает `True`, когда `len(iterable) == 0`.

```python
from pyfplib import is_empty

print(is_empty([]))  # True
print(is_empty([1])) # False
```

### `is_not_empty(value: Sized) -> bool`

Возвращает `True`, когда `len(value) != 0`.

```python
from pyfplib import is_not_empty

print(is_not_empty([1])) # True
print(is_not_empty([]))  # False
```
