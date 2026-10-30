# API функций

Модуль `pyfplib.functools` предоставляет небольшие композируемые помощники для последовательностей. Большинство из них также реэкспортируются из пакета `pyfplib` верхнего уровня; `split_first` и `split_last` нужно импортировать из `pyfplib.functools`.

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

Многие помощники принимают обратные вызовы с одним, двумя или тремя параметрами. Дополнительные параметры получают индекс элемента и всю последовательность.

---

## Итерация

### `for_each(function, sequence) -> None`

Применяет `function` к каждому элементу ради побочных эффектов.

```python
>>> for_each(lambda v: print(v), [1, 2])
1
2
>>> for_each(lambda v, i: print(i, v), ["a", "b"])
0 a
1 b
```

---

## Предикаты

### `any_of(predicate, sequence) -> bool`

Возвращает `True`, когда хотя бы один элемент удовлетворяет `predicate`. Для пустой последовательности возвращает `False`.

```python
>>> any_of(lambda v: v > 2, [1, 2, 3])
True
>>> any_of(lambda v: v > 10, [1, 2, 3])
False
```

### `all_of(predicate, sequence) -> bool`

Возвращает `True`, когда каждый элемент удовлетворяет `predicate`. Для пустой последовательности возвращает `True`.

```python
>>> all_of(lambda v: v > 0, [1, 2, 3])
True
>>> all_of(lambda v: v > 0, [1, -1])
False
```

### `none_of(predicate, sequence) -> bool`

Возвращает `True`, когда ни один элемент не удовлетворяет `predicate`.

```python
>>> none_of(lambda v: v > 10, [1, 2, 3])
True
>>> none_of(lambda v: v > 2, [1, 2, 3])
False
```

---

## Свёртка

### `fold(function, sequence, initial=None) -> Option[R]`

Сводит последовательность к одному значению. Обратный вызов получает аккумулятор и текущий элемент, а также (необязательно) индекс элемента.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [1, 2, 3], 0)
Some(6)
>>> fold(lambda acc, v, i: acc.unwrap_or(0) + v + i, [1, 2, 3])
Some(9)
```

Без начального значения аккумулятор начинается с `Nothing`; свёртка пустой последовательности возвращает `Nothing()`.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [])
Nothing()
```

---

## Доступ к элементам

### `head(iterable) -> Option[T]`

Возвращает первый элемент или `Nothing`, если итерируемый объект пуст. Принимает любой итерируемый объект.

```python
>>> head([10, 20])
Some(10)
>>> head([])
Nothing()
```

### `first(iterable) -> Option[T]`

Помощник, возвращающий первый элемент любого итерируемого объекта.

```python
>>> first("abc")
Some('a')
```

### `last(sequence) -> Option[T]`

Возвращает последний элемент или `Nothing`, если последовательность пуста.

```python
>>> last([10, 20])
Some(20)
>>> last([])
Nothing()
```

### `tail(sequence) -> Sequence[T]`

Возвращает последовательность без первого элемента. Пустые последовательности возвращаются без изменений.

```python
>>> tail([1, 2, 3])
[2, 3]
>>> tail([])
[]
```

### `split_first(sequence) -> tuple[Option[T], Sequence[T]]`

Разделяет последовательность на первый элемент и оставшийся хвост.

```python
>>> split_first([1, 2, 3])
(Some(1), [2, 3])
>>> split_first([])
(Nothing(), [])
```

### `split_last(sequence) -> tuple[Sequence[T], Option[T]]`

Разделяет последовательность на начальную часть и последний элемент.

```python
>>> split_last([1, 2, 3])
([1, 2], Some(3))
>>> split_last([])
([], Nothing())
```

---

## Поиск

### `index(predicate, sequence) -> Option[int]`

Возвращает индекс первого подходящего элемента. `predicate` может быть вызываемым объектом или значением для сравнения.

```python
>>> index(3, [1, 2, 3, 4])
Some(2)
>>> index(lambda v: v > 2, [1, 2, 3, 4])
Some(2)
>>> index(10, [1, 2, 3])
Nothing()
```

### `find(callback, sequence) -> Option[T]`

Возвращает первый элемент, для которого `callback` возвращает непустой `Option` или любое истинное значение.

```python
>>> find(lambda v: Some(v) if v % 2 == 0 else Nothing(), [1, 2, 3])
Some(2)
>>> find(lambda v: v > 2, [1, 2, 3])
Some(3)
>>> find(lambda v: v > 10, [1, 2, 3])
Nothing()
```

---

## Проверка размера

### `is_empty(iterable) -> bool`

Возвращает `True`, когда `len(iterable) == 0`.

```python
>>> is_empty([])
True
>>> is_empty([1])
False
```

### `is_not_empty(value) -> bool`

Возвращает `True`, когда `len(value) != 0`.

```python
>>> is_not_empty([1])
True
>>> is_not_empty([])
False
```
