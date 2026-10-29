# SPDX-FileCopyrightText: 2026-present Comet11x
# SPDX-License-Identifier: MIT
"""This module provides Option[T] and Result[T, E]"""

from collections.abc import Callable
from typing import TypeVar, cast, overload

from pyfplib.errors import ExpectedError, UnwrapError

Ts = TypeVar("Ts")


class Result[T, E]:
    """
    Result<T, E> monad for Python.

    Represents a value that is either Some(T) containing data,
    or Nothing() representing absence of value.

    Provides safe null-handling through method chaining
    instead of explicit None checks.
    """

    __match_args__ = ("value",)

    def __init__(self, *, value: T | None = None, error: E | None = None):
        self.__is_ok = error is None
        self.__value: T | E = cast(T, value) if self.__is_ok else cast(E, error)

    @property
    def value(self) -> T | E:
        """Returns a contained value."""
        return self.__value

    def is_ok(self) -> bool:
        """Returns True if the result is Ok[T, E]."""
        return self.__is_ok

    def is_err(self) -> bool:
        """Returns True if the result is Err[T, E]."""
        return not self.__is_ok

    def __bool__(self) -> bool:
        """Boolean conversion - True if Ok, False if Err."""
        return self.is_ok()

    def inspect(self, fn: Callable[[T], None]) -> "Result[T, E]":
        """\
        Applies the given function fn to a contained value if the result is Ok[T, E].
        """
        if self.is_ok():
            fn(cast(T, self.__value))
        return self

    def inspect_err(self, fn: Callable[[E], None]) -> "Result[T, E]":
        """\
        Applies the given function fn to a contained value if the result is Err[T, E].
        """
        if self.is_err():
            fn(cast(E, self.__value))
        return self

    def ok(self) -> "Option[T]":
        """\
        Returns Some[T] if this result is Ok[T, E],
        otherwise it returns Nothing[T].
        """
        return Some(cast(T, self.__value)) if self.is_ok() else Nothing()

    def err(self) -> "Option[E]":
        """\
        Returns Some[Exception] if this result is Err[E],
        otherwise it returns Nothing[Exception].
        """
        return Some(cast(E, self.__value)) if self.is_err() else Nothing()

    def unwrap(self) -> T:
        """
        Extracts a contained value, raising UnwrapError if Err.

        Raises:
            UnwrapError: When attempting to unwrap Err
        """
        if self.is_err():
            msg = "called `Result.unwrap()` on a `Err` value"
            raise UnwrapError(msg)
        value: T = cast(T, self.__value)
        return value

    def unwrap_err(self) -> E:
        """
        Extracts a contained error, raising UnwrapError if Ok.

        Raises:
            UnwrapError: When attempting to unwrap Ok
        """
        if self.is_ok():
            msg = "called `Result.unwrap_err()` on a `Ok` value"
            raise UnwrapError(msg)
        return cast(E, self.__value)

    def expect(self, message: str) -> T:
        """Returns a contained value or raises ExpectedError"""
        if self.is_err():
            raise ExpectedError(message)
        return cast(T, self.__value)

    def expect_err(self, message: str) -> E:
        """Returns a contained value or raises ExpectedError"""
        if self.is_ok():
            raise ExpectedError(message)
        return cast(E, self.__value)

    def unwrap_or(self, default: T) -> T:
        """Returns a contained value or provided default if the result is Err[T, E]."""
        return cast(T, self.__value) if self.is_ok() else default

    def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
        return cast(T, self.__value) if self.is_ok() else fn(cast(E, self.__value))

    def unwrap_err_or(self, default: E) -> E:
        """Returns a contained value or provided default if the result is Ok[T, E]."""
        return cast(E, self.__value) if self.is_err() else default

    def map[U](self, fn: Callable[[T], U]) -> "Result[U, E]":
        """Maps a Result[T, E] to Result[U, E]"""
        if self.is_ok():
            return Ok(fn(self.unwrap()))
        else:
            return Err(self.unwrap_err())

    def map_or[U](self, default: T, fn: Callable[[T], U]) -> "Result[U, E]":
        """Maps a Result[T, E] to Result[U, E]"""
        value: T = cast(T, self.__value) if self.is_ok() else default
        return cast(Result[U, E], Ok(fn(value)))

    def map_or_else[U](self, default: Callable[[E], T], fn: Callable[[T], U]) -> U:
        """
        Maps Result[T, E] to U by applying the given function fn to a contained Ok value.
        If the result is None, it applies the given fallback function default to a contained Err value.
        """
        value: T = cast(T, self.__value) if self.is_ok() else default(self.unwrap_err())
        return fn(value)

    def map_err[U](self, fn: Callable[[E], U]) -> "Result[T, U]":
        if self.is_err():
            res_err: Result[T, U] = Err(fn(cast(E, self.__value)))
            return res_err
        else:
            res_ok: Result[T, U] = Ok(cast(T, self.__value))
            return res_ok

    @overload
    def flatten(self: "Result[Result[T, E], E]") -> "Result[T, E]": ...

    @overload
    def flatten(self: "Result[T, E]") -> "Result[T, E]": ...

    def flatten(self):
        return self.__value if isinstance(self.__value, Result) else self

    @overload
    def flatten_all(self: "Result[Result[T, E], E]") -> "Result[T, E]": ...

    @overload
    def flatten_all(self: "Result[T, E]") -> "Result[T, E]": ...

    def flatten_all(self) -> "Result":
        value: Result | object = self
        while isinstance(value.__value, Result):
            value: Result = value.__value
        return value

    def __and__(self, other: "Result[T, E] | Callable[[T], Result[T, E]]") -> "Result[T, E]":
        if self.is_err():
            return self
        else:
            if isinstance(other, Callable):
                fn = cast(Callable[[T], "Result[T, E]"], other)
                return fn(cast(T, self.__value))
            else:
                return cast(Result[T, E], other)

    def and_then(self, fn: Callable[[T], "Result[T, E]"]) -> "Result[T, E]":
        return fn(cast(T, self.__value)) if self.is_ok() and callable(fn) else self

    def __or__(self, other: "Result[T, E] | Callable[[E], Result[T, E]]") -> "Result[T, E]":
        if self.is_ok():
            res = self
        else:
            if isinstance(other, Callable):
                fn = cast(Callable[[E], "Result[T, E]"], other)
                res = fn(cast(E, self.__value))
            else:
                res = cast(Result[T, E], other)
        return res

    def or_else(self, fn: Callable[[E], "Result[T, E]"]) -> "Result[T, E]":
        return fn(cast(E, self.__value)) if self.is_err() and callable(fn) else self

    @staticmethod
    def try_call[R](fn: Callable[..., R], *args, **kwargs) -> "Result[R, Exception]":
        """Tries to call the given function fn and returns a result of the execution."""
        try:
            ret: R = fn(*args, **kwargs)
            return Ok(ret)
        except Exception as err:  # noqa: BLE001
            return Err(err)


