"""Functional programming library"""

from typing import Callable, Iterable, Sequence, TypeVar
from pyfplib.result import Err, Ok, Result
from pyfplib.option import from_optional, Nothing, Option, Some
from pyfplib.either import from_result, Either, Left, Right


T = TypeVar("T")


def one_of(iterable: Iterable[T], condition: Callable[[T], bool]) -> bool:
    """\
    Returns True if the callback function returns True
    for one of elements of an iterable.
    """
    cond = False
    for elem in iterable:
        if condition(elem):
            cond = True
            break
    return cond


def all_of(iterable: Iterable[T], callback: Callable[[T], bool]) -> bool:
    """\
    Returns True if the callback function returns True
    for all of elements of an iterable.
    """
    cond = False
    for elem in iterable:
        cond = callback(elem)
        if not cond:
            break
    return cond


def first(sequence: Sequence[T]) -> Option[T]:
    """\
    Returns Some[T] with 1st element of the sequence
    if the length of the sequence is not equal 0.
    If the length of the sequence is equal 0 this function returns Nothing[T].
    """
    o: Option
    if len(sequence) == 0:
        o = Nothing[T]()
    else:
        o = Some[T](sequence[0])
    return o


def last(sequence: Sequence[T]) -> Option[T]:
    """\
    Returns Some[T] with last element of the sequence
    if the length of the sequence is not equal 0.
    If the length of the sequence is equal 0 this function returns Nothing[T].
    """
    o: Option
    if len(sequence) == 0:
        o = Nothing[T]()
    else:
        o = Some[T](sequence[-1])
    return o


__all__ = (
    "Option", "Nothing", "Some", "from_optional",
    "Result", "Ok", "Err",
    "Either", "Left", "Right", "from_result",
    "all_of", "one_of", "first", "last",
)
