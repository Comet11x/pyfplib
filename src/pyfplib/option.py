# SPDX-FileCopyrightText: 2026-present Comet11x
# SPDX-License-Identifier: MIT
"""\
This module provides Option[T] type
and two constructors of Option: Some[T](T) and Nothing[T]().
"""

from pyfplib._core import Nothing as N
from pyfplib._core import Option as O
from pyfplib._core import Some as S

Option = O
Some = S
Nothing = N
