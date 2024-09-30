import pytest

from pyfplib import Err, Ok, Result, first, try_call


def create_result() -> Result:
    return Ok("TEST")

def test_result():
    match create_result():
        case Ok("TEST"):
            print("OK")
        case Err(Exception("TEST")):
            pytest.fail()
