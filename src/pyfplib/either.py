"""This module provides Either type and
two constructors of Either: Left[L, R] and Right[L, R].
"""

from typing import Callable, Generic, Optional, TypeVar, Union, cast

from pyfplib.option import Option
from pyfplib.result import Result, T

L = TypeVar("L")
R = TypeVar("R")
U = TypeVar("U")


class Either(Generic[L, R]):
    """Either is a basic class."""

    def __init__(self, *, left: Optional[L] = None, right: Optional[R] = None):
        self.__left: Optional[L] = left
        self.__right: Optional[R] = right

    def is_left(self) -> bool:
        """Returns True if left value is not None."""
        return self.__left is not None

    def is_right(self) -> bool:
        """Returns True if right value is not None."""
        return self.__right is not None

    def if_lef(self, fn: Callable[[L], None]) -> "Either[L, R]":
        """\
        Calls fn function and returns itself.
        The fn function will be called if the left value is not None.
        """
        if self.is_left():
            fn(cast(L, self.__left))
        return self

    def if_right(self, fn: Callable[[R], None]) -> "Either[L, R]":
        """\
        Calls fn function and returns itself.
        The fn function will be called if the right value is not None.
        """
        if self.is_right():
            fn(cast(R, self.__right))
        return self

    def left(self) -> Option[L]:
        """Returns left value as Option[L]."""
        return Option.from_optional(self.__left)

    def right(self) -> Option[R]:
        """Returns right value as Option[R]."""
        return Option.from_optional(self.__right)

    def map_left(self, fn: Callable[[L], U]) -> "Either[U, R]":
        """Maps an Either[L, R] to Either[U, R]."""
        either: Either[U, R]
        if self.is_left():
            either = Left[U, R](fn(cast(L, self.__left)))
        else:
            either = Right[U, R](cast(R, self.__right))
        return either

    def map_right(self, fn: Callable[[R], U]) -> "Either[L, U]":
        """Maps an Either[L, R] to Either[L, U]."""
        either: Either[L, U]
        if self.is_right():
            either = Right[L, U](fn(cast(R, self.__right)))
        else:
            either = Left[L, U](cast(L, self.__left))
        return either

    @staticmethod
    def from_result(result: Result) -> "Either[T, Exception]":
        """Creates Either[T, Exception] from Result."""
        either: Either
        if result.is_ok():
            either = Left[T, Exception](cast(T, result.ok().unwrap()))
        else:
            either = Right[T, Exception](cast(Exception, result.err().unwrap()))
        return either


class Left(Either[L, R]):
    """\
    This Either constructor creates a new instance of Either
    with a left value.
    """

    def __init__(self, value: L):
        super().__init__(left=value)

    @property
    def value(self) -> Union[L, R]:
        """Getter returns left or right value."""
        return cast(L, self.left())


class Right(Either[L, R]):
    """\
    This Either constructor creates a new instance of Either
    with a right value.
    """

    def __init__(self, value: R):
        super().__init__(right=value)

    @property
    def value(self) -> Union[L, R]:
        """Getter returns left or right value."""
        return cast(R, self.right())


__all__ = ("Either", "Left", "Right")
