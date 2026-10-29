# API de Funções

O módulo `pyfplib.functools` fornece pequenos auxiliares combináveis para sequências. A maioria também é reexportada pelo pacote `pyfplib`; `split_first` e `split_last` devem ser importados de `pyfplib.functools`.

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

Muitos auxiliares aceitam callbacks com um, dois ou três parâmetros. Os parâmetros extras recebem o índice do elemento e a sequência completa.

---

## Iteração

### `for_each(function, sequence) -> None`

Aplica `function` a cada elemento por seus efeitos colaterais.

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

Retorna `True` quando pelo menos um elemento satisfaz `predicate`. Retorna `False` para uma sequência vazia.

```python
>>> any_of(lambda v: v > 2, [1, 2, 3])
True
>>> any_of(lambda v: v > 10, [1, 2, 3])
False
```

### `all_of(predicate, sequence) -> bool`

Retorna `True` quando todos os elementos satisfazem `predicate`. Retorna `True` para uma sequência vazia.

```python
>>> all_of(lambda v: v > 0, [1, 2, 3])
True
>>> all_of(lambda v: v > 0, [1, -1])
False
```

### `none_of(predicate, sequence) -> bool`

Retorna `True` quando nenhum elemento satisfaz `predicate`.

```python
>>> none_of(lambda v: v > 10, [1, 2, 3])
True
>>> none_of(lambda v: v > 2, [1, 2, 3])
False
```

---

## Dobra

### `fold(function, sequence, initial=None) -> Option[R]`

Reduz uma sequência a um único valor. O callback recebe o acumulador e o elemento atual e, opcionalmente, o índice do elemento.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [1, 2, 3], 0)
Some(6)
>>> fold(lambda acc, v, i: acc.unwrap_or(0) + v + i, [1, 2, 3])
Some(9)
```

Sem um valor inicial, o acumulador começa como `Nothing`; dobrar uma sequência vazia retorna `Nothing()`.

```python
>>> fold(lambda acc, v: acc.unwrap_or(0) + v, [])
Nothing()
```

---

## Acesso a elementos

### `head(iterable) -> Option[T]`

Retorna o primeiro elemento, ou `Nothing` quando o iterável está vazio. Aceita qualquer iterável.

```python
>>> head([10, 20])
Some(10)
>>> head([])
Nothing()
```

### `first(iterable) -> Option[T]`

Auxiliar que retorna o primeiro elemento de qualquer iterável.

```python
>>> first("abc")
Some('a')
```

### `last(sequence) -> Option[T]`

Retorna o último elemento, ou `Nothing` quando a sequência está vazia.

```python
>>> last([10, 20])
Some(20)
>>> last([])
Nothing()
```

### `tail(sequence) -> Sequence[T]`

Retorna a sequência sem seu primeiro elemento. Sequências vazias são retornadas inalteradas.

```python
>>> tail([1, 2, 3])
[2, 3]
>>> tail([])
[]
```

### `split_first(sequence) -> tuple[Option[T], Sequence[T]]`

Divide uma sequência em seu primeiro elemento e a cauda restante.

```python
>>> split_first([1, 2, 3])
(Some(1), [2, 3])
>>> split_first([])
(Nothing(), [])
```

### `split_last(sequence) -> tuple[Sequence[T], Option[T]]`

Divide uma sequência em sua parte inicial e seu último elemento.

```python
>>> split_last([1, 2, 3])
([1, 2], Some(3))
>>> split_last([])
([], Nothing())
```

---

## Busca

### `index(predicate, sequence) -> Option[int]`

Retorna o índice do primeiro elemento correspondente. `predicate` pode ser um callable ou um valor para comparação.

```python
>>> index(3, [1, 2, 3, 4])
Some(2)
>>> index(lambda v: v > 2, [1, 2, 3, 4])
Some(2)
>>> index(10, [1, 2, 3])
Nothing()
```

### `find(callback, sequence) -> Option[T]`

Retorna o primeiro elemento para o qual `callback` retorna um `Option` não vazio ou qualquer valor verdadeiro.

```python
>>> find(lambda v: Some(v) if v % 2 == 0 else Nothing(), [1, 2, 3])
Some(2)
>>> find(lambda v: v > 2, [1, 2, 3])
Some(3)
>>> find(lambda v: v > 10, [1, 2, 3])
Nothing()
```

---

## Verificações de tamanho

### `is_empty(iterable) -> bool`

Retorna `True` quando `len(iterable) == 0`.

```python
>>> is_empty([])
True
>>> is_empty([1])
False
```

### `is_not_empty(value) -> bool`

Retorna `True` quando `len(value) != 0`.

```python
>>> is_not_empty([1])
True
>>> is_not_empty([])
False
```
