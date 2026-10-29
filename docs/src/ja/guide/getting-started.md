# セットアップ

## インストール

```bash
pip install -U pyfplib
```

pyfplib はランタイム依存がなく、Python 3.12 以降をサポートします。

## Option

値が存在しない可能性がある場合は `Option` を使用します。`Some` は値を包み、`Nothing` はその不在を表します。

```python
from pyfplib import Nothing, Some

user = Some({"name": "Ada", "email": "ada@example.com"})

email = user.map(lambda u: u.get("email")).unwrap_or("unknown")
print(email)  # ada@example.com

missing = Nothing()
print(missing.unwrap_or("unknown"))  # unknown
```

## Result

API 境界を越えて例外を投げずに、失敗する可能性のある操作をモデル化するには `Result` を使用します。

```python
from pyfplib import Err, Ok, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

print(divide(10, 2).unwrap())                 # 5.0
print(divide(10, 0).unwrap_or(float("nan")))  # nan

# 例外を Err 値に変換
parsed = Result.try_call(int, "not a number")
print(parsed.is_err())  # True
```

## 関数型ヘルパー

`functools` モジュールには、一般的なシーケンス操作のための小さなヘルパーがあります。

```python
from pyfplib import all_of, any_of, find, fold, head, tail
from pyfplib import Nothing, Some

numbers = [1, 2, 3, 4, 5]

print(head(numbers))                       # Some(1)
print(tail(numbers))                       # [2, 3, 4, 5]
print(any_of(lambda n: n > 4, numbers))    # True
print(all_of(lambda n: n > 0, numbers))    # True
print(find(lambda n: Some(n) if n % 2 == 0 else Nothing(), numbers))  # Some(2)

total = fold(lambda acc, n: acc.unwrap_or(0) + n, numbers, 0)
print(total)  # Some(15)
```

## 次のステップ

- [Option API](/ja/guide/option) — `Some`、`Nothing`、`Option` の完全なリファレンス
- [Result API](/ja/guide/result) — `Ok`、`Err`、`Result` の完全なリファレンス
- [関数 API](/ja/guide/functools) — シーケンスヘルパーの完全なリファレンス
