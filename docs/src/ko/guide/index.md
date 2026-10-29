# pyfplib란?

**pyfplib**은 Rust에서 영감을 받은 작은 Python 함수형 프로그래밍 라이브러리입니다. 선택적 값과 실패할 수 있는 연산을 위한 명시적 타입과 함께 시퀀스를 다루는 조합 가능한 도우미를 제공합니다.

| 계층 | 모듈 | 목적 |
|---|---|---|
| **Option** | `pyfplib.option` | 없을 수 있는 값을 표현: `Some(value)` 또는 `Nothing()` |
| **Result** | `pyfplib.result` | 성공 또는 실패를 표현: `Ok(value)` 또는 `Err(error)` |
| **함수** | `pyfplib.functools` | `fold`, `find`, `any_of`, `all_of` 같은 시퀀스 도우미 |

## 설계 원칙

- **암시적보다 명시적** — 부재와 실패는 숨겨진 `None` 검사나 흩어진 예외가 아닌 값입니다.
- **조합 가능** — `map`, `and_then`, `or_else` 및 연산자 오버로딩으로 위에서 아래로 읽히는 파이프라인을 만들 수 있습니다.
- **Rust에서 영감** — API는 Rust의 익숙한 `Option` 및 `Result` 의미를 Python에 맞게 적용합니다.
- **의존성 없음** — 런타임 의존성이 없는 순수 Python, Python 3.12 이상과 호환됩니다.

## 아키텍처

```
                 pyfplib
        ┌───────────┼───────────┐
        │           │           │
     Option       Result     functools
   Some/Nothing  Ok/Err     fold, find,
        │           │        any_of, ...
        └─────┬─────┘           │
              │                 │
              ▼                 ▼
      조합 가능한 파이프라인   시퀀스 도우미
```

`Option`과 `Result`는 `pyfplib._core`의 동일한 구현을 공유하며 `pyfplib.option`과 `pyfplib.result`에서 다시 내보냅니다. 대부분의 사용자는 최상위 `pyfplib` 패키지만 있으면 됩니다.

## 다음 단계

- [시작하기](/ko/guide/getting-started) — pyfplib를 설치하고 첫 파이프라인을 시험해 보세요
- [Option API](/ko/guide/option) — `Some`, `Nothing`, `Option` 전체 참조
- [Result API](/ko/guide/result) — `Ok`, `Err`, `Result` 전체 참조
- [함수 API](/ko/guide/functools) — 시퀀스 도우미 전체 참조
