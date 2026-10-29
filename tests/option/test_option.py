import pytest

from pyfplib import Err, Nothing, Ok, Option, Some
from pyfplib.errors import ExpectedError, UnwrapError


class TestConstruction:
    def test_some_construction(self):
        opt = Some(42)
        assert opt.is_some()
        assert not opt.is_none()
        assert opt.value == 42

    def test_nothing_construction(self):
        opt = Nothing()
        assert not opt.is_some()
        assert opt.is_none()
        assert opt.value is None

    def test_some_with_none_value_is_functionally_nothing(self):
        opt = Some(None)
        assert not opt.is_some()
        assert opt.is_none()
        assert opt.value is None

    def test_bool_some(self):
        assert bool(Some(42))

    def test_bool_nothing(self):
        assert not bool(Nothing())


class TestInspect:
    def test_inspect_some_calls_fn(self):
        side_effects = []
        _ = Some(42).inspect(side_effects.append)
        assert side_effects == [42]

    def test_inspect_some_returns_self(self):
        opt = Some(42)
        assert opt.inspect(lambda v: None) is opt

    def test_inspect_nothing_skips_fn(self):
        side_effects = []
        _ = Nothing().inspect(side_effects.append)
        assert side_effects == []

    def test_inspect_nothing_returns_self(self):
        opt = Nothing()
        assert opt.inspect(lambda v: None) is opt

    def test_inspect_none_nothing_calls_fn(self):
        side_effects = []
        Nothing().inspect_none(lambda: side_effects.append("called"))
        assert side_effects == ["called"]

    def test_inspect_none_nothing_returns_self(self):
        opt = Nothing()
        assert opt.inspect_none(lambda: None) is opt

    def test_inspect_none_some_skips_fn(self):
        side_effects = []
        _ = Some(42).inspect_none(lambda: side_effects.append("called"))
        assert side_effects == []

    def test_inspect_none_some_returns_self(self):
        opt = Some(42)
        assert opt.inspect_none(lambda: None) is opt


class TestUnwrap:
    def test_unwrap_some(self):
        assert Some(42).unwrap() == 42

    def test_unwrap_nothing_raises(self):
        with pytest.raises(UnwrapError) as exc:
            Nothing().unwrap()
        assert "on a `Nothing` value" in str(exc.value)

    def test_expect_some(self):
        assert Some(42).expect("msg") == 42

    def test_expect_nothing_raises(self):
        with pytest.raises(ExpectedError, match="custom msg"):
            Nothing().expect("custom msg")

    def test_unwrap_or_some(self):
        assert Some(42).unwrap_or(0) == 42

    def test_unwrap_or_nothing(self):
        assert Nothing().unwrap_or(0) == 0

    def test_unwrap_or_else_some(self):
        assert Some(42).unwrap_or_else(lambda: 0) == 42

    def test_unwrap_or_else_nothing(self):
        assert Nothing().unwrap_or_else(lambda: 99) == 99


class TestMap:
    def test_map_some(self):
        opt = Some(42).map(lambda x: x * 2)
        assert isinstance(opt, Some)
        assert opt.value == 84

    def test_map_nothing(self):
        opt = Nothing().map(lambda x: x * 2)
        assert isinstance(opt, Nothing)

    def test_map_or_some(self):
        opt = Some(42).map_or(0, lambda x: x * 2)
        assert isinstance(opt, Some)
        assert opt.value == 84

    def test_map_or_nothing(self):
        opt = Nothing().map_or(0, lambda x: x * 2)
        assert isinstance(opt, Some)
        assert opt.value == 0

    def test_map_or_else_some(self):
        res = Some(42).map_or_else(lambda: 0, lambda x: x * 2)
        assert res == 84

    def test_map_or_else_nothing(self):
        res = Nothing().map_or_else(lambda: 99, lambda x: x * 2)
        assert res == 99


class TestFlatten:
    def test_flatten_some_option(self):
        inner = Some(42)
        outer = Some(inner)
        assert outer.flatten() is inner

    def test_flatten_some_non_option(self):
        opt = Some(42)
        assert opt.flatten() is opt

    def test_flatten_nothing(self):
        opt = Nothing()
        assert opt.flatten() is opt

    def test_flatten_all_nested(self):
        inner = Some(42)
        middle = Some(inner)
        outer = Some(middle)
        assert outer.flatten_all() is inner

    def test_flatten_all_single(self):
        opt = Some(42)
        assert opt.flatten_all() is opt

    def test_flatten_all_three_levels(self):
        v = Some(Some(Some(42)))
        res = v.flatten_all()
        assert isinstance(res, Some)
        assert res.value == 42

    def test_flatten_all_nothing(self):
        opt = Nothing()
        assert opt.flatten_all().is_none()


class TestConversionToResult:
    def test_ok_or_some(self):
        res = Some(42).ok_or("error")
        assert isinstance(res, Ok)
        assert res.value == 42

    def test_ok_or_nothing(self):
        res = Nothing().ok_or("error")
        assert isinstance(res, Err)
        assert res.value == "error"

    def test_ok_or_else_some(self):
        res = Some(42).ok_or_else(lambda: "error")
        assert isinstance(res, Ok)
        assert res.value == 42

    def test_ok_or_else_nothing(self):
        res = Nothing().ok_or_else(lambda: "computed error")
        assert isinstance(res, Err)
        assert res.value == "computed error"


