# API Option

`Option[T]` rappresenta un valore che può essere presente (`Some`) o assente (`Nothing`). Si trova in `pyfplib.option` ed è riesportato dal pacchetto `pyfplib`.

```python
from pyfplib import Nothing, Option, Some
```

---

## Costruttori

### `Some(value: T)`

Avvolge un valore diverso da `None` in un `Option`. Poiché `Option` usa `None` internamente per rappresentare l'assenza, `Some(None)` si comporta come `Nothing()`.

```python
from pyfplib import Some

print(Some(42).is_some())    # True
print(Some(42).unwrap())     # 42
print(Some(None).is_none())  # True
```

### `Nothing()`

Crea un `Option` vuoto. Un `Nothing` è sempre `is_none()`.

```python
from pyfplib import Nothing

print(Nothing().is_none())     # True
print(Nothing().unwrap_or(0))  # 0
```

---

## Ispezione

| Metodo | Restituisce | Descrizione |
|---|---|---|
| `is_some()` | `bool` | `True` quando un valore è presente. |
| `is_none()` | `bool` | `True` quando nessun valore è presente. |
| `value` | `T \| None` | Il valore grezzo contenuto (può essere `None`). |
| `__bool__()` | `bool` | Vero per `Some`, falso per `Nothing`. |
| `__eq__(other)` | `bool` | Confronta i valori contenuti quando entrambi sono `Option`. |
| `__hash__()` | `int` | Calcola l'hash del valore contenuto. |

```python
from pyfplib import Nothing, Some

print(bool(Some(1)), bool(Nothing()))  # (True, False)
print(Some(1) == Some(1))              # True
```

### `inspect(fn: Callable[[T], None]) -> Option[T]`

Chiama `fn` con il valore contenuto quando è `Some`, poi restituisce l'opzione invariata.

```python
from pyfplib import Option, Some

option: Option[int] = Some(2)
returned = option.inspect(lambda value: print(f"inspected: {value}"))
print(returned)  # Some(2)
```

### `inspect_none(fn: Callable[[], None]) -> Option[T]`

Chiama `fn` senza argomenti quando è `Nothing`, poi restituisce l'opzione invariata.

```python
from pyfplib import Nothing

returned = Nothing().inspect_none(lambda: print("empty"))
print(returned)  # Nothing()
```

---

## Estrazione

| Metodo | Restituisce | Eccezione | Descrizione |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Restituisce il valore o solleva se vuoto. |
| `expect(message)` | `T` | `ExpectedError` | Restituisce il valore o solleva con `message`. |
| `unwrap_or(default)` | `T` | — | Restituisce il valore o `default`. |
| `unwrap_or_else(fn)` | `T` | — | Restituisce il valore o chiama `fn()` per un fallback. |

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

## Pattern Matching

`Option` supporta il pattern matching strutturale di Python. Usa `Some(value)` per associare il valore contenuto e `Nothing()` per corrispondere a un option vuoto, senza chiamare prima `is_some()`.

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

## Trasformazione

### `map(fn: Callable[[T], U]) -> Option[U]`

Applica `fn` al valore contenuto, avvolgendo il risultato in `Some`. `Nothing` resta `Nothing`.

```python
from pyfplib import Nothing, Some

def double(value: int) -> int:
    return value * 2

print(Some(3).map(double))    # Some(6)
print(Nothing().map(double))  # Nothing()
```

### `map_or(default: U, fn: Callable[[T], U]) -> Option[U]`

Applica `fn` a un valore `Some` oppure usa `default` e restituisce sempre un `Option` (`Some`). Usa `map_or_else` quando ti serve il valore semplice.

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

Applica `fn` quando è `Some`, altrimenti chiama `default()`.

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

Riduce di un livello l'annidamento. Un'opzione non annidata viene restituita invariata.

```python
from pyfplib import Some

print(Some(Some(1)).flatten())  # Some(1)
print(Some(1).flatten())        # Some(1)
```

### `flatten_all() -> Option[T]`

Riduce tutti i livelli di annidamento fino a raggiungere il valore non-option più interno.

```python
from pyfplib import Some

print(Some(Some(Some(1))).flatten_all())  # Some(1)
```

