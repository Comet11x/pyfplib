# API Result

`Result[T, E]` représente soit le succès (`Ok`), soit l'échec (`Err`). Il se trouve dans `pyfplib.result` et est réexporté depuis le paquet `pyfplib`.

```python
from pyfplib import Err, Ok, Result
```

---

## Constructeurs

### `Ok(value: T)`

Crée un résultat de succès.

```python
from pyfplib import Ok, Result

result: Result[int, str] = Ok(42)
print(result.is_ok())  # True
print(result.unwrap()) # 42
```

### `Err(error: E)`

Crée un résultat d'échec.

```python
from pyfplib import Err, Result

result: Result[int, str] = Err("boom")
print(result.is_err())           # True
print(repr(result.unwrap_err())) # 'boom'
```

---

## Inspection

| Méthode | Retourne | Description |
|---|---|---|
| `is_ok()` | `bool` | `True` lorsque le résultat est `Ok`. |
| `is_err()` | `bool` | `True` lorsque le résultat est `Err`. |
| `value` | `T \| E` | La valeur ou l'erreur contenue. |
| `__bool__()` | `bool` | Vrai pour `Ok`, faux pour `Err`. |
| `inspect(fn)` | `Result[T, E]` | Appelle `fn` avec la valeur `Ok`, renvoie `self`. |
| `inspect_err(fn)` | `Result[T, E]` | Appelle `fn` avec la valeur `Err`, renvoie `self`. |
| `ok()` | `Option[T]` | `Some(value)` pour `Ok`, sinon `Nothing()`. |
| `err()` | `Option[E]` | `Some(error)` pour `Err`, sinon `Nothing()`. |

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

## Extraction

| Méthode | Retourne | Exception | Description |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Renvoie la valeur `Ok` ou lève sur `Err`. |
| `unwrap_err()` | `E` | `UnwrapError` | Renvoie la valeur `Err` ou lève sur `Ok`. |
| `expect(message)` | `T` | `ExpectedError` | Renvoie la valeur `Ok` ou lève avec `message`. |
| `expect_err(message)` | `E` | `ExpectedError` | Renvoie la valeur `Err` ou lève avec `message`. |
| `unwrap_or(default)` | `T` | — | Renvoie la valeur `Ok` ou `default`. |
| `unwrap_or_else(fn)` | `T` | — | Renvoie la valeur `Ok` ou `fn(error)`. |
| `unwrap_err_or(default)` | `E` | — | Renvoie la valeur `Err` ou `default`. |

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

## Correspondance de motifs

`Result` prend en charge la correspondance de motifs structurelle de Python. Utilisez `Ok(value)` pour lier une valeur de succès et `Err(error)` pour lier l'erreur, sans appeler `is_ok()` au préalable.

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

Applique `fn` à la valeur `Ok`. `Err` est renvoyé inchangé.

```python
from pyfplib import Err, Ok

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map(triple))    # Ok(6)
print(Err("e").map(triple)) # Err('e')
```

### `map_or(default: T, fn: Callable[[T], U]) -> Result[U, E]`

Applique `fn` à la valeur `Ok` ou à `default` lorsque le résultat est `Err`. Le résultat est toujours `Ok`. Utilisez `map_or_else` lorsque vous avez besoin de la valeur simple.

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

Applique `fn` à la valeur `Ok`, ou appelle `default(error)` sur `Err` et applique `fn` à cette valeur de repli, en renvoyant la valeur simple.

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

Applique `fn` à la valeur `Err`. `Ok` est renvoyé inchangé.

```python
from pyfplib import Err, Ok

print(Err("boom").map_err(str.upper))  # Err('BOOM')
print(Ok(1).map_err(str.upper))        # Ok(1)
```

### `flatten() -> Result[T, E]`

Aplatit un niveau d'imbrication. Un résultat non imbriqué est renvoyé inchangé.

```python
from pyfplib import Ok

print(Ok(Ok(1)).flatten())  # Ok(1)
print(Ok(1).flatten())      # Ok(1)
```

### `flatten_all() -> Result[T, E]`

Aplatit tous les niveaux d'imbrication jusqu'à atteindre la valeur non-`Result` la plus interne.

```python
from pyfplib import Ok

print(Ok(Ok(Ok(1))).flatten_all())  # Ok(1)
```

---

## Combinaison

### `and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]`

Exécute `fn` uniquement lorsque le résultat est `Ok` ; sinon renvoie `Err` inchangé.

```python
from pyfplib import Err, Ok, Result

def increment(value: int) -> Result[int, str]:
    return Ok(value + 1)

print(Ok(2).and_then(increment))    # Ok(3)
print(Err("e").and_then(increment)) # Err('e')
```

### `or_else(fn: Callable[[E], Result[T, E]]) -> Result[T, E]`

Exécute `fn` uniquement lorsque le résultat est `Err` ; sinon renvoie l'`Ok` d'origine.

```python
from pyfplib import Err, Ok, Result

def recover(error: str) -> Result[int, str]:
    return Ok(0)

print(Err("e").or_else(recover))  # Ok(0)
print(Ok(1).or_else(recover))     # Ok(1)
```

---

## Opérateurs

`Result` surcharge `&` et `|` pour refléter `and_then` et `or_else`.

| Expression | Équivalent | Description |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Renvoie `b` lorsque `a` est `Ok`, sinon `Err`. |
| `a & fn` | `a.and_then(lambda v: fn(v))` | Appelle `fn(value)` lorsque `a` est `Ok`. |
| `a \| b` | `a.or_else(lambda _: b)` | Renvoie `a` lorsque `Ok`, sinon `b`. |
| `a \| fn` | `a.or_else(lambda e: fn(e))` | Appelle `fn(error)` lorsque `a` est `Err`. |

```python
from pyfplib import Err, Ok

print(Ok(1) & Ok(2))    # Ok(2)
print(Err("e") & Ok(2)) # Err('e')
print(Err("e") | Ok(2)) # Ok(2)
```

---

## Gestion des exceptions

### `Result.try_call(fn: Callable[..., R], *args, **kwargs) -> Result[R, Exception]` *(statique)*

Appelle `fn` avec les arguments fournis et convertit toute `Exception` levée en `Err`.

```python
from pyfplib import Result

print(Result.try_call(int, "42"))            # Ok(42)
print(Result.try_call(int, "oops").is_err()) # True
```

---

## Erreurs

- `UnwrapError` — levée par `unwrap()` et `unwrap_err()` lorsque la mauvaise variante est présente.
- `ExpectedError` — levée par `expect()` et `expect_err()` avec le message fourni.

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
