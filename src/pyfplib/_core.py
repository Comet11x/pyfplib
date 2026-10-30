# SPDX-FileCopyrightText: 2026-present Comet11x
# SPDX-License-Identifier: MIT
"""This module provides Option[T] and Result[T, E]"""

from collections.abc import Callable
from typing import TypeVar, cast

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

    # Lets positional patterns bind to `value`, e.g. `case Ok(v)`.
    __match_args__ = ("value",)

    def __init__(self, *, value: T | None = None, error: E | None = None):
        # A result is Ok exactly when no error was supplied; the two states share one slot.
        self.__is_ok = error is None
        self.__value: T | E = cast(T, value) if self.__is_ok else cast(E, error)

    @property
    def value(self) -> T | E:
        """
        Returns a contained value.

        Returns:
            T | E: The Ok value or the Err error.
        """
        return self.__value

    def is_ok(self) -> bool:
        """
        Returns True if the result is Ok[T, E].

        Returns:
            bool: True when this result holds an Ok value.
        """
        return self.__is_ok

    def is_err(self) -> bool:
        """
        Returns True if the result is Err[T, E].

        Returns:
            bool: True when this result holds an Err value.
        """
        return not self.__is_ok

    def __bool__(self) -> bool:
        """
        Boolean conversion - True if Ok, False if Err.

        Returns:
            bool: The truthiness of this result.
        """
        return self.is_ok()

    def __repr__(self) -> str:
        """
        Returns a readable representation of this result.

        Returns:
            str: ``Ok(value)`` or ``Err(error)``.
        """
        return f"Ok({self.__value!r})" if self.is_ok() else f"Err({self.__value!r})"

    def inspect(self, fn: Callable[[T], None]) -> "Result[T, E]":
        """
        Applies the given function fn to a contained value if the result is Ok[T, E].

        Args:
            fn: Callback invoked with the Ok value.

        Returns:
            Result[T, E]: This result, for method chaining.
        """
        if self.is_ok():
            fn(cast(T, self.__value))
        return self

    def inspect_err(self, fn: Callable[[E], None]) -> "Result[T, E]":
        """
        Applies the given function fn to a contained value if the result is Err[T, E].

        Args:
            fn: Callback invoked with the Err value.

        Returns:
            Result[T, E]: This result, for method chaining.
        """
        if self.is_err():
            fn(cast(E, self.__value))
        return self

    def ok(self) -> "Option[T]":
        """
        Returns Some[T] if this result is Ok[T, E], otherwise Nothing[T].

        Returns:
            Option[T]: The Ok value as an Option.
        """
        return Some(cast(T, self.__value)) if self.is_ok() else Nothing()

    def err(self) -> "Option[E]":
        """
        Returns Some[E] if this result is Err[E], otherwise Nothing[E].

        Returns:
            Option[E]: The Err value as an Option.
        """
        return Some(cast(E, self.__value)) if self.is_err() else Nothing()

    def unwrap(self) -> T:
        """
        Extracts a contained value, raising UnwrapError if Err.

        Returns:
            T: The contained Ok value.

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

        Returns:
            E: The contained Err value.

        Raises:
            UnwrapError: When attempting to unwrap Ok
        """
        if self.is_ok():
            msg = "called `Result.unwrap_err()` on a `Ok` value"
            raise UnwrapError(msg)
        return cast(E, self.__value)

    def expect(self, message: str) -> T:
        """
        Returns a contained value or raises ExpectedError.

        Args:
            message: Error message used when this result is Err.

        Returns:
            T: The contained Ok value.

        Raises:
            ExpectedError: When this result is Err.
        """
        if self.is_err():
            raise ExpectedError(message)
        return cast(T, self.__value)

    def expect_err(self, message: str) -> E:
        """
        Returns a contained error or raises ExpectedError.

        Args:
            message: Error message used when this result is Ok.

        Returns:
            E: The contained Err value.

        Raises:
            ExpectedError: When this result is Ok.
        """
        if self.is_ok():
            raise ExpectedError(message)
        return cast(E, self.__value)

    def unwrap_or(self, default: T) -> T:
        """
        Returns a contained value or provided default if the result is Err[T, E].

        Args:
            default: Value returned when this result is Err.

        Returns:
            T: The Ok value or `default`.
        """
        return cast(T, self.__value) if self.is_ok() else default

    def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
        """
        Returns a contained value or computes a fallback from the Err value.

        Args:
            fn: Callback receiving the Err value and returning a fallback.

        Returns:
            T: The Ok value or the value produced by `fn`.
        """
        return cast(T, self.__value) if self.is_ok() else fn(cast(E, self.__value))

    def unwrap_err_or(self, default: E) -> E:
        """
        Returns a contained error or provided default if the result is Ok[T, E].

        Args:
            default: Value returned when this result is Ok.

        Returns:
            E: The Err value or `default`.
        """
        return cast(E, self.__value) if self.is_err() else default

    def map[U](self, fn: Callable[[T], U]) -> "Result[U, E]":
        """
        Maps a Result[T, E] to Result[U, E].

        Args:
            fn: Callback applied to the Ok value.

        Returns:
            Result[U, E]: A new Ok with the mapped value, or the original Err.
        """
        if self.is_ok():
            return Ok(fn(self.unwrap()))
        else:
            return Err(self.unwrap_err())

    def map_or[U](self, default: T, fn: Callable[[T], U]) -> "Result[U, E]":
        """
        Maps a Result[T, E] to Result[U, E], using a default for Err values.

        Args:
            default: Value used when this result is Err.
            fn: Callback applied to the Ok value or `default`.

        Returns:
            Result[U, E]: An Ok wrapping the mapped value.
        """
        value: T = cast(T, self.__value) if self.is_ok() else default
        return cast(Result[U, E], Ok(fn(value)))

    def map_or_else[U](self, default: Callable[[E], T], fn: Callable[[T], U]) -> U:
        """
        Maps Result[T, E] to U by applying the given function fn to a contained Ok value.
        If the result is Err, it applies the given fallback function default to the Err value.

        Args:
            default: Callback receiving the Err value and returning a fallback.
            fn: Callback applied to the Ok value or the fallback result.

        Returns:
            U: The mapped value.
        """
        value: T = cast(T, self.__value) if self.is_ok() else default(self.unwrap_err())
        return fn(value)

    def map_err[U](self, fn: Callable[[E], U]) -> "Result[T, U]":
        """
        Maps the Err value of a Result[T, E] to Result[T, U].

        Args:
            fn: Callback applied to the Err value.

        Returns:
            Result[T, U]: The original Ok, or an Err with the mapped error.
        """
        # Transform only the error branch, leaving Ok values untouched.
        if self.is_err():
            res_err: Result[T, U] = Err(fn(cast(E, self.__value)))
            return res_err
        else:
            res_ok: Result[T, U] = Ok(cast(T, self.__value))
            return res_ok

    # @overload
    # def flatten(self: "Result[Result[T, E], E]") -> "Result[T, E]": ...

    # @overload
    # def flatten(self: "Result[T, E]") -> "Result[T, E]": ...

    def flatten(self) -> "Result":
        """
        Collapses one level of nesting.

        Returns:
            Result[T, E]: The inner result when nested, otherwise this result.
        """
        # Collapse exactly one level of nesting; non-nested results are returned as-is.
        return self.__value if isinstance(self.__value, Result) else self

    # @overload
    # def flatten_all(self: "Result[Result[T, E], E]") -> "Result[T, E]": ...

    # @overload
    # def flatten_all(self: "Result[T, E]") -> "Result[T, E]": ...

    def flatten_all(self) -> "Result":
        """
        Collapses every level of nesting.

        Returns:
            Result[T, E]: The innermost result.
        """
        # Walk down nested results until reaching a value that is not a Result.
        value: Result | object = self
        while isinstance(value.__value, Result):
            value: Result = value.__value
        return value

    def __and__(self, other: "Result[T, E] | Callable[[T], Result[T, E]]") -> "Result[T, E]":
        """
        Chains results with `and` semantics.

        Args:
            other: A result or a callback returning one, used when this result is Ok.

        Returns:
            Result[T, E]: This Err, or the result produced from `other`.
        """
        # `and` semantics: an Err short-circuits, while an Ok defers to `other`.
        if self.is_err():
            return self
        else:
            if isinstance(other, Callable):
                fn = cast(Callable[[T], "Result[T, E]"], other)
                return fn(cast(T, self.__value))
            else:
                return cast(Result[T, E], other)

    def and_then(self, fn: Callable[[T], "Result[T, E]"]) -> "Result[T, E]":
        """
        Runs the next step only when this result is Ok.

        Args:
            fn: Callback receiving the Ok value and returning a new result.

        Returns:
            Result[T, E]: The callback result, or this Err unchanged.
        """
        # Monadic bind: run the next step only when this result is Ok.
        return fn(cast(T, self.__value)) if self.is_ok() and callable(fn) else self

    def __or__(self, other: "Result[T, E] | Callable[[E], Result[T, E]]") -> "Result[T, E]":
        """
        Chains results with `or` semantics.

        Args:
            other: A result or a callback returning one, used when this result is Err.

        Returns:
            Result[T, E]: This Ok, or the result produced from `other`.
        """
        # `or` semantics: an Ok short-circuits, while an Err defers to `other`.
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
        """
        Runs a recovery step only when this result is Err.

        Args:
            fn: Callback receiving the Err value and returning a new result.

        Returns:
            Result[T, E]: The callback result, or this Ok unchanged.
        """
        # Recovery step: invoked only for an Err value.
        return fn(cast(E, self.__value)) if self.is_err() and callable(fn) else self

    @staticmethod
    def try_call[R](fn: Callable[..., R], *args, **kwargs) -> "Result[R, Exception]":
        """
        Tries to call the given function fn and returns a result of the execution.

        Args:
            fn: Callable to invoke.
            *args: Positional arguments forwarded to `fn`.
            **kwargs: Keyword arguments forwarded to `fn`.

        Returns:
            Result[R, Exception]: Ok with the return value, or Err with the raised exception.
        """
        # Turn any raised exception into an Err value instead of letting it propagate.
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
        """
        Returns the raw contained value (use with caution - may be None).

        Returns:
            T | None: The contained value, or None for Nothing.
        """
        return self.__value

    def is_some(self) -> bool:
        """
        Returns True if this Option contains a value (Some[T]).

        Returns:
            bool: True when a value is present.
        """
        return self.__value is not None

    def is_none(self) -> bool:
        """
        Returns True if this Option contains no value (Nothing).

        Returns:
            bool: True when no value is present.
        """
        return self.__value is None

    def __bool__(self) -> bool:
        """
        Boolean conversion - True if Some[T], False if Nothing.

        Returns:
            bool: The truthiness of this option.
        """
        return self.is_some()

    def __repr__(self) -> str:
        """
        Returns a readable representation of this option.

        Returns:
            str: ``Some(value)`` or ``Nothing()``.
        """
        return "Nothing()" if self.is_none() else f"Some({self.__value!r})"

    def inspect(self, fn: Callable[[T], None]) -> "Option[T]":
        """
        Executes callback if Some[T], otherwise does nothing.

        Args:
            fn: callback to execute with contained value

        Returns:
            Option[T]: This option, for method chaining.
        """
        if self.__value is not None:
            fn(self.__value)
        return self

    def inspect_none(self, fn: Callable[[], None]) -> "Option[T]":
        """
        Executes callback if Nothing, otherwise does nothing.

        Args:
            fn: callback to execute when no value present

        Returns:
            Option[T]: This option, for method chaining.
        """
        if self.__value is None:
            fn()
        return self

    def unwrap(self) -> T:
        """
        Extracts the contained value, raising UnwrapError if Nothing.

        Returns:
            T: The contained value.

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

        Returns:
            T: The contained value.

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
            default: a value returned if the option is empty

        Returns:
            T: The contained value or `default`.
        """
        return default if self.is_none() else cast(T, self.__value)

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        """
        Returns the contained Some value or computes it from a closure.

        Args:
            fn: Callback producing a fallback value when this option is empty.

        Returns:
            T: The contained value or the value produced by `fn`.
        """
        return fn() if self.is_none() else cast(T, self.__value)

    def map[U](self, fn: Callable[[T], U]) -> "Option[U]":
        """
        Maps the contained value with a function.

        Args:
            fn: a pure function mapping T to U

        Returns:
            Option[U]: Some with the mapped value, or Nothing.
        """
        if self.is_some():
            return Some(fn(self.unwrap()))
        else:
            return Nothing()

    def map_or[U](self, default: U, fn: Callable[[T], U]) -> "Option[U]":
        """
        Maps the contained value, using a default when this option is empty.

        Args:
            default: Value used when this option is Nothing.
            fn: a pure function mapping T to U

        Returns:
            Option[U]: An Option wrapping the mapped value or `default`.
        """
        value = default if self.is_none() else fn(cast(T, self.__value))
        return Some(value)

    def map_or_else[U](self, default: Callable[[], U], fn: Callable[[T], U]) -> U:
        """
        Maps the contained value or computes a fallback when empty.

        Args:
            default: Callback producing a fallback when this option is Nothing.
            fn: a pure function mapping T to U

        Returns:
            U: The mapped value or the fallback.
        """
        return default() if self.is_none() else fn(cast(T, self.__value))

    # @overload
    # def flatten(self: "Option[Option[T]]") -> "Option[T]": ...

    # @overload
    # def flatten(self: "Option[T]") -> "Option[T]": ...

    def flatten(self) -> "Option":
        """
        Collapses one level of nesting.

        Returns:
            Option[T]: The inner option when nested, otherwise this option.
        """
        return self.__value if isinstance(self.__value, Option) else self

    # @overload
    # def flatten_all(self: "Option[Option[T]]") -> "Option[T]": ...

    # @overload
    # def flatten_all(self: "Option[T]") -> "Option[T]": ...

    def flatten_all(self) -> "Option":
        """
        Collapses every level of nesting.

        Returns:
            Option[T]: The innermost option.
        """
        value: Option[T] | object = self
        while isinstance(value.__value, Option):
            value = value.__value
        return value

    def ok_or[E](self, err: E) -> Result[T, E]:
        """
        Converts this option into a Result.

        Args:
            err: Error used when this option is Nothing.

        Returns:
            Result[T, E]: Ok with the contained value, or Err with `err`.
        """
        if self.is_none():
            res: Result[T, E] = Err(err)
        else:
            res: Result[T, E] = Ok(self.unwrap())
        return res

    def ok_or_else[E](self, fn: Callable[[], E]) -> Result[T, E]:
        """
        Converts this option into a Result, computing the error when empty.

        Args:
            fn: Callback producing the error when this option is Nothing.

        Returns:
            Result[T, E]: Ok with the contained value, or Err produced by `fn`.
        """
        if self.is_none():
            res: Result[T, E] = Err(fn())
        else:
            res: Result[T, E] = Ok(self.unwrap())
        return res

    def __eq__(self, other: object) -> bool:
        """
        Equality comparison based on contained values.

        Args:
            other: Object to compare against.

        Returns:
            bool: True when both are Options holding equal values.
        """
        ret: bool = False
        if isinstance(other, Option):
            ret = self.__value == other.value
        return ret

    def __hash__(self):
        """
        Hashes the contained value.

        Returns:
            int: The hash of the contained value.
        """
        return hash(self.__value)

    def __and__[U](self, other: "Option[U] | Callable[[], Option[U]]") -> "Option[U]":
        """
        Chains options with `and` semantics.

        Args:
            other: An option or a callback returning one, used when this option is Some.

        Returns:
            Option[U]: Nothing, or the option produced from `other`.
        """
        # `and` semantics: Nothing short-circuits, Some defers to `other`.
        if self.is_some():
            return cast(Callable[[], Option[U]], other)() if isinstance(other, Callable) else cast(Option[U], other)
        else:
            return Nothing()

    def and_then[U](self, fn: Callable[[T], "Option[U]"]) -> "Option[U]":
        """
        Runs the next step only when a value is present.

        Args:
            fn: Callback receiving the contained value and returning a new option.

        Returns:
            Option[U]: The callback result, or Nothing.
        """
        # Monadic bind: run the next step only when a value is present.
        if self.is_some() and callable(fn):
            return fn(cast(T, self.__value))
        else:
            return Nothing()

    def __or__(self, other: "Option[T] | Callable[[], Option[T]]") -> "Option[T]":
        """
        Chains options with `or` semantics.

        Args:
            other: An option or a callback returning one, used when this option is Nothing.

        Returns:
            Option[T]: This option, or the option produced from `other`.
        """
        # `or` semantics: Some short-circuits, Nothing defers to `other`.
        if self.is_some():
            return self
        else:
            return cast(Callable[[], Option[T]], other)() if isinstance(other, Callable) else other

    def or_else(self, fn: Callable[[], "Option[T]"]) -> "Option[T]":
        """
        Runs a recovery step only when this option is empty.

        Args:
            fn: Callback returning a fallback option when this option is Nothing.

        Returns:
            Option[T]: This option, or the callback result.
        """
        # Recovery step: invoked only when this option is empty.
        return fn() if self.is_none() and callable(fn) else self

    def xor(self, other: "Option[T]") -> "Option[T]":
        """
        Returns a value only when exactly one of the two options is Some.

        Args:
            other: Option to combine with.

        Returns:
            Option[T]: The sole Some value, or Nothing.
        """
        # Return a value only when exactly one of the two options is Some.
        if self.is_some() and other.is_none():
            return self
        elif self.is_none() and other.is_some():
            return other
        else:
            return Nothing()

    def push(self, value: T) -> T:
        """
        Stores a new value and returns the previously held one.

        Args:
            value: New value to store.

        Returns:
            T: The previously held value, or `value` when this option was empty.
        """
        # Return the previously held value (or the new one when empty), then store `value`.
        ret = cast(T, self.__value) if self.is_some() else value
        self.__value = value
        return ret

    @staticmethod
    def from_optional(value: T | None = None) -> "Option[T]":
        """
        Creates Option[T] from Optional[T].

        Args:
            value: Value to wrap; None produces Nothing.

        Returns:
            Option[T]: Some(value) or Nothing.
        """
        return Nothing() if value is None else Some(value)

    def zip[U](self, other: "Option[U]") -> "Option[tuple[T, U]]":
        """
        Combines two options into a tuple when both contain a value.

        Args:
            other: Option to combine with.

        Returns:
            Option[tuple[T, U]]: A tuple of both values, or Nothing.
        """
        # Combine two options only when both contain a value.
        if self.is_some() and other.is_some():
            return Some((cast(T, self.__value), cast(U, other.__value)))
        else:
            return Nothing()

    def zip_with[U, R](self, other: "Option[U]", ctr: Callable[[T, U], R]) -> "Option[R]":
        """
        Combines two options with a callback when both contain a value.

        Args:
            other: Option to combine with.
            ctr: Callback receiving both contained values.

        Returns:
            Option[R]: The callback result, or Nothing.
        """
        # Combine two present values with `ctr`, otherwise return Nothing.
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
