# Erste Schritte

## Installation

```bash
pip install -U pyfplib
```

pyfplib hat keine Laufzeitabhängigkeiten und unterstützt Python 3.12 und neuer.

## Option

Verwenden Sie `Option`, wenn ein Wert fehlen kann. `Some` verpackt einen Wert, `Nothing` repräsentiert seine Abwesenheit.

```python
from pyfplib import Nothing, Some

user = Some({"name": "Ada", "email": "ada@example.com"})

email = user.map(lambda u: u.get("email")).unwrap_or("unknown")
print(email)  # ada@example.com

missing = Nothing()
print(missing.unwrap_or("unknown"))  # unknown
```

## Result

Verwenden Sie `Result`, um Operationen zu modellieren, die fehlschlagen können, ohne Ausnahmen über API-Grenzen hinweg zu werfen.

```python
from pyfplib import Err, Ok, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

print(divide(10, 2).unwrap())                 # 5.0
print(divide(10, 0).unwrap_or(float("nan")))  # nan

# Ausnahmen in einen Err-Wert umwandeln
parsed = Result.try_call(int, "not a number")
print(parsed.is_err())  # True
```

## Funktionale Helfer

Das Modul `functools` enthält kleine Helfer für häufige Sequenzoperationen.

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

## Wie geht es weiter?

- [Option-API](/de/guide/option) — vollständige Referenz zu `Some`, `Nothing` und `Option`
- [Result-API](/de/guide/result) — vollständige Referenz zu `Ok`, `Err` und `Result`
- [Funktions-API](/de/guide/functools) — vollständige Referenz zu den Sequenz-Helfern
