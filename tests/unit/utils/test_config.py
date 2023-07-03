import sys
from collections import Counter
from typing import Union

from pytest import mark

from objectory import OBJECT_TARGET
from objectory.utils import is_object_config

py310_plus = mark.skipif(sys.version_info < (3, 10), reason="Requires python 3.10+")


def create_list() -> list:
    return [1, 2, 3, 4]


def create_list_union() -> Union[list, tuple]:
    return [1, 2, 3, 4]


def create_list_without_type_hint():  # noqa: ANN201
    return [1, 2, 3, 4]


if sys.version_info >= (3, 10):

    def create_list_union2() -> list | tuple:
        return [1, 2, 3, 4]


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
        ({OBJECT_TARGET: "unit.utils.test_config.create_list"}, list),
        ({OBJECT_TARGET: "unit.utils.test_config.create_list"}, object),
        ({OBJECT_TARGET: "unit.utils.test_config.create_list_union"}, tuple),
        ({OBJECT_TARGET: "unit.utils.test_config.create_list_union"}, list),
        ({OBJECT_TARGET: "unit.utils.test_config.create_list_union"}, object),
    ),
)
def test_is_object_config_true(config: dict, cls: type[object]) -> None:
    assert is_object_config(config, cls)


@py310_plus
def test_is_object_config_true_union_type() -> None:
    assert is_object_config({OBJECT_TARGET: "unit.utils.test_config.create_list_union2"}, tuple)


def test_is_object_config_true_child_class() -> None:
    assert is_object_config({OBJECT_TARGET: "collections.Counter", "iterable": [1, 2, 1, 3]}, dict)


def test_is_object_config_false_missing_target() -> None:
    assert not is_object_config({}, int)


def test_is_object_config_false_incorrect_class() -> None:
    assert not is_object_config({OBJECT_TARGET: "builtins.int"}, float)


def test_is_object_config_false_function_without_type_hint() -> None:
    assert not is_object_config(
        {OBJECT_TARGET: "unit.utils.test_config.create_list_without_type_hint"}, float
    )
