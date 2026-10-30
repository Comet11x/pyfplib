# Pour Commencer

## Installation

```bash
pip install -U pyfplib
```

pyfplib n'a aucune dépendance d'exécution et prend en charge Python 3.12 et versions ultérieures.

## Option

Utilisez `Option` lorsqu'une valeur peut être absente. `Some` enveloppe une valeur, `Nothing` représente son absence.

```python
from pyfplib import Nothing, Some

user = Some({"name": "Ada", "email": "ada@example.com"})

email = user.map(lambda u: u.get("email")).unwrap_or("unknown")
print(email)  # ada@example.com

missing = Nothing()
print(missing.unwrap_or("unknown"))  # unknown
```

## Result

Utilisez `Result` pour modéliser les opérations pouvant échouer sans propager d'exceptions au-delà des frontières de l'API.

```python
from pyfplib import Err, Ok, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

print(divide(10, 2).unwrap())                 # 5.0
print(divide(10, 0).unwrap_or(float("nan")))  # nan

# Convertit les exceptions en valeur Err
parsed = Result.try_call(int, "not a number")
print(parsed.is_err())  # True
```

## Helpers fonctionnels

Le module `functools` contient de petits helpers pour les opérations courantes sur les séquences.

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

## Et ensuite ?

- [API Option](/fr/guide/option) — référence complète pour `Some`, `Nothing` et `Option`
- [API Result](/fr/guide/result) — référence complète pour `Ok`, `Err` et `Result`
- [API Fonctions](/fr/guide/functools) — référence complète pour les helpers de séquence
