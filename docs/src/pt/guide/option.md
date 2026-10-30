# API de Option

`Option[T]` representa um valor que pode estar presente (`Some`) ou ausente (`Nothing`). Ele fica em `pyfplib.option` e é reexportado pelo pacote `pyfplib`.

```python
from pyfplib import Nothing, Option, Some
```

---

## Construtores

### `Some(value)`

Envolve um valor em um `Option`. Um `Some` sempre é `is_some()`.

```python
>>> Some(42).is_some()
True
>>> Some(42).unwrap()
42
```

### `Nothing()`

Cria um `Option` vazio. Um `Nothing` sempre é `is_none()`.

```python
>>> Nothing().is_none()
True
>>> Nothing().unwrap_or(0)
0
```

---

## Inspeção

| Método | Retorna | Descrição |
|---|---|---|
| `is_some()` | `bool` | `True` quando um valor está presente. |
| `is_none()` | `bool` | `True` quando nenhum valor está presente. |
| `value` | `T \| None` | O valor bruto contido (pode ser `None`). |
| `__bool__()` | `bool` | Verdadeiro para `Some`, falso para `Nothing`. |
| `__eq__(other)` | `bool` | Compara os valores contidos quando ambos são `Option`. |
| `__hash__()` | `int` | Calcula o hash do valor contido. |

```python
>>> bool(Some(1)), bool(Nothing())
(True, False)
>>> Some(1) == Some(1)
True
```

### `inspect(fn) -> Option[T]`

Chama `fn` com o valor contido quando é `Some`, depois retorna a opção inalterada.

```python
>>> Some(2).inspect(lambda v: print(v))
2
Some(2)
```

### `inspect_none(fn) -> Option[T]`

Chama `fn` sem argumentos quando é `Nothing`, depois retorna a opção inalterada.

```python
>>> Nothing().inspect_none(lambda: print("empty"))
empty
Nothing()
```

---

## Extração

| Método | Retorna | Exceção | Descrição |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Retorna o valor ou lança se estiver vazio. |
| `expect(message)` | `T` | `ExpectedError` | Retorna o valor ou lança com `message`. |
| `unwrap_or(default)` | `T` | — | Retorna o valor ou `default`. |
| `unwrap_or_else(fn)` | `T` | — | Retorna o valor ou chama `fn()` para um fallback. |

```python
>>> Some(3).unwrap_or(0)
3
>>> Nothing().unwrap_or(0)
0
>>> Nothing().unwrap_or_else(lambda: 10)
10
```

---

## Transformação

### `map(fn) -> Option[U]`

Aplica `fn` ao valor contido, envolvendo o resultado em `Some`. `Nothing` permanece `Nothing`.

```python
>>> Some(3).map(lambda v: v * 2)
Some(6)
>>> Nothing().map(lambda v: v * 2)
Nothing()
```

### `map_or(default, fn) -> Option[U]`

Aplica `fn` quando é `Some`, caso contrário usa `default`. O resultado é sempre envolvido em `Some`.

```python
>>> Some(3).map_or(0, lambda v: v * 2)
Some(6)
>>> Nothing().map_or(0, lambda v: v * 2)
Some(0)
```

### `map_or_else(default, fn) -> U`

Aplica `fn` quando é `Some`, caso contrário chama `default()`.

```python
>>> Some(3).map_or_else(lambda: 0, lambda v: v * 2)
6
>>> Nothing().map_or_else(lambda: 0, lambda v: v * 2)
0
```

### `flatten() -> Option[T]`

Achata um nível de aninhamento.

```python
>>> Some(Some(1)).flatten()
Some(1)
>>> Some(1).flatten()
Some(1)
```

### `flatten_all() -> Option[T]`

Achata todos os níveis de aninhamento.

```python
>>> Some(Some(Some(1))).flatten_all()
Some(1)
```

---

## Conversão

### `ok_or(err) -> Result[T, E]`

Converte um `Option` em `Result`, usando `err` quando está vazio.

```python
>>> Some(1).ok_or("missing")
Ok(1)
>>> Nothing().ok_or("missing")
Err('missing')
```

### `ok_or_else(fn) -> Result[T, E]`

Como `ok_or`, mas chama `fn()` para produzir o erro quando está vazio.

```python
>>> Nothing().ok_or_else(lambda: "missing")
Err('missing')
```

### `from_optional(value) -> Option[T]` *(estático)*

Constrói um `Option` a partir de um valor que pode ser `None`.

```python
>>> Option.from_optional(None)
Nothing()
>>> Option.from_optional(5)
Some(5)
```

---

## Combinação

### `and_then(fn) -> Option[U]`

Executa `fn` apenas quando é `Some`; caso contrário retorna `Nothing`.

```python
>>> Some(2).and_then(lambda v: Some(v + 1))
Some(3)
>>> Nothing().and_then(lambda v: Some(v + 1))
Nothing()
```

### `or_else(fn) -> Option[T]`

Executa `fn` apenas quando é `Nothing`; caso contrário retorna a opção original.

```python
>>> Nothing().or_else(lambda: Some(9))
Some(9)
>>> Some(1).or_else(lambda: Some(9))
Some(1)
```

### `xor(other) -> Option[T]`

Retorna um valor apenas quando exatamente uma das duas opções é `Some`.

```python
>>> Some(1).xor(Nothing())
Some(1)
>>> Some(1).xor(Some(2))
Nothing()
```

### `zip(other) -> Option[tuple[T, U]]`

Emparelha os valores quando ambas as opções são `Some`.

```python
>>> Some(1).zip(Some("a"))
Some((1, 'a'))
```

### `zip_with(other, ctr) -> Option[R]`

Combina ambos os valores com `ctr` quando ambas as opções são `Some`.

```python
>>> Some(1).zip_with(Some(2), lambda a, b: a + b)
Some(3)
```

---

## Operadores

`Option` sobrecarrega `&` e `|` para refletir `and_then` e `or_else`.

| Expressão | Equivalente | Descrição |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Retorna `b` quando `a` é `Some`, caso contrário `Nothing`. |
| `a & fn` | `a.and_then(lambda _: fn())` | Chama `fn()` quando `a` é `Some`. |
| `a \| b` | `a.or_else(lambda: b)` | Retorna `a` quando é `Some`, caso contrário `b`. |
| `a \| fn` | `a.or_else(fn)` | Chama `fn()` quando `a` é `Nothing`. |

```python
>>> Some(1) & Some(2)
Some(2)
>>> Nothing() & Some(2)
Nothing()
>>> Nothing() | Some(2)
Some(2)
```

---

## Mutação

### `push(value) -> T`

Armazena `value` e retorna o valor anteriormente contido (ou `value` se a opção estava vazia).

```python
>>> opt = Some(1)
>>> opt.push(2)
1
>>> opt
Some(2)
```

---

## Erros

- `UnwrapError` — lançada por `unwrap()` quando a opção é `Nothing`.
- `ExpectedError` — lançada por `expect(message)` quando a opção é `Nothing`.

```python
from pyfplib import Nothing
from pyfplib.errors import ExpectedError, UnwrapError

try:
    Nothing().unwrap()
except UnwrapError as exc:
    print(exc)
```
