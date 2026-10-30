# Result API

`Result[T, E]`는 성공(`Ok`) 또는 실패(`Err`)를 나타냅니다. `pyfplib.result`에 있으며 최상위 `pyfplib` 패키지에서 다시 내보냅니다.

```python
from pyfplib import Err, Ok, Result
```

---

## 생성자

### `Ok(value)`

성공 결과를 만듭니다.

```python
>>> Ok(42).is_ok()
True
>>> Ok(42).unwrap()
42
```

### `Err(error)`

실패 결과를 만듭니다.

```python
>>> Err("boom").is_err()
True
>>> Err("boom").unwrap_err()
'boom'
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
>>> bool(Ok(1)), bool(Err("e"))
(True, False)
>>> Ok(1).ok()
Some(1)
>>> Err("e").ok()
Nothing()
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
>>> Ok(1).unwrap_or(0)
1
>>> Err("e").unwrap_or(0)
0
>>> Err("e").unwrap_or_else(lambda e: len(e))
1
```

---

## 변환

### `map(fn) -> Result[U, E]`

`Ok` 값에 `fn`을 적용합니다. `Err`는 그대로 반환됩니다.

```python
>>> Ok(2).map(lambda v: v * 3)
Ok(6)
>>> Err("e").map(lambda v: v * 3)
Err('e')
```

### `map_or(default, fn) -> Result[U, E]`

`Ok` 값에 `fn`을 적용하거나 `default`를 사용합니다. 결과는 항상 `Ok`입니다.

```python
>>> Ok(2).map_or(0, lambda v: v * 3)
Ok(6)
>>> Err("e").map_or(0, lambda v: v * 3)
Ok(0)
```

### `map_or_else(default, fn) -> U`

`Ok` 값에 `fn`을 적용하거나 `Err`이면 `default(error)`를 호출합니다.

```python
>>> Ok(2).map_or_else(lambda e: 0, lambda v: v * 3)
6
>>> Err("e").map_or_else(lambda e: len(e), lambda v: v * 3)
3
```

### `map_err(fn) -> Result[T, U]`

`Err` 값에 `fn`을 적용합니다. `Ok`는 그대로 반환됩니다.

```python
>>> Err("boom").map_err(str.upper)
Err('BOOM')
>>> Ok(1).map_err(str.upper)
Ok(1)
```

### `flatten() -> Result[T, E]`

한 단계의 중첩을 평탄화합니다.

```python
>>> Ok(Ok(1)).flatten()
Ok(1)
>>> Ok(1).flatten()
Ok(1)
```

### `flatten_all() -> Result[T, E]`

모든 단계의 중첩을 평탄화합니다.

```python
>>> Ok(Ok(Ok(1))).flatten_all()
Ok(1)
```

---

## 결합

### `and_then(fn) -> Result[T, E]`

결과가 `Ok`일 때만 `fn`을 실행하고, 아니면 `Err`를 그대로 반환합니다.

```python
>>> Ok(2).and_then(lambda v: Ok(v + 1))
Ok(3)
>>> Err("e").and_then(lambda v: Ok(v + 1))
Err('e')
```

### `or_else(fn) -> Result[T, E]`

결과가 `Err`일 때만 `fn`을 실행하고, 아니면 원래 `Ok`를 반환합니다.

```python
>>> Err("e").or_else(lambda e: Ok(0))
Ok(0)
>>> Ok(1).or_else(lambda e: Ok(0))
Ok(1)
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
>>> Ok(1) & Ok(2)
Ok(2)
>>> Err("e") & Ok(2)
Err('e')
>>> Err("e") | Ok(2)
Ok(2)
```

---

## 예외 처리

### `Result.try_call(fn, *args, **kwargs) -> Result[R, Exception]` *(정적)*

`fn`을 호출하고 발생한 예외를 `Err`로 변환합니다.

```python
>>> Result.try_call(int, "42")
Ok(42)
>>> Result.try_call(int, "oops").is_err()
True
```

---

## 오류

- `UnwrapError` — 잘못된 변형이 있을 때 `unwrap()`과 `unwrap_err()`가 발생시킵니다.
- `ExpectedError` — `expect()`와 `expect_err()`가 주어진 메시지와 함께 발생시킵니다.

```python
from pyfplib import Err
from pyfplib.errors import UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)
```
