# Option API

`Option[T]` は存在する値（`Some`）または存在しない値（`Nothing`）を表します。`pyfplib.option` にあり、トップレベルの `pyfplib` パッケージから再エクスポートされます。

```python
from pyfplib import Nothing, Option, Some
```

---

## コンストラクタ

### `Some(value)`

値を `Option` で包みます。`Some` は常に `is_some()` です。

```python
>>> Some(42).is_some()
True
>>> Some(42).unwrap()
42
```

### `Nothing()`

空の `Option` を作成します。`Nothing` は常に `is_none()` です。

```python
>>> Nothing().is_none()
True
>>> Nothing().unwrap_or(0)
0
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
>>> bool(Some(1)), bool(Nothing())
(True, False)
>>> Some(1) == Some(1)
True
```

### `inspect(fn) -> Option[T]`

`Some` のとき包含値で `fn` を呼び出し、その後オプションをそのまま返します。

```python
>>> Some(2).inspect(lambda v: print(v))
2
Some(2)
```

### `inspect_none(fn) -> Option[T]`

`Nothing` のとき引数なしで `fn` を呼び出し、その後オプションをそのまま返します。

```python
>>> Nothing().inspect_none(lambda: print("empty"))
empty
Nothing()
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
>>> Some(3).unwrap_or(0)
3
>>> Nothing().unwrap_or(0)
0
>>> Nothing().unwrap_or_else(lambda: 10)
10
```

---

## 変換

### `map(fn) -> Option[U]`

包含値に `fn` を適用し、結果を `Some` で包みます。`Nothing` は `Nothing` のままです。

```python
>>> Some(3).map(lambda v: v * 2)
Some(6)
>>> Nothing().map(lambda v: v * 2)
Nothing()
```

### `map_or(default, fn) -> Option[U]`

`Some` のとき `fn` を適用し、そうでなければ `default` を使用します。結果は常に `Some` で包まれます。

```python
>>> Some(3).map_or(0, lambda v: v * 2)
Some(6)
>>> Nothing().map_or(0, lambda v: v * 2)
Some(0)
```

### `map_or_else(default, fn) -> U`

`Some` のとき `fn` を適用し、そうでなければ `default()` を呼び出します。

```python
>>> Some(3).map_or_else(lambda: 0, lambda v: v * 2)
6
>>> Nothing().map_or_else(lambda: 0, lambda v: v * 2)
0
```

### `flatten() -> Option[T]`

1 段階のネストを平坦化します。

```python
>>> Some(Some(1)).flatten()
Some(1)
>>> Some(1).flatten()
Some(1)
```

### `flatten_all() -> Option[T]`

すべてのネストを平坦化します。

```python
>>> Some(Some(Some(1))).flatten_all()
Some(1)
```

---

## Result への変換

### `ok_or(err) -> Result[T, E]`

`Option` を `Result` に変換し、空の場合は `err` を使用します。

```python
>>> Some(1).ok_or("missing")
Ok(1)
>>> Nothing().ok_or("missing")
Err('missing')
```

### `ok_or_else(fn) -> Result[T, E]`

`ok_or` と同様ですが、空の場合に `fn()` を呼び出してエラーを生成します。

```python
>>> Nothing().ok_or_else(lambda: "missing")
Err('missing')
```

### `from_optional(value) -> Option[T]` *（静的）*

`None` の可能性がある値から `Option` を構築します。

```python
>>> Option.from_optional(None)
Nothing()
>>> Option.from_optional(5)
Some(5)
```

---

## 結合

### `and_then(fn) -> Option[U]`

`Some` のときのみ `fn` を実行し、そうでなければ `Nothing` を返します。

```python
>>> Some(2).and_then(lambda v: Some(v + 1))
Some(3)
>>> Nothing().and_then(lambda v: Some(v + 1))
Nothing()
```

### `or_else(fn) -> Option[T]`

`Nothing` のときのみ `fn` を実行し、そうでなければ元のオプションを返します。

```python
>>> Nothing().or_else(lambda: Some(9))
Some(9)
>>> Some(1).or_else(lambda: Some(9))
Some(1)
```

### `xor(other) -> Option[T]`

2 つのオプションのうちちょうど一方だけが `Some` のときに値を返します。

```python
>>> Some(1).xor(Nothing())
Some(1)
>>> Some(1).xor(Some(2))
Nothing()
```

### `zip(other) -> Option[tuple[T, U]]`

両方のオプションが `Some` のとき値をペアにします。

```python
>>> Some(1).zip(Some("a"))
Some((1, 'a'))
```

### `zip_with(other, ctr) -> Option[R]`

両方のオプションが `Some` のとき `ctr` で 2 つの値を結合します。

```python
>>> Some(1).zip_with(Some(2), lambda a, b: a + b)
Some(3)
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
>>> Some(1) & Some(2)
Some(2)
>>> Nothing() & Some(2)
Nothing()
>>> Nothing() | Some(2)
Some(2)
```

---

## 変更

### `push(value) -> T`

`value` を保存し、以前保持していた値（オプションが空だった場合は `value`）を返します。

```python
>>> opt = Some(1)
>>> opt.push(2)
1
>>> opt
Some(2)
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
    print(exc)
```
