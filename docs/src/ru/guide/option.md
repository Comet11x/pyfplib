# API Option

`Option[T]` представляет значение, которое может присутствовать (`Some`) или отсутствовать (`Nothing`). Он находится в `pyfplib.option` и реэкспортируется из пакета `pyfplib` верхнего уровня.

```python
from pyfplib import Nothing, Option, Some
```

---

## Конструкторы

### `Some(value: T)`

Оборачивает значение, отличное от `None`, в `Option`. Поскольку внутри `Option` использует `None` для обозначения отсутствия, `Some(None)` ведёт себя как `Nothing()`.

```python
from pyfplib import Some

print(Some(42).is_some())    # True
print(Some(42).unwrap())     # 42
print(Some(None).is_none())  # True
```

### `Nothing()`

Создаёт пустой `Option`. У `Nothing` всегда `is_none()`.

```python
from pyfplib import Nothing

print(Nothing().is_none())     # True
print(Nothing().unwrap_or(0))  # 0
```

---

## Инспекция

| Метод | Возвращает | Описание |
|---|---|---|
| `is_some()` | `bool` | `True`, когда значение присутствует. |
| `is_none()` | `bool` | `True`, когда значения нет. |
| `value` | `T \| None` | Сырое содержащееся значение (может быть `None`). |
| `__bool__()` | `bool` | Истинно для `Some`, ложно для `Nothing`. |
| `__eq__(other)` | `bool` | Сравнивает содержащиеся значения, если оба — `Option`. |
| `__hash__()` | `int` | Хеширует содержащееся значение. |

```python
from pyfplib import Nothing, Some

print(bool(Some(1)), bool(Nothing()))  # (True, False)
print(Some(1) == Some(1))              # True
```

### `inspect(fn: Callable[[T], None]) -> Option[T]`

Вызывает `fn` с содержащимся значением для `Some`, затем возвращает опцию без изменений.

```python
from pyfplib import Option, Some

option: Option[int] = Some(2)
returned = option.inspect(lambda value: print(f"inspected: {value}"))
print(returned)  # Some(2)
```

### `inspect_none(fn: Callable[[], None]) -> Option[T]`

Вызывает `fn` без аргументов для `Nothing`, затем возвращает опцию без изменений.

```python
from pyfplib import Nothing

returned = Nothing().inspect_none(lambda: print("empty"))
print(returned)  # Nothing()
```

---

## Извлечение

| Метод | Возвращает | Исключение | Описание |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Возвращает значение или выбрасывает исключение, если опция пуста. |
| `expect(message)` | `T` | `ExpectedError` | Возвращает значение или выбрасывает исключение с `message`. |
| `unwrap_or(default)` | `T` | — | Возвращает значение или `default`. |
| `unwrap_or_else(fn)` | `T` | — | Возвращает значение или вызывает `fn()` для запасного значения. |

```python
from pyfplib import Nothing, Some

def fallback() -> int:
    return 10

print(Some(3).unwrap_or(0))               # 3
print(Nothing().unwrap_or(0))             # 0
print(Some(3).unwrap_or_else(fallback))   # 3
print(Nothing().unwrap_or_else(fallback)) # 10
```

---

## Сопоставление с образцом

`Option` поддерживает структурное сопоставление с образцом в Python. Используйте `Some(value)`, чтобы связать содержащееся значение, и `Nothing()` для пустого option — без предварительного вызова `is_some()`.

```python
from pyfplib import Nothing, Option, Some

def describe(option: Option[int]) -> str:
    match option:
        case Some(value):
            return f"got {value}"
        case Nothing():
            return "nothing"

print(describe(Some(42)))   # got 42
print(describe(Nothing()))  # nothing
```

---

## Преобразование

### `map(fn: Callable[[T], U]) -> Option[U]`

Применяет `fn` к содержащемуся значению, оборачивая результат в `Some`. `Nothing` остаётся `Nothing`.

```python
from pyfplib import Nothing, Some

def double(value: int) -> int:
    return value * 2

print(Some(3).map(double))    # Some(6)
print(Nothing().map(double))  # Nothing()
```

### `map_or(default: U, fn: Callable[[T], U]) -> Option[U]`

Применяет `fn` к значению `Some` или использует `default`; всегда возвращает `Option` (`Some`). Используйте `map_or_else`, если нужно получить обычное значение.

```python
from pyfplib import Nothing, Option, Some

def double(value: int) -> int:
    return value * 2

present: Option[int] = Some(3)
empty: Option[int] = Nothing()

print(present.map_or(0, double))  # Some(6)
print(empty.map_or(0, double))    # Some(0)
```

### `map_or_else(default: Callable[[], U], fn: Callable[[T], U]) -> U`

Применяет `fn` для `Some`, иначе вызывает `default()`.

```python
from pyfplib import Nothing, Some

def default() -> int:
    return 0

def double(value: int) -> int:
    return value * 2

print(Some(3).map_or_else(default, double))   # 6
print(Nothing().map_or_else(default, double)) # 0
```

