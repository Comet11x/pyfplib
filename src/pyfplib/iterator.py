from typing import Any, Callable, Generic, Iterable, List, TypeVar

from pyfplib.functools import find, fold, for_each
from pyfplib.option import Nothing, Option, Some
from pyfplib.result import Result

T = TypeVar("T")


class Iter(Generic[T]):
    """ """

    Self = "Iter"

    def __init__(self, iterable: Iterable[T]):
        self.__iterable = iterable
        self.__prepared: Option[Iterable[T]] = Nothing()
        self.__pipeline: List[Callable[[Any], Any]] = []
        self.__index = 0

    @property
    def __target(self) -> Iterable[Any]:
        return self.__prepared.unwrap_or(self.__iterable)

    def __apply(self) -> List[T]:
        """ """
        acc = self.__target
        if len(self.__pipeline) != 0:
            for fn in self.__pipeline:
                acc = fn(acc)
            self.__prepared = Some(acc)
            self.__pipeline = []

        return self.__target

    def reverse(self) -> Self:
        self.__pipeline.append(lambda seq: list(reversed(seq)))
        return self

    def sort(self) -> Self:
        self.__pipeline.append(lambda itr: sorted(itr))
        return self

    def map(self, callback: Callable[[T], Any]) -> Self:
        acc = self.__iterable
        for fn in self.__pipeline:
            acc = fn(acc)
        self.__acc = acc
        out = list(map(callback, self.__acc))
        return Iter(out)

    def skip(self, number: int) -> Self:
        self.__pipeline.append(lambda itr: itr[number:])
        return self

    def skip_while(self, callback: Callable[[Any], bool]) -> Self:
        def skip(itr):
            o = find(lambda pair: (callback(pair[1]) and Nothing()) or Some(pair[0]), enumerate(itr))
            return o.map(lambda idx: itr[idx]).unwrap_or([])

        self.__pipeline.append(skip)
        return self

    def step_by(self, step: int) -> Self:
        self.__pipeline.append(lambda itr: itr[::step])
        return self

    def take(self, index: int) -> Option[T]:
        return Result.try_call(lambda itr, idx: itr[idx], self.__apply(), index).ok()

    def zip(self, iterable: Iterable[Any]) -> Self:
        self.__pipeline.append(lambda itr: list(zip(itr, iterable)))
        return self

    def filter(self, callback: Callable[[T], bool]) -> Self:
        self.__pipeline.append(lambda itr: list(filter(callback, itr)))
        return self

    def fold(self, first: Any, callback: Callable[[Any, T], Any]) -> Any:
        return fold(callback, self.__apply(), first)

    def for_each(self, callback: Callable[[Any], None]):
        """"""
        for_each(callback, self.__apply())

    def __iter__(self):
        return iter(self.__apply())

    def __next__(self):
        self.__apply()
        if self.__index < len(self.__prepared):
            item = self.__target[self.__index]
            self.__index += 1
            return item
        self.__index = 0
        raise StopIteration

    def collect(self, ctor: Callable[[Iterable[T]], Iterable[Any]]) -> Iterable[Any]:
        """"""
        return ctor(self.__apply())

    def __len__(self) -> int:
        return len(self.__target)

    def len(self) -> int:
        return len(self)
