from dataclasses import dataclass
from typing import Any, Callable, Iterable, List, Tuple

import pytest

from pyfplib import all_of

Fn = type(lambda _: _)


@dataclass
class Case:
    callback: Callable[[Any], bool]
    iterable: Iterable[Any]
    expected: Any


@pytest.mark.parametrize(
    "case",
    (
        Case(callback=lambda x: x < 100, iterable=[1, 2, 3, 4], expected=True),
        Case(callback=lambda x: x < 0, iterable=[1, 2, 3, 4], expected=False),
        Case(callback=lambda x: x < 3, iterable=[1, 2, 3, 4], expected=False),
        Case(callback=lambda x: x < 3, iterable=[], expected=True),
    ),
)
def test_all_of(case: Case):
    assert all_of(case.callback, case.iterable) == case.expected
