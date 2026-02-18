"""This module provides Result[T] type
and two constructors of Option: Ok[T] and Err[T].
"""

from typing import Callable, Generic, Optional, TypeVar, cast

from pyfplib.errors import ExpectedError, UnwrapError

T = TypeVar("T")
U = TypeVar("U")


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

    def if_some(self, fn: Callable[[T], None]) -> "Option[T]":
        """
        Executes callback if Some[T], otherwise does nothing.
        Returns self for method chaining.

        Args:
            fn: callback to execute with contained value
        """
        if self.__value is not None:
            fn(self.__value)
        return self

    def if_none(self, fn: Callable[[], None]) -> "Option[T]":
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
        """Returns contained value or raises ExpectedError"""
        if self.__value is None:
            raise ExpectedError(message)
        return self.__value

    def unwrap_or(self, value: T) -> T:
        """Returns contained value or provided default if Nothing."""
        return value if self.__value is None else self.__value

    def map(self, fn: Callable[[T], U]) -> "Option[U]":
        """
        Maps contained value T -> U, returns Nothing() if no value.
        Preserves Option structure for method chaining.

        Args:
            fn: a pure function mapping T to U
        """
        return Some(fn(self.__value)) if self.__value is not None else Nothing()

    def map_from(self, fn: Callable[[T], "Option[U]"]) -> "Option[U]":
        """
        Maps contained value through a function returning Option[U].
        FlatMaps Option[T] -> Option[U], returns Nothing() if no value.

        Args:
            fn: the function returning Option[U]
        """
        return fn(self.__value) if self.__value is not None else Nothing()

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

    @staticmethod
    def from_optional(value: Optional[T] = None) -> "Option[T]":
        """Creates Option[T] from Optional[T]."""
        return Nothing() if value is None else Some(cast(T, value))


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
