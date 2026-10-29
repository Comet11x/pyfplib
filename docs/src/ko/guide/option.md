# Option API

`Option[T]`는 존재할 수 있는 값(`Some`) 또는 없는 값(`Nothing`)을 나타냅니다. `pyfplib.option`에 있으며 최상위 `pyfplib` 패키지에서 다시 내보냅니다.

```python
from pyfplib import Nothing, Option, Some
```

---

## 생성자

### `Some(value)`

값을 `Option`으로 감쌉니다. `Some`은 항상 `is_some()`입니다.

```python
>>> Some(42).is_some()
True
>>> Some(42).unwrap()
42
```

### `Nothing()`

빈 `Option`을 만듭니다. `Nothing`은 항상 `is_none()`입니다.

```python
>>> Nothing().is_none()
True
>>> Nothing().unwrap_or(0)
0
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
>>> bool(Some(1)), bool(Nothing())
(True, False)
>>> Some(1) == Some(1)
True
```

### `inspect(fn) -> Option[T]`

`Some`일 때 포함된 값으로 `fn`을 호출한 뒤 옵션을 그대로 반환합니다.

```python
>>> Some(2).inspect(lambda v: print(v))
2
Some(2)
```

### `inspect_none(fn) -> Option[T]`

`Nothing`일 때 인자 없이 `fn`을 호출한 뒤 옵션을 그대로 반환합니다.

```python
>>> Nothing().inspect_none(lambda: print("empty"))
empty
Nothing()
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
>>> Some(3).unwrap_or(0)
3
>>> Nothing().unwrap_or(0)
0
>>> Nothing().unwrap_or_else(lambda: 10)
10
```

---

## 변환

### `map(fn) -> Option[U]`

포함된 값에 `fn`을 적용하고 결과를 `Some`으로 감쌉니다. `Nothing`은 `Nothing`으로 유지됩니다.

```python
>>> Some(3).map(lambda v: v * 2)
Some(6)
>>> Nothing().map(lambda v: v * 2)
Nothing()
```

### `map_or(default, fn) -> Option[U]`

`Some`이면 `fn`을 적용하고, 아니면 `default`를 사용합니다. 결과는 항상 `Some`으로 감쌉니다.

```python
>>> Some(3).map_or(0, lambda v: v * 2)
Some(6)
>>> Nothing().map_or(0, lambda v: v * 2)
Some(0)
```

### `map_or_else(default, fn) -> U`

`Some`이면 `fn`을 적용하고, 아니면 `default()`를 호출합니다.

```python
>>> Some(3).map_or_else(lambda: 0, lambda v: v * 2)
6
>>> Nothing().map_or_else(lambda: 0, lambda v: v * 2)
0
```

### `flatten() -> Option[T]`

한 단계의 중첩을 평탄화합니다.

```python
>>> Some(Some(1)).flatten()
Some(1)
>>> Some(1).flatten()
Some(1)
```

### `flatten_all() -> Option[T]`

모든 단계의 중첩을 평탄화합니다.

```python
>>> Some(Some(Some(1))).flatten_all()
Some(1)
```

---

## Result로 변환

### `ok_or(err) -> Result[T, E]`

`Option`을 `Result`로 변환하며, 비어 있으면 `err`를 사용합니다.

```python
>>> Some(1).ok_or("missing")
Ok(1)
>>> Nothing().ok_or("missing")
Err('missing')
```

### `ok_or_else(fn) -> Result[T, E]`

`ok_or`와 같지만 비어 있을 때 `fn()`을 호출해 오류를 만듭니다.

```python
>>> Nothing().ok_or_else(lambda: "missing")
Err('missing')
```

### `from_optional(value) -> Option[T]` *(정적)*

`None`일 수 있는 값으로 `Option`을 만듭니다.

```python
>>> Option.from_optional(None)
Nothing()
>>> Option.from_optional(5)
Some(5)
```

---

## 결합

### `and_then(fn) -> Option[U]`

`Some`일 때만 `fn`을 실행하고, 아니면 `Nothing`을 반환합니다.

```python
>>> Some(2).and_then(lambda v: Some(v + 1))
Some(3)
>>> Nothing().and_then(lambda v: Some(v + 1))
Nothing()
```

### `or_else(fn) -> Option[T]`

`Nothing`일 때만 `fn`을 실행하고, 아니면 원래 옵션을 반환합니다.

```python
>>> Nothing().or_else(lambda: Some(9))
Some(9)
>>> Some(1).or_else(lambda: Some(9))
Some(1)
```

### `xor(other) -> Option[T]`

두 옵션 중 정확히 하나만 `Some`일 때 값을 반환합니다.

```python
>>> Some(1).xor(Nothing())
Some(1)
>>> Some(1).xor(Some(2))
Nothing()
```

### `zip(other) -> Option[tuple[T, U]]`

두 옵션이 모두 `Some`일 때 값을 쌍으로 묶습니다.

```python
>>> Some(1).zip(Some("a"))
Some((1, 'a'))
```

### `zip_with(other, ctr) -> Option[R]`

두 옵션이 모두 `Some`일 때 `ctr`로 두 값을 결합합니다.

```python
>>> Some(1).zip_with(Some(2), lambda a, b: a + b)
Some(3)
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
>>> Some(1) & Some(2)
Some(2)
>>> Nothing() & Some(2)
Nothing()
>>> Nothing() | Some(2)
Some(2)
```

---

## 변경

### `push(value) -> T`

`value`를 저장하고 이전에 보관하던 값(옵션이 비어 있었다면 `value`)을 반환합니다.

```python
>>> opt = Some(1)
>>> opt.push(2)
1
>>> opt
Some(2)
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
    print(exc)
```
