# Option API

`Option[T]` 表示可能存在的值（`Some`）或缺失的值（`Nothing`）。它位于 `pyfplib.option`，并从顶层 `pyfplib` 包重新导出。

```python
from pyfplib import Nothing, Option, Some
```

---

## 构造函数

### `Some(value: T)`

将非 `None` 的值包装为 `Option`。由于 `Option` 内部使用 `None` 表示缺失，`Some(None)` 的行为与 `Nothing()` 相同。

```python
from pyfplib import Some

print(Some(42).is_some())    # True
print(Some(42).unwrap())     # 42
print(Some(None).is_none())  # True
```

### `Nothing()`

创建空 `Option`。`Nothing` 始终 `is_none()`。

```python
from pyfplib import Nothing

print(Nothing().is_none())     # True
print(Nothing().unwrap_or(0))  # 0
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
from pyfplib import Nothing, Some

print(bool(Some(1)), bool(Nothing()))  # (True, False)
print(Some(1) == Some(1))              # True
```

### `inspect(fn: Callable[[T], None]) -> Option[T]`

当为 `Some` 时用包含的值调用 `fn`，然后原样返回该选项。

```python
from pyfplib import Option, Some

option: Option[int] = Some(2)
returned = option.inspect(lambda value: print(f"inspected: {value}"))
print(returned)  # Some(2)
```

### `inspect_none(fn: Callable[[], None]) -> Option[T]`

当为 `Nothing` 时无参数调用 `fn`，然后原样返回该选项。

```python
from pyfplib import Nothing

returned = Nothing().inspect_none(lambda: print("empty"))
print(returned)  # Nothing()
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
from pyfplib import Nothing, Some

def fallback() -> int:
    return 10

print(Some(3).unwrap_or(0))               # 3
print(Nothing().unwrap_or(0))             # 0
print(Some(3).unwrap_or_else(fallback))   # 3
print(Nothing().unwrap_or_else(fallback)) # 10
```

---

## 模式匹配

`Option` 支持 Python 的结构化模式匹配。使用 `Some(value)` 绑定包含的值，使用 `Nothing()` 匹配空 option，无需先调用 `is_some()`。

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

## 变换

### `map(fn: Callable[[T], U]) -> Option[U]`

对包含的值应用 `fn`，并将结果包装为 `Some`。`Nothing` 保持为 `Nothing`。

```python
from pyfplib import Nothing, Some

def double(value: int) -> int:
    return value * 2

print(Some(3).map(double))    # Some(6)
print(Nothing().map(double))  # Nothing()
```

### `map_or(default: U, fn: Callable[[T], U]) -> Option[U]`

对 `Some` 值应用 `fn`，否则使用 `default`，并且始终返回 `Option`（`Some`）。如果需要普通值，请使用 `map_or_else`。

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

当为 `Some` 时应用 `fn`，否则调用 `default()`。

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

折叠一层嵌套。没有嵌套的选项会原样返回。

```python
from pyfplib import Some

print(Some(Some(1)).flatten())  # Some(1)
print(Some(1).flatten())        # Some(1)
```

### `flatten_all() -> Option[T]`

折叠所有嵌套层级，直到到达最内层的非选项值。

```python
from pyfplib import Some

print(Some(Some(Some(1))).flatten_all())  # Some(1)
```

---

## 转换

### `ok_or(err: E) -> Result[T, E]`

将 `Option` 转换为 `Result`，为空时使用 `err`。

```python
from pyfplib import Nothing, Some

print(Some(1).ok_or("missing"))   # Ok(1)
print(Nothing().ok_or("missing")) # Err('missing')
```

### `ok_or_else(fn: Callable[[], E]) -> Result[T, E]`

类似 `ok_or`，但为空时调用 `fn()` 生成错误。

```python
from pyfplib import Nothing

def missing_error() -> str:
    return "missing"

print(Nothing().ok_or_else(missing_error))  # Err('missing')
```

### `from_optional(value: T | None) -> Option[T]` *（静态）*

从可能为 `None` 的值创建 `Option`：`None` 变为 `Nothing`，其他任何值变为 `Some`。

```python
from pyfplib import Option

value: int | None = None
print(Option.from_optional(value))  # Nothing()
print(Option.from_optional(5))      # Some(5)
```

---

## 组合

### `and_then(fn: Callable[[T], Option[U]]) -> Option[U]`

仅在 `Some` 时运行 `fn`；否则返回 `Nothing`。

```python
from pyfplib import Nothing, Option, Some

def increment(value: int) -> Option[int]:
    return Some(value + 1)

print(Some(2).and_then(increment))   # Some(3)
print(Nothing().and_then(increment)) # Nothing()
```

### `or_else(fn: Callable[[], Option[T]]) -> Option[T]`

仅在 `Nothing` 时运行 `fn`；否则返回原选项。

```python
from pyfplib import Nothing, Option, Some

def recover() -> Option[int]:
    return Some(9)

print(Nothing().or_else(recover))  # Some(9)
print(Some(1).or_else(recover))    # Some(1)
```

### `xor(other: Option[T]) -> Option[T]`

当两个选项中恰好一个为 `Some` 时返回一个值。

```python
from pyfplib import Nothing, Some

print(Some(1).xor(Nothing()))  # Some(1)
print(Some(1).xor(Some(2)))    # Nothing()
```

### `zip(other: Option[U]) -> Option[tuple[T, U]]`

当两个选项都为 `Some` 时配对值。

```python
from pyfplib import Some

print(Some(1).zip(Some("a")))  # Some((1, 'a'))
```

### `zip_with(other: Option[U], ctr: Callable[[T, U], R]) -> Option[R]`

当两个选项都为 `Some` 时用 `ctr` 组合两个值。

```python
from pyfplib import Some

def add(left: int, right: int) -> int:
    return left + right

print(Some(1).zip_with(Some(2), add))  # Some(3)
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
from pyfplib import Nothing, Some

print(Some(1) & Some(2))    # Some(2)
print(Nothing() & Some(2))  # Nothing()
print(Nothing() | Some(2))  # Some(2)
```

---

## 变更

### `push(value: T) -> T`

就地修改选项：存储 `value` 并返回之前持有的值；如果选项为空，则返回 `value` 本身。

```python
from pyfplib import Option, Some

option: Option[int] = Some(1)
previous = option.push(2)

print(previous)  # 1
print(option)    # Some(2)
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
    print(exc)  # called `Option.unwrap()` on a `Nothing` value

try:
    Nothing().expect("value is required")
except ExpectedError as exc:
    print(exc)  # value is required
```
