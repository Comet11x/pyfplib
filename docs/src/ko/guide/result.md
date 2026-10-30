# Result API

`Result[T, E]`는 성공(`Ok`) 또는 실패(`Err`)를 나타냅니다. `pyfplib.result`에 있으며 최상위 `pyfplib` 패키지에서 다시 내보냅니다.

```python
from pyfplib import Err, Ok, Result
```

---

## 생성자

### `Ok(value: T)`

성공 결과를 만듭니다.

```python
from pyfplib import Ok, Result

result: Result[int, str] = Ok(42)
print(result.is_ok())  # True
print(result.unwrap()) # 42
```

### `Err(error: E)`

실패 결과를 만듭니다.

```python
from pyfplib import Err, Result

result: Result[int, str] = Err("boom")
print(result.is_err())           # True
print(repr(result.unwrap_err())) # 'boom'
```

---

## 검사

| 메서드 | 반환 | 설명 |
|---|---|---|
| `is_ok()` | `bool` | 결과가 `Ok`이면 `True`. |
| `is_err()` | `bool` | 결과가 `Err`이면 `True`. |
| `value` | `T \| E` | 포함된 값 또는 오류. |
| `__bool__()` | `bool` | `Ok`이면 참, `Err`이면 거짓. |
| `inspect(fn)` | `Result[T, E]` | `Ok` 값으로 `fn`을 호출하고 `self`를 반환합니다. |
| `inspect_err(fn)` | `Result[T, E]` | `Err` 값으로 `fn`을 호출하고 `self`를 반환합니다. |
| `ok()` | `Option[T]` | `Ok`이면 `Some(value)`, 아니면 `Nothing()`. |
| `err()` | `Option[E]` | `Err`이면 `Some(error)`, 아니면 `Nothing()`. |

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

## 추출

| 메서드 | 반환 | 예외 | 설명 |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | `Ok` 값을 반환하거나 `Err`이면 예외를 발생시킵니다. |
| `unwrap_err()` | `E` | `UnwrapError` | `Err` 값을 반환하거나 `Ok`이면 예외를 발생시킵니다. |
| `expect(message)` | `T` | `ExpectedError` | `Ok` 값을 반환하거나 `message`와 함께 예외를 발생시킵니다. |
| `expect_err(message)` | `E` | `ExpectedError` | `Err` 값을 반환하거나 `message`와 함께 예외를 발생시킵니다. |
| `unwrap_or(default)` | `T` | — | `Ok` 값 또는 `default`를 반환합니다. |
| `unwrap_or_else(fn)` | `T` | — | `Ok` 값 또는 `fn(error)`를 반환합니다. |
| `unwrap_err_or(default)` | `E` | — | `Err` 값 또는 `default`를 반환합니다. |

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

## 패턴 매칭

`Result`는 Python의 구조적 패턴 매칭을 지원합니다. `Ok(value)`로 성공 값을 바인딩하고 `Err(error)`로 오류를 바인딩하며, 먼저 `is_ok()`을 호출할 필요가 없습니다.

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

## 변환

### `map(fn: Callable[[T], U]) -> Result[U, E]`

`Ok` 값에 `fn`을 적용합니다. `Err`는 그대로 반환됩니다.

```python
from pyfplib import Err, Ok

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map(triple))    # Ok(6)
print(Err("e").map(triple)) # Err('e')
```

### `map_or(default: T, fn: Callable[[T], U]) -> Result[U, E]`

`Ok` 값에 `fn`을 적용하거나 결과가 `Err`이면 `default`에 `fn`을 적용합니다. 결과는 항상 `Ok`입니다. 일반 값이 필요하면 `map_or_else`를 사용하세요.

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

`Ok` 값에 `fn`을 적용하거나 `Err`에서 `default(error)`를 호출한 뒤 그 폴백 값에 `fn`을 적용하여 일반 값을 반환합니다.

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

`Err` 값에 `fn`을 적용합니다. `Ok`는 그대로 반환됩니다.

```python
from pyfplib import Err, Ok

print(Err("boom").map_err(str.upper))  # Err('BOOM')
print(Ok(1).map_err(str.upper))        # Ok(1)
```

### `flatten() -> Result[T, E]`

중첩을 한 단계 평탄화합니다. 중첩되지 않은 결과는 그대로 반환됩니다.

```python
from pyfplib import Ok

print(Ok(Ok(1)).flatten())  # Ok(1)
print(Ok(1).flatten())      # Ok(1)
```

### `flatten_all() -> Result[T, E]`

가장 안쪽의 비-`Result` 값에 도달할 때까지 모든 중첩 단계를 평탄화합니다.

```python
from pyfplib import Ok

print(Ok(Ok(Ok(1))).flatten_all())  # Ok(1)
```

---

## 결합

### `and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]`

결과가 `Ok`일 때만 `fn`을 실행하고, 아니면 `Err`를 그대로 반환합니다.

```python
from pyfplib import Err, Ok, Result

def increment(value: int) -> Result[int, str]:
    return Ok(value + 1)

print(Ok(2).and_then(increment))    # Ok(3)
print(Err("e").and_then(increment)) # Err('e')
```

### `or_else(fn: Callable[[E], Result[T, E]]) -> Result[T, E]`

결과가 `Err`일 때만 `fn`을 실행하고, 아니면 원래 `Ok`를 반환합니다.

```python
from pyfplib import Err, Ok, Result

def recover(error: str) -> Result[int, str]:
    return Ok(0)

print(Err("e").or_else(recover))  # Ok(0)
print(Ok(1).or_else(recover))     # Ok(1)
```

---

## 연산자

`Result`는 `and_then`과 `or_else`를 반영하도록 `&`와 `|`를 오버로드합니다.

| 표현식 | 동등 | 설명 |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | `a`가 `Ok`이면 `b`, 아니면 `Err`. |
| `a & fn` | `a.and_then(lambda v: fn(v))` | `a`가 `Ok`이면 `fn(value)` 호출. |
| `a \| b` | `a.or_else(lambda _: b)` | `a`가 `Ok`이면 `a`, 아니면 `b`. |
| `a \| fn` | `a.or_else(lambda e: fn(e))` | `a`가 `Err`이면 `fn(error)` 호출. |

```python
from pyfplib import Err, Ok

print(Ok(1) & Ok(2))    # Ok(2)
print(Err("e") & Ok(2)) # Err('e')
print(Err("e") | Ok(2)) # Ok(2)
```

---

## 예외 처리

### `Result.try_call(fn: Callable[..., R], *args, **kwargs) -> Result[R, Exception]` *(정적)*

제공된 인수로 `fn`을 호출하고 발생한 모든 `Exception`을 `Err`로 변환합니다.

```python
from pyfplib import Result

print(Result.try_call(int, "42"))            # Ok(42)
print(Result.try_call(int, "oops").is_err()) # True
```

---

## 오류

- `UnwrapError` — 잘못된 변형이 있을 때 `unwrap()`과 `unwrap_err()`가 발생시킵니다.
- `ExpectedError` — `expect()`와 `expect_err()`가 주어진 메시지와 함께 발생시킵니다.

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
