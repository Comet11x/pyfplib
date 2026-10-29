# pyfplib とは？

**pyfplib** は Rust にインスパイアされた小さな Python 関数型プログラミングライブラリです。オプショナルな値と失敗する可能性のある操作のための明示的な型に加え、シーケンスを扱うための合成可能なヘルパーを提供します。

| レイヤー | モジュール | 目的 |
|---|---|---|
| **Option** | `pyfplib.option` | 存在しない可能性のある値を表現：`Some(value)` または `Nothing()` |
| **Result** | `pyfplib.result` | 成功または失敗を表現：`Ok(value)` または `Err(error)` |
| **関数** | `pyfplib.functools` | `fold`、`find`、`any_of`、`all_of` などのシーケンスヘルパー |

## 設計原則

- **暗黙より明示** — 不在と失敗は値であり、隠れた `None` チェックや散らばった例外ではありません。
- **合成可能** — `map`、`and_then`、`or_else`、演算子オーバーロードにより、上から下へ読めるパイプラインを構築できます。
- **Rust にインスパイア** — API は Rust の馴染み深い `Option` と `Result` のセマンティクスを Python 向けに適応しています。
- **依存関係なし** — ランタイム依存のない純粋な Python。Python 3.12 以降に対応。

## アーキテクチャ

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
     合成可能なパイプライン   シーケンスヘルパー
```

`Option` と `Result` は `pyfplib._core` の同じ実装を共有し、`pyfplib.option` と `pyfplib.result` から再エクスポートされます。ほとんどのユーザーはトップレベルの `pyfplib` パッケージだけで十分です。

## 次のステップ

- [セットアップ](/ja/guide/getting-started) — pyfplib をインストールし、最初のパイプラインを試す
- [Option API](/ja/guide/option) — `Some`、`Nothing`、`Option` の完全なリファレンス
- [Result API](/ja/guide/result) — `Ok`、`Err`、`Result` の完全なリファレンス
- [関数 API](/ja/guide/functools) — シーケンスヘルパーの完全なリファレンス
