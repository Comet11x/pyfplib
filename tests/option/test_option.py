""""""
import pytest

from pyfplib import Some, Nothing, from_optional


@pytest.mark.parametrize(
    "args", (
        (None, Nothing[int]()),
        (123, Some[int](123)),
        ("Hello", Some[str]("Hello"))
    )
)
def test_create_from_optional(args):
    """Test from_optional function"""
    value, ex = args
    o = from_optional(value)
    assert o == ex
