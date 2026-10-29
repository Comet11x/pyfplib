# Primeiros Passos

## Instalação

```bash
pip install -U pyfplib
```

O pyfplib não tem dependências de runtime e suporta Python 3.12 e superior.

## Option

Use `Option` quando um valor pode estar ausente. `Some` envolve um valor e `Nothing` representa sua ausência.

```python
from pyfplib import Nothing, Some

user = Some({"name": "Ada", "email": "ada@example.com"})

email = user.map(lambda u: u.get("email")).unwrap_or("unknown")
print(email)  # ada@example.com

missing = Nothing()
print(missing.unwrap_or("unknown"))  # unknown
```

## Result

Use `Result` para modelar operações que podem falhar sem propagar exceções pelas fronteiras da API.

```python
from pyfplib import Err, Ok, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

print(divide(10, 2).unwrap())                 # 5.0
print(divide(10, 0).unwrap_or(float("nan")))  # nan

# Converte exceções em um valor Err
parsed = Result.try_call(int, "not a number")
print(parsed.is_err())  # True
```

## Auxiliares funcionais

O módulo `functools` contém pequenos auxiliares para operações comuns em sequências.

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

## Próximos passos

- [API de Option](/pt/guide/option) — referência completa para `Some`, `Nothing` e `Option`
- [API de Result](/pt/guide/result) — referência completa para `Ok`, `Err` e `Result`
- [API de Funções](/pt/guide/functools) — referência completa para os auxiliares de sequência
