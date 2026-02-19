# Changelog

All notable changes to this project will be documented in this file.

<!-- ignore lint rules that are often triggered by content generated from commits / git-cliff -->
<!-- markdownlint-disable line-length no-bare-urls ul-style emphasis-style -->

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
## How do I make a good changelog?
Guiding Principles

- Changelogs are for humans, not machines.
- There should be an entry for every single version.
- The same types of changes should be grouped.
- Versions and sections should be linkable.
- The latest version comes first.
- The release date of each version is displayed.
- Mention whether you follow Semantic Versioning.

Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.
-->

## [Unreleased]

- v0.3 Documentation

## [0.2.3] - 2026-02-20

### Fixed

- `find` function from `functools`

## [0.2.2] - 2026-02-13

### Fixed

- [Result methods](https://github.com/Comet11x/pyfplib/issues/1)

## [0.2.0/0.2.1] - 2026-02-13

### Added

- `Iterator`.
  
### Updated

- `Result`;
- `functools` module.

### Breaking changes

#### Renamed

- `functions` to `functools` module

### Removed

- `Result`
  - `if_ok` method, it was renamed to `inspect`;
  - `if_err` method, it was renamed to `inspect_err`.

## [0.1.1] - 2026-02-09

### Fixed

- `Result` monad.
- `Option` monad.
- `Either` monad

## [0.1.0] - 2026-02-02

### Added

- `Result` monad.
- `Option` monad.
- `Either` monad
- `functions` module
