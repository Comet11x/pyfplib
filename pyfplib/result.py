"""This module provides Result[T] type
and two constructors of Option: Ok[T] and Err[T].
"""

from typing import Any, Callable, Generic, TypeVar, cast

from mypy_extensions import KwArg, VarArg

from pyfplib.option import Nothing, Option, Some

T = TypeVar("T")
R = TypeVar("R")
U = TypeVar("U")


class _Result(Generic[T]):

    __match_args__ = ("value",)

    def __init__(self, value: T | Exception):
        self.__value = value
        self.__is_ok = not isinstance(value, Exception)

    @property
    def value(self) -> T | Exception:
        """Returns a raw value."""
        return self.__value

    def is_ok(self) -> bool:
        """Returns True if the option is Ok[T]."""
        return self.__is_ok

    def is_err(self) -> bool:
        """Returns True if the option is Err[T]."""
        return not self.__is_ok

    def if_ok(self, fn: Callable[[T], None]) -> "Result[T]":
        """\
        Calls fn function and returns itself.
        The fn function will be called if this option is Ok[T].
        """
        if self.is_ok():
            fn(cast(T, self.__value))
        return self

    def if_err(self, fn: Callable[[Exception], None]) -> "Result[T]":
        """\
        Calls fn function and returns itself.
        The fn function will be called if this option is Err[T].
        """
        if self.is_err():
            fn(cast(Exception, self.__value))
        return self

    def ok(self) -> Option[T]:
        """\
        Returns Some[T] if this option is Ok[T],
        otherwise it returns Nothing[T].
        """
        return Some[T](cast(T, self.__value)) if self.is_ok() else Nothing[T]()

    def err(self) -> Option[Exception]:
        """\
        Returns Some[Exception] if this option is Err[T],
        otherwise it returns Nothing[Exception].
        """
        option: Option[Exception]
        if self.is_err():
            option = Some[Exception](cast(Exception, self.__value))
        else:
            option = Nothing[Exception]()
        return option

    def map(self, fn: Callable[[T], U]) -> "Result[U]":
        """Maps an Result[T] to Result[U]"""
        result: Result[U]
        if self.is_ok():
            result = Ok[U](fn(cast(T, self.__value)))
        else:
            result = Err[U](cast(Exception, self.__value))
        return result

    def map_from(self, fn: Callable[[T], "Result[U]"]) -> "Result[U]":
        """Maps an Result[T] to Result[U]"""
        result: Result[U]
        if self.is_ok():
            result = fn(cast(T, self.__value))
        else:
            result = Err[U](cast(Exception, self.__value))
        return result


class Ok(_Result[T]):
    """Result constructor."""

    def __init__(self, value: T):
        super().__init__(value)


class Err(_Result[T]):
    """Result constructor."""

    def __init__(self, error: Exception):
        super().__init__(error)


def try_call(fn: Callable[[VarArg(Any), KwArg(Any)], R], *args, **kwargs) -> "Result[R]":
    """Tries to call fn function and returns a result of the execution."""
    try:
        ret: R = fn(*args, **kwargs)
        return Ok[R](ret)
    except Exception as err:
        return Err[R](err)


Result = Ok[T] | Err[T]

__all__ = ("Ok", "Err")
