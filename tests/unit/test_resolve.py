from __future__ import annotations

import pytest

from objectory import resolve_object
from objectory.errors import FactoryError, IncorrectTypeFactoryError


class Animal:
    """Base class for testing."""


class Dog(Animal):
    """Concrete subclass for testing."""

    def __init__(self, name: str = "Rex") -> None:
        self.name = name


####################################
#     Tests for resolve_object     #
####################################


# --- Pass-through ---


def test_resolve_object_returns_same_instance_when_no_cls() -> None:
    obj = Dog()
    assert resolve_object(obj) is obj


def test_resolve_object_returns_same_instance_with_matching_cls() -> None:
    obj = Dog()
    assert resolve_object(obj, cls=Dog) is obj


def test_resolve_object_returns_same_instance_with_parent_cls() -> None:
    obj = Dog()
    assert resolve_object(obj, cls=Animal) is obj


# --- Default cls=object ---


def test_resolve_object_default_cls_accepts_any_instance() -> None:
    assert resolve_object(42) == 42


def test_resolve_object_default_cls_accepts_string() -> None:
    assert resolve_object("hello") == "hello"


# --- From dict ---


def test_resolve_object_from_dict_returns_instance() -> None:
    result = resolve_object({"_target_": "tests.unit.test_resolve.Dog"}, cls=Dog)
    assert isinstance(result, Dog)


def test_resolve_object_from_dict_no_cls_still_resolves() -> None:
    result = resolve_object({"_target_": "tests.unit.test_resolve.Dog"})
    assert isinstance(result, Dog)


# --- Invalid input ---


def test_resolve_object_invalid_type_raises_incorrect_type_error() -> None:
    with pytest.raises(
        IncorrectTypeFactoryError, match=r"Received object is not a Animal instance"
    ):
        resolve_object("not-an-animal", cls=Animal)


def test_resolve_object_wrong_subclass_raises_incorrect_type_error() -> None:
    with pytest.raises(IncorrectTypeFactoryError, match=r"Received object is not a Dog instance"):
        resolve_object(Animal(), cls=Dog)


def test_resolve_object_from_dict_wrong_cls_raises_incorrect_type_error() -> None:
    with pytest.raises(IncorrectTypeFactoryError, match=r"Received object is not a str instance"):
        resolve_object({"_target_": "tests.unit.test_resolve.Dog"}, cls=str)


def test_resolve_object_invalid_type_can_be_caught_as_factory_error() -> None:
    with pytest.raises(FactoryError):
        resolve_object("not-an-animal", cls=Animal)


def test_resolve_object_from_dict_missing_target_raises_incorrect_type_error() -> None:
    with pytest.raises(IncorrectTypeFactoryError, match=r"missing the `_target_` key"):
        resolve_object({"name": "Rex"}, cls=Dog)
