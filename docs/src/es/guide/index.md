# ¿Qué es pyfplib?

**pyfplib** es una pequeña biblioteca de programación funcional para Python inspirada en Rust. Proporciona tipos explícitos para valores opcionales y operaciones que pueden fallar, junto con un conjunto de ayudantes componibles para secuencias.

| Capa | Módulo | Propósito |
|---|---|---|
| **Option** | `pyfplib.option` | Representa un valor que puede faltar: `Some(value)` o `Nothing()` |
| **Result** | `pyfplib.result` | Representa éxito o fallo: `Ok(value)` o `Err(error)` |
| **Funciones** | `pyfplib.functools` | Ayudantes de secuencia como `fold`, `find`, `any_of` y `all_of` |

## Principios de diseño

- **Explícito en lugar de implícito** — la ausencia y el fallo son valores, no comprobaciones `None` ocultas ni excepciones dispersas.
- **Componible** — `map`, `and_then`, `or_else` y los operadores sobrecargados permiten construir pipelines legibles de arriba a abajo.
- **Inspirado en Rust** — la API sigue la semántica familiar de `Option` y `Result` de Rust, adaptada a Python.
- **Sin dependencias** — Python puro sin dependencias de tiempo de ejecución, compatible con Python 3.12 y superior.

## Arquitectura

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
   pipelines componibles   ayudantes de secuencia
```

`Option` y `Result` comparten la misma implementación en `pyfplib._core` y se reexportan desde `pyfplib.option` y `pyfplib.result`. La mayoría de los usuarios solo necesitan el paquete `pyfplib` de nivel superior.

## Siguientes pasos

- [Primeros Pasos](/es/guide/getting-started) — instala pyfplib y prueba tu primer pipeline
- [API de Option](/es/guide/option) — referencia completa de `Some`, `Nothing` y `Option`
- [API de Result](/es/guide/result) — referencia completa de `Ok`, `Err` y `Result`
- [API de Funciones](/es/guide/functools) — referencia completa de los ayudantes de secuencia
