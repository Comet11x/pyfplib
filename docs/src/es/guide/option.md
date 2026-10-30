# API de Option

`Option[T]` representa un valor que puede estar presente (`Some`) o ausente (`Nothing`). Se encuentra en `pyfplib.option` y se reexporta desde el paquete `pyfplib`.

```python
from pyfplib import Nothing, Option, Some
```

---

## Constructores

### `Some(value: T)`

Envuelve un valor distinto de `None` en un `Option`. Como `Option` usa `None` internamente para representar la ausencia, `Some(None)` se comporta como `Nothing()`.

```python
from pyfplib import Some

print(Some(42).is_some())    # True
print(Some(42).unwrap())     # 42
print(Some(None).is_none())  # True
```

### `Nothing()`

Crea un `Option` vacío. Un `Nothing` siempre es `is_none()`.

```python
from pyfplib import Nothing

print(Nothing().is_none())     # True
print(Nothing().unwrap_or(0))  # 0
```

---

## Inspección

| Método | Devuelve | Descripción |
|---|---|---|
| `is_some()` | `bool` | `True` cuando hay un valor presente. |
| `is_none()` | `bool` | `True` cuando no hay ningún valor. |
| `value` | `T \| None` | El valor bruto contenido (puede ser `None`). |
| `__bool__()` | `bool` | Verdadero para `Some`, falso para `Nothing`. |
| `__eq__(other)` | `bool` | Compara los valores contenidos cuando ambos son `Option`. |
| `__hash__()` | `int` | Calcula el hash del valor contenido. |

```python
from pyfplib import Nothing, Some

print(bool(Some(1)), bool(Nothing()))  # (True, False)
print(Some(1) == Some(1))              # True
```

### `inspect(fn: Callable[[T], None]) -> Option[T]`

Llama a `fn` con el valor contenido cuando es `Some`, luego devuelve la opción sin cambios.

```python
from pyfplib import Option, Some

option: Option[int] = Some(2)
returned = option.inspect(lambda value: print(f"inspected: {value}"))
print(returned)  # Some(2)
```

### `inspect_none(fn: Callable[[], None]) -> Option[T]`

Llama a `fn` sin argumentos cuando es `Nothing`, luego devuelve la opción sin cambios.

```python
from pyfplib import Nothing

returned = Nothing().inspect_none(lambda: print("empty"))
print(returned)  # Nothing()
```

---

## Extracción

| Método | Devuelve | Excepción | Descripción |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Devuelve el valor o lanza si está vacío. |
| `expect(message)` | `T` | `ExpectedError` | Devuelve el valor o lanza con `message`. |
| `unwrap_or(default)` | `T` | — | Devuelve el valor o `default`. |
| `unwrap_or_else(fn)` | `T` | — | Devuelve el valor o llama a `fn()` para un respaldo. |

```python
from pyfplib import Nothing, Some

def fallback() -> int:
    return 10

print(Some(3).unwrap_or(0))               # 3
print(Nothing().unwrap_or(0))             # 0
print(Some(3).unwrap_or_else(fallback))   # 3
print(Nothing().unwrap_or_else(fallback)) # 10
```

---

## Coincidencia de patrones

`Option` admite la coincidencia de patrones estructural de Python. Usa `Some(value)` para vincular el valor contenido y `Nothing()` para coincidir con un option vacío, sin llamar primero a `is_some()`.

```python
from pyfplib import Nothing, Option, Some

def describe(option: Option[int]) -> str:
    match option:
        case Some(value):
            return f"got {value}"
        case Nothing():
            return "nothing"

print(describe(Some(42)))   # got 42
print(describe(Nothing()))  # nothing
```

---

## Transformación

### `map(fn: Callable[[T], U]) -> Option[U]`

Aplica `fn` al valor contenido y envuelve el resultado en `Some`. `Nothing` permanece `Nothing`.

```python
from pyfplib import Nothing, Some

def double(value: int) -> int:
    return value * 2

print(Some(3).map(double))    # Some(6)
print(Nothing().map(double))  # Nothing()
```

### `map_or(default: U, fn: Callable[[T], U]) -> Option[U]`

Aplica `fn` a un valor `Some` o usa `default`, y siempre devuelve un `Option` (`Some`). Usa `map_or_else` cuando necesites el valor simple.

```python
from pyfplib import Nothing, Option, Some

def double(value: int) -> int:
    return value * 2

present: Option[int] = Some(3)
empty: Option[int] = Nothing()

print(present.map_or(0, double))  # Some(6)
print(empty.map_or(0, double))    # Some(0)
```

### `map_or_else(default: Callable[[], U], fn: Callable[[T], U]) -> U`

Aplica `fn` cuando es `Some`, de lo contrario llama a `default()`.

```python
from pyfplib import Nothing, Some

def default() -> int:
    return 0

def double(value: int) -> int:
    return value * 2

print(Some(3).map_or_else(default, double))   # 6
print(Nothing().map_or_else(default, double)) # 0
```

