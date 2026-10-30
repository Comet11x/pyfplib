# 함수 API

`pyfplib.functools` 모듈은 시퀀스를 위한 작고 조합 가능한 헬퍼를 제공합니다. 대부분은 최상위 `pyfplib` 패키지에서도 다시 내보내지지만, `first`, `split_first`, `split_last`는 `pyfplib.functools`에서 가져와야 합니다.

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

많은 도우미가 하나, 둘 또는 세 개의 매개변수를 받는 콜백을 허용합니다. 추가 매개변수는 요소 인덱스와 전체 시퀀스를 받습니다.

---

## 반복

### `for_each(function: Callable[..., None], sequence: Sequence[T]) -> None`

부수 효과를 위해 `function`을 각 요소에 적용합니다. 콜백은 `(value)`, `(value, index)`, `(value, index, sequence)`를 받을 수 있습니다.

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

## 조건자

### `any_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

적어도 하나의 요소가 `predicate`를 만족하면 `True`를 반환하고, 빈 시퀀스에는 `False`를 반환합니다. 콜백은 `(value)`, `(value, index)`, `(value, index, sequence)`를 받을 수 있습니다.

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

모든 요소가 `predicate`를 만족하면 `True`를 반환하고, 빈 시퀀스에는 `True`를 반환합니다. 콜백은 `(value)`, `(value, index)`, `(value, index, sequence)`를 받을 수 있습니다.

```python
from pyfplib import all_of

def is_positive(value: int) -> bool:
    return value > 0

print(all_of(is_positive, [1, 2, 3]))  # True
print(all_of(is_positive, [1, -1, 2])) # False
print(all_of(lambda value: False, [])) # True
```

### `none_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

어떤 요소도 `predicate`를 만족하지 않으면 `True`를 반환하고, 빈 시퀀스에는 `True`를 반환합니다. 콜백은 `(value)`, `(value, index)`, `(value, index, sequence)`를 받을 수 있습니다.

```python
from pyfplib import none_of

def is_negative(value: int) -> bool:
    return value < 0

print(none_of(is_negative, [1, 2, 3]))              # True
print(none_of(lambda value: value > 2, [1, 2, 3]))  # False
print(none_of(lambda value: True, []))              # True
```

---

## 폴딩

### `fold(function: Callable[[Option[R], T], R] | Callable[[Option[R], T, int], R], sequence: Sequence[T], initial: R | None = None) -> Option[R]`

시퀀스를 `Option[R]`로 축소합니다. 콜백은 `Option[R]`인 누산기와 현재 요소를 받고, 선택적으로 요소 인덱스도 받습니다. 초기값이 없으면 누산기는 `Nothing`으로 시작하며, 초기값 없이 빈 시퀀스를 접으면 `Nothing()`을 반환합니다.

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

## 요소 접근

### `head(iterable: Iterable[T]) -> Option[T]`

첫 번째 요소를 반환하거나, 이터러블이 비어 있으면 `Nothing`을 반환합니다. 모든 이터러블을 받습니다.

```python
from pyfplib import head

print(head([10, 20])) # Some(10)
print(head([]))       # Nothing()
print(head("abc"))    # Some('a')
```

### `first(iterable: Iterable[T]) -> Option[T]`

모든 이터러블의 첫 번째 요소를 반환합니다. `head`와 동일하게 동작합니다.

```python
from pyfplib.functools import first

print(first("abc")) # Some('a')
print(first([]))    # Nothing()
```

### `last(sequence: Sequence[T]) -> Option[T]`

마지막 요소를 반환하거나, 시퀀스가 비어 있으면 `Nothing`을 반환합니다.

```python
from pyfplib import last

print(last([10, 20])) # Some(20)
print(last([]))       # Nothing()
```

### `tail(sequence: Sequence[T]) -> Sequence[T]`

첫 번째 요소를 제외한 시퀀스를 반환합니다. 빈 시퀀스는 그대로 반환됩니다.

```python
from pyfplib import tail

print(tail([1, 2, 3])) # [2, 3]
print(tail([]))        # []
```

### `split_first(sequence: Sequence[T]) -> tuple[Option[T], Sequence[T]]`

시퀀스를 첫 번째 요소와 나머지 꼬리로 분할합니다. 빈 시퀀스는 `(Nothing(), sequence)`를 반환합니다.

```python
from pyfplib.functools import split_first

print(split_first([1, 2, 3])) # (Some(1), [2, 3])
print(split_first([]))        # (Nothing(), [])
```

### `split_last(sequence: Sequence[T]) -> tuple[Sequence[T], Option[T]]`

시퀀스를 초기 부분과 마지막 요소로 분할합니다. 빈 시퀀스는 `(sequence, Nothing())`을 반환합니다.

```python
from pyfplib.functools import split_last

print(split_last([1, 2, 3])) # ([1, 2], Some(3))
print(split_last([]))        # ([], Nothing())
```

---

## 검색

### `index(predicate: Callable[..., bool | Option[Any]] | T, sequence: Sequence[T]) -> Option[int]`

첫 번째로 일치하는 요소의 인덱스를 반환합니다. `predicate`는 값 또는 호출 가능 객체일 수 있으며, 호출 가능 객체는 `(value)`, `(value, index)`, `(value, index, sequence)`를 받을 수 있습니다. 일치하는 요소가 없으면 `Nothing()`을 반환합니다.

```python
from pyfplib import index

numbers: list[int] = [1, 2, 3, 4]

print(index(3, numbers))                        # Some(2)
print(index(lambda value: value > 2, numbers))  # Some(2)
print(index(10, numbers))                       # Nothing()
```

### `find(callback: Callable[[T], Option[T] | bool], sequence: Sequence[T]) -> Option[T]`

`callback`이 비어 있지 않은 `Option` 또는 참인 값을 반환하는 첫 번째 요소를 반환합니다. 일치하는 요소가 없으면 `Nothing()`을 반환합니다.

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

## 크기 확인

### `is_empty(iterable: Sized) -> bool`

`len(iterable) == 0`이면 `True`를 반환합니다.

```python
from pyfplib import is_empty

print(is_empty([]))  # True
print(is_empty([1])) # False
```

### `is_not_empty(value: Sized) -> bool`

`len(value) != 0`이면 `True`를 반환합니다.

```python
from pyfplib import is_not_empty

print(is_not_empty([1])) # True
print(is_not_empty([]))  # False
```
