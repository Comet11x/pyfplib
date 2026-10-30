# API de Result

`Result[T, E]` representa sucesso (`Ok`) ou falha (`Err`). Ele fica em `pyfplib.result` e é reexportado pelo pacote `pyfplib`.

```python
from pyfplib import Err, Ok, Result
```

---

## Construtores

### `Ok(value: T)`

Cria um resultado de sucesso.

```python
from pyfplib import Ok, Result

result: Result[int, str] = Ok(42)
print(result.is_ok())  # True
print(result.unwrap()) # 42
```

### `Err(error: E)`

Cria um resultado de falha.

```python
from pyfplib import Err, Result

result: Result[int, str] = Err("boom")
print(result.is_err())           # True
print(repr(result.unwrap_err())) # 'boom'
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
from pyfplib import Err, Ok, Result

ok_result: Result[int, str] = Ok(1)
err_result: Result[int, str] = Err("e")

print(bool(ok_result), bool(err_result))  # (True, False)
print(ok_result.ok())                     # Some(1)
print(err_result.ok())                    # Nothing()
print(err_result.err())                   # Some('e')
print(ok_result.err())                    # Nothing()

returned = ok_result.inspect(lambda value: print(f"ok: {value}"))
print(returned)  # Ok(1)

returned_err = err_result.inspect_err(lambda error: print(f"err: {error}"))
print(returned_err)  # Err('e')
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
from pyfplib import Err, Ok

def error_length(error: str) -> int:
    return len(error)

print(Ok(1).unwrap_or(0))                        # 1
print(Err("e").unwrap_or(0))                     # 0
print(Err("e").unwrap_or_else(error_length))     # 1
print(repr(Err("e").unwrap_err_or("fallback")))  # 'e'
print(repr(Ok(1).unwrap_err_or("fallback")))     # 'fallback'
```

---

## Correspondência de padrões

`Result` oferece suporte à correspondência de padrões estruturais do Python. Use `Ok(value)` para vincular um valor de sucesso e `Err(error)` para vincular o erro, sem chamar `is_ok()` antes.

```python
from pyfplib import Err, Ok, Result

def describe(result: Result[int, str]) -> str:
    match result:
        case Ok(value):
            return f"ok: {value}"
        case Err(error):
            return f"error: {error}"

print(describe(Ok(42)))      # ok: 42
print(describe(Err("boom"))) # error: boom
```

---

## Transformação

### `map(fn: Callable[[T], U]) -> Result[U, E]`

Aplica `fn` ao valor `Ok`. `Err` é retornado inalterado.

```python
from pyfplib import Err, Ok

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map(triple))    # Ok(6)
print(Err("e").map(triple)) # Err('e')
```

### `map_or(default: T, fn: Callable[[T], U]) -> Result[U, E]`

Aplica `fn` ao valor `Ok` ou a `default` quando o resultado é `Err`. O resultado é sempre `Ok`. Use `map_or_else` quando precisar do valor simples.

```python
from pyfplib import Err, Ok, Result

def triple(value: int) -> int:
    return value * 3

ok_result: Result[int, str] = Ok(2)
err_result: Result[int, str] = Err("e")

print(ok_result.map_or(1, triple))  # Ok(6)
print(err_result.map_or(1, triple)) # Ok(3)
```

### `map_or_else(default: Callable[[E], T], fn: Callable[[T], U]) -> U`

Aplica `fn` ao valor `Ok`, ou chama `default(error)` em `Err` e aplica `fn` a esse valor de fallback, retornando o valor simples.

```python
from pyfplib import Err, Ok

def error_length(error: str) -> int:
    return len(error)

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map_or_else(error_length, triple))    # 6
print(Err("e").map_or_else(error_length, triple)) # 3
```

### `map_err(fn: Callable[[E], U]) -> Result[T, U]`

Aplica `fn` ao valor `Err`. `Ok` é retornado inalterado.

```python
from pyfplib import Err, Ok

print(Err("boom").map_err(str.upper))  # Err('BOOM')
print(Ok(1).map_err(str.upper))        # Ok(1)
```

### `flatten() -> Result[T, E]`

Achata um nível de aninhamento. Um resultado não aninhado é retornado sem alterações.

```python
from pyfplib import Ok

print(Ok(Ok(1)).flatten())  # Ok(1)
print(Ok(1).flatten())      # Ok(1)
```

### `flatten_all() -> Result[T, E]`

Achata todos os níveis de aninhamento até alcançar o valor não-`Result` mais interno.

```python
from pyfplib import Ok

print(Ok(Ok(Ok(1))).flatten_all())  # Ok(1)
```

---

## Combinação

### `and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]`

Executa `fn` apenas quando o resultado é `Ok`; caso contrário retorna `Err` inalterado.

```python
from pyfplib import Err, Ok, Result

def increment(value: int) -> Result[int, str]:
    return Ok(value + 1)

print(Ok(2).and_then(increment))    # Ok(3)
print(Err("e").and_then(increment)) # Err('e')
```

### `or_else(fn: Callable[[E], Result[T, E]]) -> Result[T, E]`

Executa `fn` apenas quando o resultado é `Err`; caso contrário retorna o `Ok` original.

```python
from pyfplib import Err, Ok, Result

def recover(error: str) -> Result[int, str]:
    return Ok(0)

print(Err("e").or_else(recover))  # Ok(0)
print(Ok(1).or_else(recover))     # Ok(1)
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
from pyfplib import Err, Ok

print(Ok(1) & Ok(2))    # Ok(2)
print(Err("e") & Ok(2)) # Err('e')
print(Err("e") | Ok(2)) # Ok(2)
```

---

## Tratamento de exceções

### `Result.try_call(fn: Callable[..., R], *args, **kwargs) -> Result[R, Exception]` *(estático)*

Chama `fn` com os argumentos fornecidos e converte qualquer `Exception` levantada em `Err`.

```python
from pyfplib import Result

print(Result.try_call(int, "42"))            # Ok(42)
print(Result.try_call(int, "oops").is_err()) # True
```

---

## Erros

- `UnwrapError` — lançada por `unwrap()` e `unwrap_err()` quando a variante errada está presente.
- `ExpectedError` — lançada por `expect()` e `expect_err()` com a mensagem fornecida.

```python
from pyfplib import Err, Ok
from pyfplib.errors import ExpectedError, UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)  # called `Result.unwrap()` on a `Err` value

try:
    Ok(1).unwrap_err()
except UnwrapError as exc:
    print(exc)  # called `Result.unwrap_err()` on a `Ok` value

try:
    Err("boom").expect("success required")
except ExpectedError as exc:
    print(exc)  # success required

try:
    Ok(1).expect_err("failure required")
except ExpectedError as exc:
    print(exc)  # failure required
```
