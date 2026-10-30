# Result API

`Result[T, E]` 表示成功（`Ok`）或失败（`Err`）。它位于 `pyfplib.result`，并从顶层 `pyfplib` 包重新导出。

```python
from pyfplib import Err, Ok, Result
```

---

## 构造函数

### `Ok(value: T)`

创建成功结果。

```python
from pyfplib import Ok, Result

result: Result[int, str] = Ok(42)
print(result.is_ok())  # True
print(result.unwrap()) # 42
```

### `Err(error: E)`

创建失败结果。

```python
from pyfplib import Err, Result

result: Result[int, str] = Err("boom")
print(result.is_err())           # True
print(repr(result.unwrap_err())) # 'boom'
```

---

## 检查

| 方法 | 返回 | 说明 |
|---|---|---|
| `is_ok()` | `bool` | 结果为 `Ok` 时返回 `True`。 |
| `is_err()` | `bool` | 结果为 `Err` 时返回 `True`。 |
| `value` | `T \| E` | 包含的值或错误。 |
| `__bool__()` | `bool` | `Ok` 为真，`Err` 为假。 |
| `inspect(fn)` | `Result[T, E]` | 用 `Ok` 值调用 `fn`，返回 `self`。 |
| `inspect_err(fn)` | `Result[T, E]` | 用 `Err` 值调用 `fn`，返回 `self`。 |
| `ok()` | `Option[T]` | `Ok` 时为 `Some(value)`，否则为 `Nothing()`。 |
| `err()` | `Option[E]` | `Err` 时为 `Some(error)`，否则为 `Nothing()`。 |

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

## 提取

| 方法 | 返回 | 异常 | 说明 |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | 返回 `Ok` 值；为 `Err` 时抛出异常。 |
| `unwrap_err()` | `E` | `UnwrapError` | 返回 `Err` 值；为 `Ok` 时抛出异常。 |
| `expect(message)` | `T` | `ExpectedError` | 返回 `Ok` 值；否则抛出带有 `message` 的异常。 |
| `expect_err(message)` | `E` | `ExpectedError` | 返回 `Err` 值；否则抛出带有 `message` 的异常。 |
| `unwrap_or(default)` | `T` | — | 返回 `Ok` 值或 `default`。 |
| `unwrap_or_else(fn)` | `T` | — | 返回 `Ok` 值或 `fn(error)`。 |
| `unwrap_err_or(default)` | `E` | — | 返回 `Err` 值或 `default`。 |

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

## 模式匹配

`Result` 支持 Python 的结构化模式匹配。使用 `Ok(value)` 绑定成功值，使用 `Err(error)` 绑定错误，无需先调用 `is_ok()`。

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

## 变换

### `map(fn: Callable[[T], U]) -> Result[U, E]`

对 `Ok` 值应用 `fn`。`Err` 原样返回。

```python
from pyfplib import Err, Ok

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map(triple))    # Ok(6)
print(Err("e").map(triple)) # Err('e')
```

### `map_or(default: T, fn: Callable[[T], U]) -> Result[U, E]`

对 `Ok` 值应用 `fn`，或在结果为 `Err` 时对 `default` 应用 `fn`。结果始终为 `Ok`。如果需要普通值，请使用 `map_or_else`。

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

对 `Ok` 值应用 `fn`，或在 `Err` 时调用 `default(error)` 并对该回退值应用 `fn`，返回普通值。

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

对 `Err` 值应用 `fn`。`Ok` 原样返回。

```python
from pyfplib import Err, Ok

print(Err("boom").map_err(str.upper))  # Err('BOOM')
print(Ok(1).map_err(str.upper))        # Ok(1)
```

### `flatten() -> Result[T, E]`

折叠一层嵌套。非嵌套结果原样返回。

```python
from pyfplib import Ok

print(Ok(Ok(1)).flatten())  # Ok(1)
print(Ok(1).flatten())      # Ok(1)
```

### `flatten_all() -> Result[T, E]`

折叠所有嵌套层级，直到到达最内层的非 `Result` 值。

```python
from pyfplib import Ok

print(Ok(Ok(Ok(1))).flatten_all())  # Ok(1)
```

---

## 组合

### `and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]`

仅在结果为 `Ok` 时运行 `fn`；否则原样返回 `Err`。

```python
from pyfplib import Err, Ok, Result

def increment(value: int) -> Result[int, str]:
    return Ok(value + 1)

print(Ok(2).and_then(increment))    # Ok(3)
print(Err("e").and_then(increment)) # Err('e')
```

### `or_else(fn: Callable[[E], Result[T, E]]) -> Result[T, E]`

仅在结果为 `Err` 时运行 `fn`；否则返回原 `Ok`。

```python
from pyfplib import Err, Ok, Result

def recover(error: str) -> Result[int, str]:
    return Ok(0)

print(Err("e").or_else(recover))  # Ok(0)
print(Ok(1).or_else(recover))     # Ok(1)
```

---

## 运算符

`Result` 重载了 `&` 和 `|`，对应 `and_then` 和 `or_else`。

| 表达式 | 等价于 | 说明 |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | 当 `a` 为 `Ok` 时返回 `b`，否则返回 `Err`。 |
| `a & fn` | `a.and_then(lambda v: fn(v))` | 当 `a` 为 `Ok` 时调用 `fn(value)`。 |
| `a \| b` | `a.or_else(lambda _: b)` | 当 `a` 为 `Ok` 时返回 `a`，否则返回 `b`。 |
| `a \| fn` | `a.or_else(lambda e: fn(e))` | 当 `a` 为 `Err` 时调用 `fn(error)`。 |

```python
from pyfplib import Err, Ok

print(Ok(1) & Ok(2))    # Ok(2)
print(Err("e") & Ok(2)) # Err('e')
print(Err("e") | Ok(2)) # Ok(2)
```

---

## 异常处理

### `Result.try_call(fn: Callable[..., R], *args, **kwargs) -> Result[R, Exception]` *（静态）*

使用提供的参数调用 `fn`，并将任何抛出的 `Exception` 转换为 `Err`。

```python
from pyfplib import Result

print(Result.try_call(int, "42"))            # Ok(42)
print(Result.try_call(int, "oops").is_err()) # True
```

---

## 错误

- `UnwrapError` — 当存在错误的变体时由 `unwrap()` 和 `unwrap_err()` 抛出。
- `ExpectedError` — 由 `expect()` 和 `expect_err()` 抛出，并带有提供的消息。

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
