# SPDX-FileCopyrightText: 2026-present Comet11x
# SPDX-License-Identifier: MIT
"""\
This module provides Result[T, E] type
and two constructors of Option: Ok[T, E](T) and Err[T, E](E).
"""

from pyfplib._core import Err as E
from pyfplib._core import Ok as O
from pyfplib._core import Result as R

Result = R
Ok = O
Err = E