class TestEquality:
    def test_eq_same_value(self):
        assert Some(42) == Some(42)

    def test_eq_different_value(self):
        assert Some(42) != Some(43)

    def test_eq_nothing_with_nothing(self):
        assert Nothing() == Nothing()

    def test_eq_some_vs_nothing(self):
        assert Some(42) != Nothing()

    def test_eq_non_option(self):
        assert Some(42) != 42

    def test_eq_some_none_vs_nothing(self):
        assert Some(None) == Nothing()

    def test_hash_some(self):
        assert hash(Some(42)) == hash(42)

    def test_hash_nothing(self):
        assert hash(Nothing()) == hash(None)


class TestAndThen:
    def test_and_then_some_callable(self):
        opt = Some(42).and_then(lambda x: Some(x * 2))
        assert isinstance(opt, Some)
        assert opt.value == 84

    def test_and_then_nothing(self):
        opt = Nothing().and_then(lambda x: Some(x))
        assert isinstance(opt, Nothing)

    def test_and_then_non_callable(self):
        opt = Some(42).and_then(None)  # type: ignore
        assert isinstance(opt, Nothing)

    def test_and_then_nothing_non_callable(self):
        opt = Nothing().and_then(None)  # type: ignore
        assert isinstance(opt, Nothing)

    def test_and_then_returns_nothing_for_none(self):
        opt = Some(42).and_then(lambda x: Nothing())
        assert isinstance(opt, Nothing)


class TestOrElse:
    def test_or_else_nothing_callable(self):
        opt = Nothing[int]().or_else(lambda: Some(42))
        assert isinstance(opt, Some)
        assert opt.unwrap() == 42

    def test_or_else_some(self):
        opt = Some(42).or_else(lambda: Some(0))
        assert isinstance(opt, Some)
        assert opt.unwrap() == 42

    def test_or_else_nothing_non_callable(self):
        opt = Nothing().or_else(lambda: Some(0))
        assert isinstance(opt, Some)

    def test_or_else_some_non_callable(self):
        opt = Some(42).or_else(Nothing)
        assert isinstance(opt, Some)
        assert opt.unwrap() == 42


class TestAndOperator:
    def test_and_some_with_option(self):
        opt = Some(5) & Some(10)
        assert isinstance(opt, Some)
        assert opt.value == 10

    def test_and_some_with_callable(self):
        opt = Some(5) & (lambda: Some(20))
        assert isinstance(opt, Some)
        assert opt.value == 20

    def test_and_nothing_with_option(self):
        opt = Nothing() & Some(10)
        assert isinstance(opt, Nothing)

    def test_and_nothing_with_callable(self):
        opt = Nothing() & (lambda: Some(20))
        assert isinstance(opt, Nothing)


class TestOrOperator:
    def test_or_nothing_with_callable(self):
        opt = Nothing[int]() | (lambda: Some(20))
        assert isinstance(opt, Some)
        assert opt.value == 20

    def test_or_nothing_with_option(self):
        opt = Nothing() | Some(10)
        assert opt.is_some()
        assert isinstance(opt, Some)

    def test_or_some_with_option(self):
        opt = Some(42) | Some(0)
        assert isinstance(opt, Some)
        assert opt.value == 42

    def test_or_some_with_callable(self):
        opt = Some(42) | (lambda: Some(0))
        assert isinstance(opt, Some)
        assert opt.unwrap() == 42


class TestXor:
    def test_xor_some_nothing(self):
        opt = Some(42).xor(Nothing())
        assert isinstance(opt, Some)
        assert opt.value == 42

    def test_xor_nothing_some(self):
        opt = Nothing().xor(Some(42))
        assert isinstance(opt, Some)
        assert opt.value == 42

    def test_xor_both_some(self):
        opt = Some(42).xor(Some(84))
        assert isinstance(opt, Nothing)

    def test_xor_both_nothing(self):
        opt = Nothing().xor(Nothing())
        assert isinstance(opt, Nothing)


class TestPush:
    def test_push_some(self):
        opt = Some(42)
        old = opt.push(84)
        assert old == 42
        assert opt.value == 84

    def test_push_nothing(self):
        opt = Nothing()
        old = opt.push(42)
        assert old == 42
        assert opt.value == 42


class TestFromOptional:
    def test_from_optional_none(self):
        opt = Option.from_optional(None)
        assert isinstance(opt, Nothing)

    def test_from_optional_value(self):
        opt = Option.from_optional(42)
        assert isinstance(opt, Some)
        assert opt.value == 42

    def test_from_optional_default(self):
        opt = Option.from_optional()
        assert isinstance(opt, Nothing)


class TestZip:
    def test_zip_both_some(self):
        opt = Some(42).zip(Some("hello"))
        assert isinstance(opt, Some)
        assert opt.value == (42, "hello")

    def test_zip_first_none(self):
        opt = Nothing().zip(Some("hello"))
        assert isinstance(opt, Nothing)

    def test_zip_second_none(self):
        opt = Some(42).zip(Nothing())
        assert isinstance(opt, Nothing)

    def test_zip_both_none(self):
        opt = Nothing().zip(Nothing())
        assert isinstance(opt, Nothing)


class TestZipWith:
    def test_zip_with_both_some(self):
        opt = Some(42).zip_with(Some(58), lambda a, b: a + b)
        assert isinstance(opt, Some)
        assert opt.value == 100

    def test_zip_with_first_none(self):
        opt = Nothing().zip_with(Some(58), lambda a, b: a + b)
        assert isinstance(opt, Nothing)

    def test_zip_with_second_none(self):
        opt = Some(42).zip_with(Nothing(), lambda a, b: a + b)
        assert isinstance(opt, Nothing)

    def test_zip_with_both_none(self):
        opt = Nothing().zip_with(Nothing(), lambda a, b: a + b)
        assert isinstance(opt, Nothing)