---

## Conversione

### `ok_or(err: E) -> Result[T, E]`

Converte un `Option` in un `Result`, usando `err` quando è vuoto.

```python
from pyfplib import Nothing, Some

print(Some(1).ok_or("missing"))   # Ok(1)
print(Nothing().ok_or("missing")) # Err('missing')
```

### `ok_or_else(fn: Callable[[], E]) -> Result[T, E]`

Come `ok_or`, ma chiama `fn()` per produrre l'errore quando è vuoto.

```python
from pyfplib import Nothing

def missing_error() -> str:
    return "missing"

print(Nothing().ok_or_else(missing_error))  # Err('missing')
```

### `from_optional(value: T | None) -> Option[T]` *(statico)*

Crea un `Option` da un valore che può essere `None`: `None` diventa `Nothing`, qualsiasi altro valore diventa `Some`.

```python
from pyfplib import Option

value: int | None = None
print(Option.from_optional(value))  # Nothing()
print(Option.from_optional(5))      # Some(5)
```

---

## Combinazione

### `and_then(fn: Callable[[T], Option[U]]) -> Option[U]`

Esegue `fn` solo quando è `Some`; altrimenti restituisce `Nothing`.

```python
from pyfplib import Nothing, Option, Some

def increment(value: int) -> Option[int]:
    return Some(value + 1)

print(Some(2).and_then(increment))   # Some(3)
print(Nothing().and_then(increment)) # Nothing()
```

### `or_else(fn: Callable[[], Option[T]]) -> Option[T]`

Esegue `fn` solo quando è `Nothing`; altrimenti restituisce l'opzione originale.

```python
from pyfplib import Nothing, Option, Some

def recover() -> Option[int]:
    return Some(9)

print(Nothing().or_else(recover))  # Some(9)
print(Some(1).or_else(recover))    # Some(1)
```

### `xor(other: Option[T]) -> Option[T]`

Restituisce un valore solo quando esattamente una delle due opzioni è `Some`.

```python
from pyfplib import Nothing, Some

print(Some(1).xor(Nothing()))  # Some(1)
print(Some(1).xor(Some(2)))    # Nothing()
```

### `zip(other: Option[U]) -> Option[tuple[T, U]]`

Accoppia i valori quando entrambe le opzioni sono `Some`.

```python
from pyfplib import Some

print(Some(1).zip(Some("a")))  # Some((1, 'a'))
```

### `zip_with(other: Option[U], ctr: Callable[[T, U], R]) -> Option[R]`

Combina entrambi i valori con `ctr` quando entrambe le opzioni sono `Some`.

```python
from pyfplib import Some

def add(left: int, right: int) -> int:
    return left + right

print(Some(1).zip_with(Some(2), add))  # Some(3)
```

---

## Operatori

`Option` sovraccarica `&` e `|` per rispecchiare `and_then` e `or_else`.

| Espressione | Equivalente | Descrizione |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Restituisce `b` quando `a` è `Some`, altrimenti `Nothing`. |
| `a & fn` | `a.and_then(lambda _: fn())` | Chiama `fn()` quando `a` è `Some`. |
| `a \| b` | `a.or_else(lambda: b)` | Restituisce `a` quando è `Some`, altrimenti `b`. |
| `a \| fn` | `a.or_else(fn)` | Chiama `fn()` quando `a` è `Nothing`. |

```python
from pyfplib import Nothing, Some

print(Some(1) & Some(2))    # Some(2)
print(Nothing() & Some(2))  # Nothing()
print(Nothing() | Some(2))  # Some(2)
```

---

## Mutazione

### `push(value: T) -> T`

Modifica l'opzione sul posto: memorizza `value` e restituisce il valore precedente, oppure `value` stesso se l'opzione era vuota.

```python
from pyfplib import Option, Some

option: Option[int] = Some(1)
previous = option.push(2)

print(previous)  # 1
print(option)    # Some(2)
```

---

## Errori

- `UnwrapError` — sollevata da `unwrap()` quando l'opzione è `Nothing`.
- `ExpectedError` — sollevata da `expect(message)` quando l'opzione è `Nothing`.

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
