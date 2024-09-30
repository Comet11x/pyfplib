""""""
import pytest

from pyfplib import Nothing, Option, Some, from_optional


@pytest.mark.parametrize(
    "args", (
        (None, Nothing[int]()),
        (123, Some[int](123)),
        ("Hello", Some[str]("Hello"))
    )
)
def test_from_optional(args):
    """Test from_optional function"""
    value, ex = args
    o = from_optional(value)
    assert o == ex


def fn() -> Option:
    return Some("Hello")

def test_some_must_be_ok():
    match fn():
        case Some("Hello"):
            print("Ok")
        case Nothing():
            pytest.fail()
