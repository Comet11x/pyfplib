# Result-API

`Result[T, E]` repräsentiert entweder Erfolg (`Ok`) oder Fehler (`Err`). Es befindet sich in `pyfplib.result` und wird aus dem Paket `pyfplib` re-exportiert.

```python
from pyfplib import Err, Ok, Result
```

---

## Konstruktoren

### `Ok(value)`

Erstellt ein erfolgreiches Ergebnis.

```python
>>> Ok(42).is_ok()
True
>>> Ok(42).unwrap()
42
```

### `Err(error)`

Erstellt ein fehlgeschlagenes Ergebnis.

```python
>>> Err("boom").is_err()
True
>>> Err("boom").unwrap_err()
'boom'
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
>>> bool(Ok(1)), bool(Err("e"))
(True, False)
>>> Ok(1).ok()
Some(1)
>>> Err("e").ok()
Nothing()
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
>>> Ok(1).unwrap_or(0)
1
>>> Err("e").unwrap_or(0)
0
>>> Err("e").unwrap_or_else(lambda e: len(e))
1
```

---

## Transformation

### `map(fn) -> Result[U, E]`

Wendet `fn` auf den `Ok`-Wert an. `Err` wird unverändert zurückgegeben.

```python
>>> Ok(2).map(lambda v: v * 3)
Ok(6)
>>> Err("e").map(lambda v: v * 3)
Err('e')
```

### `map_or(default, fn) -> Result[U, E]`

Wendet `fn` auf den `Ok`-Wert an oder verwendet `default`. Das Ergebnis ist immer `Ok`.

```python
>>> Ok(2).map_or(0, lambda v: v * 3)
Ok(6)
>>> Err("e").map_or(0, lambda v: v * 3)
Ok(0)
```

### `map_or_else(default, fn) -> U`

Wendet `fn` auf den `Ok`-Wert an oder ruft `default(error)` bei `Err` auf.

```python
>>> Ok(2).map_or_else(lambda e: 0, lambda v: v * 3)
6
>>> Err("e").map_or_else(lambda e: len(e), lambda v: v * 3)
3
```

### `map_err(fn) -> Result[T, U]`

Wendet `fn` auf den `Err`-Wert an. `Ok` wird unverändert zurückgegeben.

```python
>>> Err("boom").map_err(str.upper)
Err('BOOM')
>>> Ok(1).map_err(str.upper)
Ok(1)
```

### `flatten() -> Result[T, E]`

Faltet eine Ebene der Verschachtelung.

```python
>>> Ok(Ok(1)).flatten()
Ok(1)
>>> Ok(1).flatten()
Ok(1)
```

### `flatten_all() -> Result[T, E]`

Faltet alle Ebenen der Verschachtelung.

```python
>>> Ok(Ok(Ok(1))).flatten_all()
Ok(1)
```

---

## Kombinieren

### `and_then(fn) -> Result[T, E]`

Führt `fn` nur aus, wenn das Ergebnis `Ok` ist; sonst wird `Err` unverändert zurückgegeben.

```python
>>> Ok(2).and_then(lambda v: Ok(v + 1))
Ok(3)
>>> Err("e").and_then(lambda v: Ok(v + 1))
Err('e')
```

### `or_else(fn) -> Result[T, E]`

Führt `fn` nur aus, wenn das Ergebnis `Err` ist; sonst wird das ursprüngliche `Ok` zurückgegeben.

```python
>>> Err("e").or_else(lambda e: Ok(0))
Ok(0)
>>> Ok(1).or_else(lambda e: Ok(0))
Ok(1)
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
>>> Ok(1) & Ok(2)
Ok(2)
>>> Err("e") & Ok(2)
Err('e')
>>> Err("e") | Ok(2)
Ok(2)
```

---

## Ausnahmebehandlung

### `Result.try_call(fn, *args, **kwargs) -> Result[R, Exception]` *(statisch)*

Ruft `fn` auf und wandelt jede ausgelöste Ausnahme in ein `Err` um.

```python
>>> Result.try_call(int, "42")
Ok(42)
>>> Result.try_call(int, "oops").is_err()
True
```

---

## Fehler

- `UnwrapError` — wird von `unwrap()` und `unwrap_err()` geworfen, wenn die falsche Variante vorliegt.
- `ExpectedError` — wird von `expect()` und `expect_err()` mit der übergebenen Nachricht geworfen.

```python
from pyfplib import Err
from pyfplib.errors import UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)
```
