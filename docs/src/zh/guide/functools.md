# 函数 API

`pyfplib.functools` 模块提供小型、可组合的序列辅助函数。大多数函数也从顶层 `pyfplib` 包重新导出；`split_first` 和 `split_last` 必须从 `pyfplib.functools` 导入。

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

许多辅助函数接受带一个、两个或三个参数的回调。额外参数接收元素索引和完整序列。

---

## 迭代

### `for_each(function, sequence) -> None`

对每个元素应用 `function`，用于副作用。

```python
>>> for_each(lambda v: print(v), [1, 2])
1
2
>>> for_each(lambda v, i: print(i, v), ["a", "b"])
0 a
1 b
```

---

## 谓词

### `any_of(predicate, sequence) -> bool`

当至少一个元素满足 `predicate` 时返回 `True`。空序列返回 `False`。

```python
>>> any_of(lambda v: v > 2, [1, 2, 3])
True
>>> any_of(lambda v: v > 10, [1, 2, 3])
False
```

### `all_of(predicate, sequence) -> bool`

当每个元素都满足 `predicate` 时返回 `True`。空序列返回 `True`。

```python
>>> all_of(lambda v: v > 0, [1, 2, 3])
True
>>> all_of(lambda v: v > 0, [1, -1])
False
```

### `none_of(predicate, sequence) -> bool`

当没有元素满足 `predicate` 时返回 `True`。

```python
>>> none_of(lambda v: v > 10, [1, 2, 3])
True
>>> none_of(lambda v: v > 2, [1, 2, 3])
False
```

---

## 折叠

### `fold(function, sequence, initial=None) -> Option[R]`

将序列归约为单个值。回调接收累加器和当前元素，也可接收元素索引。

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [1, 2, 3], 0)
Some(6)
>>> fold(lambda acc, v, i: acc.unwrap_or(0) + v + i, [1, 2, 3])
Some(9)
```

没有初始值时，累加器从 `Nothing` 开始；折叠空序列返回 `Nothing()`。

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [])
Nothing()
```

---

## 元素访问

### `head(iterable) -> Option[T]`

返回第一个元素；可迭代对象为空时返回 `Nothing`。接受任何可迭代对象。

```python
>>> head([10, 20])
Some(10)
>>> head([])
Nothing()
```

### `first(iterable) -> Option[T]`

返回任何可迭代对象第一个元素的辅助函数。

```python
>>> first("abc")
Some('a')
```

### `last(sequence) -> Option[T]`

返回最后一个元素；序列为空时返回 `Nothing`。

```python
>>> last([10, 20])
Some(20)
>>> last([])
Nothing()
```

### `tail(sequence) -> Sequence[T]`

返回去掉第一个元素后的序列。空序列原样返回。

```python
>>> tail([1, 2, 3])
[2, 3]
>>> tail([])
[]
```

### `split_first(sequence) -> tuple[Option[T], Sequence[T]]`

将序列拆分为第一个元素和剩余尾部。

```python
>>> split_first([1, 2, 3])
(Some(1), [2, 3])
>>> split_first([])
(Nothing(), [])
```

### `split_last(sequence) -> tuple[Sequence[T], Option[T]]`

将序列拆分为初始部分和最后一个元素。

```python
>>> split_last([1, 2, 3])
([1, 2], Some(3))
>>> split_last([])
([], Nothing())
```

---

## 搜索

### `index(predicate, sequence) -> Option[int]`

返回第一个匹配元素的索引。`predicate` 可以是可调用对象或用于比较的值。

```python
>>> index(3, [1, 2, 3, 4])
Some(2)
>>> index(lambda v: v > 2, [1, 2, 3, 4])
Some(2)
>>> index(10, [1, 2, 3])
Nothing()
```

### `find(callback, sequence) -> Option[T]`

返回第一个使 `callback` 返回非空 `Option` 或任何真值的元素。

```python
>>> find(lambda v: Some(v) if v % 2 == 0 else Nothing(), [1, 2, 3])
Some(2)
>>> find(lambda v: v > 2, [1, 2, 3])
Some(3)
>>> find(lambda v: v > 10, [1, 2, 3])
Nothing()
```

---

## 大小检查

### `is_empty(iterable) -> bool`

当 `len(iterable) == 0` 时返回 `True`。

```python
>>> is_empty([])
True
>>> is_empty([1])
False
```

### `is_not_empty(value) -> bool`

当 `len(value) != 0` 时返回 `True`。

```python
>>> is_not_empty([1])
True
>>> is_not_empty([])
False
```
