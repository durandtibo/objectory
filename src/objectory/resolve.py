r"""Provide a generic resolution utility for creating objects from an
existing instance or an objectory configuration dictionary."""

from __future__ import annotations

__all__ = ["resolve_object"]

import logging
from typing import Any, TypeVar

from objectory.constants import OBJECT_TARGET
from objectory.errors import IncorrectTypeFactoryError
from objectory.universal import factory

logger: logging.Logger = logging.getLogger(__name__)

T = TypeVar("T")


def resolve_object(obj: T | dict[str, Any], cls: type[T] = object) -> T:
    """Resolve an instance of ``cls`` from an existing object or a
    configuration dictionary.

    If ``obj`` is already an instance of ``cls`` it is returned
    as-is.  If it is a :class:`dict`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`.

    Note:
        Any :class:`dict` (including instances of ``dict``
        subclasses, e.g. ``Counter`` or ``OrderedDict``) is always
        treated as a factory configuration, even when it is already
        a valid instance of ``cls``. Do not use this function to
        resolve objects whose expected type is itself a ``dict``
        subclass.

    Args:
        obj: Either a fully configured instance of ``cls``, or a
            :class:`dict` containing an ``objectory`` factory
            specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name).
        cls: The expected type. Used to validate the resolved object,
            whether ``obj`` was already an instance or was built from
            a configuration dictionary. Defaults to :class:`object`,
            which accepts any resolved value without validation.

    Returns:
        A configured instance of ``cls``.

    Raises:
        IncorrectTypeFactoryError: If ``obj`` is a :class:`dict`
            missing the ``"_target_"`` key, or if the resolved
            object is not an instance of ``cls``.

    Example:
        ```pycon
        >>> from datetime import date
        >>> from objectory import resolve_object
        >>> # From an existing instance:
        >>> d = resolve_object(date(2020, 1, 1), cls=date)
        >>> # From a configuration dictionary:
        >>> d = resolve_object(
        ...     {"_target_": "datetime.date", "year": 2020, "month": 1, "day": 1}, cls=date
        ... )

        ```
    """
    cls_name = getattr(cls, "__qualname__", str(cls))
    if isinstance(obj, dict):
        if OBJECT_TARGET not in obj:
            msg = (
                f"Cannot resolve a {cls_name} instance from the configuration because it is "
                f"missing the `{OBJECT_TARGET}` key (received: {obj})"
            )
            raise IncorrectTypeFactoryError(msg)
        logger.info("Initializing a %s instance from its configuration...", cls_name)
        obj = factory(**obj)
    if not isinstance(obj, cls):
        msg = f"Received object is not a {cls_name} instance (received: {type(obj)})"
        raise IncorrectTypeFactoryError(msg)
    return obj
