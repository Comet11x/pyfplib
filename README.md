# PyFPLib

[![PyPI - Version](https://img.shields.io/pypi/v/pyfplib.svg)](https://pypi.org/project/pyfplib)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyfplib.svg)](https://pypi.org/project/pyfplib)
[![Tests](https://github.com/comet11x/pyfplib/actions/workflows/test.yml/badge.svg)](https://github.com/comet11x/pyfplib/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/Comet11x/pyfplib/badge.svg?branch=dev)](https://coveralls.io/github/Comet11x/pyfplib?branch=dev)

-----

## 🎯 Description

PyFPLib is a tiny Rust-inspired functional programming library for Python.
It can serve as a basis for monadic computations in your Python code.

## 📦 Installation

```shell
pip install -U pyfplib
```

## 🚀 Examples

### Option

```python
from pyfplib import Nothing, Option, Some

age: Option[int] = Option.from_optional(30)

print(age.map(lambda x: x + 1))       # Some(31)
print(Nothing().map(lambda x: x + 1)) # Nothing()
print(age.unwrap_or(0))               # 30
print(Nothing().unwrap_or(0))         # 0
print(age.ok_or("missing"))           # Ok(30)
```

### Result

```python
from pyfplib import Err, Ok, Result

def parse_int(value: str) -> Result[int, str]:
    try:
        return Ok(int(value))
    except ValueError:
        return Err(f"not an integer: {value}")

print(parse_int("42").map(lambda x: x * 2)) # Ok(84)
print(parse_int("nope").map_err(str.upper)) # Err('NOT AN INTEGER: NOPE')
print(parse_int("nope").unwrap_or(0))       # 0

print(Result.try_call(int, "42"))           # Ok(42)
print(Result.try_call(int, "nope"))         # Err(ValueError(...))

def half(x: int) -> Result[int, str]:
    return Ok(x // 2) if x % 2 == 0 else Err(f"{x} is odd")

print(Ok(8).and_then(half).and_then(half).map(lambda x: x + 1)) # Ok(3)
print(Ok(9).and_then(half))                                     # Err('9 is odd')
```

### Functional helpers

```python
from pyfplib import Nothing, Some, all_of, any_of, find, fold, head, index, last, none_of, tail

numbers = [1, 2, 3, 4, 5]

print(any_of(lambda x: x > 4, numbers))  # True
print(all_of(lambda x: x > 0, numbers))  # True
print(none_of(lambda x: x < 0, numbers)) # True

print(head(numbers))  # Some(1)
print(last(numbers))  # Some(5)
print(tail(numbers))  # [2, 3, 4, 5]
print(index(3, numbers)) # Some(2)

print(fold(lambda acc, x: acc.unwrap_or(0) + x, numbers, 0)) # Some(15)
print(find(lambda x: Some(x) if x % 2 == 0 else Nothing(), numbers)) # Some(2)
```

### Pattern matching

```python
from pyfplib import Err, Nothing, Ok, Option, Result, Some

option: Option[int] = Some(42)
match option:
    case Some(value):
        print(f"got {value}") # got 42
    case Nothing():
        print("nothing")

result: Result[int, str] = Err("boom")
match result:
    case Ok(value):
        print(f"ok: {value}")
    case Err(error):
        print(f"error: {error}") # error: boom
```


## 📖 Documentation

[Documentation pages](https://comet11x.github.io/pyfplib/).


## License

`pyfplib` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
