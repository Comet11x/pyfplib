# API Result

`Result[T, E]` rappresenta successo (`Ok`) o fallimento (`Err`). Si trova in `pyfplib.result` ed è riesportato dal pacchetto `pyfplib`.

```python
from pyfplib import Err, Ok, Result
```

---

## Costruttori

### `Ok(value)`

Crea un risultato di successo.

```python
>>> Ok(42).is_ok()
True
>>> Ok(42).unwrap()
42
```

### `Err(error)`

Crea un risultato di fallimento.

```python
>>> Err("boom").is_err()
True
>>> Err("boom").unwrap_err()
'boom'
```

---

## Ispezione

| Metodo | Restituisce | Descrizione |
|---|---|---|
| `is_ok()` | `bool` | `True` quando il risultato è `Ok`. |
| `is_err()` | `bool` | `True` quando il risultato è `Err`. |
| `value` | `T \| E` | Il valore o l'errore contenuto. |
| `__bool__()` | `bool` | Vero per `Ok`, falso per `Err`. |
| `inspect(fn)` | `Result[T, E]` | Chiama `fn` con il valore `Ok`, restituisce `self`. |
| `inspect_err(fn)` | `Result[T, E]` | Chiama `fn` con il valore `Err`, restituisce `self`. |
| `ok()` | `Option[T]` | `Some(value)` per `Ok`, altrimenti `Nothing()`. |
| `err()` | `Option[E]` | `Some(error)` per `Err`, altrimenti `Nothing()`. |

```python
>>> bool(Ok(1)), bool(Err("e"))
(True, False)
>>> Ok(1).ok()
Some(1)
>>> Err("e").ok()
Nothing()
```

---

## Estrazione

| Metodo | Restituisce | Eccezione | Descrizione |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Restituisce il valore `Ok` o solleva su `Err`. |
| `unwrap_err()` | `E` | `UnwrapError` | Restituisce il valore `Err` o solleva su `Ok`. |
| `expect(message)` | `T` | `ExpectedError` | Restituisce il valore `Ok` o solleva con `message`. |
| `expect_err(message)` | `E` | `ExpectedError` | Restituisce il valore `Err` o solleva con `message`. |
| `unwrap_or(default)` | `T` | — | Restituisce il valore `Ok` o `default`. |
| `unwrap_or_else(fn)` | `T` | — | Restituisce il valore `Ok` o `fn(error)`. |
| `unwrap_err_or(default)` | `E` | — | Restituisce il valore `Err` o `default`. |

```python
>>> Ok(1).unwrap_or(0)
1
>>> Err("e").unwrap_or(0)
0
>>> Err("e").unwrap_or_else(lambda e: len(e))
1
```

---

## Trasformazione

### `map(fn) -> Result[U, E]`

Applica `fn` al valore `Ok`. `Err` viene restituito invariato.

```python
>>> Ok(2).map(lambda v: v * 3)
Ok(6)
>>> Err("e").map(lambda v: v * 3)
Err('e')
```

### `map_or(default, fn) -> Result[U, E]`

Applica `fn` al valore `Ok` o usa `default`. Il risultato è sempre `Ok`.

```python
>>> Ok(2).map_or(0, lambda v: v * 3)
Ok(6)
>>> Err("e").map_or(0, lambda v: v * 3)
Ok(0)
```

### `map_or_else(default, fn) -> U`

Applica `fn` al valore `Ok`, oppure chiama `default(error)` su `Err`.

```python
>>> Ok(2).map_or_else(lambda e: 0, lambda v: v * 3)
6
>>> Err("e").map_or_else(lambda e: len(e), lambda v: v * 3)
3
```

### `map_err(fn) -> Result[T, U]`

Applica `fn` al valore `Err`. `Ok` viene restituito invariato.

```python
>>> Err("boom").map_err(str.upper)
Err('BOOM')
>>> Ok(1).map_err(str.upper)
Ok(1)
```

### `flatten() -> Result[T, E]`

Appiattisce un livello di annidamento.

```python
>>> Ok(Ok(1)).flatten()
Ok(1)
>>> Ok(1).flatten()
Ok(1)
```

### `flatten_all() -> Result[T, E]`

Appiattisce tutti i livelli di annidamento.

```python
>>> Ok(Ok(Ok(1))).flatten_all()
Ok(1)
```

---

## Combinazione

### `and_then(fn) -> Result[T, E]`

Esegue `fn` solo quando il risultato è `Ok`; altrimenti restituisce `Err` invariato.

```python
>>> Ok(2).and_then(lambda v: Ok(v + 1))
Ok(3)
>>> Err("e").and_then(lambda v: Ok(v + 1))
Err('e')
```

### `or_else(fn) -> Result[T, E]`

Esegue `fn` solo quando il risultato è `Err`; altrimenti restituisce l'`Ok` originale.

```python
>>> Err("e").or_else(lambda e: Ok(0))
Ok(0)
>>> Ok(1).or_else(lambda e: Ok(0))
Ok(1)
```

---

## Operatori

`Result` sovraccarica `&` e `|` per rispecchiare `and_then` e `or_else`.

| Espressione | Equivalente | Descrizione |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Restituisce `b` quando `a` è `Ok`, altrimenti `Err`. |
| `a & fn` | `a.and_then(lambda v: fn(v))` | Chiama `fn(value)` quando `a` è `Ok`. |
| `a \| b` | `a.or_else(lambda _: b)` | Restituisce `a` quando è `Ok`, altrimenti `b`. |
| `a \| fn` | `a.or_else(lambda e: fn(e))` | Chiama `fn(error)` quando `a` è `Err`. |

```python
>>> Ok(1) & Ok(2)
Ok(2)
>>> Err("e") & Ok(2)
Err('e')
>>> Err("e") | Ok(2)
Ok(2)
```

---

## Gestione delle eccezioni

### `Result.try_call(fn, *args, **kwargs) -> Result[R, Exception]` *(statico)*

Chiama `fn` e converte qualsiasi eccezione sollevata in un `Err`.

```python
>>> Result.try_call(int, "42")
Ok(42)
>>> Result.try_call(int, "oops").is_err()
True
```

---

## Errori

- `UnwrapError` — sollevata da `unwrap()` e `unwrap_err()` quando è presente la variante sbagliata.
- `ExpectedError` — sollevata da `expect()` e `expect_err()` con il messaggio fornito.

```python
from pyfplib import Err
from pyfplib.errors import UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)
```
