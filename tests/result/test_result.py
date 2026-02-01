import pytest

from pyfplib import Err, Ok, Result, first


def create_result() -> Result:
    return Ok("TEST")

def test_result():
    result = create_result()
    value = "TEST"
    match result:
        case Ok(value):
            assert result.unwrap() == value
        case Err(Exception("TEST")):
            pytest.fail()
