# API de Result

`Result[T, E]` representa sucesso (`Ok`) ou falha (`Err`). Ele fica em `pyfplib.result` e é reexportado pelo pacote `pyfplib`.

```python
from pyfplib import Err, Ok, Result
```

---

## Construtores

### `Ok(value)`

Cria um resultado de sucesso.

```python
>>> Ok(42).is_ok()
True
>>> Ok(42).unwrap()
42
```

### `Err(error)`

Cria um resultado de falha.

```python
>>> Err("boom").is_err()
True
>>> Err("boom").unwrap_err()
'boom'
```

---

## Inspeção

| Método | Retorna | Descrição |
|---|---|---|
| `is_ok()` | `bool` | `True` quando o resultado é `Ok`. |
| `is_err()` | `bool` | `True` quando o resultado é `Err`. |
| `value` | `T \| E` | O valor ou erro contido. |
| `__bool__()` | `bool` | Verdadeiro para `Ok`, falso para `Err`. |
| `inspect(fn)` | `Result[T, E]` | Chama `fn` com o valor `Ok`, retorna `self`. |
| `inspect_err(fn)` | `Result[T, E]` | Chama `fn` com o valor `Err`, retorna `self`. |
| `ok()` | `Option[T]` | `Some(value)` para `Ok`, caso contrário `Nothing()`. |
| `err()` | `Option[E]` | `Some(error)` para `Err`, caso contrário `Nothing()`. |

```python
>>> bool(Ok(1)), bool(Err("e"))
(True, False)
>>> Ok(1).ok()
Some(1)
>>> Err("e").ok()
Nothing()
```

---

## Extração

| Método | Retorna | Exceção | Descrição |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Retorna o valor `Ok` ou lança em `Err`. |
| `unwrap_err()` | `E` | `UnwrapError` | Retorna o valor `Err` ou lança em `Ok`. |
| `expect(message)` | `T` | `ExpectedError` | Retorna o valor `Ok` ou lança com `message`. |
| `expect_err(message)` | `E` | `ExpectedError` | Retorna o valor `Err` ou lança com `message`. |
| `unwrap_or(default)` | `T` | — | Retorna o valor `Ok` ou `default`. |
| `unwrap_or_else(fn)` | `T` | — | Retorna o valor `Ok` ou `fn(error)`. |
| `unwrap_err_or(default)` | `E` | — | Retorna o valor `Err` ou `default`. |

```python
>>> Ok(1).unwrap_or(0)
1
>>> Err("e").unwrap_or(0)
0
>>> Err("e").unwrap_or_else(lambda e: len(e))
1
```

---

## Transformação

### `map(fn) -> Result[U, E]`

Aplica `fn` ao valor `Ok`. `Err` é retornado inalterado.

```python
>>> Ok(2).map(lambda v: v * 3)
Ok(6)
>>> Err("e").map(lambda v: v * 3)
Err('e')
```

### `map_or(default, fn) -> Result[U, E]`

Aplica `fn` ao valor `Ok` ou usa `default`. O resultado é sempre `Ok`.

```python
>>> Ok(2).map_or(0, lambda v: v * 3)
Ok(6)
>>> Err("e").map_or(0, lambda v: v * 3)
Ok(0)
```

### `map_or_else(default, fn) -> U`

Aplica `fn` ao valor `Ok`, ou chama `default(error)` em `Err`.

```python
>>> Ok(2).map_or_else(lambda e: 0, lambda v: v * 3)
6
>>> Err("e").map_or_else(lambda e: len(e), lambda v: v * 3)
3
```

### `map_err(fn) -> Result[T, U]`

Aplica `fn` ao valor `Err`. `Ok` é retornado inalterado.

```python
>>> Err("boom").map_err(str.upper)
Err('BOOM')
>>> Ok(1).map_err(str.upper)
Ok(1)
```

### `flatten() -> Result[T, E]`

Achata um nível de aninhamento.

```python
>>> Ok(Ok(1)).flatten()
Ok(1)
>>> Ok(1).flatten()
Ok(1)
```

### `flatten_all() -> Result[T, E]`

Achata todos os níveis de aninhamento.

```python
>>> Ok(Ok(Ok(1))).flatten_all()
Ok(1)
```

---

## Combinação

### `and_then(fn) -> Result[T, E]`

Executa `fn` apenas quando o resultado é `Ok`; caso contrário retorna `Err` inalterado.

```python
>>> Ok(2).and_then(lambda v: Ok(v + 1))
Ok(3)
>>> Err("e").and_then(lambda v: Ok(v + 1))
Err('e')
```

### `or_else(fn) -> Result[T, E]`

Executa `fn` apenas quando o resultado é `Err`; caso contrário retorna o `Ok` original.

```python
>>> Err("e").or_else(lambda e: Ok(0))
Ok(0)
>>> Ok(1).or_else(lambda e: Ok(0))
Ok(1)
```

---

## Operadores

`Result` sobrecarrega `&` e `|` para refletir `and_then` e `or_else`.

| Expressão | Equivalente | Descrição |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Retorna `b` quando `a` é `Ok`, caso contrário `Err`. |
| `a & fn` | `a.and_then(lambda v: fn(v))` | Chama `fn(value)` quando `a` é `Ok`. |
| `a \| b` | `a.or_else(lambda _: b)` | Retorna `a` quando é `Ok`, caso contrário `b`. |
| `a \| fn` | `a.or_else(lambda e: fn(e))` | Chama `fn(error)` quando `a` é `Err`. |

```python
>>> Ok(1) & Ok(2)
Ok(2)
>>> Err("e") & Ok(2)
Err('e')
>>> Err("e") | Ok(2)
Ok(2)
```

---

## Tratamento de exceções

### `Result.try_call(fn, *args, **kwargs) -> Result[R, Exception]` *(estático)*

Chama `fn` e converte qualquer exceção lançada em `Err`.

```python
>>> Result.try_call(int, "42")
Ok(42)
>>> Result.try_call(int, "oops").is_err()
True
```

---

## Erros

- `UnwrapError` — lançada por `unwrap()` e `unwrap_err()` quando a variante errada está presente.
- `ExpectedError` — lançada por `expect()` e `expect_err()` com a mensagem fornecida.

```python
from pyfplib import Err
from pyfplib.errors import UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)
```
