# API de Funciones

El módulo `pyfplib.functools` proporciona pequeños ayudantes componibles para secuencias. La mayoría también se reexportan desde el paquete `pyfplib`; `split_first` y `split_last` deben importarse desde `pyfplib.functools`.

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

Muchos ayudantes aceptan callbacks con uno, dos o tres parámetros. Los parámetros adicionales reciben el índice del elemento y la secuencia completa.

---

## Iteración

### `for_each(function, sequence) -> None`

Aplica `function` a cada elemento por sus efectos secundarios.

```python
>>> for_each(lambda v: print(v), [1, 2])
1
2
>>> for_each(lambda v, i: print(i, v), ["a", "b"])
0 a
1 b
```

---

## Predicados

### `any_of(predicate, sequence) -> bool`

Devuelve `True` cuando al menos un elemento satisface `predicate`. Devuelve `False` para una secuencia vacía.

```python
>>> any_of(lambda v: v > 2, [1, 2, 3])
True
>>> any_of(lambda v: v > 10, [1, 2, 3])
False
```

### `all_of(predicate, sequence) -> bool`

Devuelve `True` cuando todos los elementos satisfacen `predicate`. Devuelve `True` para una secuencia vacía.

```python
>>> all_of(lambda v: v > 0, [1, 2, 3])
True
>>> all_of(lambda v: v > 0, [1, -1])
False
```

### `none_of(predicate, sequence) -> bool`

Devuelve `True` cuando ningún elemento satisface `predicate`.

```python
>>> none_of(lambda v: v > 10, [1, 2, 3])
True
>>> none_of(lambda v: v > 2, [1, 2, 3])
False
```

---

## Plegado

### `fold(function, sequence, initial=None) -> Option[R]`

Reduce una secuencia a un único valor. El callback recibe el acumulador y el elemento actual, y opcionalmente el índice del elemento.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [1, 2, 3], 0)
Some(6)
>>> fold(lambda acc, v, i: acc.unwrap_or(0) + v + i, [1, 2, 3])
Some(9)
```

Sin un valor inicial, el acumulador comienza como `Nothing`; plegar una secuencia vacía devuelve `Nothing()`.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [])
Nothing()
```

---

## Acceso a elementos

### `head(iterable) -> Option[T]`

Devuelve el primer elemento, o `Nothing` cuando el iterable está vacío. Acepta cualquier iterable.

```python
>>> head([10, 20])
Some(10)
>>> head([])
Nothing()
```

### `first(iterable) -> Option[T]`

Ayudante que devuelve el primer elemento de cualquier iterable.

```python
>>> first("abc")
Some('a')
```

### `last(sequence) -> Option[T]`

Devuelve el último elemento, o `Nothing` cuando la secuencia está vacía.

```python
>>> last([10, 20])
Some(20)
>>> last([])
Nothing()
```

### `tail(sequence) -> Sequence[T]`

Devuelve la secuencia sin su primer elemento. Las secuencias vacías se devuelven sin cambios.

```python
>>> tail([1, 2, 3])
[2, 3]
>>> tail([])
[]
```

### `split_first(sequence) -> tuple[Option[T], Sequence[T]]`

Divide una secuencia en su primer elemento y la cola restante.

```python
>>> split_first([1, 2, 3])
(Some(1), [2, 3])
>>> split_first([])
(Nothing(), [])
```

### `split_last(sequence) -> tuple[Sequence[T], Option[T]]`

Divide una secuencia en su parte inicial y su último elemento.

```python
>>> split_last([1, 2, 3])
([1, 2], Some(3))
>>> split_last([])
([], Nothing())
```

---

## Búsqueda

### `index(predicate, sequence) -> Option[int]`

Devuelve el índice del primer elemento coincidente. `predicate` puede ser un callable o un valor con el que comparar.

```python
>>> index(3, [1, 2, 3, 4])
Some(2)
>>> index(lambda v: v > 2, [1, 2, 3, 4])
Some(2)
>>> index(10, [1, 2, 3])
Nothing()
```

### `find(callback, sequence) -> Option[T]`

Devuelve el primer elemento para el que `callback` devuelve un `Option` no vacío o cualquier valor verdadero.

```python
>>> find(lambda v: Some(v) if v % 2 == 0 else Nothing(), [1, 2, 3])
Some(2)
>>> find(lambda v: v > 2, [1, 2, 3])
Some(3)
>>> find(lambda v: v > 10, [1, 2, 3])
Nothing()
```

---

## Comprobaciones de tamaño

### `is_empty(iterable) -> bool`

Devuelve `True` cuando `len(iterable) == 0`.

```python
>>> is_empty([])
True
>>> is_empty([1])
False
```

### `is_not_empty(value) -> bool`

Devuelve `True` cuando `len(value) != 0`.

```python
>>> is_not_empty([1])
True
>>> is_not_empty([])
False
```
