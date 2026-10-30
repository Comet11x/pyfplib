# Option API

`Option[T]`는 존재할 수 있는 값(`Some`) 또는 없는 값(`Nothing`)을 나타냅니다. `pyfplib.option`에 있으며 최상위 `pyfplib` 패키지에서 다시 내보냅니다.

```python
from pyfplib import Nothing, Option, Some
```

---

## 생성자

### `Some(value: T)`

`None`이 아닌 값을 `Option`으로 감쌉니다. `Option`은 내부적으로 `None`을 부재를 나타내는 값으로 사용하므로 `Some(None)`은 `Nothing()`처럼 동작합니다.

```python
from pyfplib import Some

print(Some(42).is_some())    # True
print(Some(42).unwrap())     # 42
print(Some(None).is_none())  # True
```

### `Nothing()`

빈 `Option`을 만듭니다. `Nothing`은 항상 `is_none()`입니다.

```python
from pyfplib import Nothing

print(Nothing().is_none())     # True
print(Nothing().unwrap_or(0))  # 0
```

---

## 검사

| 메서드 | 반환 | 설명 |
|---|---|---|
| `is_some()` | `bool` | 값이 있으면 `True`. |
| `is_none()` | `bool` | 값이 없으면 `True`. |
| `value` | `T \| None` | 포함된 원시 값(`None`일 수 있음). |
| `__bool__()` | `bool` | `Some`이면 참, `Nothing`이면 거짓. |
| `__eq__(other)` | `bool` | 둘 다 `Option`이면 포함된 값을 비교합니다. |
| `__hash__()` | `int` | 포함된 값의 해시를 계산합니다. |

```python
from pyfplib import Nothing, Some

print(bool(Some(1)), bool(Nothing()))  # (True, False)
print(Some(1) == Some(1))              # True
```

### `inspect(fn: Callable[[T], None]) -> Option[T]`

`Some`일 때 포함된 값으로 `fn`을 호출한 뒤 옵션을 그대로 반환합니다.

```python
from pyfplib import Option, Some

option: Option[int] = Some(2)
returned = option.inspect(lambda value: print(f"inspected: {value}"))
print(returned)  # Some(2)
```

### `inspect_none(fn: Callable[[], None]) -> Option[T]`

`Nothing`일 때 인자 없이 `fn`을 호출한 뒤 옵션을 그대로 반환합니다.

```python
from pyfplib import Nothing

returned = Nothing().inspect_none(lambda: print("empty"))
print(returned)  # Nothing()
```

---

## 추출

| 메서드 | 반환 | 예외 | 설명 |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | 값을 반환하거나 비어 있으면 예외를 발생시킵니다. |
| `expect(message)` | `T` | `ExpectedError` | 값을 반환하거나 `message`와 함께 예외를 발생시킵니다. |
| `unwrap_or(default)` | `T` | — | 값을 반환하거나 `default`를 반환합니다. |
| `unwrap_or_else(fn)` | `T` | — | 값을 반환하거나 `fn()`을 호출해 대체 값을 얻습니다. |

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

## 패턴 매칭

`Option`은 Python의 구조적 패턴 매칭을 지원합니다. `Some(value)`로 포함된 값을 바인딩하고 `Nothing()`으로 빈 option을 일치시키며, 먼저 `is_some()`을 호출할 필요가 없습니다.

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

## 변환

### `map(fn: Callable[[T], U]) -> Option[U]`

포함된 값에 `fn`을 적용하고 결과를 `Some`으로 감쌉니다. `Nothing`은 `Nothing`으로 유지됩니다.

```python
from pyfplib import Nothing, Some

def double(value: int) -> int:
    return value * 2

print(Some(3).map(double))    # Some(6)
print(Nothing().map(double))  # Nothing()
```

### `map_or(default: U, fn: Callable[[T], U]) -> Option[U]`

`Some` 값에 `fn`을 적용하거나 `default`를 사용하며, 항상 `Option`(`Some`)을 반환합니다. 일반 값이 필요하면 `map_or_else`를 사용하세요.

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

`Some`이면 `fn`을 적용하고, 아니면 `default()`를 호출합니다.

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

중첩을 한 단계 줄입니다. 중첩되지 않은 옵션은 그대로 반환됩니다.

```python
from pyfplib import Some

print(Some(Some(1)).flatten())  # Some(1)
print(Some(1).flatten())        # Some(1)
```

### `flatten_all() -> Option[T]`

