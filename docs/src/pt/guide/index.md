# O que é pyfplib?

**pyfplib** é uma pequena biblioteca de programação funcional para Python inspirada em Rust. Ela fornece tipos explícitos para valores opcionais e operações que podem falhar, além de um conjunto de auxiliares combináveis para sequências.

| Camada | Módulo | Objetivo |
|---|---|---|
| **Option** | `pyfplib.option` | Representa um valor que pode estar ausente: `Some(value)` ou `Nothing()` |
| **Result** | `pyfplib.result` | Representa sucesso ou falha: `Ok(value)` ou `Err(error)` |
| **Funções** | `pyfplib.functools` | Auxiliares de sequência como `fold`, `find`, `any_of` e `all_of` |

## Princípios de design

- **Explícito em vez de implícito** — ausência e falha são valores, não verificações `None` ocultas ou exceções espalhadas.
- **Combinável** — `map`, `and_then`, `or_else` e operadores sobrecarregados permitem construir pipelines legíveis de cima para baixo.
- **Inspirado em Rust** — a API segue a semântica familiar de `Option` e `Result` do Rust, adaptada para Python.
- **Sem dependências** — Python puro sem dependências de runtime, compatível com Python 3.12 e superior.

## Arquitetura

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
   pipelines combináveis   auxiliares de sequência
```

`Option` e `Result` compartilham a mesma implementação em `pyfplib._core` e são reexportados de `pyfplib.option` e `pyfplib.result`. A maioria dos usuários precisa apenas do pacote `pyfplib` de nível superior.

## Próximos passos

- [Primeiros Passos](/pt/guide/getting-started) — instale o pyfplib e experimente seu primeiro pipeline
- [API de Option](/pt/guide/option) — referência completa para `Some`, `Nothing` e `Option`
- [API de Result](/pt/guide/result) — referência completa para `Ok`, `Err` e `Result`
- [API de Funções](/pt/guide/functools) — referência completa para os auxiliares de sequência
