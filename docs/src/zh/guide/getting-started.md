# 快速开始

## 安装

```bash
pip install -U pyfplib
```

pyfplib 没有运行时依赖，支持 Python 3.12 及更高版本。

## Option

当值可能缺失时使用 `Option`。`Some` 包装一个值，`Nothing` 表示其缺失。

```python
from pyfplib import Nothing, Some

user = Some({"name": "Ada", "email": "ada@example.com"})

email = user.map(lambda u: u.get("email")).unwrap_or("unknown")
print(email)  # ada@example.com

missing = Nothing()
print(missing.unwrap_or("unknown"))  # unknown
```

## Result

使用 `Result` 对可能失败的操作建模，而无需让异常跨越 API 边界。

```python
from pyfplib import Err, Ok, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

print(divide(10, 2).unwrap())                 # 5.0
print(divide(10, 0).unwrap_or(float("nan")))  # nan

# 将异常转换为 Err 值
parsed = Result.try_call(int, "not a number")
print(parsed.is_err())  # True
```

## 函数式辅助

`functools` 模块包含用于常见序列操作的小型辅助函数。

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

## 下一步

- [Option API](/zh/guide/option) — `Some`、`Nothing` 和 `Option` 的完整参考
- [Result API](/zh/guide/result) — `Ok`、`Err` 和 `Result` 的完整参考
- [函数 API](/zh/guide/functools) — 序列辅助函数的完整参考
