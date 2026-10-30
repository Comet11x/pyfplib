# Result API

`Result[T, E]` は成功（`Ok`）または失敗（`Err`）を表します。`pyfplib.result` にあり、トップレベルの `pyfplib` パッケージから再エクスポートされます。

```python
from pyfplib import Err, Ok, Result
```

---

## コンストラクタ

### `Ok(value: T)`

成功結果を作成します。

```python
from pyfplib import Ok, Result

result: Result[int, str] = Ok(42)
print(result.is_ok())  # True
print(result.unwrap()) # 42
```

### `Err(error: E)`

失敗結果を作成します。

```python
from pyfplib import Err, Result

result: Result[int, str] = Err("boom")
print(result.is_err())           # True
print(repr(result.unwrap_err())) # 'boom'
```

---

## 検査

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `is_ok()` | `bool` | 結果が `Ok` のとき `True`。 |
| `is_err()` | `bool` | 結果が `Err` のとき `True`。 |
| `value` | `T \| E` | 包含値またはエラー。 |
| `__bool__()` | `bool` | `Ok` で真、`Err` で偽。 |
| `inspect(fn)` | `Result[T, E]` | `Ok` 値で `fn` を呼び出し、`self` を返します。 |
| `inspect_err(fn)` | `Result[T, E]` | `Err` 値で `fn` を呼び出し、`self` を返します。 |
| `ok()` | `Option[T]` | `Ok` なら `Some(value)`、そうでなければ `Nothing()`。 |
| `err()` | `Option[E]` | `Err` なら `Some(error)`、そうでなければ `Nothing()`。 |

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

## 抽出

| メソッド | 戻り値 | 例外 | 説明 |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | `Ok` 値を返すか、`Err` で例外を送出します。 |
| `unwrap_err()` | `E` | `UnwrapError` | `Err` 値を返すか、`Ok` で例外を送出します。 |
| `expect(message)` | `T` | `ExpectedError` | `Ok` 値を返すか、`message` 付きで例外を送出します。 |
| `expect_err(message)` | `E` | `ExpectedError` | `Err` 値を返すか、`message` 付きで例外を送出します。 |
| `unwrap_or(default)` | `T` | — | `Ok` 値または `default` を返します。 |
| `unwrap_or_else(fn)` | `T` | — | `Ok` 値または `fn(error)` を返します。 |
| `unwrap_err_or(default)` | `E` | — | `Err` 値または `default` を返します。 |

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

## パターンマッチング

`Result` は Python の構造的パターンマッチングをサポートします。`Ok(value)` で成功値をバインドし、`Err(error)` でエラーをバインドします。事前に `is_ok()` を呼び出す必要はありません。

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

## 変換

### `map(fn: Callable[[T], U]) -> Result[U, E]`

`Ok` 値に `fn` を適用します。`Err` はそのまま返されます。

```python
from pyfplib import Err, Ok

def triple(value: int) -> int:
    return value * 3

print(Ok(2).map(triple))    # Ok(6)
print(Err("e").map(triple)) # Err('e')
```

### `map_or(default: T, fn: Callable[[T], U]) -> Result[U, E]`

`Ok` 値に `fn` を適用するか、結果が `Err` の場合は `default` に `fn` を適用します。結果は常に `Ok` です。通常の値が必要な場合は `map_or_else` を使用してください。

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

`Ok` 値に `fn` を適用するか、`Err` の場合は `default(error)` を呼び出してそのフォールバック値に `fn` を適用し、通常の値を返します。

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

`Err` 値に `fn` を適用します。`Ok` はそのまま返されます。

```python
from pyfplib import Err, Ok

print(Err("boom").map_err(str.upper))  # Err('BOOM')
print(Ok(1).map_err(str.upper))        # Ok(1)
```

### `flatten() -> Result[T, E]`

ネストを 1 レベル平坦化します。ネストされていない結果はそのまま返されます。

```python
from pyfplib import Ok

print(Ok(Ok(1)).flatten())  # Ok(1)
print(Ok(1).flatten())      # Ok(1)
```

### `flatten_all() -> Result[T, E]`

最も内側の非 `Result` 値に到達するまで、すべてのネスト階層を平坦化します。

```python
from pyfplib import Ok

print(Ok(Ok(Ok(1))).flatten_all())  # Ok(1)
```

---

## 結合

### `and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]`

結果が `Ok` のときのみ `fn` を実行し、そうでなければ `Err` をそのまま返します。

```python
from pyfplib import Err, Ok, Result

def increment(value: int) -> Result[int, str]:
    return Ok(value + 1)

print(Ok(2).and_then(increment))    # Ok(3)
print(Err("e").and_then(increment)) # Err('e')
```

### `or_else(fn: Callable[[E], Result[T, E]]) -> Result[T, E]`

結果が `Err` のときのみ `fn` を実行し、そうでなければ元の `Ok` を返します。

```python
from pyfplib import Err, Ok, Result

def recover(error: str) -> Result[int, str]:
    return Ok(0)

print(Err("e").or_else(recover))  # Ok(0)
print(Ok(1).or_else(recover))     # Ok(1)
```

---

## 演算子

`Result` は `and_then` と `or_else` に対応するよう `&` と `|` をオーバーロードします。

| 式 | 同等 | 説明 |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | `a` が `Ok` なら `b`、そうでなければ `Err`。 |
| `a & fn` | `a.and_then(lambda v: fn(v))` | `a` が `Ok` なら `fn(value)` を呼び出します。 |
| `a \| b` | `a.or_else(lambda _: b)` | `a` が `Ok` なら `a`、そうでなければ `b`。 |
| `a \| fn` | `a.or_else(lambda e: fn(e))` | `a` が `Err` なら `fn(error)` を呼び出します。 |

```python
from pyfplib import Err, Ok

print(Ok(1) & Ok(2))    # Ok(2)
print(Err("e") & Ok(2)) # Err('e')
print(Err("e") | Ok(2)) # Ok(2)
```

---

## 例外処理

### `Result.try_call(fn: Callable[..., R], *args, **kwargs) -> Result[R, Exception]` *（静的）*

指定された引数で `fn` を呼び出し、発生した `Exception` を `Err` に変換します。

```python
from pyfplib import Result

print(Result.try_call(int, "42"))            # Ok(42)
print(Result.try_call(int, "oops").is_err()) # True
```

---

## エラー

- `UnwrapError` — 誤ったバリアントが存在するときに `unwrap()` と `unwrap_err()` が送出します。
- `ExpectedError` — `expect()` と `expect_err()` が指定されたメッセージとともに送出します。

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
