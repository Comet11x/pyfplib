# 함수 API

`pyfplib.functools` 모듈은 시퀀스를 위한 작고 조합 가능한 도우미를 제공합니다. 대부분은 최상위 `pyfplib` 패키지에서도 다시 내보내며, `split_first`와 `split_last`는 `pyfplib.functools`에서 가져와야 합니다.

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

많은 도우미가 하나, 둘 또는 세 개의 매개변수를 받는 콜백을 허용합니다. 추가 매개변수는 요소 인덱스와 전체 시퀀스를 받습니다.

---

## 반복

### `for_each(function, sequence) -> None`

부수 효과를 위해 각 요소에 `function`을 적용합니다.

```python
>>> for_each(lambda v: print(v), [1, 2])
1
2
>>> for_each(lambda v, i: print(i, v), ["a", "b"])
0 a
1 b
```

---

## 조건자

### `any_of(predicate, sequence) -> bool`

적어도 하나의 요소가 `predicate`를 만족하면 `True`를 반환합니다. 빈 시퀀스에는 `False`를 반환합니다.

```python
>>> any_of(lambda v: v > 2, [1, 2, 3])
True
>>> any_of(lambda v: v > 10, [1, 2, 3])
False
```

### `all_of(predicate, sequence) -> bool`

모든 요소가 `predicate`를 만족하면 `True`를 반환합니다. 빈 시퀀스에는 `True`를 반환합니다.

```python
>>> all_of(lambda v: v > 0, [1, 2, 3])
True
>>> all_of(lambda v: v > 0, [1, -1])
False
```

### `none_of(predicate, sequence) -> bool`

어떤 요소도 `predicate`를 만족하지 않으면 `True`를 반환합니다.

```python
>>> none_of(lambda v: v > 10, [1, 2, 3])
True
>>> none_of(lambda v: v > 2, [1, 2, 3])
False
```

---

## 폴딩

### `fold(function, sequence, initial=None) -> Option[R]`

시퀀스를 하나의 값으로 축소합니다. 콜백은 누산기와 현재 요소를 받고, 선택적으로 요소 인덱스도 받습니다.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [1, 2, 3], 0)
Some(6)
>>> fold(lambda acc, v, i: acc.unwrap_or(0) + v + i, [1, 2, 3])
Some(9)
```

초기 값이 없으면 누산기는 `Nothing`으로 시작하며, 빈 시퀀스를 폴딩하면 `Nothing()`을 반환합니다.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [])
Nothing()
```

---

## 요소 접근

### `head(iterable) -> Option[T]`

첫 번째 요소를 반환하거나, 이터러블이 비어 있으면 `Nothing`을 반환합니다. 모든 이터러블을 받습니다.

```python
>>> head([10, 20])
Some(10)
>>> head([])
Nothing()
```

### `first(iterable) -> Option[T]`

모든 이터러블의 첫 번째 요소를 반환하는 도우미입니다.

```python
>>> first("abc")
Some('a')
```

### `last(sequence) -> Option[T]`

마지막 요소를 반환하거나, 시퀀스가 비어 있으면 `Nothing`을 반환합니다.

```python
>>> last([10, 20])
Some(20)
>>> last([])
Nothing()
```

### `tail(sequence) -> Sequence[T]`

첫 번째 요소를 제외한 시퀀스를 반환합니다. 빈 시퀀스는 그대로 반환됩니다.

```python
>>> tail([1, 2, 3])
[2, 3]
>>> tail([])
[]
```

### `split_first(sequence) -> tuple[Option[T], Sequence[T]]`

시퀀스를 첫 번째 요소와 나머지 꼬리로 나눕니다.

```python
>>> split_first([1, 2, 3])
(Some(1), [2, 3])
>>> split_first([])
(Nothing(), [])
```

### `split_last(sequence) -> tuple[Sequence[T], Option[T]]`

시퀀스를 초기 부분과 마지막 요소로 나눕니다.

```python
>>> split_last([1, 2, 3])
([1, 2], Some(3))
>>> split_last([])
([], Nothing())
```

---

## 검색

### `index(predicate, sequence) -> Option[int]`

첫 번째 일치 요소의 인덱스를 반환합니다. `predicate`는 호출 가능 객체 또는 비교할 값일 수 있습니다.

```python
>>> index(3, [1, 2, 3, 4])
Some(2)
>>> index(lambda v: v > 2, [1, 2, 3, 4])
Some(2)
>>> index(10, [1, 2, 3])
Nothing()
```

### `find(callback, sequence) -> Option[T]`

`callback`이 비어 있지 않은 `Option` 또는 참인 값을 반환하는 첫 번째 요소를 반환합니다.

```python
>>> find(lambda v: Some(v) if v % 2 == 0 else Nothing(), [1, 2, 3])
Some(2)
>>> find(lambda v: v > 2, [1, 2, 3])
Some(3)
>>> find(lambda v: v > 10, [1, 2, 3])
Nothing()
```

---

## 크기 확인

### `is_empty(iterable) -> bool`

`len(iterable) == 0`이면 `True`를 반환합니다.

```python
>>> is_empty([])
True
>>> is_empty([1])
False
```

### `is_not_empty(value) -> bool`

`len(value) != 0`이면 `True`를 반환합니다.

```python
>>> is_not_empty([1])
True
>>> is_not_empty([])
False
```
