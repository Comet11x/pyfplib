# API Result

`Result[T, E]` représente soit le succès (`Ok`), soit l'échec (`Err`). Il se trouve dans `pyfplib.result` et est réexporté depuis le paquet `pyfplib`.

```python
from pyfplib import Err, Ok, Result
```

---

## Constructeurs

### `Ok(value)`

Crée un résultat de succès.

```python
>>> Ok(42).is_ok()
True
>>> Ok(42).unwrap()
42
```

### `Err(error)`

Crée un résultat d'échec.

```python
>>> Err("boom").is_err()
True
>>> Err("boom").unwrap_err()
'boom'
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
>>> bool(Ok(1)), bool(Err("e"))
(True, False)
>>> Ok(1).ok()
Some(1)
>>> Err("e").ok()
Nothing()
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

Applique `fn` à la valeur `Ok`. `Err` est renvoyé inchangé.

```python
>>> Ok(2).map(lambda v: v * 3)
Ok(6)
>>> Err("e").map(lambda v: v * 3)
Err('e')
```

### `map_or(default, fn) -> Result[U, E]`

Applique `fn` à la valeur `Ok` ou utilise `default`. Le résultat est toujours `Ok`.

```python
>>> Ok(2).map_or(0, lambda v: v * 3)
Ok(6)
>>> Err("e").map_or(0, lambda v: v * 3)
Ok(0)
```

### `map_or_else(default, fn) -> U`

Applique `fn` à la valeur `Ok`, ou appelle `default(error)` sur `Err`.

```python
>>> Ok(2).map_or_else(lambda e: 0, lambda v: v * 3)
6
>>> Err("e").map_or_else(lambda e: len(e), lambda v: v * 3)
3
```

### `map_err(fn) -> Result[T, U]`

Applique `fn` à la valeur `Err`. `Ok` est renvoyé inchangé.

```python
>>> Err("boom").map_err(str.upper)
Err('BOOM')
>>> Ok(1).map_err(str.upper)
Ok(1)
```

### `flatten() -> Result[T, E]`

Aplatit un niveau d'imbrication.

```python
>>> Ok(Ok(1)).flatten()
Ok(1)
>>> Ok(1).flatten()
Ok(1)
```

### `flatten_all() -> Result[T, E]`

Aplatit tous les niveaux d'imbrication.

```python
>>> Ok(Ok(Ok(1))).flatten_all()
Ok(1)
```

---

## Combinaison

### `and_then(fn) -> Result[T, E]`

Exécute `fn` uniquement lorsque le résultat est `Ok` ; sinon renvoie `Err` inchangé.

```python
>>> Ok(2).and_then(lambda v: Ok(v + 1))
Ok(3)
>>> Err("e").and_then(lambda v: Ok(v + 1))
Err('e')
```

### `or_else(fn) -> Result[T, E]`

Exécute `fn` uniquement lorsque le résultat est `Err` ; sinon renvoie l'`Ok` d'origine.

```python
>>> Err("e").or_else(lambda e: Ok(0))
Ok(0)
>>> Ok(1).or_else(lambda e: Ok(0))
Ok(1)
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
>>> Ok(1) & Ok(2)
Ok(2)
>>> Err("e") & Ok(2)
Err('e')
>>> Err("e") | Ok(2)
Ok(2)
```

---

## Gestion des exceptions

### `Result.try_call(fn, *args, **kwargs) -> Result[R, Exception]` *(statique)*

Appelle `fn` et convertit toute exception levée en `Err`.

```python
>>> Result.try_call(int, "42")
Ok(42)
>>> Result.try_call(int, "oops").is_err()
True
```

---

## Erreurs

- `UnwrapError` — levée par `unwrap()` et `unwrap_err()` lorsque la mauvaise variante est présente.
- `ExpectedError` — levée par `expect()` et `expect_err()` avec le message fourni.

```python
from pyfplib import Err
from pyfplib.errors import UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)
```
