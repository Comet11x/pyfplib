# API Option

`Option[T]` représente une valeur qui peut être présente (`Some`) ou absente (`Nothing`). Il se trouve dans `pyfplib.option` et est réexporté depuis le paquet `pyfplib`.

```python
from pyfplib import Nothing, Option, Some
```

---

## Constructeurs

### `Some(value)`

Enveloppe une valeur dans un `Option`. Un `Some` est toujours `is_some()`.

```python
>>> Some(42).is_some()
True
>>> Some(42).unwrap()
42
```

### `Nothing()`

Crée un `Option` vide. Un `Nothing` est toujours `is_none()`.

```python
>>> Nothing().is_none()
True
>>> Nothing().unwrap_or(0)
0
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
>>> bool(Some(1)), bool(Nothing())
(True, False)
>>> Some(1) == Some(1)
True
```

### `inspect(fn) -> Option[T]`

Appelle `fn` avec la valeur contenue lorsque l'option est `Some`, puis renvoie l'option inchangée.

```python
>>> Some(2).inspect(lambda v: print(v))
2
Some(2)
```

### `inspect_none(fn) -> Option[T]`

Appelle `fn` sans argument lorsque l'option est `Nothing`, puis renvoie l'option inchangée.

```python
>>> Nothing().inspect_none(lambda: print("empty"))
empty
Nothing()
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

Applique `fn` à la valeur contenue et enveloppe le résultat dans `Some`. `Nothing` reste `Nothing`.

```python
>>> Some(3).map(lambda v: v * 2)
Some(6)
>>> Nothing().map(lambda v: v * 2)
Nothing()
```

### `map_or(default, fn) -> Option[U]`

Applique `fn` lorsque l'option est `Some`, sinon utilise `default`. Le résultat est toujours enveloppé dans `Some`.

```python
>>> Some(3).map_or(0, lambda v: v * 2)
Some(6)
>>> Nothing().map_or(0, lambda v: v * 2)
Some(0)
```

### `map_or_else(default, fn) -> U`

Applique `fn` lorsque l'option est `Some`, sinon appelle `default()`.

```python
>>> Some(3).map_or_else(lambda: 0, lambda v: v * 2)
6
>>> Nothing().map_or_else(lambda: 0, lambda v: v * 2)
0
```

### `flatten() -> Option[T]`

Aplatit un niveau d'imbrication.

```python
>>> Some(Some(1)).flatten()
Some(1)
>>> Some(1).flatten()
Some(1)
```

### `flatten_all() -> Option[T]`

Aplatit tous les niveaux d'imbrication.

```python
>>> Some(Some(Some(1))).flatten_all()
Some(1)
```

---

## Conversion

### `ok_or(err) -> Result[T, E]`

Convertit un `Option` en `Result`, en utilisant `err` lorsque l'option est vide.

```python
>>> Some(1).ok_or("missing")
Ok(1)
>>> Nothing().ok_or("missing")
Err('missing')
```

### `ok_or_else(fn) -> Result[T, E]`

Comme `ok_or`, mais appelle `fn()` pour produire l'erreur lorsque l'option est vide.

```python
>>> Nothing().ok_or_else(lambda: "missing")
Err('missing')
```

### `from_optional(value) -> Option[T]` *(statique)*

Construit un `Option` à partir d'une valeur pouvant être `None`.

```python
>>> Option.from_optional(None)
Nothing()
>>> Option.from_optional(5)
Some(5)
```

---

## Combinaison

### `and_then(fn) -> Option[U]`

Exécute `fn` uniquement lorsque l'option est `Some` ; sinon renvoie `Nothing`.

```python
>>> Some(2).and_then(lambda v: Some(v + 1))
Some(3)
>>> Nothing().and_then(lambda v: Some(v + 1))
Nothing()
```

### `or_else(fn) -> Option[T]`

Exécute `fn` uniquement lorsque l'option est `Nothing` ; sinon renvoie l'option d'origine.

```python
>>> Nothing().or_else(lambda: Some(9))
Some(9)
>>> Some(1).or_else(lambda: Some(9))
Some(1)
```

### `xor(other) -> Option[T]`

Renvoie une valeur uniquement lorsque exactement l'une des deux options est `Some`.

```python
>>> Some(1).xor(Nothing())
Some(1)
>>> Some(1).xor(Some(2))
Nothing()
```

### `zip(other) -> Option[tuple[T, U]]`

Associe les valeurs lorsque les deux options sont `Some`.

```python
>>> Some(1).zip(Some("a"))
Some((1, 'a'))
```

### `zip_with(other, ctr) -> Option[R]`

Combine les deux valeurs avec `ctr` lorsque les deux options sont `Some`.

```python
>>> Some(1).zip_with(Some(2), lambda a, b: a + b)
Some(3)
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

Stocke `value` et renvoie la valeur précédemment contenue (ou `value` si l'option était vide).

```python
>>> opt = Some(1)
>>> opt.push(2)
1
>>> opt
Some(2)
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
    print(exc)
```
