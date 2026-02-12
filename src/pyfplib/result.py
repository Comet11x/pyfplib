""" """

__author__ = "Comet11x <>"
__copyright__ = "Copyright 2026, Comet11x"
__license__ = "MIT"
__version__ = "0.1.0"

from typing import Callable, Generic, Optional, TypeVar, Union

from pyfplib.errors import ExpectedError, UnwrapError
from pyfplib.option import Nothing, Option, Some

T = TypeVar("T")
E = TypeVar("E")
R = TypeVar("R")
U = TypeVar("U")


class Result(Generic[T, E]):
    __match_args__ = ("value",)

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

    def if_ok(self, fn: Callable[[T], None]) -> "Result[T, E]":
        """\
        Calls fn function and returns itself.
        The fn function will be called if this option is Ok[T, E].
        """
        return self.inspect(fn)

    def if_err(self, fn: Callable[[E], None]) -> "Result[T, E]":
        """\
        Calls fn function and returns itself.
        The fn function will be called if this option is Err[E].
        """
        return self.inspect_err(fn)

    def ok(self) -> Option[T]:
        """\
        Returns Some[T] if this result is Ok[T, E],
        otherwise it returns Nothing[T].
        """
        return Some(self.__value) if self.is_ok() else Nothing()

    def err(self) -> Option[E]:
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

    def unwrap_or(self, value: T) -> T:
        """Returns a contained value or provided default if Err."""
        return self.__value if self.is_ok() is None else value

    def unwrap_err_or(self, value: E) -> E:
        """Returns a contained value or provided default if Ok."""
        return self.__value if self.is_err() is None else value

    def map(self, fn: Callable[[T], U]) -> "Result[U, E]":
        """Maps a Result[T, E] to Result[U, E]"""
        return Ok(fn(self.__value)) if self.is_ok() else Err(self.__value)

    def map_or(self, default: T, fn: Callable[[T], U]) -> "Result[U, E]":
        """Maps a Result[T] to Result[U]"""
        return fn(self.__value) if self.is_ok() else fn(default)

    def map_or_else(self, default: Callable[[E], T], fn: Callable[[T], U]) -> U:
        """\
        Maps Result[T, E] to U by applying the given function fn to a contained Ok value.
        If the result is None, it applies the given fallback function default to a contained Err value.
        """
        return fn(self.__value) if self.is_ok() else fn(default(self.__value))

    def map_err(self, fn: Callable[[E], U]) -> "Result[T, U]":
        return Err(fn(self.__value)) if self.is_err() else self

    @staticmethod
    def try_call(fn: Callable[..., R], *args, **kwargs) -> "Result[R, E]":
        """Tries to call fn function and returns a result of the execution."""
        try:
            ret: R = fn(*args, **kwargs)
            return Ok[R, E](ret)
        except Exception as err:
            return Err[R, E](err)


class Ok(Result[T, E]):
    """Result constructor."""

    def __init__(self, value: T):
        super().__init__(value=value)


class Err(Result[T, E]):
    """Result constructor."""

    def __init__(self, error: E):
        super().__init__(error=error)
