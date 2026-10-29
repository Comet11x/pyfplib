# SPDX-FileCopyrightText: 2026-present Comet11x
# SPDX-License-Identifier: MIT
"""
functools.py

This module provides a set of functions.

Example usage:

    from pyfplib import
    result = add(5, 3)

Functions:
- add(a, b): Returns the sum of a and b.
- subtract(a, b): Returns the difference of a and b.
- multiply(a, b): Returns the product of a and b.
- divide(a, b): Returns the quotient of a and b. Raises ValueError for division by zero.
"""

import inspect
from collections.abc import Callable, Iterable, Sequence, Sized
from typing import Any, cast, overload

from pyfplib.option import Nothing, Option, Some


class _FnWrapper[T, R]:
    ONE = 1
    TWO = 2
    THREE = 3
    FORE = 4

    def __init__(self, fn: Callable[..., R]) -> None:
        self._fn = fn
        self._sig = inspect.signature(fn)
        self._params_num = len(self._sig.parameters)

    @property
    def signature(self) -> inspect.Signature:
        return self._sig

    @property
    def params_number(self) -> int:
        return self._params_num

    def __call__(self, v: T, i: int = 0, c: Sequence[T] | None = None) -> R:
        if self._params_num == _FnWrapper.ONE:
            return self._fn(v)
        elif self._params_num == _FnWrapper.TWO:
            return self._fn(v, i)
        else:
            c = c if c is not None else ()
            return self._fn(v, i, c)


class _FnWrapper2[T, R](_FnWrapper[T, R]):
    def __init__(self, fn: Callable[..., R], *, pipeline: Iterable[Callable[..., R]] = []) -> None:
        super().__init__(fn)
        self._pipeline = pipeline

    def __call__(self, v: T, i: int = 0, c: Sequence[T] | None = None) -> R:
        ret_value = super().__call__(v, i, c)
        for fn in self._pipeline:
            ret_value = fn(ret_value)
        return ret_value


class _FnWrapper3[T, R]:
    def __init__(self, fn: Callable[..., R]) -> None:
        self._fn = fn
        self._sig = inspect.signature(fn)
        self._params_num = len(self._sig.parameters)

    @property
    def params_number(self) -> int:
        return self._params_num

    def __call__(self, p: R | T | None, v: T, i: int = 0, c: Sequence[T] | None = None) -> R:
        if self._params_num == _FnWrapper.ONE:
            return self._fn(v)
        elif self._params_num == _FnWrapper.TWO:
            return self._fn(p, v)
        elif self._params_num == _FnWrapper.THREE:
            return self._fn(p, v, i)
        else:
            return self._fn(p, v, i, c)


@overload
def for_each[T](function: Callable[[T], None], sequence: Sequence[T]) -> None: ...


@overload
def for_each[T](function: Callable[[T, int], None], sequence: Sequence[T]) -> None: ...


def for_each[T](function: Callable[[T, int, Sequence[T]], None], sequence: Sequence[T]) -> None:
    """Applies the given function for each elements of the given sequence object

    Args:
        function: a callback to execute with elements
        sequence: provides elements to apply the callback
    """
    if is_empty(sequence):
        return

    wrapper = _FnWrapper(function)

    if wrapper.params_number == _FnWrapper.ONE:
        for item in sequence:
            wrapper(item)
    else:
        for idx, item in enumerate(sequence):
            wrapper(item, idx, sequence)


@overload
def any_of[T](predicate: Callable[[T], bool], sequence: Sequence[T]): ...


@overload
def any_of[T](predicate: Callable[[T, int], bool], sequence: Sequence[T]): ...


def any_of[T](predicate: Callable[[T, int, Sequence[T]], bool], sequence: Sequence[T]) -> bool:
    """
    Checks if any elements of an iterable object satisfy a given condition.

    It returns false if an iterable oject is empty.

    Args:
        predicate: A function checking elements.
        iterable: An iterable object providing elements for checking.

    Returns:
        bool: The result of the checking.
    """
    return _abstract_check(predicate=_FnWrapper(predicate), sequence=sequence, init_value=False, check=lambda v: v)


@overload
def all_of[T](predicate: Callable[[T], bool], iterable: Iterable[T]): ...


@overload
def all_of[T](predicate: Callable[[T, int], bool], iterable: Iterable[T]): ...


def all_of[T](predicate: Callable[[T, int, Sequence[T]], bool], sequence: Sequence[T]) -> bool:
    """
    Checks if every element of an iterable object satisfy a given condition.

    It returns true if an iterable object is empty.

    Args:
        predicate: a function checking elements.
        iterable: an iterable object providing elements for checking.

    Returns:
        bool: The result of the checking.
    """
    return _abstract_check(predicate=_FnWrapper(predicate), sequence=sequence, init_value=True, check=lambda v: not v)


@overload
def none_of[T](predicate: Callable[[T], bool], iterable: Iterable[T]): ...


@overload
def none_of[T](predicate: Callable[[T, int], bool], iterable: Iterable[T]): ...


def none_of[T](callback: Callable[[T], bool], sequence: Sequence[T]) -> bool:
    """
    Checks if no one element of an iterable object not satisfy a given condition.

    It returns true if an iterable object is empty.

    Args:
        predicate: a function checking elements.
        sequence: a sequence object providing elements for checking.

    Returns:
        bool: The result of the checking.
    """
    return _abstract_check(
        predicate=_FnWrapper2(callback, pipeline=(lambda v: not v,)),
        sequence=sequence,
        init_value=True,
        check=lambda v: not v,
    )


