from pyfplib import Nothing, Some
from pyfplib.functools import (
    _FnWrapper,
    _FnWrapper3,
    all_of,
    any_of,
    find,
    first,
    fold,
    for_each,
    head,
    index,
    is_empty,
    is_not_empty,
    last,
    none_of,
    split_first,
    split_last,
    tail,
)


class TestForEach:
    def test_applies_function_to_each_element(self):
        side_effects = []
        for_each(lambda x: side_effects.append(x * 2), [1, 2, 3])
        assert side_effects == [2, 4, 6]

    def test_empty_iterable_does_nothing(self):
        side_effects = []
        for_each(lambda x: side_effects.append(x), [])
        assert side_effects == []

    def test_with_two_param_function(self):
        side_effects = []
        for_each(lambda v, i: side_effects.append((v, i)), ["a", "b"])
        assert side_effects == [("a", 0), ("b", 1)]


class TestAnyOf:
    def test_returns_true_when_any_matches(self):
        assert any_of(lambda x: x > 2, [1, 2, 3]) is True

    def test_returns_false_when_none_matches(self):
        assert any_of(lambda x: x > 10, [1, 2, 3]) is False

    def test_returns_false_for_empty(self):
        assert any_of(lambda x: True, []) is False

    def test_short_circuits_on_first_match(self):
        evaluated = []

        def pred(x):
            evaluated.append(x)
            return x > 2

        assert any_of(pred, [1, 2, 3, 4, 5]) is True
        assert evaluated == [1, 2, 3]

    def test_with_two_param_predicate(self):
        assert any_of(lambda v, i: v + i > 5, [1, 2, 3, 4]) is True


class TestAllOf:
    def test_returns_true_when_all_match(self):
        assert all_of(lambda x: x < 10, [1, 2, 3]) is True

    def test_returns_false_when_any_fails(self):
        assert all_of(lambda x: x > 0, [1, -1, 2]) is False

    def test_returns_true_for_empty(self):
        assert all_of(lambda x: False, []) is True

    def test_short_circuits_on_first_failure(self):
        evaluated = []

        def pred(x):
            evaluated.append(x)
            return x > 0

        assert all_of(pred, [1, 2, -1, 3]) is False
        assert evaluated == [1, 2, -1]

    def test_with_two_param_predicate(self):
        assert all_of(lambda v, i: v > i, [5, 5, 5]) is True


class TestNoneOf:
    def test_returns_true_when_none_match(self):
        assert none_of(lambda x: x > 10, [1, 2, 3]) is True

    def test_returns_false_when_any_match(self):
        assert none_of(lambda x: x > 2, [1, 2, 3]) is False

    def test_returns_true_for_empty(self):
        assert none_of(lambda x: True, []) is True

    def test_with_two_param_predicate(self):
        assert none_of(lambda v, i: v == i, [1, 2, 0]) is True


