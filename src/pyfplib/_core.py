""""""

__author__ = "Comet11x <comet11x@protonmail.com>"
__copyright__ = "Copyright 2026, Comet11x"
__license__ = "MIT"
__version__ = "0.3.0"

from collections.abc import Iterable
from typing import Any, Callable, Generic, Optional, Tuple, TypeVar, Union

from pyfplib.errors import ExpectedError, UnwrapError

T = TypeVar("T")
E = TypeVar("E")
R = TypeVar("R")
U = TypeVar("U")


class Result(Generic[T, E]):
    __match_args__ = ("value",)

    Self = "Result"

    __Fn = type(lambda _: _)

    def __init__(self, *, value: Optional[T] = None, error: Optional[E] = None):
        if error is None:
            self.__value = value
            self.__is_ok = True
        else:
            self.__value = error
            self.__is_ok = False

    @property
    def value(self) -> Union[T, E]:
        """Returns a contained value."""
        return self.__value

    def is_ok(self) -> bool:
        """Returns True if the result is Ok[T, E]."""
        return self.__is_ok

    def is_err(self) -> bool:
        """Returns True if the result is Err[T, E]."""
        return not self.__is_ok

    def inspect(self, fn: Callable[[T], None]) -> "Result[T, E]":
        """\
        Applies the given function fn to a contained value if the result is Ok[T, E].
        """
        if self.is_ok():
            fn(self.__value)
        return self

    def inspect_err(self, fn: Callable[[E], None]) -> "Result[T, E]":
        """\
        Applies the given function fn to a contained value if the result is Err[T, E].
        """
        if self.is_err():
            fn(self.__value)
        return self

    def ok(self) -> "Option[T]":
        """\
        Returns Some[T] if this result is Ok[T, E],
        otherwise it returns Nothing[T].
        """
        return Some(self.__value) if self.is_ok() else Nothing()

    def err(self) -> "Option[E]":
        """\
        Returns Some[Exception] if this result is Err[E],
        otherwise it returns Nothing[Exception].
        """
        return Some(self.__value) if self.is_err() else Nothing()

    def unwrap(self) -> T:
        """
        Extracts a contained value, raising UnwrapError if Err.

        Raises:
            UnwrapError: When attempting to unwrap Err
        """
        if self.is_err():
            msg = "called `Result.unwrap()` on a `Err` value"
            raise UnwrapError(msg)
        return self.__value

    def unwrap_err(self) -> E:
        """
        Extracts a contained error, raising UnwrapError if Ok.

        Raises:
            UnwrapError: When attempting to unwrap Ok
        """
        if self.is_ok():
            msg = "called `Result.unwrap_err()` on a `Ok` value"
            raise UnwrapError(msg)
        return self.__value

    def expect(self, message: str) -> T:
        """Returns a contained value or raises ExpectedError"""
        if self.is_err():
            raise ExpectedError(message)
        return self.__value

    def expect_err(self, message: str) -> E:
        """Returns a contained value or raises ExpectedError"""
        if self.is_ok():
            raise ExpectedError(message)
        return self.__value

    def unwrap_or(self, default: T) -> T:
        """Returns a contained value or provided default if the result is Err[T, E]."""
        return self.__value if self.is_ok() else default

    def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
        return self.__value if self.is_ok() else fn(self.__value)

    def unwrap_err_or(self, default: E) -> E:
        """Returns a contained value or provided default if the result is Ok[T, E]."""
        return self.__value if self.is_err() else default

    def map(self, fn: Callable[[T], U]) -> "Result[U, E]":
        """Maps a Result[T, E] to Result[U, E]"""
        return Ok(fn(self.__value)) if self.is_ok() else Err(self.__value)

    def map_or(self, default: T, fn: Callable[[T], U]) -> "Result[U, E]":
        """Maps a Result[T] to Result[U]"""
        return fn(self.__value) if self.is_ok() else fn(default)

    def map_or_else(self, default: Callable[[E], T], fn: Callable[[T], U]) -> U:
        """
        Maps Result[T, E] to U by applying the given function fn to a contained Ok value.
        If the result is None, it applies the given fallback function default to a contained Err value.
        """
        return fn(self.__value) if self.is_ok() else fn(default(self.__value))

    def map_err(self, fn: Callable[[E], U]) -> "Result[T, U]":
        return Err(fn(self.__value)) if self.is_err() else self

    def flatten(self) -> Self:
        return self.__value.flatten() if isinstance(self.__value, Result) else self

    def flatten_all(self) -> Self:
        return self.__value if isinstance(self.__value, Result) else self

    def __and__(self, other: Union[Self, Callable[[T], Self]]) -> Self:
        return other if self.is_ok() else self

    def and_then(self, fn: Callable[[T], Self]) -> Self:
        return fn(self.__value) if self.is_ok() and isinstance(fn, Result.__Fn) else self

    def __or__(self, other: Union[Self, Callable[[T], Self]]) -> Self:
        return other if self.is_err() else self

    def or_else(self, fn: Callable[[E], Self]) -> Self:
        return fn(self.__value) if self.is_err() and isinstance(fn, Result.__Fn) else self

    @staticmethod
    def try_call(fn: Callable[..., R], *args, **kwargs) -> "Result[R, E]":
        """Tries to call the given function fn and returns an execution result."""
        try:
            ret: R = fn(*args, **kwargs)
            return Ok(ret)
        except Exception as err:
            return Err(err)


class Ok(Result):
    """Result constructor."""

    def __init__(self, value: T):
        super().__init__(value=value)


class Err(Result):
    """Result constructor."""

    def __init__(self, error: E):
        super().__init__(error=error)


