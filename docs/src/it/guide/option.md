# API Option

`Option[T]` rappresenta un valore che può essere presente (`Some`) o assente (`Nothing`). Si trova in `pyfplib.option` ed è riesportato dal pacchetto `pyfplib`.

```python
from pyfplib import Nothing, Option, Some
```

---

## Costruttori

### `Some(value)`

Avvolge un valore in un `Option`. Un `Some` è sempre `is_some()`.

```python
>>> Some(42).is_some()
True
>>> Some(42).unwrap()
42
```

### `Nothing()`

Crea un `Option` vuoto. Un `Nothing` è sempre `is_none()`.

```python
>>> Nothing().is_none()
True
>>> Nothing().unwrap_or(0)
0
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
>>> bool(Some(1)), bool(Nothing())
(True, False)
>>> Some(1) == Some(1)
True
```

### `inspect(fn) -> Option[T]`

Chiama `fn` con il valore contenuto quando è `Some`, poi restituisce l'opzione invariata.

```python
>>> Some(2).inspect(lambda v: print(v))
2
Some(2)
```

### `inspect_none(fn) -> Option[T]`

Chiama `fn` senza argomenti quando è `Nothing`, poi restituisce l'opzione invariata.

```python
>>> Nothing().inspect_none(lambda: print("empty"))
empty
Nothing()
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
>>> Some(3).unwrap_or(0)
3
>>> Nothing().unwrap_or(0)
0
>>> Nothing().unwrap_or_else(lambda: 10)
10
```

---

## Trasformazione

### `map(fn) -> Option[U]`

Applica `fn` al valore contenuto, avvolgendo il risultato in `Some`. `Nothing` resta `Nothing`.

```python
>>> Some(3).map(lambda v: v * 2)
Some(6)
>>> Nothing().map(lambda v: v * 2)
Nothing()
```

### `map_or(default, fn) -> Option[U]`

Applica `fn` quando è `Some`, altrimenti usa `default`. Il risultato è sempre avvolto in `Some`.

```python
>>> Some(3).map_or(0, lambda v: v * 2)
Some(6)
>>> Nothing().map_or(0, lambda v: v * 2)
Some(0)
```

### `map_or_else(default, fn) -> U`

Applica `fn` quando è `Some`, altrimenti chiama `default()`.

```python
>>> Some(3).map_or_else(lambda: 0, lambda v: v * 2)
6
>>> Nothing().map_or_else(lambda: 0, lambda v: v * 2)
0
```

### `flatten() -> Option[T]`

Appiattisce un livello di annidamento.

```python
>>> Some(Some(1)).flatten()
Some(1)
>>> Some(1).flatten()
Some(1)
```

### `flatten_all() -> Option[T]`

Appiattisce tutti i livelli di annidamento.

```python
>>> Some(Some(Some(1))).flatten_all()
Some(1)
```

---

## Conversione

### `ok_or(err) -> Result[T, E]`

Converte un `Option` in un `Result`, usando `err` quando è vuoto.

```python
>>> Some(1).ok_or("missing")
Ok(1)
>>> Nothing().ok_or("missing")
Err('missing')
```

### `ok_or_else(fn) -> Result[T, E]`

Come `ok_or`, ma chiama `fn()` per produrre l'errore quando è vuoto.

```python
>>> Nothing().ok_or_else(lambda: "missing")
Err('missing')
```

### `from_optional(value) -> Option[T]` *(statico)*

Costruisce un `Option` da un valore che può essere `None`.

```python
>>> Option.from_optional(None)
Nothing()
>>> Option.from_optional(5)
Some(5)
```

---

## Combinazione

### `and_then(fn) -> Option[U]`

Esegue `fn` solo quando è `Some`; altrimenti restituisce `Nothing`.

```python
>>> Some(2).and_then(lambda v: Some(v + 1))
Some(3)
>>> Nothing().and_then(lambda v: Some(v + 1))
Nothing()
```

### `or_else(fn) -> Option[T]`

Esegue `fn` solo quando è `Nothing`; altrimenti restituisce l'opzione originale.

```python
>>> Nothing().or_else(lambda: Some(9))
Some(9)
>>> Some(1).or_else(lambda: Some(9))
Some(1)
```

### `xor(other) -> Option[T]`

Restituisce un valore solo quando esattamente una delle due opzioni è `Some`.

```python
>>> Some(1).xor(Nothing())
Some(1)
>>> Some(1).xor(Some(2))
Nothing()
```

### `zip(other) -> Option[tuple[T, U]]`

Accoppia i valori quando entrambe le opzioni sono `Some`.

```python
>>> Some(1).zip(Some("a"))
Some((1, 'a'))
```

### `zip_with(other, ctr) -> Option[R]`

Combina entrambi i valori con `ctr` quando entrambe le opzioni sono `Some`.

```python
>>> Some(1).zip_with(Some(2), lambda a, b: a + b)
Some(3)
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
>>> Some(1) & Some(2)
Some(2)
>>> Nothing() & Some(2)
Nothing()
>>> Nothing() | Some(2)
Some(2)
```

---

## Mutazione

### `push(value) -> T`

Memorizza `value` e restituisce il valore precedente (o `value` se l'opzione era vuota).

```python
>>> opt = Some(1)
>>> opt.push(2)
1
>>> opt
Some(2)
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
    print(exc)
```
