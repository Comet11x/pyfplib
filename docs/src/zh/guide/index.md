# 什么是 pyfplib？

**pyfplib** 是一个受 Rust 启发的轻量级 Python 函数式编程库。它为可选值和可能失败的操作提供显式类型，并提供一组可组合的序列辅助函数。

| 层 | 模块 | 用途 |
|---|---|---|
| **Option** | `pyfplib.option` | 表示可能缺失的值：`Some(value)` 或 `Nothing()` |
| **Result** | `pyfplib.result` | 表示成功或失败：`Ok(value)` 或 `Err(error)` |
| **函数** | `pyfplib.functools` | 序列辅助函数，如 `fold`、`find`、`any_of` 和 `all_of` |

## 设计原则

- **显式优于隐式** — 缺失和失败是值，而不是隐藏的 `None` 检查或散落的异常。
- **可组合** — `map`、`and_then`、`or_else` 和运算符重载让你构建从上到下阅读的管道。
- **受 Rust 启发** — API 遵循 Rust 中熟悉的 `Option` 和 `Result` 语义，并适配 Python。
- **无依赖** — 纯 Python，无运行时依赖，兼容 Python 3.12 及更高版本。

## 架构

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
        可组合管道           序列辅助函数
```

`Option` 和 `Result` 在 `pyfplib._core` 中共享同一核心实现，并从 `pyfplib.option` 和 `pyfplib.result` 重新导出。大多数用户只需要顶层的 `pyfplib` 包。

## 后续步骤

- [快速开始](/zh/guide/getting-started) — 安装 pyfplib 并尝试第一个管道
- [Option API](/zh/guide/option) — `Some`、`Nothing` 和 `Option` 的完整参考
- [Result API](/zh/guide/result) — `Ok`、`Err` 和 `Result` 的完整参考
- [函数 API](/zh/guide/functools) — 序列辅助函数的完整参考
