# Option API

`Option[T]` は存在する値（`Some`）または存在しない値（`Nothing`）を表します。`pyfplib.option` にあり、トップレベルの `pyfplib` パッケージから再エクスポートされます。

```python
from pyfplib import Nothing, Option, Some
```

---

## コンストラクタ

### `Some(value: T)`

`None` 以外の値を `Option` に包みます。`Option` は内部で `None` を不在の表現に使用するため、`Some(None)` は `Nothing()` と同じように動作します。

```python
from pyfplib import Some

print(Some(42).is_some())    # True
print(Some(42).unwrap())     # 42
print(Some(None).is_none())  # True
```

### `Nothing()`

空の `Option` を作成します。`Nothing` は常に `is_none()` です。

```python
from pyfplib import Nothing

print(Nothing().is_none())     # True
print(Nothing().unwrap_or(0))  # 0
```

---

## 検査

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `is_some()` | `bool` | 値が存在する場合 `True`。 |
| `is_none()` | `bool` | 値が存在しない場合 `True`。 |
| `value` | `T \| None` | 生の包含値（`None` の場合あり）。 |
| `__bool__()` | `bool` | `Some` で真、`Nothing` で偽。 |
| `__eq__(other)` | `bool` | 両方が `Option` の場合に包含値を比較します。 |
| `__hash__()` | `int` | 包含値のハッシュを計算します。 |

```python
from pyfplib import Nothing, Some

print(bool(Some(1)), bool(Nothing()))  # (True, False)
print(Some(1) == Some(1))              # True
```

### `inspect(fn: Callable[[T], None]) -> Option[T]`

`Some` のとき包含値で `fn` を呼び出し、その後オプションをそのまま返します。

```python
from pyfplib import Option, Some

option: Option[int] = Some(2)
returned = option.inspect(lambda value: print(f"inspected: {value}"))
print(returned)  # Some(2)
```

### `inspect_none(fn: Callable[[], None]) -> Option[T]`

`Nothing` のとき引数なしで `fn` を呼び出し、その後オプションをそのまま返します。

```python
from pyfplib import Nothing

returned = Nothing().inspect_none(lambda: print("empty"))
print(returned)  # Nothing()
```

---

## 抽出

| メソッド | 戻り値 | 例外 | 説明 |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | 値を返すか、空の場合に例外を送出します。 |
| `expect(message)` | `T` | `ExpectedError` | 値を返すか、`message` 付きで例外を送出します。 |
| `unwrap_or(default)` | `T` | — | 値または `default` を返します。 |
| `unwrap_or_else(fn)` | `T` | — | 値または `fn()` を呼び出した代替値を返します。 |

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

## パターンマッチング

`Option` は Python の構造的パターンマッチングをサポートします。`Some(value)` で含まれる値をバインドし、`Nothing()` で空の option に一致させます。事前に `is_some()` を呼び出す必要はありません。

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

## 変換

### `map(fn: Callable[[T], U]) -> Option[U]`

包含値に `fn` を適用し、結果を `Some` で包みます。`Nothing` は `Nothing` のままです。

```python
from pyfplib import Nothing, Some

def double(value: int) -> int:
    return value * 2

print(Some(3).map(double))    # Some(6)
print(Nothing().map(double))  # Nothing()
```

### `map_or(default: U, fn: Callable[[T], U]) -> Option[U]`

`Some` の値に `fn` を適用するか `default` を使用し、常に `Option`（`Some`）を返します。素の値が必要な場合は `map_or_else` を使用してください。

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

`Some` のとき `fn` を適用し、そうでなければ `default()` を呼び出します。

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

ネストを 1 レベル解消します。ネストされていないオプションはそのまま返されます。

```python
from pyfplib import Some

print(Some(Some(1)).flatten())  # Some(1)
print(Some(1).flatten())        # Some(1)
```

### `flatten_all() -> Option[T]`

最も内側のオプションでない値に到達するまで、すべてのネストを解消します。

```python
from pyfplib import Some

print(Some(Some(Some(1))).flatten_all())  # Some(1)
```

---

