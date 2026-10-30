# API Result

`Result[T, E]` представляет либо успех (`Ok`), либо ошибку (`Err`). Он находится в `pyfplib.result` и реэкспортируется из пакета `pyfplib` верхнего уровня.

```python
from pyfplib import Err, Ok, Result
```

---

## Конструкторы

### `Ok(value: T)`

Создаёт успешный результат.

```python
from pyfplib import Ok, Result

result: Result[int, str] = Ok(42)
print(result.is_ok())  # True
print(result.unwrap()) # 42
```

### `Err(error: E)`

Создаёт результат с ошибкой.

```python
from pyfplib import Err, Result

result: Result[int, str] = Err("boom")
print(result.is_err())           # True
print(repr(result.unwrap_err())) # 'boom'
```

---

## Инспекция

| Метод | Возвращает | Описание |
|---|---|---|
| `is_ok()` | `bool` | `True`, когда результат — `Ok`. |
| `is_err()` | `bool` | `True`, когда результат — `Err`. |
| `value` | `T \| E` | Содержащееся значение или ошибка. |
| `__bool__()` | `bool` | Истинно для `Ok`, ложно для `Err`. |
| `inspect(fn)` | `Result[T, E]` | Вызывает `fn` со значением `Ok`, возвращает `self`. |
| `inspect_err(fn)` | `Result[T, E]` | Вызывает `fn` со значением `Err`, возвращает `self`. |
| `ok()` | `Option[T]` | `Some(value)` для `Ok`, иначе `Nothing()`. |
| `err()` | `Option[E]` | `Some(error)` для `Err`, иначе `Nothing()`. |

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

## Извлечение

| Метод | Возвращает | Исключение | Описание |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Возвращает значение `Ok` или выбрасывает исключение для `Err`. |
| `unwrap_err()` | `E` | `UnwrapError` | Возвращает значение `Err` или выбрасывает исключение для `Ok`. |
| `expect(message)` | `T` | `ExpectedError` | Возвращает значение `Ok` или выбрасывает исключение с `message`. |
| `expect_err(message)` | `E` | `ExpectedError` | Возвращает значение `Err` или выбрасывает исключение с `message`. |
| `unwrap_or(default)` | `T` | — | Возвращает значение `Ok` или `default`. |
| `unwrap_or_else(fn)` | `T` | — | Возвращает значение `Ok` или `fn(error)`. |
| `unwrap_err_or(default)` | `E` | — | Возвращает значение `Err` или `default`. |

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

## Сопоставление с образцом

`Result` поддерживает структурное сопоставление с образцом в Python. Используйте `Ok(value)`, чтобы связать успешное значение, и `Err(error)` для ошибки — без предварительного вызова `is_ok()`.

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

## Преобразование

### `map(fn: Callable[[T], U]) -> Result[U, E]`

Применяет `fn` к значению `Ok`. `Err` возвращается без изменений.

```python
from pyfplib import Err, Ok

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map(triple))    # Ok(6)
print(Err("e").map(triple)) # Err('e')
```

### `map_or(default: T, fn: Callable[[T], U]) -> Result[U, E]`

Применяет `fn` к значению `Ok` или к `default`, если результат — `Err`. Результат всегда `Ok`. Используйте `map_or_else`, если нужно получить обычное значение.

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

Применяет `fn` к значению `Ok` или вызывает `default(error)` для `Err` и применяет `fn` к этому запасному значению, возвращая обычное значение.

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

Применяет `fn` к значению `Err`. `Ok` возвращается без изменений.

```python
from pyfplib import Err, Ok

print(Err("boom").map_err(str.upper))  # Err('BOOM')
print(Ok(1).map_err(str.upper))        # Ok(1)
```

### `flatten() -> Result[T, E]`

Схлопывает один уровень вложенности. Результат без вложенности возвращается без изменений.

```python
from pyfplib import Ok

print(Ok(Ok(1)).flatten())  # Ok(1)
print(Ok(1).flatten())      # Ok(1)
```

### `flatten_all() -> Result[T, E]`

Схлопывает все уровни вложенности, пока не будет достигнуто самое внутреннее не-`Result` значение.

```python
from pyfplib import Ok

print(Ok(Ok(Ok(1))).flatten_all())  # Ok(1)
```

---

## Комбинирование

### `and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]`

Выполняет `fn` только когда результат — `Ok`; иначе возвращает `Err` без изменений.

```python
from pyfplib import Err, Ok, Result

def increment(value: int) -> Result[int, str]:
    return Ok(value + 1)

print(Ok(2).and_then(increment))    # Ok(3)
print(Err("e").and_then(increment)) # Err('e')
```

### `or_else(fn: Callable[[E], Result[T, E]]) -> Result[T, E]`

Выполняет `fn` только когда результат — `Err`; иначе возвращает исходный `Ok`.

```python
from pyfplib import Err, Ok, Result

def recover(error: str) -> Result[int, str]:
    return Ok(0)

print(Err("e").or_else(recover))  # Ok(0)
print(Ok(1).or_else(recover))     # Ok(1)
```

---

## Операторы

`Result` перегружает `&` и `|`, повторяя `and_then` и `or_else`.

| Выражение | Эквивалент | Описание |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Возвращает `b`, когда `a` — `Ok`, иначе `Err`. |
| `a & fn` | `a.and_then(lambda v: fn(v))` | Вызывает `fn(value)`, когда `a` — `Ok`. |
| `a \| b` | `a.or_else(lambda _: b)` | Возвращает `a`, когда `Ok`, иначе `b`. |
| `a \| fn` | `a.or_else(lambda e: fn(e))` | Вызывает `fn(error)`, когда `a` — `Err`. |

```python
from pyfplib import Err, Ok

print(Ok(1) & Ok(2))    # Ok(2)
print(Err("e") & Ok(2)) # Err('e')
print(Err("e") | Ok(2)) # Ok(2)
```

---

## Обработка исключений

### `Result.try_call(fn: Callable[..., R], *args, **kwargs) -> Result[R, Exception]` *(статический)*

Вызывает `fn` с переданными аргументами и преобразует любое возникшее исключение `Exception` в `Err`.

```python
from pyfplib import Result

print(Result.try_call(int, "42"))            # Ok(42)
print(Result.try_call(int, "oops").is_err()) # True
```

---

## Ошибки

- `UnwrapError` — выбрасывается `unwrap()` и `unwrap_err()`, когда присутствует не тот вариант.
- `ExpectedError` — выбрасывается `expect()` и `expect_err()` с переданным сообщением.

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
