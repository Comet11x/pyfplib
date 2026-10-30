# API Result

`Result[T, E]` представляет либо успех (`Ok`), либо ошибку (`Err`). Он находится в `pyfplib.result` и реэкспортируется из пакета `pyfplib` верхнего уровня.

```python
from pyfplib import Err, Ok, Result
```

---

## Конструкторы

### `Ok(value)`

Создаёт успешный результат.

```python
>>> Ok(42).is_ok()
True
>>> Ok(42).unwrap()
42
```

### `Err(error)`

Создаёт результат с ошибкой.

```python
>>> Err("boom").is_err()
True
>>> Err("boom").unwrap_err()
'boom'
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
>>> bool(Ok(1)), bool(Err("e"))
(True, False)
>>> Ok(1).ok()
Some(1)
>>> Err("e").ok()
Nothing()
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
>>> Ok(1).unwrap_or(0)
1
>>> Err("e").unwrap_or(0)
0
>>> Err("e").unwrap_or_else(lambda e: len(e))
1
```

---

## Преобразование

### `map(fn) -> Result[U, E]`

Применяет `fn` к значению `Ok`. `Err` возвращается без изменений.

```python
>>> Ok(2).map(lambda v: v * 3)
Ok(6)
>>> Err("e").map(lambda v: v * 3)
Err('e')
```

### `map_or(default, fn) -> Result[U, E]`

Применяет `fn` к значению `Ok` или использует `default`. Результат всегда `Ok`.

```python
>>> Ok(2).map_or(0, lambda v: v * 3)
Ok(6)
>>> Err("e").map_or(0, lambda v: v * 3)
Ok(0)
```

### `map_or_else(default, fn) -> U`

Применяет `fn` к значению `Ok` или вызывает `default(error)` для `Err`.

```python
>>> Ok(2).map_or_else(lambda e: 0, lambda v: v * 3)
6
>>> Err("e").map_or_else(lambda e: len(e), lambda v: v * 3)
3
```

### `map_err(fn) -> Result[T, U]`

Применяет `fn` к значению `Err`. `Ok` возвращается без изменений.

```python
>>> Err("boom").map_err(str.upper)
Err('BOOM')
>>> Ok(1).map_err(str.upper)
Ok(1)
```

### `flatten() -> Result[T, E]`

Схлопывает один уровень вложенности.

```python
>>> Ok(Ok(1)).flatten()
Ok(1)
>>> Ok(1).flatten()
Ok(1)
```

### `flatten_all() -> Result[T, E]`

Схлопывает все уровни вложенности.

```python
>>> Ok(Ok(Ok(1))).flatten_all()
Ok(1)
```

---

## Комбинирование

### `and_then(fn) -> Result[T, E]`

Выполняет `fn` только когда результат — `Ok`; иначе возвращает `Err` без изменений.

```python
>>> Ok(2).and_then(lambda v: Ok(v + 1))
Ok(3)
>>> Err("e").and_then(lambda v: Ok(v + 1))
Err('e')
```

### `or_else(fn) -> Result[T, E]`

Выполняет `fn` только когда результат — `Err`; иначе возвращает исходный `Ok`.

```python
>>> Err("e").or_else(lambda e: Ok(0))
Ok(0)
>>> Ok(1).or_else(lambda e: Ok(0))
Ok(1)
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
>>> Ok(1) & Ok(2)
Ok(2)
>>> Err("e") & Ok(2)
Err('e')
>>> Err("e") | Ok(2)
Ok(2)
```

---

## Обработка исключений

### `Result.try_call(fn, *args, **kwargs) -> Result[R, Exception]` *(статический)*

Вызывает `fn` и преобразует любое исключение в `Err`.

```python
>>> Result.try_call(int, "42")
Ok(42)
>>> Result.try_call(int, "oops").is_err()
True
```

---

## Ошибки

- `UnwrapError` — выбрасывается `unwrap()` и `unwrap_err()`, когда присутствует не тот вариант.
- `ExpectedError` — выбрасывается `expect()` и `expect_err()` с переданным сообщением.

```python
from pyfplib import Err
from pyfplib.errors import UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)
```
