r"""Implement some helper functions to manipulate objects."""

from __future__ import annotations

__all__ = [
    "all_child_classes",
    "full_object_name",
    "import_object",
    "instantiate_object",
]

import inspect
import logging
from typing import TYPE_CHECKING, Any

from tornado.util import import_object as tornado_import_object

from objectory.errors import AbstractClassFactoryError, IncorrectObjectFactoryError

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


def all_child_classes(cls: type) -> set[type]:
    r"""Get all the child classes (or subclasses) of a given class.

    Based on: https://stackoverflow.com/a/3862957

    Args:
        cls: The class whose child classes are to be retrieved.

    Returns:
        The set of all the child classes of the given class.

    Example usage:

    ```pycon
    >>> from objectory.utils import all_child_classes
    >>> class Foo:
    ...     pass
    ...
    >>> all_child_classes(Foo)
    set()
    >>> class Bar(Foo):
    ...     pass
    ...
    >>> all_child_classes(Foo)
    {<class '....Bar'>}

    ```
    """
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_child_classes(c)]
    )


def full_object_name(obj: Any) -> str:
    r"""Compute the full name of an object.

    This function works for class and function objects.

    Args:
        obj: The class or function for which the full name is to be
            computed.

    Returns:
        The full name of the object.

    Raises:
        TypeError: if the object is not a class or a function.

    Example usage:

    ```pycon
    >>> from objectory.utils import full_object_name
    >>> class MyClass:
    ...     pass
    ...
    >>> full_object_name(MyClass)
    '....MyClass'
    >>> def my_function():
    ...     pass
    ...
    >>> full_object_name(my_function)
    '....my_function'

    ```
    """
    if inspect.isclass(obj) or inspect.isfunction(obj):
        return _full_object_name(obj)
    msg = f"Incorrect object type: {obj}"
    raise TypeError(msg)


def _full_object_name(obj: object | type) -> str:
    r"""Compute the full class name of a class/function.

    Based on: https://gist.github.com/clbarnes/edd28ea32010eb159b34b075687bb49e

    Args:
        obj: The class or function for which the full name is to be
            computed.

    Returns:
        The full class name.
    """
    name = obj.__qualname__
    if (module := obj.__module__) is not None and module != "__builtin__":
        name = module + "." + name
    return name


def import_object(object_path: str) -> Any:
    r"""Import an object given its path.

    This function can be used to dynamically import a class or a
    function. The object path should have the following structure:
    ``module_path.object_name``. This function returns ``None`` if
    the object path does not respect this structure.

    Args:
        object_path: The path of the object to import.

    Returns:
        The object if the import was successful otherwise ``None``.

    Example usage:

    ```pycon
    >>> from objectory.utils import import_object
    >>> obj = import_object("collections.Counter")
    >>> obj()
    Counter()
    >>> fn = import_object("math.isclose")
    >>> fn(1, 1)
    True

    ```
    """
    if not isinstance(object_path, str):
        msg = f"`object_path` has to be a string (received: {object_path})"
        raise TypeError(msg)
    try:
        return tornado_import_object(object_path)
    except (ValueError, ImportError):
        return None


def instantiate_object(
    obj: Callable | type, *args: Any, _init_: str = "__init__", **kwargs: Any
) -> Any:
    r"""Instantiate dynamically an object from its configuration.

    Args:
        obj: The class to instantiate or the function to call.
        *args: Variable length argument list.
        _init_: The function or method to use to
            create the object. This input is ignored if ``obj`` is a
            function. If ``"__init__"``, the object is created by
            calling the constructor.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        The instantiated object if ``obj`` is a class name, otherwise
            the returned value of the function.

    Raises:
        TypeError: if ``obj`` is not a class or a function.

    Example usage:

    ```pycon
    >>> from collections import Counter
    >>> from objectory.utils import instantiate_object
    >>> instantiate_object(Counter, [1, 2, 1])
    Counter({1: 2, 2: 1})
    >>> instantiate_object(list, [1, 2, 1])
    [1, 2, 1]

    ```
    """
    if inspect.isfunction(obj):
        return obj(*args, **kwargs)
    if inspect.isclass(obj):
        return _instantiate_class_object(obj, *args, _init_=_init_, **kwargs)
    msg = f"Incorrect type: {obj}. The valid types are class and function"
    raise TypeError(msg)


def _instantiate_class_object(
    cls: type, *args: Any, _init_: str = "__init__", **kwargs: Any
) -> Any:
    r"""Instantiate an object from its class and some arguments.

    The object can be instantiated by calling the constructor
    ``__init__`` (default) or ``__new__`` or a class method.

    Args:
        cls: The class of the object to instantiate.
        *args: Variable length argument list.
        _init_: The function to use to create the object.
            If ``"__init__"``, the object is created by calling the
            constructor.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        The instantiated object.

    Raises:
        AbstractClassFactoryError: if it is an abstract class.
        IncorrectObjectFactoryError: if it is not possible to
            instantiate the object.
    """
    if inspect.isabstract(cls):
        msg = f"Cannot instantiate the class {cls} because it is an abstract class."
        raise AbstractClassFactoryError(msg)

    if _init_ == "__init__":
        return cls(*args, **kwargs)

    if not hasattr(cls, _init_):
        msg = f"{cls} does not have `{_init_}` attribute"
        raise IncorrectObjectFactoryError(msg)
    init_fn = getattr(cls, _init_)
    if not callable(init_fn):
        msg = f"`{_init_}` attribute of {cls} is not callable"
        raise IncorrectObjectFactoryError(msg)
    if _init_ == "__new__":
        return init_fn(cls, *args, **kwargs)
    return init_fn(*args, **kwargs)
