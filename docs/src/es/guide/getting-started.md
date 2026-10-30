# Primeros Pasos

## Instalación

```bash
pip install -U pyfplib
```

pyfplib no tiene dependencias de tiempo de ejecución y es compatible con Python 3.12 y superior.

## Option

Usa `Option` cuando un valor puede faltar. `Some` envuelve un valor y `Nothing` representa su ausencia.

```python
from pyfplib import Nothing, Some

user = Some({"name": "Ada", "email": "ada@example.com"})

email = user.map(lambda u: u.get("email")).unwrap_or("unknown")
print(email)  # ada@example.com

missing = Nothing()
print(missing.unwrap_or("unknown"))  # unknown
```

## Result

Usa `Result` para modelar operaciones que pueden fallar sin propagar excepciones a través de los límites de la API.

```python
from pyfplib import Err, Ok, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

print(divide(10, 2).unwrap())                 # 5.0
print(divide(10, 0).unwrap_or(float("nan")))  # nan

# Convierte excepciones en un valor Err
parsed = Result.try_call(int, "not a number")
print(parsed.is_err())  # True
```

## Ayudantes funcionales

El módulo `functools` contiene pequeños ayudantes para operaciones comunes con secuencias.

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

## Siguientes pasos

- [API de Option](/es/guide/option) — referencia completa de `Some`, `Nothing` y `Option`
- [API de Result](/es/guide/result) — referencia completa de `Ok`, `Err` y `Result`
- [API de Funciones](/es/guide/functools) — referencia completa de los ayudantes de secuencia
