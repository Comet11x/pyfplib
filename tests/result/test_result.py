import pytest

from pyfplib import Err, Nothing, Ok, Result, Some
from pyfplib.errors import ExpectedError, UnwrapError


class TestConstruction:
    def test_ok_construction(self):
        ok_value = -1
        expected_ok_value = ok_value
        result = Ok(ok_value)
        assert result.is_ok()
        assert not result.is_err()
        assert result.unwrap() == expected_ok_value

    def test_err_construction(self):
        err_value = "error message"
        expected_err_value = err_value
        result = Err(err_value)
        assert not result.is_ok()
        assert result.is_err()
        assert result.unwrap_err() == expected_err_value

    def test_result_ok_via_value(self):
        ok_value = "ok"
        expected_ok_value = ok_value
        result = Result(value=ok_value)
        assert result.is_ok()
        assert result.unwrap() == expected_ok_value

    def test_result_ok_with_explicit_none_error(self):
        ok_value = 96
        expected_ok_value = ok_value
        result = Result(value=ok_value, error=None)
        assert result.is_ok()
        assert result.unwrap() == expected_ok_value

    def test_result_err_via_error(self):
        err_value = "oops"
        expected_err_value = err_value
        result = Result(error=err_value)
        assert not result.is_ok()
        assert result.is_err()
        assert result.unwrap_err() == expected_err_value

    def test_result_both_defaults_to_err(self):
        ok_value = "ok"
        err_value = "error"
        expected_err_value = err_value
        result = Result(value=ok_value, error=err_value)
        assert not result.is_ok()
        assert result.is_err()
        assert result.unwrap_err() == expected_err_value

    def test_result_empty_is_ok_with_none(self):
        result = Result()
        assert result.is_ok()
        assert result.unwrap() is None

    def test_bool_ok(self):
        assert bool(Ok(None))

    def test_bool_err(self):
        assert not bool(Err("error"))


class TestInspect:
    def test_inspect_ok_calls_fn(self):
        ok_value = "ok"
        side_effects = []
        res = Ok(ok_value).inspect(side_effects.append)
        assert res.is_ok()
        assert not res.is_err()
        assert ok_value in side_effects

    def test_inspect_ok_returns_self(self):
        ok_value = "ok value"
        res = Ok(ok_value)
        assert res.inspect(lambda v: None) is res

    def test_inspect_err_skips_fn(self):
        err_value = "err"
        side_effects = []
        _ = Err(err_value).inspect(side_effects.append)
        assert err_value is not side_effects

    def test_inspect_err_returns_self(self):
        res = Err("error")
        assert res.inspect(lambda v: None) is res

    def test_inspect_err_ok_skips_fn(self):
        ok_value = (1, 2, 3)
        side_effects = []
        _ = Ok(ok_value).inspect_err(side_effects.append)
        assert ok_value is not side_effects

    def test_inspect_err_ok_returns_self(self):
        res = Ok(-1)
        assert res.inspect_err(lambda v: None) is res

    def test_inspect_err_err_calls_fn(self):
        err_value = "ERROR"
        side_effects = []
        _ = Err(err_value).inspect_err(side_effects.append)
        assert err_value is not side_effects

    def test_inspect_err_err_returns_self(self):
        res = Err(["error"])
        assert res.inspect_err(lambda v: None) is res


class TestOkErrConversion:
    def test_ok_returns_some_for_ok(self):
        ok_value = "ok"
        expected_ok_value = ok_value
        opt = Ok(ok_value).ok()
        assert isinstance(opt, Some)
        assert opt.is_some()
        assert opt.unwrap() == expected_ok_value

    def test_ok_returns_nothing_for_err(self):
        opt = Err("e").ok()
        assert isinstance(opt, Nothing)
        assert opt.is_none()

    def test_err_returns_nothing_for_ok(self):
        opt = Ok(0b001).err()
        assert isinstance(opt, Nothing)
        assert opt.is_none()

    def test_err_returns_some_for_err(self):
        err_value = "e"
        expected_value = err_value
        opt = Err(err_value).err()
        assert isinstance(opt, Some)
        assert opt.is_some()
        assert opt.unwrap() == expected_value


