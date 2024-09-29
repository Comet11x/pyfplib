"""This module provides Either type and
two constructors of Either: Left[L, R] and Right[L, R].
"""
from typing import cast, TypeVar, Generic, Optional
from pyfplib.result import Result, T
from pyfplib.option import Option, from_optional

L = TypeVar("L")
R = TypeVar("R")


class _Either(Generic[L, R]):
    """_Either is a basic class."""

    def __init__(self, *, left: Optional[L] = None, right: Optional[R] = None):
        self.__left: Optional[L] = left
        self.__right: Optional[R] = right

    def is_left(self) -> bool:
        """Returns True if left value is not None."""
        return self.__left is not None

    def is_right(self) -> bool:
        """Returns True if right value is not None."""
        return self.__right is not None

    def left(self) -> Option:
        """Returns left value as Option[L]."""
        return from_optional(self.__left)

    def right(self) -> Option:
        """Returns right value as Option[R]."""
        return from_optional(self.__right)


class Left(_Either[L, R]):
    """\
    This Either constructor creates a new instance of Either
    with a left value.
    """

    def __init__(self, value: L):
        super().__init__(left=value)

    @property
    def value(self) -> L | R:
        """Getter returns left or right value."""
        return cast(L, self.left())


class Right(_Either[L, R]):
    """\
    This Either constructor creates a new instance of Either
    with a right value.
    """

    def __init__(self, value: R):
        super().__init__(right=value)

    @property
    def value(self) -> L | R:
        """Getter returns left or right value."""
        return cast(R, self.right())


Either = Left[L, R] | Right[L, R]


def from_result(result: Result) -> Either[T, Exception]:
    """Creates Either[T, Exception] from Result."""
    either: Either
    if result.is_ok():
        either = Left[T, Exception](cast(T, result.ok().unwrap()))
    else:
        either = Right[T, Exception](cast(Exception, result.err().unwrap()))
    return either


__all__ = ("Either", Left.__name__, Right.__name__)
