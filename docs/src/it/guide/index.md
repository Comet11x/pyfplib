# Cos'è pyfplib?

**pyfplib** è una piccola libreria di programmazione funzionale per Python ispirata a Rust. Fornisce tipi espliciti per valori opzionali e operazioni che possono fallire, insieme a una serie di helper componibili per le sequenze.

| Livello | Modulo | Scopo |
|---|---|---|
| **Option** | `pyfplib.option` | Rappresenta un valore che può mancare: `Some(value)` o `Nothing()` |
| **Result** | `pyfplib.result` | Rappresenta successo o fallimento: `Ok(value)` o `Err(error)` |
| **Funzioni** | `pyfplib.functools` | Helper per sequenze come `fold`, `find`, `any_of` e `all_of` |

## Principi di progettazione

- **Esplicito invece di implicito** — assenza e fallimento sono valori, non controlli `None` nascosti o eccezioni sparse.
- **Componibile** — `map`, `and_then`, `or_else` e gli operatori sovraccaricati permettono di costruire pipeline leggibili dall'alto verso il basso.
- **Ispirato a Rust** — l'API segue la familiare semantica di `Option` e `Result` di Rust, adattata a Python.
- **Senza dipendenze** — Python puro senza dipendenze runtime, compatibile con Python 3.12 e versioni successive.

## Architettura

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
      pipeline componibili   helper per sequenze
```

`Option` e `Result` condividono la stessa implementazione in `pyfplib._core` e sono riesportati da `pyfplib.option` e `pyfplib.result`. La maggior parte degli utenti ha bisogno solo del pacchetto `pyfplib` di primo livello.

## Prossimi passi

- [Per Iniziare](/it/guide/getting-started) — installa pyfplib e prova la tua prima pipeline
- [API Option](/it/guide/option) — riferimento completo per `Some`, `Nothing` e `Option`
- [API Result](/it/guide/result) — riferimento completo per `Ok`, `Err` e `Result`
- [API Funzioni](/it/guide/functools) — riferimento completo per gli helper per sequenze