class TestUnwrap:
    def test_unwrap_ok(self):
        ok_value = -1
        expected_value = ok_value
        assert Ok(ok_value).unwrap() == expected_value

    def test_unwrap_raises_on_err(self):
        with pytest.raises(UnwrapError) as exc:
            Err("e").unwrap()
        assert "on a `Err` value" in str(exc.value)

    def test_unwrap_err_err(self):
        err_value = "error"
        expected_err_value = err_value
        assert Err(err_value).unwrap_err() == expected_err_value

    def test_unwrap_err_raises_on_ok(self):
        with pytest.raises(UnwrapError) as exc:
            Ok(-100).unwrap_err()
        assert "on a `Ok` value" in str(exc.value)

    def test_expect_ok(self):
        ok_value = 100
        expected_value = ok_value
        assert Ok(ok_value).expect("should work") == expected_value

    def test_expect_raises_on_err(self):
        with pytest.raises(ExpectedError, match="custom message"):
            Err("e").expect("custom message")

    def test_expect_err_err(self):
        err_value = "e"
        expected_err_value = err_value
        assert Err(err_value).expect_err("should work") == expected_err_value

    def test_expect_err_raises_on_ok(self):
        with pytest.raises(ExpectedError, match="custom"):
            Ok(1e3).expect_err("custom")

    def test_unwrap_or_ok(self):
        ok_value = 32
        exported_ok_value = ok_value
        assert Ok(ok_value).unwrap_or(0) == exported_ok_value

    def test_unwrap_or_err(self):
        err_value = "e"
        default_value = 0
        assert Err(err_value).unwrap_or(default_value) == default_value

    def test_unwrap_or_else_ok(self):
        ok_value = "ok"
        expected_value = ok_value
        alternative_value = "alternative"
        assert Ok(ok_value).unwrap_or_else(lambda _: alternative_value) == expected_value

    def test_unwrap_or_else_err(self):
        err_value = "err"
        assert Err(err_value).unwrap_or_else(lambda e: e == err_value)

    def test_unwrap_err_or_ok(self):
        ok_value = "ok"
        default_value = "default"
        assert Ok(ok_value).unwrap_err_or(default_value) == default_value

    def test_unwrap_err_or_err(self):
        err_value = "e"
        default_value = "default"
        expected_value = err_value
        assert Err(err_value).unwrap_err_or(default_value) == expected_value


class TestMap:
    def test_map_ok(self):
        ok_value = 10
        fn = lambda x: x**2
        expected_value = fn(ok_value)
        res = Ok(ok_value).map(fn)
        assert res.is_ok()
        assert res.unwrap() == expected_value

    def test_map_err(self):
        err_value = "e"
        fn = lambda x: f"message: {x}"
        expected_value = err_value
        res = Err(err_value).map(fn)
        assert res.is_err()
        assert res.unwrap_err() == expected_value

    def test_map_or_ok(self):
        res = Ok(42).map_or(0, lambda x: x * 2)
        assert res.is_ok()
        assert res.unwrap() == 42 * 2

    def test_map_or_err_calls_fn_on_default(self):
        res = Err("e").map_or(0, lambda x: x * 2)
        assert res.is_ok()
        assert res.value == 0

    def test_map_or_else_ok(self):
        value = 42
        fn = lambda x: x * 2
        expected = fn(value)
        res = Ok(value).map_or_else(lambda e: 0, fn)
        assert res == expected

    def test_map_or_else_err(self):
        res = Err("e").map_or_else(lambda e: len(e), lambda x: x * 2)
        assert res == 2

    def test_map_err_ok(self):
        res = Ok(42).map_err(lambda e: e.upper())
        assert res.is_ok()
        assert res.value == 42

    def test_map_err_err(self):
        res = Err("error").map_err(lambda e: e.upper())
        assert res.is_err()
        assert res.value == "ERROR"


