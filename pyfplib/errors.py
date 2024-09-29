"""This module provides errors of pyfplib."""


class UnwrapError(Exception):
    """UnwrapError extends Exception."""

    def __init__(self):
        super().__init__("unwrap `Nothing` value")
