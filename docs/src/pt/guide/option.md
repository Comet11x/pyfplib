# API de Option

`Option[T]` representa um valor que pode estar presente (`Some`) ou ausente (`Nothing`). Ele fica em `pyfplib.option` e é reexportado pelo pacote `pyfplib`.

```python
from pyfplib import Nothing, Option, Some
```

---

## Construtores

### `Some(value: T)`

Envolve um valor diferente de `None` em um `Option`. Como `Option` usa `None` internamente para representar ausência, `Some(None)` se comporta como `Nothing()`.

```python
from pyfplib import Some

print(Some(42).is_some())    # True
print(Some(42).unwrap())     # 42
print(Some(None).is_none())  # True
```

### `Nothing()`

Cria um `Option` vazio. Um `Nothing` sempre é `is_none()`.

```python
from pyfplib import Nothing

print(Nothing().is_none())     # True
print(Nothing().unwrap_or(0))  # 0
```

---

## Inspeção

| Método | Retorna | Descrição |
|---|---|---|
| `is_some()` | `bool` | `True` quando um valor está presente. |
| `is_none()` | `bool` | `True` quando nenhum valor está presente. |
| `value` | `T \| None` | O valor bruto contido (pode ser `None`). |
| `__bool__()` | `bool` | Verdadeiro para `Some`, falso para `Nothing`. |
| `__eq__(other)` | `bool` | Compara os valores contidos quando ambos são `Option`. |
| `__hash__()` | `int` | Calcula o hash do valor contido. |

```python
from pyfplib import Nothing, Some

print(bool(Some(1)), bool(Nothing()))  # (True, False)
print(Some(1) == Some(1))              # True
```

### `inspect(fn: Callable[[T], None]) -> Option[T]`

Chama `fn` com o valor contido quando é `Some`, depois retorna a opção inalterada.

```python
from pyfplib import Option, Some

option: Option[int] = Some(2)
returned = option.inspect(lambda value: print(f"inspected: {value}"))
print(returned)  # Some(2)
```

### `inspect_none(fn: Callable[[], None]) -> Option[T]`

Chama `fn` sem argumentos quando é `Nothing`, depois retorna a opção inalterada.

```python
from pyfplib import Nothing

returned = Nothing().inspect_none(lambda: print("empty"))
print(returned)  # Nothing()
```

---

## Extração

| Método | Retorna | Exceção | Descrição |
|---|---|---|---|
| `unwrap()` | `T` | `UnwrapError` | Retorna o valor ou lança se estiver vazio. |
| `expect(message)` | `T` | `ExpectedError` | Retorna o valor ou lança com `message`. |
| `unwrap_or(default)` | `T` | — | Retorna o valor ou `default`. |
| `unwrap_or_else(fn)` | `T` | — | Retorna o valor ou chama `fn()` para um fallback. |

```python
from pyfplib import Nothing, Some

def fallback() -> int:
    return 10

print(Some(3).unwrap_or(0))               # 3
print(Nothing().unwrap_or(0))             # 0
print(Some(3).unwrap_or_else(fallback))   # 3
print(Nothing().unwrap_or_else(fallback)) # 10
```

---

## Correspondência de padrões

`Option` oferece suporte à correspondência de padrões estruturais do Python. Use `Some(value)` para vincular o valor contido e `Nothing()` para corresponder a um option vazio, sem chamar `is_some()` antes.

```python
from pyfplib import Nothing, Option, Some

def describe(option: Option[int]) -> str:
    match option:
        case Some(value):
            return f"got {value}"
        case Nothing():
            return "nothing"

print(describe(Some(42)))   # got 42
print(describe(Nothing()))  # nothing
```

---

## Transformação

### `map(fn: Callable[[T], U]) -> Option[U]`

Aplica `fn` ao valor contido, envolvendo o resultado em `Some`. `Nothing` permanece `Nothing`.

```python
from pyfplib import Nothing, Some

def double(value: int) -> int:
    return value * 2

print(Some(3).map(double))    # Some(6)
print(Nothing().map(double))  # Nothing()
```

### `map_or(default: U, fn: Callable[[T], U]) -> Option[U]`

Aplica `fn` a um valor `Some` ou usa `default`, e sempre retorna um `Option` (`Some`). Use `map_or_else` quando precisar do valor simples.

```python
from pyfplib import Nothing, Option, Some

def double(value: int) -> int:
    return value * 2

present: Option[int] = Some(3)
empty: Option[int] = Nothing()

print(present.map_or(0, double))  # Some(6)
print(empty.map_or(0, double))    # Some(0)
```

### `map_or_else(default: Callable[[], U], fn: Callable[[T], U]) -> U`

Aplica `fn` quando é `Some`, caso contrário chama `default()`.

```python
from pyfplib import Nothing, Some

def default() -> int:
    return 0

def double(value: int) -> int:
    return value * 2

print(Some(3).map_or_else(default, double))   # 6
print(Nothing().map_or_else(default, double)) # 0
```