class Option(Generic[T]):
    """
    Rust-inspired Option<T> monad for Python.

    Represents a value that is either Some(T) containing data,
    or Nothing() representing absence of value.

    Provides safe null-handling through method chaining
    instead of explicit None checks.
    """

    # Support for structural pattern matching (Python 3.10+)
    __match_args__ = ("value",)

    Self = "Option"

    def __init__(self, value: Optional[T]):
        """
        Internal constructor - use Some(value) or Nothing() instead.

        Args:
            value: The contained value or None for Nothing
        """
        self.__value = value

    @property
    def value(self) -> Optional[T]:
        """Returns the raw contained value (use with caution - may be None)."""
        return self.__value

    def is_some(self) -> bool:
        """Returns True if this Option contains a value (Some[T])."""
        return self.__value is not None

    def is_none(self) -> bool:
        """Returns True if this Option contains no value (Nothing)."""
        return self.__value is None

    def inspect(self, fn: Callable[[T], None]) -> "Option[T]":
        """
        Executes callback if Some[T], otherwise does nothing.
        Returns self for method chaining.

        Args:
            fn: callback to execute with contained value
        """
        if self.__value is not None:
            fn(self.__value)
        return self

    def inspect_none(self, fn: Callable[[], None]) -> "Option[T]":
        """
        Executes callback if Nothing, otherwise does nothing.
        Returns self for method chaining.

        Args:
            fn: callback to execute when no value present
        """
        if self.__value is None:
            fn()
        return self

    def unwrap(self) -> T:
        """
        Extracts the contained value, raising UnwrapError if Nothing.

        Raises:
            UnwrapError: When attempting to unwrap Nothing
        """
        if self.__value is None:
            msg = "called `Option.unwrap()` on a `Nothing` value"
            raise UnwrapError(msg)
        return self.__value

    def expect(self, message: str) -> T:
        """
        Extracts the contained value, raising ExpectedError if Nothing with the given message.

        Args:
            message: an error message

        Raises:
            ExpectedError: When attempting to unwrap Nothing
        """
        if self.__value is None:
            raise ExpectedError(message)
        return self.__value

    def unwrap_or(self, default: T) -> T:
        """
        Returns contained value or a provided default value if it is Nothing.

        Args:
            default:
        """
        return default if self.is_none() else self.__value

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        """Returns the contained Some value or computes it from a closure."""
        return fn() if self.is_none() else self.__value

    def map_or(self, default: U, fn: Callable[[T], U]) -> "Option[U]":
        """

        Args:
            fn: a pure function mapping T to U
        """
        return default if self.is_none() else fn(self.__value)

    def map_or_else(self, default: Callable[[], U], fn: Callable[[T], U]) -> U:
        """
        Maps contained value through a function returning Option[U].
        FlatMaps Option[T] -> Option[U], returns Nothing() if no value.

        Args:
            fn: the function returning Option[U]
        """
        return default() if self.is_none() else fn(self.__value)

    def flatten(self) -> Self:
        return self.__value if isinstance(self.__value, Option) else self

    def flatten_all(self) -> Self:
        return self.__value.flatten_all() if isinstance(self.__value, Option) else self

    def ok_or(self, err: Any) -> "Result":
        Err(err) if self.is_none() else Ok(self.__value)

    def ok_or_else(self, fn: Callable[[], Any]) -> Result[T, Any]:
        Err(fn()) if self.is_none() else Ok(self.__value)

    def __eq__(self, other: object) -> bool:
        """Equality comparison based on contained values."""
        ret: bool = False
        if isinstance(other, Option):
            ret = self.__value == other.value
        return ret

    def __hash__(self):
        return hash(self.__value)

    def __bool__(self) -> bool:
        """Boolean conversion - True if Some[T], False if Nothing."""
        return self.is_some()

    def __and__(self, other: Union[Self, Callable[[T], Self]]) -> Self:
        return other if self.is_some() else self

    def and_then(self, fn: Callable[[T], Self]) -> Self:
        return fn(self.__value) if self.is_some() and isinstance(fn, Result.__Fn) else self

    def __or__(self, other: Union[Self, Callable[[T], Self]]) -> Self:
        return other if self.is_none() else self

    def or_else(self, fn: Callable[[], Self]) -> Self:
        return fn() if self.is_none() and isinstance(fn, Result.__Fn) else self

    def xor(self, other: Self) -> Self:
        if self.is_some() and other.is_none():
            return self
        elif self.is_none() and other.is_some():
            return other
        else:
            return Nothing()

    def push(self, value: T) -> T:
        ret = self.__value if self.is_some() else value
        self.__value = value
        return ret

    @staticmethod
    def from_optional(value: Optional[T] = None) -> "Option[T]":
        """Creates Option[T] from Optional[T]."""
        return Nothing() if value is None else Some(value)

    def zip(self, other: Self) -> Self:
        if self.is_some() and other.is_some():
            return Some((self.__value, other.__value))
        else:
            return Nothing()

    def unzip(self) -> Tuple[Self, Self]:
        if isinstance(self.__value, Iterable):
            acc = []
            for elem in self.__value:
                acc.append(Some(elem))
            return tuple(acc)

    def zip_with(self, other: Self, ctr: Callable[[T, T], U]) -> Self:
        if self.is_some() and other.is_some():
            return Some(ctr(self.__value, other.__value))
        else:
            return Nothing()


class Some(Option[T]):
    """
    Some extends Option[T].
    It is used to create Option[T] containing a value

    Usage:
        Some(123)
        Some("hello")
    """

    def __init__(self, value: T):
        super().__init__(value)


class Nothing(Option[T]):
    """
    Nothing extends Option[T].
    It is used to create empty Option[T]

    Usage:
        Nothing() - no value contained.
    """

    def __init__(self):
        super().__init__(None)
