# API de Option

`Option[T]` representa un valor que puede estar presente (`Some`) o ausente (`Nothing`). Se encuentra en `pyfplib.option` y se reexporta desde el paquete `pyfplib`.

```python
from pyfplib import Nothing, Option, Some
```

---

## Constructores

### `Some(value)`

Envuelve un valor en un `Option`. Un `Some` siempre es `is_some()`.

```python
>>> Some(42).is_some()
True
>>> Some(42).unwrap()
42
```

### `Nothing()`

Crea un `Option` vacío. Un `Nothing` siempre es `is_none()`.

```python
>>> Nothing().is_none()
True
>>> Nothing().unwrap_or(0)
0
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
>>> bool(Some(1)), bool(Nothing())
(True, False)
>>> Some(1) == Some(1)
True
```

### `inspect(fn) -> Option[T]`

Llama a `fn` con el valor contenido cuando es `Some`, luego devuelve la opción sin cambios.

```python
>>> Some(2).inspect(lambda v: print(v))
2
Some(2)
```

### `inspect_none(fn) -> Option[T]`

Llama a `fn` sin argumentos cuando es `Nothing`, luego devuelve la opción sin cambios.

```python
>>> Nothing().inspect_none(lambda: print("empty"))
empty
Nothing()
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
>>> Some(3).unwrap_or(0)
3
>>> Nothing().unwrap_or(0)
0
>>> Nothing().unwrap_or_else(lambda: 10)
10
```

---

## Transformación

### `map(fn) -> Option[U]`

Aplica `fn` al valor contenido y envuelve el resultado en `Some`. `Nothing` permanece `Nothing`.

```python
>>> Some(3).map(lambda v: v * 2)
Some(6)
>>> Nothing().map(lambda v: v * 2)
Nothing()
```

### `map_or(default, fn) -> Option[U]`

Aplica `fn` cuando es `Some`, de lo contrario usa `default`. El resultado siempre se envuelve en `Some`.

```python
>>> Some(3).map_or(0, lambda v: v * 2)
Some(6)
>>> Nothing().map_or(0, lambda v: v * 2)
Some(0)
```

### `map_or_else(default, fn) -> U`

Aplica `fn` cuando es `Some`, de lo contrario llama a `default()`.

```python
>>> Some(3).map_or_else(lambda: 0, lambda v: v * 2)
6
>>> Nothing().map_or_else(lambda: 0, lambda v: v * 2)
0
```

### `flatten() -> Option[T]`

Aplana un nivel de anidamiento.

```python
>>> Some(Some(1)).flatten()
Some(1)
>>> Some(1).flatten()
Some(1)
```

### `flatten_all() -> Option[T]`

Aplana todos los niveles de anidamiento.

```python
>>> Some(Some(Some(1))).flatten_all()
Some(1)
```

---

## Conversión

### `ok_or(err) -> Result[T, E]`

Convierte un `Option` en un `Result`, usando `err` cuando está vacío.

```python
>>> Some(1).ok_or("missing")
Ok(1)
>>> Nothing().ok_or("missing")
Err('missing')
```

### `ok_or_else(fn) -> Result[T, E]`

Como `ok_or`, pero llama a `fn()` para producir el error cuando está vacío.

```python
>>> Nothing().ok_or_else(lambda: "missing")
Err('missing')
```

### `from_optional(value) -> Option[T]` *(estático)*

Construye un `Option` a partir de un valor que puede ser `None`.

```python
>>> Option.from_optional(None)
Nothing()
>>> Option.from_optional(5)
Some(5)
```

---

## Combinación

### `and_then(fn) -> Option[U]`

Ejecuta `fn` solo cuando es `Some`; de lo contrario devuelve `Nothing`.

```python
>>> Some(2).and_then(lambda v: Some(v + 1))
Some(3)
>>> Nothing().and_then(lambda v: Some(v + 1))
Nothing()
```

### `or_else(fn) -> Option[T]`

Ejecuta `fn` solo cuando es `Nothing`; de lo contrario devuelve la opción original.

```python
>>> Nothing().or_else(lambda: Some(9))
Some(9)
>>> Some(1).or_else(lambda: Some(9))
Some(1)
```

### `xor(other) -> Option[T]`

Devuelve un valor solo cuando exactamente una de las dos opciones es `Some`.

```python
>>> Some(1).xor(Nothing())
Some(1)
>>> Some(1).xor(Some(2))
Nothing()
```

### `zip(other) -> Option[tuple[T, U]]`

Empareja los valores cuando ambas opciones son `Some`.

```python
>>> Some(1).zip(Some("a"))
Some((1, 'a'))
```

### `zip_with(other, ctr) -> Option[R]`

Combina ambos valores con `ctr` cuando ambas opciones son `Some`.

```python
>>> Some(1).zip_with(Some(2), lambda a, b: a + b)
Some(3)
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
>>> Some(1) & Some(2)
Some(2)
>>> Nothing() & Some(2)
Nothing()
>>> Nothing() | Some(2)
Some(2)
```

---

## Mutación

### `push(value) -> T`

Almacena `value` y devuelve el valor que se tenía antes (o `value` si la opción estaba vacía).

```python
>>> opt = Some(1)
>>> opt.push(2)
1
>>> opt
Some(2)
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
    print(exc)
```