### `flatten() -> Option[T]`

Reduce un nivel de anidamiento. Una opción sin anidar se devuelve sin cambios.

```python
from pyfplib import Some

print(Some(Some(1)).flatten())  # Some(1)
print(Some(1).flatten())        # Some(1)
```

### `flatten_all() -> Option[T]`

Reduce todos los niveles de anidamiento hasta alcanzar el valor no-option más interno.

```python
from pyfplib import Some

print(Some(Some(Some(1))).flatten_all())  # Some(1)
```

---

## Conversión

### `ok_or(err: E) -> Result[T, E]`

Convierte un `Option` en un `Result`, usando `err` cuando está vacío.

```python
from pyfplib import Nothing, Some

print(Some(1).ok_or("missing"))   # Ok(1)
print(Nothing().ok_or("missing")) # Err('missing')
```

### `ok_or_else(fn: Callable[[], E]) -> Result[T, E]`

Como `ok_or`, pero llama a `fn()` para producir el error cuando está vacío.

```python
from pyfplib import Nothing

def missing_error() -> str:
    return "missing"

print(Nothing().ok_or_else(missing_error))  # Err('missing')
```

### `from_optional(value: T | None) -> Option[T]` *(estático)*

Crea un `Option` a partir de un valor que puede ser `None`: `None` se convierte en `Nothing`, y cualquier otro valor se convierte en `Some`.

```python
from pyfplib import Option

value: int | None = None
print(Option.from_optional(value))  # Nothing()
print(Option.from_optional(5))      # Some(5)
```

---

## Combinación

### `and_then(fn: Callable[[T], Option[U]]) -> Option[U]`

Ejecuta `fn` solo cuando es `Some`; de lo contrario devuelve `Nothing`.

```python
from pyfplib import Nothing, Option, Some

def increment(value: int) -> Option[int]:
    return Some(value + 1)

print(Some(2).and_then(increment))   # Some(3)
print(Nothing().and_then(increment)) # Nothing()
```

### `or_else(fn: Callable[[], Option[T]]) -> Option[T]`

Ejecuta `fn` solo cuando es `Nothing`; de lo contrario devuelve la opción original.

```python
from pyfplib import Nothing, Option, Some

def recover() -> Option[int]:
    return Some(9)

print(Nothing().or_else(recover))  # Some(9)
print(Some(1).or_else(recover))    # Some(1)
```

### `xor(other: Option[T]) -> Option[T]`

Devuelve un valor solo cuando exactamente una de las dos opciones es `Some`.

```python
from pyfplib import Nothing, Some

print(Some(1).xor(Nothing()))  # Some(1)
print(Some(1).xor(Some(2)))    # Nothing()
```

### `zip(other: Option[U]) -> Option[tuple[T, U]]`

Empareja los valores cuando ambas opciones son `Some`.

```python
from pyfplib import Some

print(Some(1).zip(Some("a")))  # Some((1, 'a'))
```

### `zip_with(other: Option[U], ctr: Callable[[T, U], R]) -> Option[R]`

Combina ambos valores con `ctr` cuando ambas opciones son `Some`.

```python
from pyfplib import Some

def add(left: int, right: int) -> int:
    return left + right

print(Some(1).zip_with(Some(2), add))  # Some(3)
```

---

## Operadores

`Option` sobrecarga `&` y `|` para reflejar `and_then` y `or_else`.

| Expresión | Equivalente | Descripción |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Devuelve `b` cuando `a` es `Some`, de lo contrario `Nothing`. |
| `a & fn` | `a.and_then(lambda _: fn())` | Llama a `fn()` cuando `a` es `Some`. |
| `a \| b` | `a.or_else(lambda: b)` | Devuelve `a` cuando es `Some`, de lo contrario `b`. |
| `a \| fn` | `a.or_else(fn)` | Llama a `fn()` cuando `a` es `Nothing`. |

```python
from pyfplib import Nothing, Some

print(Some(1) & Some(2))    # Some(2)
print(Nothing() & Some(2))  # Nothing()
print(Nothing() | Some(2))  # Some(2)
```

---

## Mutación

### `push(value: T) -> T`

Modifica la opción en el lugar: almacena `value` y devuelve el valor que contenía antes, o `value` si la opción estaba vacía.

```python
from pyfplib import Option, Some

option: Option[int] = Some(1)
previous = option.push(2)

print(previous)  # 1
print(option)    # Some(2)
```

---

## Errores

- `UnwrapError` — la lanza `unwrap()` cuando la opción es `Nothing`.
- `ExpectedError` — la lanza `expect(message)` cuando la opción es `Nothing`.

```python
from pyfplib import Nothing
from pyfplib.errors import ExpectedError, UnwrapError

try:
    Nothing().unwrap()
except UnwrapError as exc:
    print(exc)  # called `Option.unwrap()` on a `Nothing` value

try:
    Nothing().expect("value is required")
except ExpectedError as exc:
    print(exc)  # value is required
```
