from typing import Any, Callable, Iterable, Sequence, Union

from pyfplib.option import Nothing, Option, Some


def for_each(callback: Callable[[Any], None], iterable: Iterable[Any]):
    """Applies the given callback for each elements of the given iterable object

    Args:
        callback: callback to execute with elements
        iterable: provides elements to apply the callback
    """
    for item in iterable:
        callback(item)


def any_of(callback: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    ret_value = False
    for item in iterable:
        ret_value = callback(item)
        if ret_value:
            break
    return ret_value


def all_of(callback: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    ret_value = True
    for item in iterable:
        ret_value = callback(item)
        if not ret_value:
            break
    return ret_value


def none_of(callback: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    ret_value = True
    for item in iterable:
        ret_value = not callback(item)
        if not ret_value:
            break
    return ret_value


def fold(
    callback: Callable[[Any, Any], Any],
    iterable: Iterable[Any],
    first: Union[Any, None] = None,
) -> Any:
    ret_value = first
    for item in iterable:
        ret_value = callback(ret_value, item)
    return ret_value


def head(iterable: Iterable[Any]) -> Option[Any]:
    return Some(iterable[0]) if len(iterable) else Nothing()


def tail(sequence: Sequence[str]) -> Sequence[str]:
    return sequence[1:] if len(sequence) else sequence


def last(iterable: Iterable[Any]) -> Option[Any]:
    return Nothing() if len(iterable) == 0 else Some(iterable[-1])


def is_empty(iterable: Iterable[Any]) -> bool:
    return len(iterable) == 0


def is_not_empty(iterable: Iterable[Any]) -> bool:
    return len(iterable) != 0


def find(callback: Callable[[Any], Option[Any]], iterable: Iterable[Any]) -> Option[Any]:
    ret_value = Nothing()
    for item in iterable:
        ret_value = callback(item)
        if isinstance(ret_value, Option) and ret_value.is_some():
            return ret_value
        elif ret_value:
            return Some(item)

    return ret_value
