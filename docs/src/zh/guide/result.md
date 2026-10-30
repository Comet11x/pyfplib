# Result API

`Result[T, E]` 表示成功（`Ok`）或失败（`Err`）。它位于 `pyfplib.result`，并从顶层 `pyfplib` 包重新导出。

```python
from pyfplib import Err, Ok, Result
```

---

## 构造函数

### `Ok(value)`

创建成功结果。

```python
>>> Ok(42).is_ok()
True
>>> Ok(42).unwrap()
42
```

### `Err(error)`

创建失败结果。

```python
>>> Err("boom").is_err()
True
>>> Err("boom").unwrap_err()
'boom'
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
>>> bool(Ok(1)), bool(Err("e"))
(True, False)
>>> Ok(1).ok()
Some(1)
>>> Err("e").ok()
Nothing()
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
>>> Ok(1).unwrap_or(0)
1
>>> Err("e").unwrap_or(0)
0
>>> Err("e").unwrap_or_else(lambda e: len(e))
1
```

---

## 变换

### `map(fn) -> Result[U, E]`

对 `Ok` 值应用 `fn`。`Err` 原样返回。

```python
>>> Ok(2).map(lambda v: v * 3)
Ok(6)
>>> Err("e").map(lambda v: v * 3)
Err('e')
```

### `map_or(default, fn) -> Result[U, E]`

对 `Ok` 值应用 `fn` 或使用 `default`。结果始终为 `Ok`。

```python
>>> Ok(2).map_or(0, lambda v: v * 3)
Ok(6)
>>> Err("e").map_or(0, lambda v: v * 3)
Ok(0)
```

### `map_or_else(default, fn) -> U`

对 `Ok` 值应用 `fn`，或在 `Err` 时调用 `default(error)`。

```python
>>> Ok(2).map_or_else(lambda e: 0, lambda v: v * 3)
6
>>> Err("e").map_or_else(lambda e: len(e), lambda v: v * 3)
3
```

### `map_err(fn) -> Result[T, U]`

对 `Err` 值应用 `fn`。`Ok` 原样返回。

```python
>>> Err("boom").map_err(str.upper)
Err('BOOM')
>>> Ok(1).map_err(str.upper)
Ok(1)
```

### `flatten() -> Result[T, E]`

折叠一层嵌套。

```python
>>> Ok(Ok(1)).flatten()
Ok(1)
>>> Ok(1).flatten()
Ok(1)
```

### `flatten_all() -> Result[T, E]`

折叠所有层级的嵌套。

```python
>>> Ok(Ok(Ok(1))).flatten_all()
Ok(1)
```

---

## 组合

### `and_then(fn) -> Result[T, E]`

仅在结果为 `Ok` 时运行 `fn`；否则原样返回 `Err`。

```python
>>> Ok(2).and_then(lambda v: Ok(v + 1))
Ok(3)
>>> Err("e").and_then(lambda v: Ok(v + 1))
Err('e')
```

### `or_else(fn) -> Result[T, E]`

仅在结果为 `Err` 时运行 `fn`；否则返回原 `Ok`。

```python
>>> Err("e").or_else(lambda e: Ok(0))
Ok(0)
>>> Ok(1).or_else(lambda e: Ok(0))
Ok(1)
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
>>> Ok(1) & Ok(2)
Ok(2)
>>> Err("e") & Ok(2)
Err('e')
>>> Err("e") | Ok(2)
Ok(2)
```

---

## 异常处理

### `Result.try_call(fn, *args, **kwargs) -> Result[R, Exception]` *（静态）*

调用 `fn` 并将任何抛出的异常转换为 `Err`。

```python
>>> Result.try_call(int, "42")
Ok(42)
>>> Result.try_call(int, "oops").is_err()
True
```

---

## 错误

- `UnwrapError` — 当存在错误的变体时由 `unwrap()` 和 `unwrap_err()` 抛出。
- `ExpectedError` — 由 `expect()` 和 `expect_err()` 抛出，并带有提供的消息。

```python
from pyfplib import Err
from pyfplib.errors import UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)
```
