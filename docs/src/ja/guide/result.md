# Result API

`Result[T, E]` は成功（`Ok`）または失敗（`Err`）を表します。`pyfplib.result` にあり、トップレベルの `pyfplib` パッケージから再エクスポートされます。

```python
from pyfplib import Err, Ok, Result
```

---

## コンストラクタ

### `Ok(value)`

成功結果を作成します。

```python
>>> Ok(42).is_ok()
True
>>> Ok(42).unwrap()
42
```

### `Err(error)`

失敗結果を作成します。

```python
>>> Err("boom").is_err()
True
>>> Err("boom").unwrap_err()
'boom'
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
>>> bool(Ok(1)), bool(Err("e"))
(True, False)
>>> Ok(1).ok()
Some(1)
>>> Err("e").ok()
Nothing()
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
>>> Ok(1).unwrap_or(0)
1
>>> Err("e").unwrap_or(0)
0
>>> Err("e").unwrap_or_else(lambda e: len(e))
1
```

---

## 変換

### `map(fn) -> Result[U, E]`

`Ok` 値に `fn` を適用します。`Err` はそのまま返されます。

```python
>>> Ok(2).map(lambda v: v * 3)
Ok(6)
>>> Err("e").map(lambda v: v * 3)
Err('e')
```

### `map_or(default, fn) -> Result[U, E]`

`Ok` 値に `fn` を適用するか `default` を使用します。結果は常に `Ok` です。

```python
>>> Ok(2).map_or(0, lambda v: v * 3)
Ok(6)
>>> Err("e").map_or(0, lambda v: v * 3)
Ok(0)
```

### `map_or_else(default, fn) -> U`

`Ok` 値に `fn` を適用するか、`Err` で `default(error)` を呼び出します。

```python
>>> Ok(2).map_or_else(lambda e: 0, lambda v: v * 3)
6
>>> Err("e").map_or_else(lambda e: len(e), lambda v: v * 3)
3
```

### `map_err(fn) -> Result[T, U]`

`Err` 値に `fn` を適用します。`Ok` はそのまま返されます。

```python
>>> Err("boom").map_err(str.upper)
Err('BOOM')
>>> Ok(1).map_err(str.upper)
Ok(1)
```

### `flatten() -> Result[T, E]`

1 段階のネストを平坦化します。

```python
>>> Ok(Ok(1)).flatten()
Ok(1)
>>> Ok(1).flatten()
Ok(1)
```

### `flatten_all() -> Result[T, E]`

すべてのネストを平坦化します。

```python
>>> Ok(Ok(Ok(1))).flatten_all()
Ok(1)
```

---

## 結合

### `and_then(fn) -> Result[T, E]`

結果が `Ok` のときのみ `fn` を実行し、そうでなければ `Err` をそのまま返します。

```python
>>> Ok(2).and_then(lambda v: Ok(v + 1))
Ok(3)
>>> Err("e").and_then(lambda v: Ok(v + 1))
Err('e')
```

### `or_else(fn) -> Result[T, E]`

結果が `Err` のときのみ `fn` を実行し、そうでなければ元の `Ok` を返します。

```python
>>> Err("e").or_else(lambda e: Ok(0))
Ok(0)
>>> Ok(1).or_else(lambda e: Ok(0))
Ok(1)
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
>>> Ok(1) & Ok(2)
Ok(2)
>>> Err("e") & Ok(2)
Err('e')
>>> Err("e") | Ok(2)
Ok(2)
```

---

## 例外処理

### `Result.try_call(fn, *args, **kwargs) -> Result[R, Exception]` *（静的）*

`fn` を呼び出し、発生した例外を `Err` に変換します。

```python
>>> Result.try_call(int, "42")
Ok(42)
>>> Result.try_call(int, "oops").is_err()
True
```

---

## エラー

- `UnwrapError` — 誤ったバリアントが存在するときに `unwrap()` と `unwrap_err()` が送出します。
- `ExpectedError` — `expect()` と `expect_err()` が指定されたメッセージとともに送出します。

```python
from pyfplib import Err
from pyfplib.errors import UnwrapError

try:
    Err("boom").unwrap()
except UnwrapError as exc:
    print(exc)
```
