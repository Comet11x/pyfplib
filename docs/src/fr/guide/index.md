# Qu'est-ce que pyfplib ?

**pyfplib** est une petite bibliothèque de programmation fonctionnelle pour Python inspirée de Rust. Elle fournit des types explicites pour les valeurs optionnelles et les opérations pouvant échouer, ainsi qu'un ensemble de helpers composables pour les séquences.

| Couche | Module | Objectif |
|---|---|---|
| **Option** | `pyfplib.option` | Représente une valeur qui peut être absente : `Some(value)` ou `Nothing()` |
| **Result** | `pyfplib.result` | Représente le succès ou l'échec : `Ok(value)` ou `Err(error)` |
| **Fonctions** | `pyfplib.functools` | Helpers de séquence comme `fold`, `find`, `any_of` et `all_of` |

## Principes de conception

- **Explicite plutôt qu'implicite** — l'absence et l'échec sont des valeurs, pas des vérifications `None` cachées ni des exceptions dispersées.
- **Composable** — `map`, `and_then`, `or_else` et les opérateurs surchargés permettent de construire des pipelines lisibles de haut en bas.
- **Inspiré de Rust** — l'API suit la sémantique familière de `Option` et `Result` de Rust, adaptée à Python.
- **Sans dépendance** — Python pur sans dépendances d'exécution, compatible avec Python 3.12 et versions ultérieures.

## Architecture

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
   pipelines composables   helpers de séquence
```

`Option` et `Result` partagent la même implémentation dans `pyfplib._core` et sont réexportés depuis `pyfplib.option` et `pyfplib.result`. La plupart des utilisateurs n'ont besoin que du paquet `pyfplib` de niveau supérieur.

## Prochaines étapes

- [Pour Commencer](/fr/guide/getting-started) — installez pyfplib et essayez votre premier pipeline
- [API Option](/fr/guide/option) — référence complète pour `Some`, `Nothing` et `Option`
- [API Result](/fr/guide/result) — référence complète pour `Ok`, `Err` et `Result`
- [API Fonctions](/fr/guide/functools) — référence complète pour les helpers de séquence
