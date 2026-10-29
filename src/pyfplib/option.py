"""\
This module provides Option[T] type
and two constructors of Option: Some[T](T) and Nothing[T]().
"""

from pyfplib._core import Nothing as N  # noqa: N817
from pyfplib._core import Option as O  # noqa: N817
from pyfplib._core import Some as S  # noqa: N817

Option = O
Some = S
Nothing = N