class Ok[T, E](Result[T, E]):
    """Result constructor."""

    def __init__(self, value: T):
        super().__init__(value=value)


class Err[T, E](Result[T, E]):
    """Result constructor."""

    def __init__(self, error: E):
        super().__init__(error=error)


class Option[T]:
    """
    Option<T> monad for Python.

    Represents a value that is either Some(T) containing data,
    or Nothing() representing absence of value.

    Provides safe null-handling through method chaining
    instead of explicit None checks.
    """

    # Support for structural pattern matching (Python 3.10+)
    __match_args__ = ("value",)

    def __init__(self, value: T | None):
        """
        Internal constructor - use Some(value) or Nothing() instead.

        Args:
            value: The contained value or None for Nothing
        """
        self.__value = value

    @property
    def value(self) -> T | None:
        """Returns the raw contained value (use with caution - may be None)."""
        return self.__value

    def is_some(self) -> bool:
        """Returns True if this Option contains a value (Some[T])."""
        return self.__value is not None

    def is_none(self) -> bool:
        """Returns True if this Option contains no value (Nothing)."""
        return self.__value is None

    def __bool__(self) -> bool:
        """Boolean conversion - True if Some[T], False if Nothing."""
        return self.is_some()

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
            default: a value returned if the option is
        """
        return default if self.is_none() else cast(T, self.__value)

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        """Returns the contained Some value or computes it from a closure."""
        return fn() if self.is_none() else cast(T, self.__value)

    def map[U](self, fn: Callable[[T], U]) -> "Option[U]":
        if self.is_some():
            return Some(fn(self.unwrap()))
        else:
            return Nothing()

    def map_or[U](self, default: U, fn: Callable[[T], U]) -> "Option[U]":
        """

        Args:
            fn: a pure function mapping T to U
        """
        value = default if self.is_none() else fn(cast(T, self.__value))
        return Some(value)

    def map_or_else[U](self, default: Callable[[], U], fn: Callable[[T], U]) -> U:
        """
        Maps contained value through a function returning Option[U].
        FlatMaps Option[T] -> Option[U], returns Nothing() if no value.

        Args:
            fn: the function returning Option[U]
        """
        return default() if self.is_none() else fn(cast(T, self.__value))

    @overload
    def flatten(self: "Option[Option[T]]") -> "Option[T]": ...

    @overload
    def flatten(self: "Option[T]") -> "Option[T]": ...

    def flatten(self):
        return self.__value if isinstance(self.__value, Option) else self

    @overload
    def flatten_all(self: "Option[Option[T]]") -> "Option[T]": ...

    @overload
    def flatten_all(self: "Option[T]") -> "Option[T]": ...

    def flatten_all(self) -> "Option[T]":
        value: Option[T] | object = self
        while isinstance(value.__value, Option):
            value = value.__value
        return value

    def ok_or[E](self, err: E) -> Result[T, E]:
        if self.is_none():
            res: Result[T, E] = Err(err)
        else:
            res: Result[T, E] = Ok(self.unwrap())
        return res

    def ok_or_else[E](self, fn: Callable[[], E]) -> Result[T, E]:
        if self.is_none():
            res: Result[T, E] = Err(fn())
        else:
            res: Result[T, E] = Ok(self.unwrap())
        return res

    def __eq__(self, other: object) -> bool:
        """Equality comparison based on contained values."""
        ret: bool = False
        if isinstance(other, Option):
            ret = self.__value == other.value
        return ret

    def __hash__(self):
        return hash(self.__value)

    def __and__[U](self, other: "Option[U] | Callable[[], Option[U]]") -> "Option[U]":
        if self.is_some():
            return cast(Callable[[], Option[U]], other)() if isinstance(other, Callable) else cast(Option[U], other)
        else:
            return Nothing()

    def and_then[U](self, fn: Callable[[T], "Option[U]"]) -> "Option[U]":
        if self.is_some() and callable(fn):
            return fn(cast(T, self.__value))
        else:
            return Nothing()

    def __or__(self, other: "Option[T] | Callable[[], Option[T]]") -> "Option[T]":
        if self.is_some():
            return self
        else:
            return cast(Callable[[], Option[T]], other)() if isinstance(other, Callable) else other

    def or_else(self, fn: Callable[[], "Option[T]"]) -> "Option[T]":
        return fn() if self.is_none() and callable(fn) else self

    def xor(self, other: "Option[T]") -> "Option[T]":
        if self.is_some() and other.is_none():
            return self
        elif self.is_none() and other.is_some():
            return other
        else:
            return Nothing()

    def push(self, value: T) -> T:
        ret = cast(T, self.__value) if self.is_some() else value
        self.__value = value
        return ret

    @staticmethod
    def from_optional(value: T | None = None) -> "Option[T]":
        """Creates Option[T] from Optional[T]."""
        return Nothing() if value is None else Some(value)

    def zip[U](self, other: "Option[U]") -> "Option[tuple[T, U]]":
        if self.is_some() and other.is_some():
            return Some((cast(T, self.__value), cast(U, other.__value)))
        else:
            return Nothing()

    def zip_with[U, R](self, other: "Option[U]", ctr: Callable[[T, U], R]) -> "Option[R]":
        if self.is_some() and other.is_some():
            return Some(ctr(cast(T, self.__value), cast(U, other.__value)))
        else:
            return Nothing()


class Some[T](Option[T]):
    """
    Some extends Option[T].
    It is used to create Option[T] containing a value

    Usage:
        Some(123)
        Some("hello")
    """

    def __init__(self, value: T):
        super().__init__(value)


class Nothing[T](Option[T]):
    """
    Nothing extends Option[T].
    It is used to create empty Option[T]

    Usage:
        Nothing() - no value contained.
    """

    def __init__(self):
        super().__init__(None)
