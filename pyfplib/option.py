"""This module provides Option type
and two constructors of Option: Some[T] and Nothing[T].
"""
from typing import Callable, Generic, Optional, TypeVar, cast

from pyfplib.errors import UnwrapError

T = TypeVar("T")
U = TypeVar("U")


class _Option(Generic[T]):
    """_Option is a basic class."""

    __match_args__ = ("value", )

    def __init__(self, value: Optional[T]):
        self.__value = value

    @property
    def value(self) -> Optional[T]:
        """Returns a raw value."""
        return self.__value

    def is_some(self) -> bool:
        """Returns True if the option is Some[T]"""
        return self.__value is not None

    def is_none(self) -> bool:
        """Returns True if the option is None[T]"""
        return self.__value is None

    def if_some(self, fn: Callable[[T], None]) -> "Option[T]":
        """Calls fn function if the option is Some[T]. It returns self."""
        if self.__value is not None:
            fn(self.__value)
        return self

    def if_none(self, fn: Callable[[], None]) -> "Option[T]":
        """Calls fn function if the option is Nothing[T]. It returns self."""
        if self.__value is None:
            fn()
        return self

    def unwrap(self) -> T:
        """\
        Returns the value if it is Some.
        If the value is None this function throws UnwrapError.
        """
        if self.__value is None:
            raise UnwrapError()
        return self.__value

    def unwrap_or(self, value: T) -> T:
        """Returns the value or a provided default."""
        return value if self.__value is None else self.__value

    def map(self, fn: Callable[[T], U]) -> "Option[U]":
        """Maps an Option[T] to Option[U]."""
        o: Option
        if self.is_some():
            o = Some[U](fn(cast(T, self.__value)))
        else:
            o = Nothing[T]()
        return o

    def map_from(self, fn: Callable[[T], "Option[U]"]) -> "Option[U]":
        """Maps an Option[T] to Option[U]."""
        o: Option
        if self.is_some():
            o = fn(cast(T, self.__value))
        else:
            o = Nothing[T]()
        return o

    def __eq__(self, other: object) -> bool:
        ret: bool = False
        if isinstance(other, _Option):
            ret = self.__value == other.value
        return ret


class Some(_Option[T]):
    """This constructor Option[T] creates with a value."""

    def __init__(self, value: T):
        super().__init__(value)


class Nothing(_Option[T]):
    """This constructor Option[T] without any value."""

    def __init__(self):
        super().__init__(None)


Option = Some[T] | Nothing[T]


def from_optional(value: Optional[T]) -> Option[T]:
    """Creates Option[T] from Optional[T]."""
    return Nothing[T]() if value is None else Some[T](cast(T, value))


__all__ = ("Option", "Some", "Nothing")