### `flatten() -> Option[T]`

Reduz um nível de aninhamento. Uma opção não aninhada é retornada sem alterações.

```python
from pyfplib import Some

print(Some(Some(1)).flatten())  # Some(1)
print(Some(1).flatten())        # Some(1)
```

### `flatten_all() -> Option[T]`

Reduz todos os níveis de aninhamento até alcançar o valor não-option mais interno.

```python
from pyfplib import Some

print(Some(Some(Some(1))).flatten_all())  # Some(1)
```

---

## Conversão

### `ok_or(err: E) -> Result[T, E]`

Converte um `Option` em `Result`, usando `err` quando está vazio.

```python
from pyfplib import Nothing, Some

print(Some(1).ok_or("missing"))   # Ok(1)
print(Nothing().ok_or("missing")) # Err('missing')
```

### `ok_or_else(fn: Callable[[], E]) -> Result[T, E]`

Como `ok_or`, mas chama `fn()` para produzir o erro quando está vazio.

```python
from pyfplib import Nothing

def missing_error() -> str:
    return "missing"

print(Nothing().ok_or_else(missing_error))  # Err('missing')
```

### `from_optional(value: T | None) -> Option[T]` *(estático)*

Cria um `Option` a partir de um valor que pode ser `None`: `None` se torna `Nothing`, e qualquer outro valor se torna `Some`.

```python
from pyfplib import Option

value: int | None = None
print(Option.from_optional(value))  # Nothing()
print(Option.from_optional(5))      # Some(5)
```

---

## Combinação

### `and_then(fn: Callable[[T], Option[U]]) -> Option[U]`

Executa `fn` apenas quando é `Some`; caso contrário retorna `Nothing`.

```python
from pyfplib import Nothing, Option, Some

def increment(value: int) -> Option[int]:
    return Some(value + 1)

print(Some(2).and_then(increment))   # Some(3)
print(Nothing().and_then(increment)) # Nothing()
```

### `or_else(fn: Callable[[], Option[T]]) -> Option[T]`

Executa `fn` apenas quando é `Nothing`; caso contrário retorna a opção original.

```python
from pyfplib import Nothing, Option, Some

def recover() -> Option[int]:
    return Some(9)

print(Nothing().or_else(recover))  # Some(9)
print(Some(1).or_else(recover))    # Some(1)
```

### `xor(other: Option[T]) -> Option[T]`

Retorna um valor apenas quando exatamente uma das duas opções é `Some`.

```python
from pyfplib import Nothing, Some

print(Some(1).xor(Nothing()))  # Some(1)
print(Some(1).xor(Some(2)))    # Nothing()
```

### `zip(other: Option[U]) -> Option[tuple[T, U]]`

Emparelha os valores quando ambas as opções são `Some`.

```python
from pyfplib import Some

print(Some(1).zip(Some("a")))  # Some((1, 'a'))
```

### `zip_with(other: Option[U], ctr: Callable[[T, U], R]) -> Option[R]`

Combina ambos os valores com `ctr` quando ambas as opções são `Some`.

```python
from pyfplib import Some

def add(left: int, right: int) -> int:
    return left + right

print(Some(1).zip_with(Some(2), add))  # Some(3)
```

---

## Operadores

`Option` sobrecarrega `&` e `|` para refletir `and_then` e `or_else`.

| Expressão | Equivalente | Descrição |
|---|---|---|
| `a & b` | `a.and_then(lambda _: b)` | Retorna `b` quando `a` é `Some`, caso contrário `Nothing`. |
| `a & fn` | `a.and_then(lambda _: fn())` | Chama `fn()` quando `a` é `Some`. |
| `a \| b` | `a.or_else(lambda: b)` | Retorna `a` quando é `Some`, caso contrário `b`. |
| `a \| fn` | `a.or_else(fn)` | Chama `fn()` quando `a` é `Nothing`. |

```python
from pyfplib import Nothing, Some

print(Some(1) & Some(2))    # Some(2)
print(Nothing() & Some(2))  # Nothing()
print(Nothing() | Some(2))  # Some(2)
```

---

## Mutação

### `push(value: T) -> T`

Modifica a opção no local: armazena `value` e retorna o valor anteriormente contido, ou o próprio `value` se a opção estava vazia.

```python
from pyfplib import Option, Some

option: Option[int] = Some(1)
previous = option.push(2)

print(previous)  # 1
print(option)    # Some(2)
```

---

## Erros

- `UnwrapError` — lançada por `unwrap()` quando a opção é `Nothing`.
- `ExpectedError` — lançada por `expect(message)` quando a opção é `Nothing`.

```python
from pyfplib import Nothing
from pyfplib.errors import ExpectedError, UnwrapError

try:
    Nothing().unwrap()
except UnwrapError as exc:
    print(exc)  # called `Option.unwrap()` on a `Nothing` value

try:
    Nothing().expect("value is required")
except ExpectedError as exc:
    print(exc)  # value is required
```
