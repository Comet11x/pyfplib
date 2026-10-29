# API de Result

`Result[T, E]` representa éxito (`Ok`) o fallo (`Err`). Se encuentra en `pyfplib.result` y se reexporta desde el paquete `pyfplib`.

```python
from pyfplib import Err, Ok, Result
```

---

## Constructores

### `Ok(value)`

Crea un resultado exitoso.

```python
>>> Ok(42).is_ok()
True
>>> Ok(42).unwrap()
42
```

### `Err(error)`

Crea un resultado fallido.

```python
>>> Err("boom").is_err()
True
>>> Err("boom").unwrap_err()
'boom'
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
>>> bool(Ok(1)), bool(Err("e"))
(True, False)
>>> Ok(1).ok()
Some(1)
>>> Err("e").ok()
Nothing()
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
>>> Ok(1).unwrap_or(0)
1
>>> Err("e").unwrap_or(0)
0
>>> Err("e").unwrap_or_else(lambda e: len(e))
1
```

---

## Transformación

### `map(fn) -> Result[U, E]`

Aplica `fn` al valor `Ok`. `Err` se devuelve sin cambios.

```python
>>> Ok(2).map(lambda v: v * 3)
Ok(6)
>>> Err("e").map(lambda v: v * 3)
Err('e')
```

### `map_or(default, fn) -> Result[U, E]`

Aplica `fn` al valor `Ok` o usa `default`. El resultado siempre es `Ok`.

```python
>>> Ok(2).map_or(0, lambda v: v * 3)
Ok(6)
>>> Err("e").map_or(0, lambda v: v * 3)
Ok(0)
```

### `map_or_else(default, fn) -> U`

Aplica `fn` al valor `Ok`, o llama a `default(error)` en `Err`.

```python
>>> Ok(2).map_or_else(lambda e: 0, lambda v: v * 3)
6
>>> Err("e").map_or_else(lambda e: len(e), lambda v: v * 3)
3
```

### `map_err(fn) -> Result[T, U]`

Aplica `fn` al valor `Err`. `Ok` se devuelve sin cambios.

```python
>>> Err("boom").map_err(str.upper)
Err('BOOM')
>>> Ok(1).map_err(str.upper)
Ok(1)
```

### `flatten() -> Result[T, E]`

Aplana un nivel de anidamiento.

```python
>>> Ok(Ok(1)).flatten()
Ok(1)
>>> Ok(1).flatten()
Ok(1)
```

### `flatten_all() -> Result[T, E]`

Aplana todos los niveles de anidamiento.

```python
>>> Ok(Ok(Ok(1))).flatten_all()
Ok(1)
```

---

## Combinación

### `and_then(fn) -> Result[T, E]`

Ejecuta `fn` solo cuando el resultado es `Ok`; de lo contrario devuelve `Err` sin cambios.

```python
>>> Ok(2).and_then(lambda v: Ok(v + 1))
Ok(3)
>>> Err("e").and_then(lambda v: Ok(v + 1))
Err('e')
```

### `or_else(fn) -> Result[T, E]`

Ejecuta `fn` solo cuando el resultado es `Err`; de lo contrario devuelve el `Ok` original.

```python
>>> Err("e").or_else(lambda e: Ok(0))
Ok(0)
>>> Ok(1).or_else(lambda e: Ok(0))
Ok(1)
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
>>> Ok(1) & Ok(2)
Ok(2)
>>> Err("e") & Ok(2)
Err('e')
>>> Err("e") | Ok(2)
Ok(2)
```

---

## Manejo de excepciones

### `Result.try_call(fn, *args, **kwargs) -> Result[R, Exception]` *(estático)*

Llama a `fn` y convierte cualquier excepción lanzada en `Err`.

```python
>>> Result.try_call(int, "42")
Ok(42)
>>> Result.try_call(int, "oops").is_err()
True
```

---

## Errores

- `UnwrapError` — la lanzan `unwrap()` y `unwrap_err()` cuando está presente la variante incorrecta.
- `ExpectedError` — la lanzan `expect()` y `expect_err()` con el mensaje proporcionado.

```python
from pyfplib import Err
from pyfplib.errors import UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)
```
