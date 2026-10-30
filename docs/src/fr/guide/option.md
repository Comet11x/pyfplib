# API Option

`Option[T]` représente une valeur qui peut être présente (`Some`) ou absente (`Nothing`). Il se trouve dans `pyfplib.option` et est réexporté depuis le paquet `pyfplib`.

```python
from pyfplib import Nothing, Option, Some
```

---

## Constructeurs

### `Some(value: T)`

Enveloppe une valeur différente de `None` dans un `Option`. Comme `Option` utilise `None` en interne pour représenter l'absence, `Some(None)` se comporte comme `Nothing()`.

```python
from pyfplib import Some

print(Some(42).is_some())    # True
print(Some(42).unwrap())     # 42
print(Some(None).is_none())  # True
```

### `Nothing()`

Crée un `Option` vide. Un `Nothing` est toujours `is_none()`.

```python
from pyfplib import Nothing

print(Nothing().is_none())     # True
print(Nothing().unwrap_or(0))  # 0
```

---

## Inspection

| Méthode | Retourne | Description |
|---|---|---|
| `is_some()` | `bool` | `True` lorsqu'une valeur est présente. |
| `is_none()` | `bool` | `True` lorsqu'aucune valeur n'est présente. |
| `value` | `T \| None` | La valeur brute contenue (peut être `None`). |
| `__bool__()` | `bool` | Vrai pour `Some`, faux pour `Nothing`. |
| `__eq__(other)` | `bool` | Compare les valeurs contenues lorsque les deux sont des `Option`. |
| `__hash__()` | `int` | Calcule le hachage de la valeur contenue. |

```python
from pyfplib import Nothing, Some

print(bool(Some(1)), bool(Nothing()))  # (True, False)
print(Some(1) == Some(1))              # True
```

### `inspect(fn: Callable[[T], None]) -> Option[T]`

Appelle `fn` avec la valeur contenue lorsque l'option est `Some`, puis renvoie l'option inchangée.

```python
from pyfplib import Option, Some

option: Option[int] = Some(2)
returned = option.inspect(lambda value: print(f"inspected: {value}"))
print(returned)  # Some(2)
```

### `inspect_none(fn: Callable[[], None]) -> Option[T]`

Appelle `fn` sans argument lorsque l'option est `Nothing`, puis renvoie l'option inchangée.

```python
from pyfplib import Nothing

returned = Nothing().inspect_none(lambda: print("empty"))
print(returned)  # Nothing()
```

---

## Extraction

| Méthode | Retourne | Exception | Description |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Renvoie la valeur ou lève une exception si vide. |
| `expect(message)` | `T` | `ExpectedError` | Renvoie la valeur ou lève avec `message`. |
| `unwrap_or(default)` | `T` | — | Renvoie la valeur ou `default`. |
| `unwrap_or_else(fn)` | `T` | — | Renvoie la valeur ou appelle `fn()` pour un repli. |

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

## Correspondance de motifs

`Option` prend en charge la correspondance de motifs structurelle de Python. Utilisez `Some(value)` pour lier la valeur contenue et `Nothing()` pour correspondre à une option vide, sans appeler `is_some()` au préalable.

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

Applique `fn` à la valeur contenue et enveloppe le résultat dans `Some`. `Nothing` reste `Nothing`.

```python
from pyfplib import Nothing, Some

def double(value: int) -> int:
    return value * 2

print(Some(3).map(double))    # Some(6)
print(Nothing().map(double))  # Nothing()
```

### `map_or(default: U, fn: Callable[[T], U]) -> Option[U]`

Applique `fn` à une valeur `Some` ou utilise `default`, et renvoie toujours un `Option` (`Some`). Utilisez `map_or_else` lorsque vous avez besoin de la valeur simple.

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

Applique `fn` lorsque l'option est `Some`, sinon appelle `default()`.

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

Réduit d'un niveau l'imbrication. Une option non imbriquée est renvoyée inchangée.

```python
from pyfplib import Some

print(Some(Some(1)).flatten())  # Some(1)
print(Some(1).flatten())        # Some(1)
```

### `flatten_all() -> Option[T]`

Réduit tous les niveaux d'imbrication jusqu'à atteindre la valeur non-option la plus interne.

