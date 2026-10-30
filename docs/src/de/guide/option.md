# Option-API

`Option[T]` repräsentiert einen Wert, der vorhanden (`Some`) oder abwesend (`Nothing`) sein kann. Es befindet sich in `pyfplib.option` und wird aus dem Paket `pyfplib` re-exportiert.

```python
from pyfplib import Nothing, Option, Some
```

---

## Konstruktoren

### `Some(value: T)`

Verpackt einen Wert ungleich `None` in ein `Option`. Da `Option` intern `None` verwendet, um Abwesenheit darzustellen, verhält sich `Some(None)` wie `Nothing()`.

```python
from pyfplib import Some

print(Some(42).is_some())    # True
print(Some(42).unwrap())     # 42
print(Some(None).is_none())  # True
```

### `Nothing()`

Erstellt ein leeres `Option`. Ein `Nothing` ist immer `is_none()`.

```python
from pyfplib import Nothing

print(Nothing().is_none())     # True
print(Nothing().unwrap_or(0))  # 0
```

---

## Inspektion

| Methode | Rückgabe | Beschreibung |
|---|---|---|
| `is_some()` | `bool` | `True`, wenn ein Wert vorhanden ist. |
| `is_none()` | `bool` | `True`, wenn kein Wert vorhanden ist. |
| `value` | `T \| None` | Der rohe enthaltene Wert (kann `None` sein). |
| `__bool__()` | `bool` | Wahr für `Some`, falsch für `Nothing`. |
| `__eq__(other)` | `bool` | Vergleicht enthaltene Werte, wenn beide `Option` sind. |
| `__hash__()` | `int` | Hasht den enthaltenen Wert. |

```python
from pyfplib import Nothing, Some

print(bool(Some(1)), bool(Nothing()))  # (True, False)
print(Some(1) == Some(1))              # True
```

### `inspect(fn: Callable[[T], None]) -> Option[T]`

Ruft `fn` bei `Some` mit dem enthaltenen Wert auf und gibt das Option unverändert zurück.

```python
from pyfplib import Option, Some

option: Option[int] = Some(2)
returned = option.inspect(lambda value: print(f"inspected: {value}"))
print(returned)  # Some(2)
```

### `inspect_none(fn: Callable[[], None]) -> Option[T]`

Ruft `fn` bei `Nothing` ohne Argumente auf und gibt das Option unverändert zurück.

```python
from pyfplib import Nothing

returned = Nothing().inspect_none(lambda: print("empty"))
print(returned)  # Nothing()
```

---

## Extraktion

| Methode | Rückgabe | Ausnahme | Beschreibung |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Gibt den Wert zurück oder wirft, wenn leer. |
| `expect(message)` | `T` | `ExpectedError` | Gibt den Wert zurück oder wirft mit `message`. |
| `unwrap_or(default)` | `T` | — | Gibt den Wert oder `default` zurück. |
| `unwrap_or_else(fn)` | `T` | — | Gibt den Wert zurück oder ruft `fn()` für einen Ersatz auf. |

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

## Musterabgleich

`Option` unterstützt Pythons strukturellen Musterabgleich. Verwende `Some(value)`, um den enthaltenen Wert zu binden, und `Nothing()`, um ein leeres Option zu erkennen, ohne vorher `is_some()` aufzurufen.

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

## Transformation

### `map(fn: Callable[[T], U]) -> Option[U]`

Wendet `fn` auf den enthaltenen Wert an und verpackt das Ergebnis in `Some`. `Nothing` bleibt `Nothing`.

```python
from pyfplib import Nothing, Some

def double(value: int) -> int:
    return value * 2

print(Some(3).map(double))    # Some(6)
print(Nothing().map(double))  # Nothing()
```

### `map_or(default: U, fn: Callable[[T], U]) -> Option[U]`

Wendet `fn` auf einen `Some`-Wert an oder verwendet `default` und gibt immer ein `Option` (`Some`) zurück. Verwende `map_or_else`, wenn du den einfachen Wert benötigst.

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

Wendet `fn` bei `Some` an, sonst wird `default()` aufgerufen.

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

Reduziert eine Verschachtelungsebene. Ein nicht verschachteltes Option wird unverändert zurückgegeben.

```python
from pyfplib import Some

print(Some(Some(1)).flatten())  # Some(1)
print(Some(1).flatten())        # Some(1)
```

### `flatten_all() -> Option[T]`

Reduziert alle Verschachtelungsebenen, bis der innerste Nicht-Option-Wert erreicht ist.

