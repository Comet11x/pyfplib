""""""

import pytest

from pyfplib import Nothing, Option, Some


@pytest.mark.parametrize("args", ((None, Nothing[int]()), (123, Some[int](123)), ("Hello", Some[str]("Hello"))))
def test_from_optional(args):
    """Test from_optional function"""
    value, ex = args
    o = Option.from_optional(value)
    assert o == ex


def fn() -> Option:
    return Some("Hello")


def test_some_must_be_some():
    option = fn()
    assert option.is_some()
    # match fn():
    #    case Some("Hello"):
    #        assert True
    #    case Nothing():
    #        pytest.fail()
