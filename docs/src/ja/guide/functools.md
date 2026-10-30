# 関数 API

`pyfplib.functools` モジュールは、シーケンスのための小さく合成可能なヘルパーを提供します。ほとんどはトップレベルの `pyfplib` パッケージからも再エクスポートされますが、`split_first` と `split_last` は `pyfplib.functools` からインポートする必要があります。

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

多くのヘルパーは 1 つ、2 つ、または 3 つの引数を持つコールバックを受け入れます。追加の引数には要素のインデックスとシーケンス全体が渡されます。

---

## 反復

### `for_each(function, sequence) -> None`

副作用のために各要素に `function` を適用します。

```python
>>> for_each(lambda v: print(v), [1, 2])
1
2
>>> for_each(lambda v, i: print(i, v), ["a", "b"])
0 a
1 b
```

---

## 述語

### `any_of(predicate, sequence) -> bool`

少なくとも 1 つの要素が `predicate` を満たす場合 `True` を返します。空のシーケンスでは `False` を返します。

```python
>>> any_of(lambda v: v > 2, [1, 2, 3])
True
>>> any_of(lambda v: v > 10, [1, 2, 3])
False
```

### `all_of(predicate, sequence) -> bool`

すべての要素が `predicate` を満たす場合 `True` を返します。空のシーケンスでは `True` を返します。

```python
>>> all_of(lambda v: v > 0, [1, 2, 3])
True
>>> all_of(lambda v: v > 0, [1, -1])
False
```

### `none_of(predicate, sequence) -> bool`

どの要素も `predicate` を満たさない場合 `True` を返します。

```python
>>> none_of(lambda v: v > 10, [1, 2, 3])
True
>>> none_of(lambda v: v > 2, [1, 2, 3])
False
```

---

## 畳み込み

### `fold(function, sequence, initial=None) -> Option[R]`

シーケンスを 1 つの値に還元します。コールバックはアキュムレータと現在の要素を受け取り、オプションで要素のインデックスも受け取ります。

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [1, 2, 3], 0)
Some(6)
>>> fold(lambda acc, v, i: acc.unwrap_or(0) + v + i, [1, 2, 3])
Some(9)
```

初期値がない場合、アキュムレータは `Nothing` から始まります。空のシーケンスを畳み込むと `Nothing()` を返します。

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [])
Nothing()
```

---

## 要素アクセス

### `head(iterable) -> Option[T]`

最初の要素を返すか、イテラブルが空の場合は `Nothing` を返します。任意のイテラブルを受け入れます。

```python
>>> head([10, 20])
Some(10)
>>> head([])
Nothing()
```

### `first(iterable) -> Option[T]`

任意のイテラブルの最初の要素を返すヘルパーです。

```python
>>> first("abc")
Some('a')
```

### `last(sequence) -> Option[T]`

最後の要素を返すか、シーケンスが空の場合は `Nothing` を返します。

```python
>>> last([10, 20])
Some(20)
>>> last([])
Nothing()
```

### `tail(sequence) -> Sequence[T]`

最初の要素を除いたシーケンスを返します。空のシーケンスはそのまま返されます。

```python
>>> tail([1, 2, 3])
[2, 3]
>>> tail([])
[]
```

### `split_first(sequence) -> tuple[Option[T], Sequence[T]]`

シーケンスを最初の要素と残りの末尾に分割します。

```python
>>> split_first([1, 2, 3])
(Some(1), [2, 3])
>>> split_first([])
(Nothing(), [])
```

### `split_last(sequence) -> tuple[Sequence[T], Option[T]]`

シーケンスを先頭部分と最後の要素に分割します。

```python
>>> split_last([1, 2, 3])
([1, 2], Some(3))
>>> split_last([])
([], Nothing())
```

---

## 検索

### `index(predicate, sequence) -> Option[int]`

最初に一致する要素のインデックスを返します。`predicate` は呼び出し可能オブジェクトまたは比較する値です。

```python
>>> index(3, [1, 2, 3, 4])
Some(2)
>>> index(lambda v: v > 2, [1, 2, 3, 4])
Some(2)
>>> index(10, [1, 2, 3])
Nothing()
```

### `find(callback, sequence) -> Option[T]`

`callback` が空でない `Option` または真の値を返す最初の要素を返します。

```python
>>> find(lambda v: Some(v) if v % 2 == 0 else Nothing(), [1, 2, 3])
Some(2)
>>> find(lambda v: v > 2, [1, 2, 3])
Some(3)
>>> find(lambda v: v > 10, [1, 2, 3])
Nothing()
```

---

## サイズチェック

### `is_empty(iterable) -> bool`

`len(iterable) == 0` のとき `True` を返します。

```python
>>> is_empty([])
True
>>> is_empty([1])
False
```

### `is_not_empty(value) -> bool`

`len(value) != 0` のとき `True` を返します。

```python
>>> is_not_empty([1])
True
>>> is_not_empty([])
False
```
