from __future__ import annotations

from collections import Counter

from pytest import mark

from objectory import OBJECT_TARGET
from objectory.utils import is_object_config

######################################
#     Tests for is_object_config     #
######################################


@mark.parametrize(
    "config,cls",
    (
        ({OBJECT_TARGET: "builtins.int"}, int),
        ({OBJECT_TARGET: "builtins.int"}, object),
        ({OBJECT_TARGET: "collections.Counter", "iterable": [1, 2, 1, 3]}, Counter),
        ({OBJECT_TARGET: "collections.Counter", "iterable": [1, 2, 1, 3]}, dict),
        ({OBJECT_TARGET: "collections.Counter", "iterable": [1, 2, 1, 3]}, object),
    ),
)
def test_is_object_config_true(config: dict, cls: type[object]) -> None:
    assert is_object_config(config, cls)


def test_is_object_config_true_child_class() -> None:
    assert is_object_config({OBJECT_TARGET: "collections.Counter", "iterable": [1, 2, 1, 3]}, dict)


def test_is_object_config_false_missing_target() -> None:
    assert not is_object_config({}, int)


def test_is_object_config_false_incorrect_class() -> None:
    assert not is_object_config({OBJECT_TARGET: "builtins.int"}, float)