class TestFlatten:
    def test_flatten_ok_result(self):
        inner = Ok(42)
        outer = Ok(inner)
        assert outer.flatten() is inner

    def test_flatten_ok_non_result(self):
        res = Ok(42)
        assert res.flatten() is res

    def test_flatten_err_result(self):
        inner = Ok(42)
        outer = Err(inner)
        assert outer.flatten() is inner

    def test_flatten_err_non_result(self):
        res = Err("e")
        assert res.flatten() is res

    def test_flatten_all_deeply_nested(self):
        inner = Ok(42)
        middle = Ok(inner)
        outer = Ok(middle)
        assert outer.flatten_all() is inner

    def test_flatten_all_single_level(self):
        res = Ok(42)
        assert res.flatten_all() is res

    def test_flatten_all_err_inner(self):
        inner = Ok(42)
        outer = Err(inner)
        res = outer.flatten_all()
        assert res.is_ok()
        assert res.value == 42

    def test_flatten_all_three_levels(self):
        v = Ok(Ok(Ok(42)))
        res = v.flatten_all()
        assert res.is_ok()
        assert res.value == 42

    def test_flatten_all_nested_err(self):
        inner = Err("inner error")
        outer = Ok(inner)
        res = outer.flatten_all()
        assert res.is_err()
        assert res.value == "inner error"


class TestAndThen:
    def test_and_then_ok_callable(self):
        res = Ok(42).and_then(lambda x: Ok(x * 2))
        assert res.is_ok()
        assert res.value == 84

    def test_and_then_err_not_called(self):
        res = Err("e").and_then(lambda x: Ok(x))
        assert res.is_err()
        assert res.value == "e"

    def test_and_then_non_callable_ok(self):
        res = Ok(42).and_then(None)  # type: ignore
        assert res.is_ok()
        assert res.value == 42

    def test_and_then_non_callable_err(self):
        res = Err("e").and_then(None)  # type: ignore
        assert res.is_err()
        assert res.value == "e"


class TestOrElse:
    def test_or_else_err_callable(self):
        res = Err("e").or_else(lambda e: Ok(len(e)))
        assert res.is_ok()
        assert res.value == 1

    def test_or_else_ok_not_called(self):
        res = Ok(42).or_else(lambda e: Ok(0))
        assert res.is_ok()
        assert res.value == 42

    def test_or_else_non_callable_err(self):
        res = Err("e").or_else(None)  # type: ignore
        assert res.is_err()
        assert res.value == "e"

    def test_or_else_non_callable_ok(self):
        res = Ok(42).or_else(None)  # type: ignore
        assert res.is_ok()
        assert res.value == 42


from typing import Any, cast


class TestAndOperator:
    def test_and_err(self):
        res = Err("e") and Ok(42)
        assert res.is_err()
        assert res.value == "e"

    def test_and_ok_with_result(self):
        res = Ok(42) & Ok(84)
        assert res.is_ok()
        assert res.value == 84

    def test_and_ok_with_callable(self):
        res = Ok(42) & (lambda v: Ok(v * 2))
        res2 = cast(Result[int, Any], res)
        assert res2.is_ok()
        assert res2.value == 84


class TestOrOperator:
    def test_or_ok_returns_self(self):
        res = Ok(42) | Ok(84)
        assert res.is_ok()
        assert res.value == 42

    def test_or_ok_with_callable(self):
        res = Ok(42) | (lambda e: Ok(0))
        assert res.is_ok()
        assert res.value == 42

    def test_or_err_with_result(self):
        res = Err("e") | Ok(42)
        assert res.is_ok()
        assert res.value == 42

    def test_or_err_with_callable(self):
        res = Err("e") | (lambda e: Ok(len(e)))
        assert res.is_ok()
        assert res.value == 1


class TestTryCall:
    def test_try_call_success(self):
        res = Result.try_call(lambda x, y: x + y, 2, 3)
        assert res.is_ok()
        assert res.value == 5

    def test_try_call_failure(self):
        def failing_fn():
            raise ValueError("boom")

        res = Result.try_call(failing_fn)
        assert res.is_err()
        assert isinstance(res.value, ValueError)
        assert str(res.value) == "boom"

    def test_try_call_with_no_args(self):
        res = Result.try_call(lambda: 42)
        assert res.is_ok()
        assert res.value == 42

    def test_try_call_with_kwargs(self):
        res = Result.try_call(lambda a, b: a + b, a=2, b=3)
        assert res.is_ok()
        assert res.value == 5