## Result への変換

### `ok_or(err: E) -> Result[T, E]`

`Option` を `Result` に変換し、空の場合は `err` を使用します。

```python
from pyfplib import Nothing, Some

print(Some(1).ok_or("missing"))   # Ok(1)
print(Nothing().ok_or("missing")) # Err('missing')
```

### `ok_or_else(fn: Callable[[], E]) -> Result[T, E]`

`ok_or` と同様ですが、空の場合に `fn()` を呼び出してエラーを生成します。

```python
from pyfplib import Nothing

def missing_error() -> str:
    return "missing"

print(Nothing().ok_or_else(missing_error))  # Err('missing')
```

### `from_optional(value: T | None) -> Option[T]` *（静的）*

`None` の可能性がある値から `Option` を作成します。`None` は `Nothing` になり、それ以外の値は `Some` になります。

```python
from pyfplib import Option

value: int | None = None
print(Option.from_optional(value))  # Nothing()
print(Option.from_optional(5))      # Some(5)
```

---

## 結合

### `and_then(fn: Callable[[T], Option[U]]) -> Option[U]`

`Some` のときのみ `fn` を実行し、そうでなければ `Nothing` を返します。

```python
from pyfplib import Nothing, Option, Some

def increment(value: int) -> Option[int]:
    return Some(value + 1)

print(Some(2).and_then(increment))   # Some(3)
print(Nothing().and_then(increment)) # Nothing()
```

### `or_else(fn: Callable[[], Option[T]]) -> Option[T]`

`Nothing` のときのみ `fn` を実行し、そうでなければ元のオプションを返します。

```python
from pyfplib import Nothing, Option, Some

def recover() -> Option[int]:
    return Some(9)

print(Nothing().or_else(recover))  # Some(9)
print(Some(1).or_else(recover))    # Some(1)
```

### `xor(other: Option[T]) -> Option[T]`

2 つのオプションのうちちょうど一方だけが `Some` のときに値を返します。

```python
from pyfplib import Nothing, Some

print(Some(1).xor(Nothing()))  # Some(1)
print(Some(1).xor(Some(2)))    # Nothing()
```

### `zip(other: Option[U]) -> Option[tuple[T, U]]`

両方のオプションが `Some` のとき値をペアにします。

```python
from pyfplib import Some

print(Some(1).zip(Some("a")))  # Some((1, 'a'))
```

### `zip_with(other: Option[U], ctr: Callable[[T, U], R]) -> Option[R]`

両方のオプションが `Some` のとき `ctr` で 2 つの値を結合します。

```python
from pyfplib import Some

def add(left: int, right: int) -> int:
    return left + right

print(Some(1).zip_with(Some(2), add))  # Some(3)
```

---

## 演算子

`Option` は `and_then` と `or_else` に対応するよう `&` と `|` をオーバーロードします。

| 式 | 同等 | 説明 |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | `a` が `Some` なら `b`、そうでなければ `Nothing`。 |
| `a & fn` | `a.and_then(lambda _: fn())` | `a` が `Some` なら `fn()` を呼び出します。 |
| `a \| b` | `a.or_else(lambda: b)` | `a` が `Some` なら `a`、そうでなければ `b`。 |
| `a \| fn` | `a.or_else(fn)` | `a` が `Nothing` なら `fn()` を呼び出します。 |

```python
from pyfplib import Nothing, Some

print(Some(1) & Some(2))    # Some(2)
print(Nothing() & Some(2))  # Nothing()
print(Nothing() | Some(2))  # Some(2)
```

---

## 変更

### `push(value: T) -> T`

オプションをその場で変更します。`value` を保存し、以前保持していた値、またはオプションが空だった場合は `value` 自体を返します。

```python
from pyfplib import Option, Some

option: Option[int] = Some(1)
previous = option.push(2)

print(previous)  # 1
print(option)    # Some(2)
```

---

## エラー

- `UnwrapError` — オプションが `Nothing` のときに `unwrap()` が送出します。
- `ExpectedError` — オプションが `Nothing` のときに `expect(message)` が送出します。

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
