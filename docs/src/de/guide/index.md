# Was ist pyfplib?

**pyfplib** ist eine kleine, von Rust inspirierte Bibliothek für funktionale Programmierung in Python. Sie bietet explizite Typen für optionale Werte und fehlbare Operationen sowie eine Reihe komponierbarer Helfer für Sequenzen.

| Schicht | Modul | Zweck |
|---|---|---|
| **Option** | `pyfplib.option` | Repräsentiert einen Wert, der fehlen kann: `Some(value)` oder `Nothing()` |
| **Result** | `pyfplib.result` | Repräsentiert Erfolg oder Fehler: `Ok(value)` oder `Err(error)` |
| **Funktionen** | `pyfplib.functools` | Sequenz-Helfer wie `fold`, `find`, `any_of` und `all_of` |

## Designprinzipien

- **Explizit statt implizit** — Abwesenheit und Fehler sind Werte, keine versteckten `None`-Prüfungen oder verstreuten Ausnahmen.
- **Komponierbar** — `map`, `and_then`, `or_else` und Operatorüberladungen ermöglichen Pipelines, die von oben nach unten lesbar sind.
- **Von Rust inspiriert** — die API folgt der vertrauten `Option`- und `Result`-Semantik aus Rust, angepasst an Python.
- **Abhängigkeitsfrei** — reines Python ohne Laufzeitabhängigkeiten, kompatibel mit Python 3.12 und neuer.

## Architektur

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
   komponierbare Pipelines  Sequenz-Helfer
```

`Option` und `Result` nutzen eine gemeinsame Implementierung in `pyfplib._core` und werden aus `pyfplib.option` und `pyfplib.result` re-exportiert. Die meisten Nutzer benötigen nur das Paket `pyfplib` auf oberster Ebene.

## Nächste Schritte

- [Erste Schritte](/de/guide/getting-started) — installieren Sie pyfplib und testen Sie Ihre erste Pipeline
- [Option-API](/de/guide/option) — vollständige Referenz zu `Some`, `Nothing` und `Option`
- [Result-API](/de/guide/result) — vollständige Referenz zu `Ok`, `Err` und `Result`
- [Funktions-API](/de/guide/functools) — vollständige Referenz zu den Sequenz-Helfern
