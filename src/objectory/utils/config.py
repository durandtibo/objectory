from __future__ import annotations

__all__ = ["is_object_config"]

from objectory.constants import OBJECT_TARGET
from objectory.utils.object_helpers import import_object


def is_object_config(config: dict, cls: type[object]) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    given class.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values.

    Args:
    ----
        config (dict): Specifies the configuration to check.
        cls (type): Specifies the object class.

    Returns:
    -------
        bool: ``True`` if the input configuration is a configuration
            for the given class.

    Example usage:

    .. code-block:: pycon

        >>> from objectory.utils import is_object_config
        >>> is_object_config({"_target_": "collections.Counter", "iterable": [1, 2, 1, 3]})
        True
    """
    target = config.get(OBJECT_TARGET)
    if target is None:
        return False
    return cls in import_object(target).__mro__
