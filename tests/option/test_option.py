""""""

import pytest

from pyfplib import Nothing, Option, Some
from pyfplib.errors import ExpectedError, UnwrapError


@pytest.mark.parametrize(
    "args", ((None, Nothing[int](), False), (123, Some[int](123), True), ("Hello", Some[str]("Hello"), True))
)
def test_from_optional(args):
    """Test from_optional function"""
    value, ex, is_some = args
    o = Option.from_optional(value)
    if is_some:
        assert o.is_some() and not o.is_none()
    else:
        assert o.is_none() and not o.is_some()
    assert o == ex


def assert_if_some(is_some):
    assert is_some


def assert_if_none(is_some):
    assert not is_some


@pytest.mark.parametrize("args", ((Nothing[int](), False), (Some[int](123), True), (Some[str]("Hello"), True)))
def test_if_fn(args):
    """Test from_optional function"""
    obj, is_some = args
    if is_some:
        obj.if_some(lambda _: assert_if_some(is_some))
        obj.if_none(lambda: assert_if_none(not is_some))
    else:
        obj.if_some(lambda _: assert_if_some(not is_some))
        obj.if_none(lambda: assert_if_none(is_some))


@pytest.mark.parametrize("args", ((None, Nothing[int]()), (123, Some[int](123)), ("Hello", Some[str]("Hello"))))
def test_unwrap_fn(args):
    """Test from_optional function"""
    expected, obj = args
    if obj.is_some():
        assert expected == obj.unwrap()
    else:
        with pytest.raises(UnwrapError):
            obj.unwrap()


@pytest.mark.parametrize("args", ((None, Nothing[int]()), (123, Some[int](123)), ("Hello", Some[str]("Hello"))))
def test_expect_fn(args):
    """Test from_optional function"""
    expected, obj = args
    if obj.is_some():
        assert expected == obj.expect("It has a value")
    else:
        with pytest.raises(ExpectedError):
            obj.expect("It does not have a value")


@pytest.mark.parametrize("args", ((None, Nothing[int]()), (123, Some[int](123)), ("Hello", Some[str]("Hello"))))
def test_unwrap_or_fn(args):
    """Test from_optional function"""
    expected, obj = args
    if obj.is_some():
        assert expected == obj.unwrap_or(-1)
    else:
        expected = -1
        assert expected == obj.unwrap_or(-1)


def ctx(value):
    def ctr() -> Option:
        return Some(value)

    def assert_fn(v):
        assert v == value
        return len(v)

    return ctr, assert_fn


def test_some_must_be_some():
    value = "Hello"
    ctor, assert_fn = ctx(value)
    option = ctor()
    assert option.is_some()
    assert len(value) == option.map(assert_fn).unwrap()

    # match fn():
    #    case Some("Hello"):
    #        assert True
    #    case Nothing():
    #        pytest.fail()
