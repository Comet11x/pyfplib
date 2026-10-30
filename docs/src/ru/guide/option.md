# API Option

`Option[T]` представляет значение, которое может присутствовать (`Some`) или отсутствовать (`Nothing`). Он находится в `pyfplib.option` и реэкспортируется из пакета `pyfplib` верхнего уровня.

```python
from pyfplib import Nothing, Option, Some
```

---

## Конструкторы

### `Some(value)`

Оборачивает значение в `Option`. У `Some` всегда `is_some()`.

```python
>>> Some(42).is_some()
True
>>> Some(42).unwrap()
42
```

### `Nothing()`

Создаёт пустой `Option`. У `Nothing` всегда `is_none()`.

```python
>>> Nothing().is_none()
True
>>> Nothing().unwrap_or(0)
0
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
>>> bool(Some(1)), bool(Nothing())
(True, False)
>>> Some(1) == Some(1)
True
```

### `inspect(fn) -> Option[T]`

Вызывает `fn` с содержащимся значением для `Some`, затем возвращает опцию без изменений.

```python
>>> Some(2).inspect(lambda v: print(v))
2
Some(2)
```

### `inspect_none(fn) -> Option[T]`

Вызывает `fn` без аргументов для `Nothing`, затем возвращает опцию без изменений.

```python
>>> Nothing().inspect_none(lambda: print("empty"))
empty
Nothing()
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
>>> Some(3).unwrap_or(0)
3
>>> Nothing().unwrap_or(0)
0
>>> Nothing().unwrap_or_else(lambda: 10)
10
```

---

## Преобразование

### `map(fn) -> Option[U]`

Применяет `fn` к содержащемуся значению, оборачивая результат в `Some`. `Nothing` остаётся `Nothing`.

```python
>>> Some(3).map(lambda v: v * 2)
Some(6)
>>> Nothing().map(lambda v: v * 2)
Nothing()
```

### `map_or(default, fn) -> Option[U]`

Применяет `fn` для `Some`, иначе использует `default`. Результат всегда оборачивается в `Some`.

```python
>>> Some(3).map_or(0, lambda v: v * 2)
Some(6)
>>> Nothing().map_or(0, lambda v: v * 2)
Some(0)
```

### `map_or_else(default, fn) -> U`

Применяет `fn` для `Some`, иначе вызывает `default()`.

```python
>>> Some(3).map_or_else(lambda: 0, lambda v: v * 2)
6
>>> Nothing().map_or_else(lambda: 0, lambda v: v * 2)
0
```

### `flatten() -> Option[T]`

Схлопывает один уровень вложенности.

```python
>>> Some(Some(1)).flatten()
Some(1)
>>> Some(1).flatten()
Some(1)
```

### `flatten_all() -> Option[T]`

Схлопывает все уровни вложенности.

```python
>>> Some(Some(Some(1))).flatten_all()
Some(1)
```

---

## Преобразование в Result

### `ok_or(err) -> Result[T, E]`

Преобразует `Option` в `Result`, используя `err`, когда опция пуста.

```python
>>> Some(1).ok_or("missing")
Ok(1)
>>> Nothing().ok_or("missing")
Err('missing')
```

### `ok_or_else(fn) -> Result[T, E]`

Как `ok_or`, но вызывает `fn()` для создания ошибки, когда опция пуста.

```python
>>> Nothing().ok_or_else(lambda: "missing")
Err('missing')
```

### `from_optional(value) -> Option[T]` *(статический)*

Создаёт `Option` из значения, которое может быть `None`.

```python
>>> Option.from_optional(None)
Nothing()
>>> Option.from_optional(5)
Some(5)
```

---

## Комбинирование

### `and_then(fn) -> Option[U]`

Выполняет `fn` только для `Some`; иначе возвращает `Nothing`.

```python
>>> Some(2).and_then(lambda v: Some(v + 1))
Some(3)
>>> Nothing().and_then(lambda v: Some(v + 1))
Nothing()
```

### `or_else(fn) -> Option[T]`

Выполняет `fn` только для `Nothing`; иначе возвращает исходную опцию.

```python
>>> Nothing().or_else(lambda: Some(9))
Some(9)
>>> Some(1).or_else(lambda: Some(9))
Some(1)
```

### `xor(other) -> Option[T]`

Возвращает значение, только когда ровно одна из двух опций — `Some`.

```python
>>> Some(1).xor(Nothing())
Some(1)
>>> Some(1).xor(Some(2))
Nothing()
```

### `zip(other) -> Option[tuple[T, U]]`

Объединяет значения в пару, когда обе опции — `Some`.

```python
>>> Some(1).zip(Some("a"))
Some((1, 'a'))
```

### `zip_with(other, ctr) -> Option[R]`

Объединяет оба значения с помощью `ctr`, когда обе опции — `Some`.

```python
>>> Some(1).zip_with(Some(2), lambda a, b: a + b)
Some(3)
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
>>> Some(1) & Some(2)
Some(2)
>>> Nothing() & Some(2)
Nothing()
>>> Nothing() | Some(2)
Some(2)
```

---

## Мутация

### `push(value) -> T`

Сохраняет `value` и возвращает предыдущее значение (или `value`, если опция была пуста).

```python
>>> opt = Some(1)
>>> opt.push(2)
1
>>> opt
Some(2)
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
    print(exc)
```