```python
from pyfplib import Some

print(Some(Some(Some(1))).flatten_all())  # Some(1)
```

---

## Konvertierung

### `ok_or(err: E) -> Result[T, E]`

Konvertiert ein `Option` in ein `Result` und verwendet `err`, wenn es leer ist.

```python
from pyfplib import Nothing, Some

print(Some(1).ok_or("missing"))   # Ok(1)
print(Nothing().ok_or("missing")) # Err('missing')
```

### `ok_or_else(fn: Callable[[], E]) -> Result[T, E]`

Wie `ok_or`, ruft aber `fn()` auf, um den Fehler zu erzeugen, wenn das Option leer ist.

```python
from pyfplib import Nothing

def missing_error() -> str:
    return "missing"

print(Nothing().ok_or_else(missing_error))  # Err('missing')
```

### `from_optional(value: T | None) -> Option[T]` *(statisch)*

Erstellt ein `Option` aus einem möglicherweise `None`-Wert: `None` wird zu `Nothing`, jeder andere Wert zu `Some`.

```python
from pyfplib import Option

value: int | None = None
print(Option.from_optional(value))  # Nothing()
print(Option.from_optional(5))      # Some(5)
```

---

## Kombinieren

### `and_then(fn: Callable[[T], Option[U]]) -> Option[U]`

Führt `fn` nur bei `Some` aus; sonst wird `Nothing` zurückgegeben.

```python
from pyfplib import Nothing, Option, Some

def increment(value: int) -> Option[int]:
    return Some(value + 1)

print(Some(2).and_then(increment))   # Some(3)
print(Nothing().and_then(increment)) # Nothing()
```

### `or_else(fn: Callable[[], Option[T]]) -> Option[T]`

Führt `fn` nur bei `Nothing` aus; sonst wird das ursprüngliche Option zurückgegeben.

```python
from pyfplib import Nothing, Option, Some

def recover() -> Option[int]:
    return Some(9)

print(Nothing().or_else(recover))  # Some(9)
print(Some(1).or_else(recover))    # Some(1)
```

### `xor(other: Option[T]) -> Option[T]`

Gibt nur dann einen Wert zurück, wenn genau eines der beiden Optionen `Some` ist.

```python
from pyfplib import Nothing, Some

print(Some(1).xor(Nothing()))  # Some(1)
print(Some(1).xor(Some(2)))    # Nothing()
```

### `zip(other: Option[U]) -> Option[tuple[T, U]]`

Paart die Werte, wenn beide Optionen `Some` sind.

```python
from pyfplib import Some

print(Some(1).zip(Some("a")))  # Some((1, 'a'))
```

### `zip_with(other: Option[U], ctr: Callable[[T, U], R]) -> Option[R]`

Kombiniert beide Werte mit `ctr`, wenn beide `Some` sind.

```python
from pyfplib import Some

def add(left: int, right: int) -> int:
    return left + right

print(Some(1).zip_with(Some(2), add))  # Some(3)
```

---

## Operatoren

`Option` überlädt `&` und `|` als Entsprechung zu `and_then` und `or_else`.

| Ausdruck | Entspricht | Beschreibung |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Gibt `b` zurück, wenn `a` `Some` ist, sonst `Nothing`. |
| `a & fn` | `a.and_then(lambda _: fn())` | Ruft `fn()` auf, wenn `a` `Some` ist. |
| `a \| b` | `a.or_else(lambda: b)` | Gibt `a` zurück, wenn `Some`, sonst `b`. |
| `a \| fn` | `a.or_else(fn)` | Ruft `fn()` auf, wenn `a` `Nothing` ist. |

```python
from pyfplib import Nothing, Some

print(Some(1) & Some(2))    # Some(2)
print(Nothing() & Some(2))  # Nothing()
print(Nothing() | Some(2))  # Some(2)
```

---

## Mutation

### `push(value: T) -> T`

Verändert das Option direkt: speichert `value` und gibt den zuvor gehaltenen Wert zurück, oder `value` selbst, wenn das Option leer war.

```python
from pyfplib import Option, Some

option: Option[int] = Some(1)
previous = option.push(2)

print(previous)  # 1
print(option)    # Some(2)
```

---

## Fehler

- `UnwrapError` — wird von `unwrap()` geworfen, wenn das Option `Nothing` ist.
- `ExpectedError` — wird von `expect(message)` geworfen, wenn das Option `Nothing` ist.

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
