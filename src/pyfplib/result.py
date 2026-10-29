"""\
This module provides Result[T, E] type
and two constructors of Option: Ok[T, E](T) and Err[T, E](E).
"""

from pyfplib._core import Err as E  # noqa: N817
from pyfplib._core import Ok as O  # noqa: N817
from pyfplib._core import Result as R  # noqa: N817

Result = R
Ok = O
Err = E