가장 안쪽의 옵션이 아닌 값에 도달할 때까지 모든 중첩 수준을 줄입니다.

```python
from pyfplib import Some

print(Some(Some(Some(1))).flatten_all())  # Some(1)
```

---

## Result로 변환

### `ok_or(err: E) -> Result[T, E]`

`Option`을 `Result`로 변환하며, 비어 있으면 `err`를 사용합니다.

```python
from pyfplib import Nothing, Some

print(Some(1).ok_or("missing"))   # Ok(1)
print(Nothing().ok_or("missing")) # Err('missing')
```

### `ok_or_else(fn: Callable[[], E]) -> Result[T, E]`

`ok_or`와 같지만 비어 있을 때 `fn()`을 호출해 오류를 만듭니다.

```python
from pyfplib import Nothing

def missing_error() -> str:
    return "missing"

print(Nothing().ok_or_else(missing_error))  # Err('missing')
```

### `from_optional(value: T | None) -> Option[T]` *(정적)*

`None`일 수 있는 값으로 `Option`을 만듭니다. `None`은 `Nothing`이 되고, 다른 값은 `Some`이 됩니다.

```python
from pyfplib import Option

value: int | None = None
print(Option.from_optional(value))  # Nothing()
print(Option.from_optional(5))      # Some(5)
```

---

## 결합

### `and_then(fn: Callable[[T], Option[U]]) -> Option[U]`

`Some`일 때만 `fn`을 실행하고, 아니면 `Nothing`을 반환합니다.

```python
from pyfplib import Nothing, Option, Some

def increment(value: int) -> Option[int]:
    return Some(value + 1)

print(Some(2).and_then(increment))   # Some(3)
print(Nothing().and_then(increment)) # Nothing()
```

### `or_else(fn: Callable[[], Option[T]]) -> Option[T]`

`Nothing`일 때만 `fn`을 실행하고, 아니면 원래 옵션을 반환합니다.

```python
from pyfplib import Nothing, Option, Some

def recover() -> Option[int]:
    return Some(9)

print(Nothing().or_else(recover))  # Some(9)
print(Some(1).or_else(recover))    # Some(1)
```

### `xor(other: Option[T]) -> Option[T]`

두 옵션 중 정확히 하나만 `Some`일 때 값을 반환합니다.

```python
from pyfplib import Nothing, Some

print(Some(1).xor(Nothing()))  # Some(1)
print(Some(1).xor(Some(2)))    # Nothing()
```

### `zip(other: Option[U]) -> Option[tuple[T, U]]`

두 옵션이 모두 `Some`일 때 값을 쌍으로 묶습니다.

```python
from pyfplib import Some

print(Some(1).zip(Some("a")))  # Some((1, 'a'))
```

### `zip_with(other: Option[U], ctr: Callable[[T, U], R]) -> Option[R]`

두 옵션이 모두 `Some`일 때 `ctr`로 두 값을 결합합니다.

```python
from pyfplib import Some

def add(left: int, right: int) -> int:
    return left + right

print(Some(1).zip_with(Some(2), add))  # Some(3)
```

---

## 연산자

`Option`은 `and_then`과 `or_else`를 반영하도록 `&`와 `|`를 오버로드합니다.

| 표현식 | 동등 | 설명 |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | `a`가 `Some`이면 `b`, 아니면 `Nothing`. |
| `a & fn` | `a.and_then(lambda _: fn())` | `a`가 `Some`이면 `fn()` 호출. |
| `a \| b` | `a.or_else(lambda: b)` | `a`가 `Some`이면 `a`, 아니면 `b`. |
| `a \| fn` | `a.or_else(fn)` | `a`가 `Nothing`이면 `fn()` 호출. |

```python
from pyfplib import Nothing, Some

print(Some(1) & Some(2))    # Some(2)
print(Nothing() & Some(2))  # Nothing()
print(Nothing() | Some(2))  # Some(2)
```

---

## 변경

### `push(value: T) -> T`

옵션을 제자리에서 변경합니다. `value`를 저장하고 이전에 보관하던 값을 반환하며, 옵션이 비어 있었다면 `value` 자체를 반환합니다.

```python
from pyfplib import Option, Some

option: Option[int] = Some(1)
previous = option.push(2)

print(previous)  # 1
print(option)    # Some(2)
```

---

## 오류

- `UnwrapError` — 옵션이 `Nothing`일 때 `unwrap()`이 발생시킵니다.
- `ExpectedError` — 옵션이 `Nothing`일 때 `expect(message)`가 발생시킵니다.

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