### `flatten() -> Option[T]`

Схлопывает один уровень вложенности. Опция без вложенности возвращается без изменений.

```python
from pyfplib import Some

print(Some(Some(1)).flatten())  # Some(1)
print(Some(1).flatten())        # Some(1)
```

### `flatten_all() -> Option[T]`

Схлопывает все уровни вложенности, пока не будет достигнуто самое внутреннее неопциональное значение.

```python
from pyfplib import Some

print(Some(Some(Some(1))).flatten_all())  # Some(1)
```

---

## Преобразование в Result

### `ok_or(err: E) -> Result[T, E]`

Преобразует `Option` в `Result`, используя `err`, когда опция пуста.

```python
from pyfplib import Nothing, Some

print(Some(1).ok_or("missing"))   # Ok(1)
print(Nothing().ok_or("missing")) # Err('missing')
```

### `ok_or_else(fn: Callable[[], E]) -> Result[T, E]`

Как `ok_or`, но вызывает `fn()` для создания ошибки, когда опция пуста.

```python
from pyfplib import Nothing

def missing_error() -> str:
    return "missing"

print(Nothing().ok_or_else(missing_error))  # Err('missing')
```

### `from_optional(value: T | None) -> Option[T]` *(статический)*

Создаёт `Option` из значения, которое может быть `None`: `None` превращается в `Nothing`, а любое другое значение — в `Some`.

```python
from pyfplib import Option

value: int | None = None
print(Option.from_optional(value))  # Nothing()
print(Option.from_optional(5))      # Some(5)
```

---

## Комбинирование

### `and_then(fn: Callable[[T], Option[U]]) -> Option[U]`

Выполняет `fn` только для `Some`; иначе возвращает `Nothing`.

```python
from pyfplib import Nothing, Option, Some

def increment(value: int) -> Option[int]:
    return Some(value + 1)

print(Some(2).and_then(increment))   # Some(3)
print(Nothing().and_then(increment)) # Nothing()
```

### `or_else(fn: Callable[[], Option[T]]) -> Option[T]`

Выполняет `fn` только для `Nothing`; иначе возвращает исходную опцию.

```python
from pyfplib import Nothing, Option, Some

def recover() -> Option[int]:
    return Some(9)

print(Nothing().or_else(recover))  # Some(9)
print(Some(1).or_else(recover))    # Some(1)
```

### `xor(other: Option[T]) -> Option[T]`

Возвращает значение, только когда ровно одна из двух опций — `Some`.

```python
from pyfplib import Nothing, Some

print(Some(1).xor(Nothing()))  # Some(1)
print(Some(1).xor(Some(2)))    # Nothing()
```

### `zip(other: Option[U]) -> Option[tuple[T, U]]`

Объединяет значения в пару, когда обе опции — `Some`.

```python
from pyfplib import Some

print(Some(1).zip(Some("a")))  # Some((1, 'a'))
```

### `zip_with(other: Option[U], ctr: Callable[[T, U], R]) -> Option[R]`

Объединяет оба значения с помощью `ctr`, когда обе опции — `Some`.

```python
from pyfplib import Some

def add(left: int, right: int) -> int:
    return left + right

print(Some(1).zip_with(Some(2), add))  # Some(3)
```

---

## Операторы

`Option` перегружает `&` и `|`, повторяя `and_then` и `or_else`.

| Выражение | Эквивалент | Описание |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Возвращает `b`, когда `a` — `Some`, иначе `Nothing`. |
| `a & fn` | `a.and_then(lambda _: fn())` | Вызывает `fn()`, когда `a` — `Some`. |
| `a \| b` | `a.or_else(lambda: b)` | Возвращает `a`, когда `Some`, иначе `b`. |
| `a \| fn` | `a.or_else(fn)` | Вызывает `fn()`, когда `a` — `Nothing`. |

```python
from pyfplib import Nothing, Some

print(Some(1) & Some(2))    # Some(2)
print(Nothing() & Some(2))  # Nothing()
print(Nothing() | Some(2))  # Some(2)
```

---

## Мутация

### `push(value: T) -> T`

Изменяет опцию на месте: сохраняет `value` и возвращает предыдущее значение или сам `value`, если опция была пуста.

```python
from pyfplib import Option, Some

option: Option[int] = Some(1)
previous = option.push(2)

print(previous)  # 1
print(option)    # Some(2)
```

---

## Ошибки

- `UnwrapError` — выбрасывается `unwrap()`, когда опция — `Nothing`.
- `ExpectedError` — выбрасывается `expect(message)`, когда опция — `Nothing`.

```python
from pyfplib import Nothing
from pyfplib.errors import ExpectedError, UnwrapError

try:
    Nothing().unwrap()
except UnwrapError as exc:
    print(exc)  # called `Option.unwrap()` on a `Nothing` value

try:
    Nothing().expect("value is required")
except ExpectedError as exc:
    print(exc)  # value is required
```
