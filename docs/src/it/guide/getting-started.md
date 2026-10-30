# Per Iniziare

## Installazione

```bash
pip install -U pyfplib
```

pyfplib non ha dipendenze runtime e supporta Python 3.12 e versioni successive.

## Option

Usa `Option` quando un valore può mancare. `Some` avvolge un valore, `Nothing` ne rappresenta l'assenza.

```python
from pyfplib import Nothing, Some

user = Some({"name": "Ada", "email": "ada@example.com"})

email = user.map(lambda u: u.get("email")).unwrap_or("unknown")
print(email)  # ada@example.com

missing = Nothing()
print(missing.unwrap_or("unknown"))  # unknown
```

## Result

Usa `Result` per modellare operazioni che possono fallire senza propagare eccezioni oltre i confini dell'API.

```python
from pyfplib import Err, Ok, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

print(divide(10, 2).unwrap())                 # 5.0
print(divide(10, 0).unwrap_or(float("nan")))  # nan

# Converti le eccezioni in un valore Err
parsed = Result.try_call(int, "not a number")
print(parsed.is_err())  # True
```

## Helper funzionali

Il modulo `functools` contiene piccoli helper per le operazioni comuni sulle sequenze.

```python
from pyfplib import all_of, any_of, find, fold, head, tail
from pyfplib import Nothing, Some

numbers = [1, 2, 3, 4, 5]

print(head(numbers))                       # Some(1)
print(tail(numbers))                       # [2, 3, 4, 5]
print(any_of(lambda n: n > 4, numbers))    # True
print(all_of(lambda n: n > 0, numbers))    # True
print(find(lambda n: Some(n) if n % 2 == 0 else Nothing(), numbers))  # Some(2)

total = fold(lambda acc, n: acc.unwrap_or(0) + n, numbers, 0)
print(total)  # Some(15)
```

## Prossimi passi

- [API Option](/it/guide/option) — riferimento completo per `Some`, `Nothing` e `Option`
- [API Result](/it/guide/result) — riferimento completo per `Ok`, `Err` e `Result`
- [API Funzioni](/it/guide/functools) — riferimento completo per gli helper per sequenze
