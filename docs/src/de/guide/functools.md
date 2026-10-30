# Funktions-API

Das Modul `pyfplib.functools` bietet kleine, komponierbare Helfer für Sequenzen. Die meisten werden auch aus dem Paket `pyfplib` re-exportiert; `split_first` und `split_last` müssen aus `pyfplib.functools` importiert werden.

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

Viele Helfer akzeptieren Callbacks mit einem, zwei oder drei Parametern. Die zusätzlichen Parameter erhalten den Elementindex und die vollständige Sequenz.

---

## Iteration

### `for_each(function, sequence) -> None`

Wendet `function` auf jedes Element an, um Seiteneffekte auszuführen.

```python
>>> for_each(lambda v: print(v), [1, 2])
1
2
>>> for_each(lambda v, i: print(i, v), ["a", "b"])
0 a
1 b
```

---

## Prädikate

### `any_of(predicate, sequence) -> bool`

Gibt `True` zurück, wenn mindestens ein Element `predicate` erfüllt. Für eine leere Sequenz wird `False` zurückgegeben.

```python
>>> any_of(lambda v: v > 2, [1, 2, 3])
True
>>> any_of(lambda v: v > 10, [1, 2, 3])
False
```

### `all_of(predicate, sequence) -> bool`

Gibt `True` zurück, wenn jedes Element `predicate` erfüllt. Für eine leere Sequenz wird `True` zurückgegeben.

```python
>>> all_of(lambda v: v > 0, [1, 2, 3])
True
>>> all_of(lambda v: v > 0, [1, -1])
False
```

### `none_of(predicate, sequence) -> bool`

Gibt `True` zurück, wenn kein Element `predicate` erfüllt.

```python
>>> none_of(lambda v: v > 10, [1, 2, 3])
True
>>> none_of(lambda v: v > 2, [1, 2, 3])
False
```

---

## Falten

### `fold(function, sequence, initial=None) -> Option[R]`

Reduziert eine Sequenz auf einen einzelnen Wert. Der Callback erhält den Akkumulator und das aktuelle Element sowie optional den Elementindex.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [1, 2, 3], 0)
Some(6)
>>> fold(lambda acc, v, i: acc.unwrap_or(0) + v + i, [1, 2, 3])
Some(9)
```

Ohne Anfangswert startet der Akkumulator als `Nothing`; das Falten einer leeren Sequenz gibt `Nothing()` zurück.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [])
Nothing()
```

---

## Elementzugriff

### `head(iterable) -> Option[T]`

Gibt das erste Element zurück oder `Nothing`, wenn das Iterable leer ist. Akzeptiert jedes Iterable.

```python
>>> head([10, 20])
Some(10)
>>> head([])
Nothing()
```

### `first(iterable) -> Option[T]`

Helfer, der das erste Element eines beliebigen Iterables zurückgibt.

```python
>>> first("abc")
Some('a')
```

### `last(sequence) -> Option[T]`

Gibt das letzte Element zurück oder `Nothing`, wenn die Sequenz leer ist.

```python
>>> last([10, 20])
Some(20)
>>> last([])
Nothing()
```

### `tail(sequence) -> Sequence[T]`

Gibt die Sequenz ohne ihr erstes Element zurück. Leere Sequenzen werden unverändert zurückgegeben.

```python
>>> tail([1, 2, 3])
[2, 3]
>>> tail([])
[]
```

### `split_first(sequence) -> tuple[Option[T], Sequence[T]]`

Teilt eine Sequenz in ihr erstes Element und den verbleibenden Rest.

```python
>>> split_first([1, 2, 3])
(Some(1), [2, 3])
>>> split_first([])
(Nothing(), [])
```

### `split_last(sequence) -> tuple[Sequence[T], Option[T]]`

Teilt eine Sequenz in ihren Anfangsteil und ihr letztes Element.

```python
>>> split_last([1, 2, 3])
([1, 2], Some(3))
>>> split_last([])
([], Nothing())
```

---

## Suchen

### `index(predicate, sequence) -> Option[int]`

Gibt den Index des ersten passenden Elements zurück. `predicate` kann ein Callable oder ein Vergleichswert sein.

```python
>>> index(3, [1, 2, 3, 4])
Some(2)
>>> index(lambda v: v > 2, [1, 2, 3, 4])
Some(2)
>>> index(10, [1, 2, 3])
Nothing()
```

### `find(callback, sequence) -> Option[T]`

Gibt das erste Element zurück, für das `callback` ein nicht leeres `Option` oder einen wahren Wert zurückgibt.

```python
>>> find(lambda v: Some(v) if v % 2 == 0 else Nothing(), [1, 2, 3])
Some(2)
>>> find(lambda v: v > 2, [1, 2, 3])
Some(3)
>>> find(lambda v: v > 10, [1, 2, 3])
Nothing()
```

---

## Größenprüfungen

### `is_empty(iterable) -> bool`

Gibt `True` zurück, wenn `len(iterable) == 0`.

```python
>>> is_empty([])
True
>>> is_empty([1])
False
```

### `is_not_empty(value) -> bool`

Gibt `True` zurück, wenn `len(value) != 0`.

```python
>>> is_not_empty([1])
True
>>> is_not_empty([])
False
```