```python
from pyfplib import Some

print(Some(Some(Some(1))).flatten_all())  # Some(1)
```

---

## Conversion

### `ok_or(err: E) -> Result[T, E]`

Convertit un `Option` en `Result`, en utilisant `err` lorsque l'option est vide.

```python
from pyfplib import Nothing, Some

print(Some(1).ok_or("missing"))   # Ok(1)
print(Nothing().ok_or("missing")) # Err('missing')
```

### `ok_or_else(fn: Callable[[], E]) -> Result[T, E]`

Comme `ok_or`, mais appelle `fn()` pour produire l'erreur lorsque l'option est vide.

```python
from pyfplib import Nothing

def missing_error() -> str:
    return "missing"

print(Nothing().ok_or_else(missing_error))  # Err('missing')
```

### `from_optional(value: T | None) -> Option[T]` *(statique)*

Crée un `Option` à partir d'une valeur éventuellement `None` : `None` devient `Nothing`, et toute autre valeur devient `Some`.

```python
from pyfplib import Option

value: int | None = None
print(Option.from_optional(value))  # Nothing()
print(Option.from_optional(5))      # Some(5)
```

---

## Combinaison

### `and_then(fn: Callable[[T], Option[U]]) -> Option[U]`

Exécute `fn` uniquement lorsque l'option est `Some` ; sinon renvoie `Nothing`.

```python
from pyfplib import Nothing, Option, Some

def increment(value: int) -> Option[int]:
    return Some(value + 1)

print(Some(2).and_then(increment))   # Some(3)
print(Nothing().and_then(increment)) # Nothing()
```

### `or_else(fn: Callable[[], Option[T]]) -> Option[T]`

Exécute `fn` uniquement lorsque l'option est `Nothing` ; sinon renvoie l'option d'origine.

```python
from pyfplib import Nothing, Option, Some

def recover() -> Option[int]:
    return Some(9)

print(Nothing().or_else(recover))  # Some(9)
print(Some(1).or_else(recover))    # Some(1)
```

### `xor(other: Option[T]) -> Option[T]`

Renvoie une valeur uniquement lorsque exactement l'une des deux options est `Some`.

```python
from pyfplib import Nothing, Some

print(Some(1).xor(Nothing()))  # Some(1)
print(Some(1).xor(Some(2)))    # Nothing()
```

### `zip(other: Option[U]) -> Option[tuple[T, U]]`

Associe les valeurs lorsque les deux options sont `Some`.

```python
from pyfplib import Some

print(Some(1).zip(Some("a")))  # Some((1, 'a'))
```

### `zip_with(other: Option[U], ctr: Callable[[T, U], R]) -> Option[R]`

Combine les deux valeurs avec `ctr` lorsque les deux options sont `Some`.

```python
from pyfplib import Some

def add(left: int, right: int) -> int:
    return left + right

print(Some(1).zip_with(Some(2), add))  # Some(3)
```

---

## Opérateurs

`Option` surcharge `&` et `|` pour refléter `and_then` et `or_else`.

| Expression | Équivalent | Description |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Renvoie `b` lorsque `a` est `Some`, sinon `Nothing`. |
| `a & fn` | `a.and_then(lambda _: fn())` | Appelle `fn()` lorsque `a` est `Some`. |
| `a \| b` | `a.or_else(lambda: b)` | Renvoie `a` lorsque `Some`, sinon `b`. |
| `a \| fn` | `a.or_else(fn)` | Appelle `fn()` lorsque `a` est `Nothing`. |

```python
from pyfplib import Nothing, Some

print(Some(1) & Some(2))    # Some(2)
print(Nothing() & Some(2))  # Nothing()
print(Nothing() | Some(2))  # Some(2)
```

---

## Mutation

### `push(value: T) -> T`

Modifie l'option sur place : stocke `value` et renvoie la valeur précédemment contenue, ou `value` elle-même si l'option était vide.

```python
from pyfplib import Option, Some

option: Option[int] = Some(1)
previous = option.push(2)

print(previous)  # 1
print(option)    # Some(2)
```

---

## Erreurs

- `UnwrapError` — levée par `unwrap()` lorsque l'option est `Nothing`.
- `ExpectedError` — levée par `expect(message)` lorsque l'option est `Nothing`.

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
