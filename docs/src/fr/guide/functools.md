# API Fonctions

Le module `pyfplib.functools` fournit de petits helpers composables pour les séquences. La plupart sont également réexportés depuis le paquet `pyfplib` ; `split_first` et `split_last` doivent être importés depuis `pyfplib.functools`.

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

De nombreux helpers acceptent des callbacks avec un, deux ou trois paramètres. Les paramètres supplémentaires reçoivent l'index de l'élément et la séquence complète.

---

## Itération

### `for_each(function, sequence) -> None`

Applique `function` à chaque élément pour ses effets de bord.

```python
>>> for_each(lambda v: print(v), [1, 2])
1
2
>>> for_each(lambda v, i: print(i, v), ["a", "b"])
0 a
1 b
```

---

## Prédicats

### `any_of(predicate, sequence) -> bool`

Renvoie `True` lorsqu'au moins un élément satisfait `predicate`. Renvoie `False` pour une séquence vide.

```python
>>> any_of(lambda v: v > 2, [1, 2, 3])
True
>>> any_of(lambda v: v > 10, [1, 2, 3])
False
```

### `all_of(predicate, sequence) -> bool`

Renvoie `True` lorsque chaque élément satisfait `predicate`. Renvoie `True` pour une séquence vide.

```python
>>> all_of(lambda v: v > 0, [1, 2, 3])
True
>>> all_of(lambda v: v > 0, [1, -1])
False
```

### `none_of(predicate, sequence) -> bool`

Renvoie `True` lorsqu'aucun élément ne satisfait `predicate`.

```python
>>> none_of(lambda v: v > 10, [1, 2, 3])
True
>>> none_of(lambda v: v > 2, [1, 2, 3])
False
```

---

## Réduction

### `fold(function, sequence, initial=None) -> Option[R]`

Réduit une séquence à une valeur unique. Le callback reçoit l'accumulateur et l'élément courant, et éventuellement l'index de l'élément.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [1, 2, 3], 0)
Some(6)
>>> fold(lambda acc, v, i: acc.unwrap_or(0) + v + i, [1, 2, 3])
Some(9)
```

Sans valeur initiale, l'accumulateur commence à `Nothing` ; réduire une séquence vide renvoie `Nothing()`.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [])
Nothing()
```

---

## Accès aux éléments

### `head(iterable) -> Option[T]`

Renvoie le premier élément, ou `Nothing` lorsque l'itérable est vide. Accepte tout itérable.

```python
>>> head([10, 20])
Some(10)
>>> head([])
Nothing()
```

### `first(iterable) -> Option[T]`

Helper qui renvoie le premier élément de tout itérable.

```python
>>> first("abc")
Some('a')
```

### `last(sequence) -> Option[T]`

Renvoie le dernier élément, ou `Nothing` lorsque la séquence est vide.

```python
>>> last([10, 20])
Some(20)
>>> last([])
Nothing()
```

### `tail(sequence) -> Sequence[T]`

Renvoie la séquence sans son premier élément. Les séquences vides sont renvoyées inchangées.

```python
>>> tail([1, 2, 3])
[2, 3]
>>> tail([])
[]
```

### `split_first(sequence) -> tuple[Option[T], Sequence[T]]`

Sépare une séquence en son premier élément et la queue restante.

```python
>>> split_first([1, 2, 3])
(Some(1), [2, 3])
>>> split_first([])
(Nothing(), [])
```

### `split_last(sequence) -> tuple[Sequence[T], Option[T]]`

Sépare une séquence en sa partie initiale et son dernier élément.

```python
>>> split_last([1, 2, 3])
([1, 2], Some(3))
>>> split_last([])
([], Nothing())
```

---

## Recherche

### `index(predicate, sequence) -> Option[int]`

Renvoie l'index du premier élément correspondant. `predicate` peut être un callable ou une valeur à comparer.

```python
>>> index(3, [1, 2, 3, 4])
Some(2)
>>> index(lambda v: v > 2, [1, 2, 3, 4])
Some(2)
>>> index(10, [1, 2, 3])
Nothing()
```

### `find(callback, sequence) -> Option[T]`

Renvoie le premier élément pour lequel `callback` renvoie un `Option` non vide ou une valeur vraie.

```python
>>> find(lambda v: Some(v) if v % 2 == 0 else Nothing(), [1, 2, 3])
Some(2)
>>> find(lambda v: v > 2, [1, 2, 3])
Some(3)
>>> find(lambda v: v > 10, [1, 2, 3])
Nothing()
```

---

## Vérifications de taille

### `is_empty(iterable) -> bool`

Renvoie `True` lorsque `len(iterable) == 0`.

```python
>>> is_empty([])
True
>>> is_empty([1])
False
```

### `is_not_empty(value) -> bool`

Renvoie `True` lorsque `len(value) != 0`.

```python
>>> is_not_empty([1])
True
>>> is_not_empty([])
False
```