class TestFold:
    def test_fold_with_initial_sum(self):
        sequence = [1, 2, 3, 4, 5]
        result = fold(lambda acc, x: acc.unwrap_or(0) + x, sequence, 0)
        assert result.unwrap_or(0) == sum(sequence)

    def test_fold_without_initial(self):
        sequence = [1, 2, 3, 4, 5]
        result = fold(lambda acc, x: acc.unwrap_or(-2) + x, sequence)
        assert result.unwrap_or(0) == (sum(sequence) - 2)

    def test_fold_without_initial_single_element(self):
        result = fold(lambda acc, x: acc.unwrap_or(0) + x, [42])
        assert result.unwrap_or(0) == 42

    def test_fold_empty_with_initial(self):
        result = fold(lambda acc, x: acc.unwrap_or(0) + x, [], 10)
        assert result.unwrap_or(0) == 10

    def test_fold_empty_without_initial(self):
        result = fold(lambda acc, x: acc.unwrap_or(0) + x, [])
        assert result.is_none()

    def test_fold_with_three_param_function(self):
        result = fold(lambda acc, x: acc.unwrap_or(0) + x, [1, 2, 3], 0)
        assert result.unwrap_or(0) == 6

    def test_fold_with_three_params_no_initial(self):
        result = fold(lambda acc, x, i: acc.unwrap_or(0) + x + i, [1, 2, 3])
        assert result.unwrap_or(0) == (1 + 2 + 1 + 3 + 2)

    def test_fold_with_one_param_function(self):
        result = fold(lambda acc, _: acc.unwrap_or(0), [1, 2, 3], 0)
        assert result.unwrap_or(-1) == 0

    def test_fold_with_single_param_function_returns_initial(self):
        result = fold(lambda _: 0, [1, 2, 3], 10)
        assert result.unwrap_or(-1) == 10

    def test_fold_with_four_param_function_returns_initial(self):
        result = fold(lambda acc, x, i, c: 0, [1, 2, 3], 10)
        assert result.unwrap_or(-1) == 10

    def test_fold_concat_strings(self):
        result = fold(lambda acc, x: acc.unwrap_or(0) + x, ["a", "b", "c"], "")
        assert result.unwrap_or("") == "abc"


class TestHead:
    def test_head_non_empty(self):
        result = head([10, 20, 30])
        assert isinstance(result, Some)
        assert result.value == 10

    def test_head_empty(self):
        result = head([])
        assert isinstance(result, Nothing)


class TestTail:
    def test_tail_non_empty(self):
        assert tail([1, 2, 3]) == [2, 3]

    def test_tail_single_element(self):
        assert tail([1]) == []

    def test_tail_empty(self):
        assert tail([]) == []

    def test_tail_string(self):
        assert tail("hello") == "ello"


class TestSplitFirst:
    def test_split_first_non_empty(self):
        first_item, rest = split_first([1, 2, 3])
        assert isinstance(first_item, Some)
        assert first_item.value == 1
        assert rest == [2, 3]

    def test_split_first_single_element(self):
        first_item, rest = split_first([1])
        assert isinstance(first_item, Some)
        assert first_item.value == 1
        assert rest == []

    def test_split_first_empty(self):
        first_item, rest = split_first([])
        assert isinstance(first_item, Nothing)
        assert rest == []


class TestSplitLast:
    def test_split_last_non_empty(self):
        rest, last_item = split_last([1, 2, 3])
        assert rest == [1, 2]
        assert isinstance(last_item, Some)
        assert last_item.value == 3

    def test_split_last_single_element(self):
        rest, last_item = split_last([1])
        assert rest == []
        assert isinstance(last_item, Some)
        assert last_item.value == 1

    def test_split_last_empty(self):
        rest, last_item = split_last([])
        assert rest == []
        assert isinstance(last_item, Nothing)


class TestFirst:
    def test_first_non_empty(self):
        result = first([10, 20, 30])
        assert isinstance(result, Some)
        assert result.value == 10

    def test_first_empty(self):
        result = first([])
        assert isinstance(result, Nothing)


class TestLast:
    def test_last_non_empty(self):
        result = last([10, 20, 30])
        assert isinstance(result, Some)
        assert result.value == 30

    def test_last_single_element(self):
        result = last([42])
        assert isinstance(result, Some)
        assert result.value == 42

    def test_last_empty(self):
        result = last([])
        assert isinstance(result, Nothing)


class TestIsEmpty:
    def test_empty_list(self):
        assert is_empty([]) is True

    def test_non_empty_list(self):
        assert is_empty([1]) is False

    def test_empty_string(self):
        assert is_empty("") is True

    def test_non_empty_string(self):
        assert is_empty("a") is False


class TestIsNotEmpty:
    def test_not_empty_list(self):
        assert is_not_empty([1]) is True

    def test_empty_list(self):
        assert is_not_empty([]) is False

    def test_not_empty_string(self):
        assert is_not_empty("a") is True

    def test_empty_string(self):
        assert is_not_empty("") is False


