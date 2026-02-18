import pytest

from pyfplib import Ok, Result


def create_result() -> Result:
    return Ok("TEST")


def test_result():
    result = create_result()
    assert result.is_ok()
    # value = "TEST"
    # match result:
    #    case Ok(value):
    #       assert result.unwrap() == value
    #    case Err(Exception("TEST")):
    #        pytest.fail()
