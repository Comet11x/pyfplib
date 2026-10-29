# Option-API

`Option[T]` repräsentiert einen Wert, der vorhanden (`Some`) oder abwesend (`Nothing`) sein kann. Es befindet sich in `pyfplib.option` und wird aus dem Paket `pyfplib` re-exportiert.

```python
from pyfplib import Nothing, Option, Some
```

---

## Konstruktoren

### `Some(value)`

Verpackt einen Wert in ein `Option`. Ein `Some` ist immer `is_some()`.

```python
>>> Some(42).is_some()
True
>>> Some(42).unwrap()
42
```

### `Nothing()`

Erstellt ein leeres `Option`. Ein `Nothing` ist immer `is_none()`.

```python
>>> Nothing().is_none()
True
>>> Nothing().unwrap_or(0)
0
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
>>> bool(Some(1)), bool(Nothing())
(True, False)
>>> Some(1) == Some(1)
True
```

### `inspect(fn) -> Option[T]`

Ruft `fn` bei `Some` mit dem enthaltenen Wert auf und gibt das Option unverändert zurück.

```python
>>> Some(2).inspect(lambda v: print(v))
2
Some(2)
```

### `inspect_none(fn) -> Option[T]`

Ruft `fn` bei `Nothing` ohne Argumente auf und gibt das Option unverändert zurück.

```python
>>> Nothing().inspect_none(lambda: print("empty"))
empty
Nothing()
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
>>> Some(3).unwrap_or(0)
3
>>> Nothing().unwrap_or(0)
0
>>> Nothing().unwrap_or_else(lambda: 10)
10
```

---

## Transformation

### `map(fn) -> Option[U]`

Wendet `fn` auf den enthaltenen Wert an und verpackt das Ergebnis in `Some`. `Nothing` bleibt `Nothing`.

```python
>>> Some(3).map(lambda v: v * 2)
Some(6)
>>> Nothing().map(lambda v: v * 2)
Nothing()
```

### `map_or(default, fn) -> Option[U]`

Wendet `fn` bei `Some` an, sonst wird `default` verwendet. Das Ergebnis ist immer in `Some` verpackt.

```python
>>> Some(3).map_or(0, lambda v: v * 2)
Some(6)
>>> Nothing().map_or(0, lambda v: v * 2)
Some(0)
```

### `map_or_else(default, fn) -> U`

Wendet `fn` bei `Some` an, sonst wird `default()` aufgerufen.

```python
>>> Some(3).map_or_else(lambda: 0, lambda v: v * 2)
6
>>> Nothing().map_or_else(lambda: 0, lambda v: v * 2)
0
```

### `flatten() -> Option[T]`

Faltet eine Ebene der Verschachtelung.

```python
>>> Some(Some(1)).flatten()
Some(1)
>>> Some(1).flatten()
Some(1)
```

### `flatten_all() -> Option[T]`

Faltet alle Ebenen der Verschachtelung.

```python
>>> Some(Some(Some(1))).flatten_all()
Some(1)
```

---

## Konvertierung

### `ok_or(err) -> Result[T, E]`

Konvertiert ein `Option` in ein `Result` und verwendet `err`, wenn es leer ist.

```python
>>> Some(1).ok_or("missing")
Ok(1)
>>> Nothing().ok_or("missing")
Err('missing')
```

### `ok_or_else(fn) -> Result[T, E]`

Wie `ok_or`, ruft aber `fn()` auf, um den Fehler zu erzeugen, wenn das Option leer ist.

```python
>>> Nothing().ok_or_else(lambda: "missing")
Err('missing')
```

### `from_optional(value) -> Option[T]` *(statisch)*

Erstellt ein `Option` aus einem möglicherweise `None`-Wert.

```python
>>> Option.from_optional(None)
Nothing()
>>> Option.from_optional(5)
Some(5)
```

---

## Kombinieren

### `and_then(fn) -> Option[U]`

Führt `fn` nur bei `Some` aus; sonst wird `Nothing` zurückgegeben.

```python
>>> Some(2).and_then(lambda v: Some(v + 1))
Some(3)
>>> Nothing().and_then(lambda v: Some(v + 1))
Nothing()
```

### `or_else(fn) -> Option[T]`

Führt `fn` nur bei `Nothing` aus; sonst wird das ursprüngliche Option zurückgegeben.

```python
>>> Nothing().or_else(lambda: Some(9))
Some(9)
>>> Some(1).or_else(lambda: Some(9))
Some(1)
```

### `xor(other) -> Option[T]`

Gibt nur dann einen Wert zurück, wenn genau eines der beiden Optionen `Some` ist.

```python
>>> Some(1).xor(Nothing())
Some(1)
>>> Some(1).xor(Some(2))
Nothing()
```

### `zip(other) -> Option[tuple[T, U]]`

Paart die Werte, wenn beide Optionen `Some` sind.

```python
>>> Some(1).zip(Some("a"))
Some((1, 'a'))
```

### `zip_with(other, ctr) -> Option[R]`

Kombiniert beide Werte mit `ctr`, wenn beide `Some` sind.

```python
>>> Some(1).zip_with(Some(2), lambda a, b: a + b)
Some(3)
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
>>> Some(1) & Some(2)
Some(2)
>>> Nothing() & Some(2)
Nothing()
>>> Nothing() | Some(2)
Some(2)
```

---

## Mutation

### `push(value) -> T`

Speichert `value` und gibt den zuvor gehaltenen Wert zurück (oder `value`, wenn das Option leer war).

```python
>>> opt = Some(1)
>>> opt.push(2)
1
>>> opt
Some(2)
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
    print(exc)
```
