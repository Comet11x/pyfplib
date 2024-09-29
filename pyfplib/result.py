from typing import TypeVar, Generic, Callable, cast
from pyfplib.option import Option, Some, Nothing

T = TypeVar("T")
R = TypeVar("R")
U = TypeVar("U")


class _Result(Generic[T]):

    def __init__(self, value: T | Exception):
        self.__value = value
        self.__is_ok = not isinstance(value, Exception)

    @property
    def value(self) -> T | Exception:
        return self.__value

    def is_ok(self) -> bool:
        return self.__is_ok

    def is_err(self) -> bool:
        return not self.__is_ok

    def if_ok(self, fn: Callable[[T], None]) -> None:
        if self.is_ok():
            fn(cast(T, self.__value))

    def if_err(self, fn: Callable[[Exception], None]) -> None:
        if self.is_err():
            fn(cast(Exception, self.__value))

    def ok(self) -> Option[T]:
        return Some[T](cast(T, self.__value)) if self.is_ok() else Nothing[T]()

    def err(self) -> Option[Exception]:
        if self.is_err():
            return Some[Exception](cast(Exception, self.__value))
        else:
            Nothing[Exception]()

    def map(self, fn: Callable[[T], U]) -> "_Result[U]":
        if self.is_ok():
            return Ok[U](fn(cast(T, self.__value)))
        else:
            return Err[U](cast(Exception, self.__value))

    def map_from(self, fn: Callable[[T], "_Result[U]"]) -> "_Result[U]":
        if self.is_ok():
            return fn(cast(T, self.__value))
        else:
            return Err[U](cast(Exception, self.__value))


class Ok(_Result[T]):
    """Result constructor."""

    def __init__(self, value: T):
        super().__init__(value)


class Err(_Result[T]):
    """Result constructor."""

    def __init__(self, error: Exception):
        super().__init__(error)


def try_call(fn: Callable[[T], R], arg: T) -> "Result[R]":
    """Tries to call fn function and returns a result of the execution."""
    try:
        ret: R = fn(arg)
        return Ok[R](ret)
    except Exception as err:
        return Err[R](err)


Result = Ok[T] | Err[T]

__all__ = (Ok.__name__, Err.__name__)
