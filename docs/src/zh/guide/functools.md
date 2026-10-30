# 函数 API

`pyfplib.functools` 模块提供小型、可组合的序列辅助函数。大多数函数也从顶层 `pyfplib` 包重新导出；`first`、`split_first` 和 `split_last` 必须从 `pyfplib.functools` 导入。

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

许多辅助函数接受带一个、两个或三个参数的回调。额外参数接收元素索引和完整序列。

---

## 迭代

### `for_each(function: Callable[..., None], sequence: Sequence[T]) -> None`

对每个元素应用 `function`，用于产生副作用。回调可以接受 `(value)`、`(value, index)` 或 `(value, index, sequence)`。

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

## 谓词

### `any_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

当至少一个元素满足 `predicate` 时返回 `True`；空序列返回 `False`。回调可以接受 `(value)`、`(value, index)` 或 `(value, index, sequence)`。

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

当每个元素都满足 `predicate` 时返回 `True`；空序列返回 `True`。回调可以接受 `(value)`、`(value, index)` 或 `(value, index, sequence)`。

```python
from pyfplib import all_of

def is_positive(value: int) -> bool:
    return value > 0

print(all_of(is_positive, [1, 2, 3]))  # True
print(all_of(is_positive, [1, -1, 2])) # False
print(all_of(lambda value: False, [])) # True
```

### `none_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

当没有元素满足 `predicate` 时返回 `True`；空序列返回 `True`。回调可以接受 `(value)`、`(value, index)` 或 `(value, index, sequence)`。

```python
from pyfplib import none_of

def is_negative(value: int) -> bool:
    return value < 0

print(none_of(is_negative, [1, 2, 3]))              # True
print(none_of(lambda value: value > 2, [1, 2, 3]))  # False
print(none_of(lambda value: True, []))              # True
```

---

## 折叠

### `fold(function: Callable[[Option[R], T], R] | Callable[[Option[R], T, int], R], sequence: Sequence[T], initial: R | None = None) -> Option[R]`

将序列归约为 `Option[R]`。回调接收作为 `Option[R]` 的累加器和当前元素，并可选接收元素索引。没有初始值时，累加器从 `Nothing` 开始；在没有初始值的情况下折叠空序列会返回 `Nothing()`。

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

## 元素访问

### `head(iterable: Iterable[T]) -> Option[T]`

返回第一个元素；可迭代对象为空时返回 `Nothing`。接受任何可迭代对象。

```python
from pyfplib import head

print(head([10, 20])) # Some(10)
print(head([]))       # Nothing()
print(head("abc"))    # Some('a')
```

### `first(iterable: Iterable[T]) -> Option[T]`

返回任何可迭代对象的第一个元素。行为与 `head` 相同。

```python
from pyfplib.functools import first

print(first("abc")) # Some('a')
print(first([]))    # Nothing()
```

### `last(sequence: Sequence[T]) -> Option[T]`

返回最后一个元素；序列为空时返回 `Nothing`。

```python
from pyfplib import last

print(last([10, 20])) # Some(20)
print(last([]))       # Nothing()
```

### `tail(sequence: Sequence[T]) -> Sequence[T]`

返回去掉第一个元素后的序列。空序列原样返回。

```python
from pyfplib import tail

print(tail([1, 2, 3])) # [2, 3]
print(tail([]))        # []
```

### `split_first(sequence: Sequence[T]) -> tuple[Option[T], Sequence[T]]`

将序列拆分为第一个元素和剩余尾部。空序列返回 `(Nothing(), sequence)`。

```python
from pyfplib.functools import split_first

print(split_first([1, 2, 3])) # (Some(1), [2, 3])
print(split_first([]))        # (Nothing(), [])
```

### `split_last(sequence: Sequence[T]) -> tuple[Sequence[T], Option[T]]`

将序列拆分为初始部分和最后一个元素。空序列返回 `(sequence, Nothing())`。

```python
from pyfplib.functools import split_last

print(split_last([1, 2, 3])) # ([1, 2], Some(3))
print(split_last([]))        # ([], Nothing())
```

---

## 搜索

### `index(predicate: Callable[..., bool | Option[Any]] | T, sequence: Sequence[T]) -> Option[int]`

返回第一个匹配元素的索引。`predicate` 可以是值或可调用对象；可调用对象可以接受 `(value)`、`(value, index)` 或 `(value, index, sequence)`。没有元素匹配时返回 `Nothing()`。

```python
from pyfplib import index

numbers: list[int] = [1, 2, 3, 4]

print(index(3, numbers))                        # Some(2)
print(index(lambda value: value > 2, numbers))  # Some(2)
print(index(10, numbers))                       # Nothing()
```

### `find(callback: Callable[[T], Option[T] | bool], sequence: Sequence[T]) -> Option[T]`

返回第一个使 `callback` 返回非空 `Option` 或任何真值的元素。没有元素匹配时返回 `Nothing()`。

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

## 大小检查

### `is_empty(iterable: Sized) -> bool`

当 `len(iterable) == 0` 时返回 `True`。

```python
from pyfplib import is_empty

print(is_empty([]))  # True
print(is_empty([1])) # False
```

### `is_not_empty(value: Sized) -> bool`

当 `len(value) != 0` 时返回 `True`。

```python
from pyfplib import is_not_empty

print(is_not_empty([1])) # True
print(is_not_empty([]))  # False
```
