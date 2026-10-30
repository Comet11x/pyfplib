# API de Result

`Result[T, E]` representa éxito (`Ok`) o fallo (`Err`). Se encuentra en `pyfplib.result` y se reexporta desde el paquete `pyfplib`.

```python
from pyfplib import Err, Ok, Result
```

---

## Constructores

### `Ok(value: T)`

Crea un resultado exitoso.

```python
from pyfplib import Ok, Result

result: Result[int, str] = Ok(42)
print(result.is_ok())  # True
print(result.unwrap()) # 42
```

### `Err(error: E)`

Crea un resultado fallido.

```python
from pyfplib import Err, Result

result: Result[int, str] = Err("boom")
print(result.is_err())           # True
print(repr(result.unwrap_err())) # 'boom'
```

---

## Inspección

| Método | Devuelve | Descripción |
|---|---|---|
| `is_ok()` | `bool` | `True` cuando el resultado es `Ok`. |
| `is_err()` | `bool` | `True` cuando el resultado es `Err`. |
| `value` | `T \| E` | El valor o error contenido. |
| `__bool__()` | `bool` | Verdadero para `Ok`, falso para `Err`. |
| `inspect(fn)` | `Result[T, E]` | Llama a `fn` con el valor `Ok`, devuelve `self`. |
| `inspect_err(fn)` | `Result[T, E]` | Llama a `fn` con el valor `Err`, devuelve `self`. |
| `ok()` | `Option[T]` | `Some(value)` para `Ok`, de lo contrario `Nothing()`. |
| `err()` | `Option[E]` | `Some(error)` para `Err`, de lo contrario `Nothing()`. |

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

## Extracción

| Método | Devuelve | Excepción | Descripción |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Devuelve el valor `Ok` o lanza en `Err`. |
| `unwrap_err()` | `E` | `UnwrapError` | Devuelve el valor `Err` o lanza en `Ok`. |
| `expect(message)` | `T` | `ExpectedError` | Devuelve el valor `Ok` o lanza con `message`. |
| `expect_err(message)` | `E` | `ExpectedError` | Devuelve el valor `Err` o lanza con `message`. |
| `unwrap_or(default)` | `T` | — | Devuelve el valor `Ok` o `default`. |
| `unwrap_or_else(fn)` | `T` | — | Devuelve el valor `Ok` o `fn(error)`. |
| `unwrap_err_or(default)` | `E` | — | Devuelve el valor `Err` o `default`. |

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

## Coincidencia de patrones

`Result` admite la coincidencia de patrones estructural de Python. Usa `Ok(value)` para vincular un valor exitoso y `Err(error)` para vincular el error, sin llamar primero a `is_ok()`.

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

## Transformación

### `map(fn: Callable[[T], U]) -> Result[U, E]`

Aplica `fn` al valor `Ok`. `Err` se devuelve sin cambios.

```python
from pyfplib import Err, Ok

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map(triple))    # Ok(6)
print(Err("e").map(triple)) # Err('e')
```

### `map_or(default: T, fn: Callable[[T], U]) -> Result[U, E]`

Aplica `fn` al valor `Ok` o a `default` cuando el resultado es `Err`. El resultado siempre es `Ok`. Usa `map_or_else` cuando necesites el valor simple.

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

Aplica `fn` al valor `Ok`, o llama a `default(error)` en `Err` y aplica `fn` a ese valor de respaldo, devolviendo el valor simple.

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

Aplica `fn` al valor `Err`. `Ok` se devuelve sin cambios.

```python
from pyfplib import Err, Ok

print(Err("boom").map_err(str.upper))  # Err('BOOM')
print(Ok(1).map_err(str.upper))        # Ok(1)
```

### `flatten() -> Result[T, E]`

Aplana un nivel de anidamiento. Un resultado no anidado se devuelve sin cambios.

```python
from pyfplib import Ok

print(Ok(Ok(1)).flatten())  # Ok(1)
print(Ok(1).flatten())      # Ok(1)
```

### `flatten_all() -> Result[T, E]`

Aplana todos los niveles de anidamiento hasta alcanzar el valor no-`Result` más interno.

```python
from pyfplib import Ok

print(Ok(Ok(Ok(1))).flatten_all())  # Ok(1)
```

---

## Combinación

### `and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]`

Ejecuta `fn` solo cuando el resultado es `Ok`; de lo contrario devuelve `Err` sin cambios.

```python
from pyfplib import Err, Ok, Result

def increment(value: int) -> Result[int, str]:
    return Ok(value + 1)

print(Ok(2).and_then(increment))    # Ok(3)
print(Err("e").and_then(increment)) # Err('e')
```

### `or_else(fn: Callable[[E], Result[T, E]]) -> Result[T, E]`

Ejecuta `fn` solo cuando el resultado es `Err`; de lo contrario devuelve el `Ok` original.

```python
from pyfplib import Err, Ok, Result

def recover(error: str) -> Result[int, str]:
    return Ok(0)

print(Err("e").or_else(recover))  # Ok(0)
print(Ok(1).or_else(recover))     # Ok(1)
```

---

## Operadores

`Result` sobrecarga `&` y `|` para reflejar `and_then` y `or_else`.

| Expresión | Equivalente | Descripción |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Devuelve `b` cuando `a` es `Ok`, de lo contrario `Err`. |
| `a & fn` | `a.and_then(lambda v: fn(v))` | Llama a `fn(value)` cuando `a` es `Ok`. |
| `a \| b` | `a.or_else(lambda _: b)` | Devuelve `a` cuando es `Ok`, de lo contrario `b`. |
| `a \| fn` | `a.or_else(lambda e: fn(e))` | Llama a `fn(error)` cuando `a` es `Err`. |

```python
from pyfplib import Err, Ok

print(Ok(1) & Ok(2))    # Ok(2)
print(Err("e") & Ok(2)) # Err('e')
print(Err("e") | Ok(2)) # Ok(2)
```

---

## Manejo de excepciones

### `Result.try_call(fn: Callable[..., R], *args, **kwargs) -> Result[R, Exception]` *(estático)*

Llama a `fn` con los argumentos proporcionados y convierte cualquier `Exception` lanzada en `Err`.

```python
from pyfplib import Result

print(Result.try_call(int, "42"))            # Ok(42)
print(Result.try_call(int, "oops").is_err()) # True
```

---

## Errores

- `UnwrapError` — la lanzan `unwrap()` y `unwrap_err()` cuando está presente la variante incorrecta.
- `ExpectedError` — la lanzan `expect()` y `expect_err()` con el mensaje proporcionado.

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
