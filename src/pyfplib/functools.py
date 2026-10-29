import inspect
from typing import Any, Callable, Iterable, Sequence, Union

from pyfplib.option import Nothing, Option, Some


def for_each(callback: Callable[[Any], None], iterable: Iterable[Any]):
    """Applies the given callback for each elements of the given iterable object

    Args:
        callback: callback to execute with elements
        iterable: provides elements to apply the callback
    """
    _, wrapper = _make_wrapper(callback)
    for idx, item in enumerate(iterable):
        wrapper(item, idx, iterable)


def any_of(callback: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return _abstract_check(callback=callback, iterable=iterable, init_value=False, check=lambda v: v)


def all_of(callback: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return _abstract_check(callback=callback, iterable=iterable, init_value=True, check=lambda v: not v)


def none_of(callback: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return _abstract_check(callback=callback, iterable=iterable, init_value=True, check=lambda v: v)


def fold(
    callback: Callable[[Any, Any], Any],
    iterable: Iterable[Any],
    first: Union[Any, None] = None,
) -> Any:
    ret_value = first
    num, wrapper = _make_wrapper(callback)
    if num > 2:
        for idx, item in enumerate(iterable):
            ret_value = wrapper(ret_value, item, idx)
    else:
        for item in iterable:
            ret_value = wrapper(ret_value, item)
    return ret_value


def head(iterable: Iterable[Any]) -> Option[Any]:
    return Some(iterable[0]) if len(iterable) else Nothing()


def tail(sequence: Sequence[str]) -> Sequence[str]:
    return sequence[1:] if len(sequence) else sequence


def first(iterable: Iterable[Any]) -> Option[Any]:
    return Some(iterable[0]) if len(iterable) else Nothing()


def last(iterable: Iterable[Any]) -> Option[Any]:
    return Nothing() if len(iterable) == 0 else Some(iterable[-1])


def is_empty(iterable: Iterable[Any]) -> bool:
    return len(iterable) == 0


def is_not_empty(iterable: Iterable[Any]) -> bool:
    return len(iterable) != 0


def index[T](predicate: Callable[[T], Any] | Option[T], iterable: Iterable[T]) -> Option[int]:
    """
    Finds the position of 1st occurrence of a specified element in the given iterable object.
    It returns Some[Any] contained the index of the found  element, and if the element is not found, it returns Nothing

    Args:
        predicate: a function checking elements or a value used for checking.
        iterable: an iterable object providing elements for checking.

    Return:
        Option[int]: A found index
    """
    if callable(predicate):
        wrapper = _FnWrapper(predicate)
        def fn(v, i, c):
            return Some(i) if wrapper(v, i, c) else None
        return find(fn, iterable)
    else:
        return find(lambda v, i: Some(i) if v == predicate else None, iterable)


def find[T](callback: Callable[[T], Option[T]], iterable: Iterable[T]) -> Option[T]:
    """
    Finds a specified element in the given iterable object.
    It returns Some[Any] contained f of the found  element, and if the element is not found, it returns Nothing

    Args:
        predicate: a function checking elements or a value used for checking.
    iterable: an iterable object providing elements for checking.

    Return:
        Option[int]: A found index
    """
    ret_value = Nothing()
    for item in iterable:
        ret_value = callback(item)
        if isinstance(ret_value, Option) and ret_value.is_some():
            return ret_value
        elif ret_value:
            return Some(item)

    return Nothing()
