# Result-API

`Result[T, E]` repräsentiert entweder Erfolg (`Ok`) oder Fehler (`Err`). Es befindet sich in `pyfplib.result` und wird aus dem Paket `pyfplib` re-exportiert.

```python
from pyfplib import Err, Ok, Result
```

---

## Konstruktoren

### `Ok(value: T)`

Erstellt ein erfolgreiches Ergebnis.

```python
from pyfplib import Ok, Result

result: Result[int, str] = Ok(42)
print(result.is_ok())  # True
print(result.unwrap()) # 42
```

### `Err(error: E)`

Erstellt ein fehlgeschlagenes Ergebnis.

```python
from pyfplib import Err, Result

result: Result[int, str] = Err("boom")
print(result.is_err())           # True
print(repr(result.unwrap_err())) # 'boom'
```

---

## Inspektion

| Methode | Rückgabe | Beschreibung |
|---|---|---|
| `is_ok()` | `bool` | `True`, wenn das Ergebnis `Ok` ist. |
| `is_err()` | `bool` | `True`, wenn das Ergebnis `Err` ist. |
| `value` | `T \| E` | Der enthaltene Wert oder Fehler. |
| `__bool__()` | `bool` | Wahr für `Ok`, falsch für `Err`. |
| `inspect(fn)` | `Result[T, E]` | Ruft `fn` mit dem `Ok`-Wert auf, gibt `self` zurück. |
| `inspect_err(fn)` | `Result[T, E]` | Ruft `fn` mit dem `Err`-Wert auf, gibt `self` zurück. |
| `ok()` | `Option[T]` | `Some(value)` für `Ok`, sonst `Nothing()`. |
| `err()` | `Option[E]` | `Some(error)` für `Err`, sonst `Nothing()`. |

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

## Extraktion

| Methode | Rückgabe | Ausnahme | Beschreibung |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Gibt den `Ok`-Wert zurück oder wirft bei `Err`. |
| `unwrap_err()` | `E` | `UnwrapError` | Gibt den `Err`-Wert zurück oder wirft bei `Ok`. |
| `expect(message)` | `T` | `ExpectedError` | Gibt den `Ok`-Wert zurück oder wirft mit `message`. |
| `expect_err(message)` | `E` | `ExpectedError` | Gibt den `Err`-Wert zurück oder wirft mit `message`. |
| `unwrap_or(default)` | `T` | — | Gibt den `Ok`-Wert oder `default` zurück. |
| `unwrap_or_else(fn)` | `T` | — | Gibt den `Ok`-Wert oder `fn(error)` zurück. |
| `unwrap_err_or(default)` | `E` | — | Gibt den `Err`-Wert oder `default` zurück. |

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

## Musterabgleich

`Result` unterstützt Pythons strukturellen Musterabgleich. Verwende `Ok(value)`, um einen erfolgreichen Wert zu binden, und `Err(error)` für den Fehler, ohne vorher `is_ok()` aufzurufen.

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

## Transformation

### `map(fn: Callable[[T], U]) -> Result[U, E]`

Wendet `fn` auf den `Ok`-Wert an. `Err` wird unverändert zurückgegeben.

```python
from pyfplib import Err, Ok

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map(triple))    # Ok(6)
print(Err("e").map(triple)) # Err('e')
```

### `map_or(default: T, fn: Callable[[T], U]) -> Result[U, E]`

Wendet `fn` auf den `Ok`-Wert an oder auf `default`, wenn das Ergebnis `Err` ist. Das Ergebnis ist immer `Ok`. Verwende `map_or_else`, wenn du den einfachen Wert benötigst.

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

Wendet `fn` auf den `Ok`-Wert an oder ruft bei `Err` `default(error)` auf und wendet `fn` auf diesen Fallback an, wobei der einfache Wert zurückgegeben wird.

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

Wendet `fn` auf den `Err`-Wert an. `Ok` wird unverändert zurückgegeben.

```python
from pyfplib import Err, Ok

print(Err("boom").map_err(str.upper))  # Err('BOOM')
print(Ok(1).map_err(str.upper))        # Ok(1)
```

### `flatten() -> Result[T, E]`

Reduziert eine Verschachtelungsebene. Ein nicht verschachteltes Ergebnis wird unverändert zurückgegeben.

```python
from pyfplib import Ok

print(Ok(Ok(1)).flatten())  # Ok(1)
print(Ok(1).flatten())      # Ok(1)
```

### `flatten_all() -> Result[T, E]`

Reduziert alle Verschachtelungsebenen, bis der innerste Nicht-`Result`-Wert erreicht ist.

```python
from pyfplib import Ok

print(Ok(Ok(Ok(1))).flatten_all())  # Ok(1)
```

---

## Kombinieren

### `and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]`

Führt `fn` nur aus, wenn das Ergebnis `Ok` ist; sonst wird `Err` unverändert zurückgegeben.

```python
from pyfplib import Err, Ok, Result

def increment(value: int) -> Result[int, str]:
    return Ok(value + 1)

print(Ok(2).and_then(increment))    # Ok(3)
print(Err("e").and_then(increment)) # Err('e')
```

### `or_else(fn: Callable[[E], Result[T, E]]) -> Result[T, E]`

Führt `fn` nur aus, wenn das Ergebnis `Err` ist; sonst wird das ursprüngliche `Ok` zurückgegeben.

```python
from pyfplib import Err, Ok, Result

def recover(error: str) -> Result[int, str]:
    return Ok(0)

print(Err("e").or_else(recover))  # Ok(0)
print(Ok(1).or_else(recover))     # Ok(1)
```

---

## Operatoren

`Result` überlädt `&` und `|` als Entsprechung zu `and_then` und `or_else`.

| Ausdruck | Entspricht | Beschreibung |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Gibt `b` zurück, wenn `a` `Ok` ist, sonst `Err`. |
| `a & fn` | `a.and_then(lambda v: fn(v))` | Ruft `fn(value)` auf, wenn `a` `Ok` ist. |
| `a \| b` | `a.or_else(lambda _: b)` | Gibt `a` zurück, wenn `Ok`, sonst `b`. |
| `a \| fn` | `a.or_else(lambda e: fn(e))` | Ruft `fn(error)` auf, wenn `a` `Err` ist. |

```python
from pyfplib import Err, Ok

print(Ok(1) & Ok(2))    # Ok(2)
print(Err("e") & Ok(2)) # Err('e')
print(Err("e") | Ok(2)) # Ok(2)
```

---

## Ausnahmebehandlung

### `Result.try_call(fn: Callable[..., R], *args, **kwargs) -> Result[R, Exception]` *(statisch)*

Ruft `fn` mit den übergebenen Argumenten auf und wandelt jede ausgelöste `Exception` in ein `Err` um.

```python
from pyfplib import Result

print(Result.try_call(int, "42"))            # Ok(42)
print(Result.try_call(int, "oops").is_err()) # True
```

---

## Fehler

- `UnwrapError` — wird von `unwrap()` und `unwrap_err()` geworfen, wenn die falsche Variante vorliegt.
- `ExpectedError` — wird von `expect()` und `expect_err()` mit der übergebenen Nachricht geworfen.

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