class TestIndex:
    def test_find_element_by_value_found(self):
        result = index(3, [1, 2, 3, 4, 5])
        assert isinstance(result, Some)
        assert result.value == 2

    def test_find_element_by_value_not_found(self):
        result = index(10, [1, 2, 3])
        assert isinstance(result, Nothing)

    def test_find_element_by_predicate_found(self):
        result = index(lambda x: x > 3, [1, 2, 3, 4, 5])
        assert isinstance(result, Some)
        assert result.value == 3

    def test_find_element_by_predicate_not_found(self):
        result = index(lambda x: x > 10, [1, 2, 3])
        assert isinstance(result, Nothing)

    def test_find_by_predicate_with_index(self):
        result = index(lambda v, i: v + i > 5, [1, 2, 3, 4])
        assert isinstance(result, Some)
        assert result.value == 3

    def test_index_empty_iterable(self):
        result = index(1, [])
        assert isinstance(result, Nothing)


class TestFind:
    def test_find_returns_some_when_callback_returns_some(self):
        result = find(lambda x: Some(x) if x > 3 else Nothing[int](), [1, 2, 4, 5])
        assert isinstance(result, Some)
        assert result.unwrap() == 4

    def test_find_returns_some_when_callback_returns_truthy(self):
        result = find(lambda x: Some(x) if x > 3 else Nothing[int](), [1, 2, 4, 5])
        assert isinstance(result, Some)
        assert result.unwrap() == 4

    def test_find_not_found_returns_nothing(self):
        result = find(lambda x: Nothing(), [1, 2, 3])
        assert isinstance(result, Nothing)

    def test_find_empty_iterable(self):
        result = find(lambda x: Some(x), [])
        assert isinstance(result, Nothing)

    def test_find_with_falsy_non_option(self):
        result = find(lambda _: Nothing(), [1, 2, 3])
        assert isinstance(result, Nothing)

    def test_find_returns_some_for_truthy_non_option(self):
        result = find(lambda x: x > 3, [1, 2, 4, 5])  # type: ignore[arg-type]
        assert isinstance(result, Some)
        assert result.value == 4


class TestFnWrapper:
    def test_one_param_call(self):
        fn = lambda v: v * 2
        wrapper = _FnWrapper(fn)
        assert wrapper.params_number == 1
        assert wrapper(5) == 10

    def test_two_param_call(self):
        fn = lambda v, i: v + i
        wrapper = _FnWrapper(fn)
        assert wrapper.params_number == 2
        assert wrapper(10, 5) == 15

    def test_three_param_call(self):
        fn = lambda v, i, a: v + i + len(list(a))
        wrapper = _FnWrapper(fn)
        assert wrapper.params_number == 3
        assert wrapper(10, 5, [1, 2, 3]) == 18

    def test_signature_property(self):
        import inspect

        fn = lambda x, y: x + y
        wrapper = _FnWrapper(fn)
        assert isinstance(wrapper.signature, inspect.Signature)
        assert len(wrapper.signature.parameters) == 2

    def test_default_args(self):
        fn = lambda v: v
        wrapper = _FnWrapper(fn)
        assert wrapper(42) == 42
        assert wrapper(42, 99) == 42


class TestFnWrapper3:
    def test_one_param_call(self):
        wrapper = _FnWrapper3(lambda v: v * 2)
        assert wrapper.params_number == 1
        assert wrapper(None, 5) == 10

    def test_two_param_call(self):
        wrapper = _FnWrapper3(lambda p, v: p + v)
        assert wrapper.params_number == 2
        assert wrapper(10, 5) == 15

    def test_three_param_call(self):
        wrapper = _FnWrapper3(lambda p, v, i: p + v + i)
        assert wrapper.params_number == 3
        assert wrapper(10, 5, 2) == 17

    def test_four_param_call(self):
        wrapper = _FnWrapper3(lambda p, v, i, c: p + v + i + len(c))
        assert wrapper.params_number == 4
        assert wrapper(10, 5, 2, [1, 2, 3]) == 20
