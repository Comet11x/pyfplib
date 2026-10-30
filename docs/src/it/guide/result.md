# API Result

`Result[T, E]` rappresenta successo (`Ok`) o fallimento (`Err`). Si trova in `pyfplib.result` ed è riesportato dal pacchetto `pyfplib`.

```python
from pyfplib import Err, Ok, Result
```

---

## Costruttori

### `Ok(value: T)`

Crea un risultato di successo.

```python
from pyfplib import Ok, Result

result: Result[int, str] = Ok(42)
print(result.is_ok())  # True
print(result.unwrap()) # 42
```

### `Err(error: E)`

Crea un risultato di fallimento.

```python
from pyfplib import Err, Result

result: Result[int, str] = Err("boom")
print(result.is_err())           # True
print(repr(result.unwrap_err())) # 'boom'
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

## Pattern Matching

`Result` supporta il pattern matching strutturale di Python. Usa `Ok(value)` per associare un valore di successo e `Err(error)` per associare l'errore, senza chiamare prima `is_ok()`.

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

## Trasformazione

### `map(fn: Callable[[T], U]) -> Result[U, E]`

Applica `fn` al valore `Ok`. `Err` viene restituito invariato.

```python
from pyfplib import Err, Ok

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map(triple))    # Ok(6)
print(Err("e").map(triple)) # Err('e')
```

### `map_or(default: T, fn: Callable[[T], U]) -> Result[U, E]`

Applica `fn` al valore `Ok` o a `default` quando il risultato è `Err`. Il risultato è sempre `Ok`. Usa `map_or_else` quando ti serve il valore semplice.

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

Applica `fn` al valore `Ok`, oppure chiama `default(error)` su `Err` e applica `fn` a quel valore di fallback, restituendo il valore semplice.

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

Applica `fn` al valore `Err`. `Ok` viene restituito invariato.

```python
from pyfplib import Err, Ok

print(Err("boom").map_err(str.upper))  # Err('BOOM')
print(Ok(1).map_err(str.upper))        # Ok(1)
```

### `flatten() -> Result[T, E]`

Riduce di un livello l'annidamento. Un risultato non annidato viene restituito invariato.

```python
from pyfplib import Ok

print(Ok(Ok(1)).flatten())  # Ok(1)
print(Ok(1).flatten())      # Ok(1)
```

### `flatten_all() -> Result[T, E]`

Riduce tutti i livelli di annidamento fino a raggiungere il valore non-`Result` più interno.

```python
from pyfplib import Ok

print(Ok(Ok(Ok(1))).flatten_all())  # Ok(1)
```

---

## Combinazione

### `and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]`

Esegue `fn` solo quando il risultato è `Ok`; altrimenti restituisce `Err` invariato.

```python
from pyfplib import Err, Ok, Result

def increment(value: int) -> Result[int, str]:
    return Ok(value + 1)

print(Ok(2).and_then(increment))    # Ok(3)
print(Err("e").and_then(increment)) # Err('e')
```

### `or_else(fn: Callable[[E], Result[T, E]]) -> Result[T, E]`

Esegue `fn` solo quando il risultato è `Err`; altrimenti restituisce l'`Ok` originale.

```python
from pyfplib import Err, Ok, Result

def recover(error: str) -> Result[int, str]:
    return Ok(0)

print(Err("e").or_else(recover))  # Ok(0)
print(Ok(1).or_else(recover))     # Ok(1)
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
from pyfplib import Err, Ok

print(Ok(1) & Ok(2))    # Ok(2)
print(Err("e") & Ok(2)) # Err('e')
print(Err("e") | Ok(2)) # Ok(2)
```

---

## Gestione delle eccezioni

### `Result.try_call(fn: Callable[..., R], *args, **kwargs) -> Result[R, Exception]` *(statico)*

Chiama `fn` con gli argomenti forniti e converte qualsiasi `Exception` sollevata in un `Err`.

```python
from pyfplib import Result

print(Result.try_call(int, "42"))            # Ok(42)
print(Result.try_call(int, "oops").is_err()) # True
```

---

## Errori

- `UnwrapError` — sollevata da `unwrap()` e `unwrap_err()` quando è presente la variante sbagliata.
- `ExpectedError` — sollevata da `expect()` e `expect_err()` con il messaggio fornito.

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
