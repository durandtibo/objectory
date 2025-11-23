r"""Utilities for introspecting Python objects and retrieving their
fully qualified names."""

from __future__ import annotations

__all__ = ["get_fully_qualified_name", "is_lambda_function"]

import inspect
from typing import Any


def get_fully_qualified_name(obj: Any) -> str:
    r"""Return the fully qualified name of a Python object.

    Supports functions, classes, methods, and instances.
    For instances, returns the fully qualified class name.

    Args:
        obj: The object whose name is to be computed.

    Returns:
        The fully qualified name.

    Example usage:

    ```pycon

    >>> from objectory.utils import get_fully_qualified_name
    >>> import collections
    >>> get_fully_qualified_name(collections.Counter)
    'collections.Counter'
    >>> class MyClass:
    ...     pass
    ...
    >>> get_fully_qualified_name(MyClass)
    '....MyClass'
    >>> get_fully_qualified_name(map)
    'builtins.map'

    ```
    """
    module = getattr(obj, "__module__", None)
    qualname = getattr(obj, "__qualname__", None)

    # If not a function/class/method, fall back to the class
    if qualname is None:
        cls = obj.__class__
        module = getattr(cls, "__module__", None)
        qualname = getattr(cls, "__qualname__", None)

    if module and module != "__main__":
        return f"{module}.{qualname}"

    return qualname


def is_lambda_function(obj: Any) -> bool:
    r"""Indicate if the object is a lambda function or not.

    Adapted from https://stackoverflow.com/a/23852434

    Args:
        obj: The object to check.

    Returns:
        ``True`` if the input is a lambda function,
            otherwise ``False``

    Example usage:

    ```pycon

    >>> from objectory.utils import is_lambda_function
    >>> is_lambda_function(lambda value: value + 1)
    True
    >>> def my_function(value: int) -> int:
    ...     return value + 1
    ...
    >>> is_lambda_function(my_function)
    False
    >>> is_lambda_function(1)
    False

    ```
    """
    if not inspect.isfunction(obj):
        return False
    return obj.__name__ == "<lambda>"