# @overload
# def fold[T](
#    function: Callable[[T, T], T],
#    sequence: Sequence[T],
#    initial: T | None = None,
# ) -> Option[T]: ...


def fold[T, R](
    function: Callable[[Option[R], T], R] | Callable[[Option[R], T, int], R],
    sequence: Sequence[T],
    initial: R | None = None,
) -> Option[R]:
    ret_value = Option.from_optional(initial)
    if len(sequence) != 0:
        wrapper = _FnWrapper3(function)
        if wrapper.params_number == _FnWrapper.TWO:
            fn = cast(Callable[[Option[R], T], R], function)
            for item in sequence:
                ret_value.push(fn(ret_value, item))
        elif wrapper.params_number == _FnWrapper.THREE:
            for idx, item in enumerate(sequence):
                ret_value.push(wrapper(ret_value, item, idx))
    return ret_value


def head[T](iterable: Iterable[T]) -> Option[T]:
    """
    Returns Some[T] contained 1st item of the given iterable object.
    If the given iterable is empty, it returns Nothing[T].

    Args:
        iterable: an iterable object provided 1st element.

    Return:
        Option[T]: Returns Some(item) if non-empty, otherwise Nothing().
    """
    iterator = iter(iterable)
    sentinel = object()
    item = next(iterator, sentinel)
    return Nothing() if item is sentinel else Some(cast(T, item))


def tail[T](sequence: Sequence[T]) -> Sequence[T]:
    """
    Returns Some[T] contained a slice of the given sequence without 1st element,
    i.g. it returns sequence[1:].
    If the sequence is empty, this function returns it.

    Args:
        sequence: a sequence used to get a slice.

    Return:
        Sequence[T]: A slice of the given sequence.
    """
    return sequence[1:] if sequence else sequence


def split_first[T](sequence: Sequence[T]) -> tuple[Option[T], Sequence[T]]:
    return (Some(sequence[0]), sequence[1:]) if sequence else (Nothing(), sequence)


def split_last[T](sequence: Sequence[T]) -> tuple[Sequence[T], Option[T]]:
    return (sequence[:-1], Some(sequence[-1])) if sequence else (sequence, Nothing())


def first[T](iterable: Iterable[T]) -> Option[T]:
    """
    Returns Some[T] contained 1st item of the given iterable object.
    If the given iterable is empty, it returns Nothing[T].

    Args:
        iterable: an iterable object provided 1st element.

    Return:
        Option[T]: Returns Some(item) if non-empty, otherwise Nothing().
    """
    iterator = iter(iterable)
    sentinel = object()
    item = next(iterator, sentinel)
    return Nothing() if item is sentinel else Some(cast(T, item))


def last[T](sequence: Sequence[T]) -> Option[T]:
    """
    Returns Some[Any] contained last item of the given sequence.
    If the given sequence is empty, it returns Nothing[Any].

    Args:
         sequence: a sequence provided last element.

    Return:
        Option[T]: Returns Some(item) if non-empty, otherwise Nothing().
    """
    return Some(sequence[-1]) if sequence else Nothing()


def is_empty(iterable: Sized) -> bool:
    """
    Checks if the given iterable object is empty.

    Args:
        iterable: an iterable object.

    Return:
        bool: Returns true if the iterable is empty, otherwise returns false.
    """
    return len(iterable) == 0


def is_not_empty(value: Sized) -> bool:
    """
    Checks whether the given object of Sized is not empty.

    Args:
        Sized: an sized object.

    Return:
        bool: Returns true if the value is not empty, otherwise returns false.
    """
    return len(value) != 0


def index[T](predicate: Callable[..., bool | Option[Any]] | T, sequence: Sequence[T]) -> Option[int]:
    """
    Finds the position of 1st occurrence of a specified element in the given iterable object.
    It returns Some[Any] contained the index of the found  element, and if the element is not found, it returns Nothing

    Args:
        predicate: a function checking elements or a value used for checking.
        iterable: an iterable object providing elements for checking.

    Return:
        Option[int]: A found index
    """
    if is_not_empty(sequence):
        if callable(predicate):
            wrapper = _FnWrapper(predicate)
            for idx, value in enumerate(sequence):
                if wrapper(value, idx, sequence):
                    return Some(idx)
        else:
            expected_value: T = cast(T, predicate)

            for idx, value in enumerate(sequence):
                if expected_value == value:
                    return Some(idx)
    return Nothing()


def find[T](callback: Callable[[T], Option[T]], sequence: Sequence[T]) -> Option[T]:
    """
    Finds a specified element in the given iterable object.
    It returns Some[Any] contained f of the found  element, and if the element is not found, it returns Nothing

    Args:
        predicate: a function checking elements or a value used for checking.
        sequence:  a sequence object providing elements for checking.

    Return:
        Option[int]: A found index
    """
    for item in sequence:
        ret_value = callback(item)
        if isinstance(ret_value, Option) and ret_value.is_some():
            return ret_value
        elif ret_value:
            return Some(item)

    return Nothing()


type _FnWrapperType[T, R] = _FnWrapper[T, R] | _FnWrapper2[T, R]


def _abstract_check[T, bool](
    *,
    predicate: _FnWrapperType[T, bool],
    sequence: Sequence[T],
    init_value: bool,
    check: Callable[[bool], bool],
):
    ret_value = init_value
    if is_empty(sequence):
        return ret_value

    if predicate.params_number == _FnWrapper.ONE:
        for item in sequence:
            ret_value = predicate(item)
            if check(ret_value):
                break
    else:
        for idx, item in enumerate(sequence):
            ret_value = predicate(item, idx, sequence)
            if check(ret_value):
                break

    return ret_value
