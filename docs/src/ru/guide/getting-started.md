# Начало работы

## Установка

```bash
pip install -U pyfplib
```

pyfplib не имеет runtime-зависимостей и поддерживает Python 3.12 и новее.

## Option

Используйте `Option`, когда значения может не быть. `Some` оборачивает значение, а `Nothing` представляет его отсутствие.

```python
from pyfplib import Nothing, Some

user = Some({"name": "Ada", "email": "ada@example.com"})

email = user.map(lambda u: u.get("email")).unwrap_or("unknown")
print(email)  # ada@example.com

missing = Nothing()
print(missing.unwrap_or("unknown"))  # unknown
```

## Result

Используйте `Result`, чтобы моделировать операции, которые могут завершиться ошибкой, не выбрасывая исключения через границы API.

```python
from pyfplib import Err, Ok, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

print(divide(10, 2).unwrap())                 # 5.0
print(divide(10, 0).unwrap_or(float("nan")))  # nan

# Преобразование исключения в значение Err
parsed = Result.try_call(int, "not a number")
print(parsed.is_err())  # True
```

## Функциональные помощники

Модуль `functools` содержит небольшие помощники для типовых операций с последовательностями.

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

## Что дальше?

- [API Option](/ru/guide/option) — полный справочник по `Some`, `Nothing` и `Option`
- [API Result](/ru/guide/result) — полный справочник по `Ok`, `Err` и `Result`
- [API функций](/ru/guide/functools) — полный справочник по помощникам для последовательностей
