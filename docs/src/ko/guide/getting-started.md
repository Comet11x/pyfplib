# 시작하기

## 설치

```bash
pip install -U pyfplib
```

pyfplib는 런타임 의존성이 없으며 Python 3.12 이상을 지원합니다.

## Option

값이 없을 수 있을 때 `Option`을 사용하세요. `Some`은 값을 감싸고 `Nothing`은 부재를 나타냅니다.

```python
from pyfplib import Nothing, Some

user = Some({"name": "Ada", "email": "ada@example.com"})

email = user.map(lambda u: u.get("email")).unwrap_or("unknown")
print(email)  # ada@example.com

missing = Nothing()
print(missing.unwrap_or("unknown"))  # unknown
```

## Result

API 경계를 넘어 예외를 던지지 않고 실패할 수 있는 연산을 모델링하려면 `Result`를 사용하세요.

```python
from pyfplib import Err, Ok, Result

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

print(divide(10, 2).unwrap())                 # 5.0
print(divide(10, 0).unwrap_or(float("nan")))  # nan

# 예외를 Err 값으로 변환
parsed = Result.try_call(int, "not a number")
print(parsed.is_err())  # True
```

## 함수형 도우미

`functools` 모듈에는 일반적인 시퀀스 연산을 위한 작은 도우미가 있습니다.

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

## 다음 단계

- [Option API](/ko/guide/option) — `Some`, `Nothing`, `Option` 전체 참조
- [Result API](/ko/guide/result) — `Ok`, `Err`, `Result` 전체 참조
- [함수 API](/ko/guide/functools) — 시퀀스 도우미 전체 참조
