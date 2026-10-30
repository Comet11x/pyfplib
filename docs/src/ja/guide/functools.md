# 関数 API

`pyfplib.functools` モジュールは、シーケンス向けの小さく合成可能なヘルパーを提供します。ほとんどはトップレベルの `pyfplib` パッケージからも再エクスポートされていますが、`first`、`split_first`、`split_last` は `pyfplib.functools` からインポートする必要があります。

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

多くのヘルパーは 1 つ、2 つ、または 3 つの引数を持つコールバックを受け入れます。追加の引数には要素のインデックスとシーケンス全体が渡されます。

---

## 反復

### `for_each(function: Callable[..., None], sequence: Sequence[T]) -> None`

副作用のために `function` を各要素に適用します。コールバックは `(value)`、`(value, index)`、または `(value, index, sequence)` を受け取れます。

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

## 述語

### `any_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

少なくとも 1 つの要素が `predicate` を満たす場合に `True` を返し、空のシーケンスでは `False` を返します。コールバックは `(value)`、`(value, index)`、または `(value, index, sequence)` を受け取れます。

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

すべての要素が `predicate` を満たす場合に `True` を返し、空のシーケンスでは `True` を返します。コールバックは `(value)`、`(value, index)`、または `(value, index, sequence)` を受け取れます。

```python
from pyfplib import all_of

def is_positive(value: int) -> bool:
    return value > 0

print(all_of(is_positive, [1, 2, 3]))  # True
print(all_of(is_positive, [1, -1, 2])) # False
print(all_of(lambda value: False, [])) # True
```

### `none_of(predicate: Callable[..., bool], sequence: Sequence[T]) -> bool`

どの要素も `predicate` を満たさない場合に `True` を返し、空のシーケンスでは `True` を返します。コールバックは `(value)`、`(value, index)`、または `(value, index, sequence)` を受け取れます。

```python
from pyfplib import none_of

def is_negative(value: int) -> bool:
    return value < 0

print(none_of(is_negative, [1, 2, 3]))              # True
print(none_of(lambda value: value > 2, [1, 2, 3]))  # False
print(none_of(lambda value: True, []))              # True
```

---

## 畳み込み

### `fold(function: Callable[[Option[R], T], R] | Callable[[Option[R], T, int], R], sequence: Sequence[T], initial: R | None = None) -> Option[R]`

シーケンスを `Option[R]` に畳み込みます。コールバックは `Option[R]` であるアキュムレータと現在の要素を受け取り、必要に応じて要素インデックスも受け取ります。初期値がない場合、アキュムレータは `Nothing` から始まり、初期値なしで空のシーケンスを畳み込むと `Nothing()` を返します。

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

## 要素アクセス

### `head(iterable: Iterable[T]) -> Option[T]`

最初の要素を返すか、イテラブルが空の場合は `Nothing` を返します。任意のイテラブルを受け入れます。

```python
from pyfplib import head

print(head([10, 20])) # Some(10)
print(head([]))       # Nothing()
print(head("abc"))    # Some('a')
```

### `first(iterable: Iterable[T]) -> Option[T]`

任意のイテラブルの最初の要素を返します。`head` と同じように動作します。

```python
from pyfplib.functools import first

print(first("abc")) # Some('a')
print(first([]))    # Nothing()
```

### `last(sequence: Sequence[T]) -> Option[T]`

最後の要素を返すか、シーケンスが空の場合は `Nothing` を返します。

```python
from pyfplib import last

print(last([10, 20])) # Some(20)
print(last([]))       # Nothing()
```

### `tail(sequence: Sequence[T]) -> Sequence[T]`

最初の要素を除いたシーケンスを返します。空のシーケンスはそのまま返されます。

```python
from pyfplib import tail

print(tail([1, 2, 3])) # [2, 3]
print(tail([]))        # []
```

### `split_first(sequence: Sequence[T]) -> tuple[Option[T], Sequence[T]]`

シーケンスを最初の要素と残りの末尾に分割します。空のシーケンスは `(Nothing(), sequence)` を返します。

```python
from pyfplib.functools import split_first

print(split_first([1, 2, 3])) # (Some(1), [2, 3])
print(split_first([]))        # (Nothing(), [])
```

### `split_last(sequence: Sequence[T]) -> tuple[Sequence[T], Option[T]]`

シーケンスを先頭部分と最後の要素に分割します。空のシーケンスは `(sequence, Nothing())` を返します。

```python
from pyfplib.functools import split_last

print(split_last([1, 2, 3])) # ([1, 2], Some(3))
print(split_last([]))        # ([], Nothing())
```

---

## 検索

### `index(predicate: Callable[..., bool | Option[Any]] | T, sequence: Sequence[T]) -> Option[int]`

最初に一致する要素のインデックスを返します。`predicate` は値または呼び出し可能オブジェクトにできます。呼び出し可能オブジェクトは `(value)`、`(value, index)`、または `(value, index, sequence)` を受け取れます。一致する要素がない場合は `Nothing()` を返します。

```python
from pyfplib import index

numbers: list[int] = [1, 2, 3, 4]

print(index(3, numbers))                        # Some(2)
print(index(lambda value: value > 2, numbers))  # Some(2)
print(index(10, numbers))                       # Nothing()
```

### `find(callback: Callable[[T], Option[T] | bool], sequence: Sequence[T]) -> Option[T]`

`callback` が空でない `Option` または真の値を返す最初の要素を返します。一致する要素がない場合は `Nothing()` を返します。

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

## サイズチェック

### `is_empty(iterable: Sized) -> bool`

`len(iterable) == 0` のとき `True` を返します。

```python
from pyfplib import is_empty

print(is_empty([]))  # True
print(is_empty([1])) # False
```

### `is_not_empty(value: Sized) -> bool`

`len(value) != 0` のとき `True` を返します。

```python
from pyfplib import is_not_empty

print(is_not_empty([1])) # True
print(is_not_empty([]))  # False
```
