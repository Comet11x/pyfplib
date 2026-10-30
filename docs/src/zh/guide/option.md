# Option API

`Option[T]` 表示可能存在的值（`Some`）或缺失的值（`Nothing`）。它位于 `pyfplib.option`，并从顶层 `pyfplib` 包重新导出。

```python
from pyfplib import Nothing, Option, Some
```

---

## 构造函数

### `Some(value)`

将值包装为 `Option`。`Some` 始终 `is_some()`。

```python
>>> Some(42).is_some()
True
>>> Some(42).unwrap()
42
```

### `Nothing()`

创建空 `Option`。`Nothing` 始终 `is_none()`。

```python
>>> Nothing().is_none()
True
>>> Nothing().unwrap_or(0)
0
```

---

## 检查

| 方法 | 返回 | 说明 |
|---|---|---|
| `is_some()` | `bool` | 存在值时返回 `True`。 |
| `is_none()` | `bool` | 不存在值时返回 `True`。 |
| `value` | `T \| None` | 原始包含值（可能为 `None`）。 |
| `__bool__()` | `bool` | `Some` 为真，`Nothing` 为假。 |
| `__eq__(other)` | `bool` | 当两者都是 `Option` 时比较包含的值。 |
| `__hash__()` | `int` | 对包含的值进行哈希。 |

```python
>>> bool(Some(1)), bool(Nothing())
(True, False)
>>> Some(1) == Some(1)
True
```

### `inspect(fn) -> Option[T]`

当为 `Some` 时用包含的值调用 `fn`，然后原样返回该选项。

```python
>>> Some(2).inspect(lambda v: print(v))
2
Some(2)
```

### `inspect_none(fn) -> Option[T]`

当为 `Nothing` 时无参数调用 `fn`，然后原样返回该选项。

```python
>>> Nothing().inspect_none(lambda: print("empty"))
empty
Nothing()
```

---

## 提取

| 方法 | 返回 | 异常 | 说明 |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | 返回值；为空时抛出异常。 |
| `expect(message)` | `T` | `ExpectedError` | 返回值；为空时抛出带有 `message` 的异常。 |
| `unwrap_or(default)` | `T` | — | 返回值或 `default`。 |
| `unwrap_or_else(fn)` | `T` | — | 返回值或调用 `fn()` 获取后备值。 |

```python
>>> Some(3).unwrap_or(0)
3
>>> Nothing().unwrap_or(0)
0
>>> Nothing().unwrap_or_else(lambda: 10)
10
```

---

## 变换

### `map(fn) -> Option[U]`

对包含的值应用 `fn`，并将结果包装为 `Some`。`Nothing` 保持为 `Nothing`。

```python
>>> Some(3).map(lambda v: v * 2)
Some(6)
>>> Nothing().map(lambda v: v * 2)
Nothing()
```

### `map_or(default, fn) -> Option[U]`

当为 `Some` 时应用 `fn`，否则使用 `default`。结果始终包装为 `Some`。

```python
>>> Some(3).map_or(0, lambda v: v * 2)
Some(6)
>>> Nothing().map_or(0, lambda v: v * 2)
Some(0)
```

### `map_or_else(default, fn) -> U`

当为 `Some` 时应用 `fn`，否则调用 `default()`。

```python
>>> Some(3).map_or_else(lambda: 0, lambda v: v * 2)
6
>>> Nothing().map_or_else(lambda: 0, lambda v: v * 2)
0
```

### `flatten() -> Option[T]`

折叠一层嵌套。

```python
>>> Some(Some(1)).flatten()
Some(1)
>>> Some(1).flatten()
Some(1)
```

### `flatten_all() -> Option[T]`

折叠所有层级的嵌套。

```python
>>> Some(Some(Some(1))).flatten_all()
Some(1)
```

---

## 转换

### `ok_or(err) -> Result[T, E]`

将 `Option` 转换为 `Result`，为空时使用 `err`。

```python
>>> Some(1).ok_or("missing")
Ok(1)
>>> Nothing().ok_or("missing")
Err('missing')
```

### `ok_or_else(fn) -> Result[T, E]`

类似 `ok_or`，但为空时调用 `fn()` 生成错误。

```python
>>> Nothing().ok_or_else(lambda: "missing")
Err('missing')
```

### `from_optional(value) -> Option[T]` *（静态）*

从可能为 `None` 的值构建 `Option`。

```python
>>> Option.from_optional(None)
Nothing()
>>> Option.from_optional(5)
Some(5)
```

---

## 组合

### `and_then(fn) -> Option[U]`

仅在 `Some` 时运行 `fn`；否则返回 `Nothing`。

```python
>>> Some(2).and_then(lambda v: Some(v + 1))
Some(3)
>>> Nothing().and_then(lambda v: Some(v + 1))
Nothing()
```

### `or_else(fn) -> Option[T]`

仅在 `Nothing` 时运行 `fn`；否则返回原选项。

```python
>>> Nothing().or_else(lambda: Some(9))
Some(9)
>>> Some(1).or_else(lambda: Some(9))
Some(1)
```

### `xor(other) -> Option[T]`

当两个选项中恰好一个为 `Some` 时返回一个值。

```python
>>> Some(1).xor(Nothing())
Some(1)
>>> Some(1).xor(Some(2))
Nothing()
```

### `zip(other) -> Option[tuple[T, U]]`

当两个选项都为 `Some` 时配对值。

```python
>>> Some(1).zip(Some("a"))
Some((1, 'a'))
```

### `zip_with(other, ctr) -> Option[R]`

当两个选项都为 `Some` 时用 `ctr` 组合两个值。

```python
>>> Some(1).zip_with(Some(2), lambda a, b: a + b)
Some(3)
```

---

## 运算符

`Option` 重载了 `&` 和 `|`，对应 `and_then` 和 `or_else`。

| 表达式 | 等价于 | 说明 |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | 当 `a` 为 `Some` 时返回 `b`，否则返回 `Nothing`。 |
| `a & fn` | `a.and_then(lambda _: fn())` | 当 `a` 为 `Some` 时调用 `fn()`。 |
| `a \| b` | `a.or_else(lambda: b)` | 当 `a` 为 `Some` 时返回 `a`，否则返回 `b`。 |
| `a \| fn` | `a.or_else(fn)` | 当 `a` 为 `Nothing` 时调用 `fn()`。 |

```python
>>> Some(1) & Some(2)
Some(2)
>>> Nothing() & Some(2)
Nothing()
>>> Nothing() | Some(2)
Some(2)
```

---

## 变更

### `push(value) -> T`

存储 `value` 并返回之前持有的值（若选项为空则返回 `value`）。

```python
>>> opt = Some(1)
>>> opt.push(2)
1
>>> opt
Some(2)
```

---

## 错误

- `UnwrapError` — 当选项为 `Nothing` 时由 `unwrap()` 抛出。
- `ExpectedError` — 当选项为 `Nothing` 时由 `expect(message)` 抛出。

```python
from pyfplib import Nothing
from pyfplib.errors import ExpectedError, UnwrapError

try:
    Nothing().unwrap()
except UnwrapError as exc:
    print(exc)
```
