# API Funzioni

Il modulo `pyfplib.functools` fornisce piccoli helper componibili per le sequenze. La maggior parte è anche riesportata dal pacchetto `pyfplib`; `split_first` e `split_last` devono essere importati da `pyfplib.functools`.

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

Molti helper accettano callback con uno, due o tre parametri. I parametri extra ricevono l'indice dell'elemento e l'intera sequenza.

---

## Iterazione

### `for_each(function, sequence) -> None`

Applica `function` a ogni elemento per i suoi effetti collaterali.

```python
>>> for_each(lambda v: print(v), [1, 2])
1
2
>>> for_each(lambda v, i: print(i, v), ["a", "b"])
0 a
1 b
```

---

## Predicati

### `any_of(predicate, sequence) -> bool`

Restituisce `True` quando almeno un elemento soddisfa `predicate`. Restituisce `False` per una sequenza vuota.

```python
>>> any_of(lambda v: v > 2, [1, 2, 3])
True
>>> any_of(lambda v: v > 10, [1, 2, 3])
False
```

### `all_of(predicate, sequence) -> bool`

Restituisce `True` quando ogni elemento soddisfa `predicate`. Restituisce `True` per una sequenza vuota.

```python
>>> all_of(lambda v: v > 0, [1, 2, 3])
True
>>> all_of(lambda v: v > 0, [1, -1])
False
```

### `none_of(predicate, sequence) -> bool`

Restituisce `True` quando nessun elemento soddisfa `predicate`.

```python
>>> none_of(lambda v: v > 10, [1, 2, 3])
True
>>> none_of(lambda v: v > 2, [1, 2, 3])
False
```

---

## Folding

### `fold(function, sequence, initial=None) -> Option[R]`

Riduce una sequenza a un singolo valore. Il callback riceve l'accumulatore e l'elemento corrente, e opzionalmente l'indice dell'elemento.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [1, 2, 3], 0)
Some(6)
>>> fold(lambda acc, v, i: acc.unwrap_or(0) + v + i, [1, 2, 3])
Some(9)
```

Senza un valore iniziale l'accumulatore parte da `Nothing`; il folding di una sequenza vuota restituisce `Nothing()`.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [])
Nothing()
```

---

## Accesso agli elementi

### `head(iterable) -> Option[T]`

Restituisce il primo elemento, o `Nothing` quando l'iterabile è vuoto. Accetta qualsiasi iterabile.

```python
>>> head([10, 20])
Some(10)
>>> head([])
Nothing()
```

### `first(iterable) -> Option[T]`

Helper che restituisce il primo elemento di qualsiasi iterabile.

```python
>>> first("abc")
Some('a')
```

### `last(sequence) -> Option[T]`

Restituisce l'ultimo elemento, o `Nothing` quando la sequenza è vuota.

```python
>>> last([10, 20])
Some(20)
>>> last([])
Nothing()
```

### `tail(sequence) -> Sequence[T]`

Restituisce la sequenza senza il primo elemento. Le sequenze vuote vengono restituite invariate.

```python
>>> tail([1, 2, 3])
[2, 3]
>>> tail([])
[]
```

### `split_first(sequence) -> tuple[Option[T], Sequence[T]]`

Divide una sequenza nel primo elemento e nella coda rimanente.

```python
>>> split_first([1, 2, 3])
(Some(1), [2, 3])
>>> split_first([])
(Nothing(), [])
```

### `split_last(sequence) -> tuple[Sequence[T], Option[T]]`

Divide una sequenza nella parte iniziale e nell'ultimo elemento.

```python
>>> split_last([1, 2, 3])
([1, 2], Some(3))
>>> split_last([])
([], Nothing())
```

---

## Ricerca

### `index(predicate, sequence) -> Option[int]`

Restituisce l'indice del primo elemento corrispondente. `predicate` può essere un callable o un valore da confrontare.

```python
>>> index(3, [1, 2, 3, 4])
Some(2)
>>> index(lambda v: v > 2, [1, 2, 3, 4])
Some(2)
>>> index(10, [1, 2, 3])
Nothing()
```

### `find(callback, sequence) -> Option[T]`

Restituisce il primo elemento per cui `callback` restituisce un `Option` non vuoto o un valore vero.

```python
>>> find(lambda v: Some(v) if v % 2 == 0 else Nothing(), [1, 2, 3])
Some(2)
>>> find(lambda v: v > 2, [1, 2, 3])
Some(3)
>>> find(lambda v: v > 10, [1, 2, 3])
Nothing()
```

---

## Controlli di dimensione

### `is_empty(iterable) -> bool`

Restituisce `True` quando `len(iterable) == 0`.

```python
>>> is_empty([])
True
>>> is_empty([1])
False
```

### `is_not_empty(value) -> bool`

Restituisce `True` quando `len(value) != 0`.

```python
>>> is_not_empty([1])
True
>>> is_not_empty([])
False
```
