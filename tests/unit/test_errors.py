from __future__ import annotations

import pytest

from objectory.errors import (
    AbstractClassFactoryError,
    AbstractFactoryTypeError,
    FactoryError,
    IncorrectObjectFactoryError,
    InvalidAttributeRegistryError,
    InvalidNameFactoryError,
    UnregisteredObjectFactoryError,
)

#############################
#     Tests for Errors      #
#############################


def test_factory_error_is_exception() -> None:
    """Test that FactoryError inherits from Exception."""
    assert issubclass(FactoryError, Exception)


def test_factory_error_can_be_raised() -> None:
    """Test that FactoryError can be instantiated and raised."""
    with pytest.raises(FactoryError):
        raise FactoryError("Test error message")


def test_factory_error_message() -> None:
    """Test that FactoryError preserves error messages."""
    msg = "Custom error message"
    error = FactoryError(msg)
    assert str(error) == msg


def test_unregistered_object_factory_error_inherits_from_factory_error() -> None:
    """Test that UnregisteredObjectFactoryError inherits from FactoryError."""
    assert issubclass(UnregisteredObjectFactoryError, FactoryError)


def test_unregistered_object_factory_error_can_be_raised() -> None:
    """Test that UnregisteredObjectFactoryError can be raised."""
    with pytest.raises(UnregisteredObjectFactoryError):
        raise UnregisteredObjectFactoryError("Object not registered")


def test_unregistered_object_factory_error_can_be_caught_as_factory_error() -> None:
    """Test that UnregisteredObjectFactoryError can be caught as FactoryError."""
    with pytest.raises(FactoryError):
        raise UnregisteredObjectFactoryError("Object not registered")


def test_incorrect_object_factory_error_inherits_from_factory_error() -> None:
    """Test that IncorrectObjectFactoryError inherits from FactoryError."""
    assert issubclass(IncorrectObjectFactoryError, FactoryError)


def test_incorrect_object_factory_error_can_be_raised() -> None:
    """Test that IncorrectObjectFactoryError can be raised."""
    with pytest.raises(IncorrectObjectFactoryError):
        raise IncorrectObjectFactoryError("Invalid object type")


def test_incorrect_object_factory_error_can_be_caught_as_factory_error() -> None:
    """Test that IncorrectObjectFactoryError can be caught as FactoryError."""
    with pytest.raises(FactoryError):
        raise IncorrectObjectFactoryError("Invalid object type")


def test_abstract_class_factory_error_inherits_from_factory_error() -> None:
    """Test that AbstractClassFactoryError inherits from FactoryError."""
    assert issubclass(AbstractClassFactoryError, FactoryError)


def test_abstract_class_factory_error_can_be_raised() -> None:
    """Test that AbstractClassFactoryError can be raised."""
    with pytest.raises(AbstractClassFactoryError):
        raise AbstractClassFactoryError("Cannot instantiate abstract class")


def test_abstract_class_factory_error_can_be_caught_as_factory_error() -> None:
    """Test that AbstractClassFactoryError can be caught as FactoryError."""
    with pytest.raises(FactoryError):
        raise AbstractClassFactoryError("Cannot instantiate abstract class")


def test_invalid_name_factory_error_inherits_from_factory_error() -> None:
    """Test that InvalidNameFactoryError inherits from FactoryError."""
    assert issubclass(InvalidNameFactoryError, FactoryError)


def test_invalid_name_factory_error_can_be_raised() -> None:
    """Test that InvalidNameFactoryError can be raised."""
    with pytest.raises(InvalidNameFactoryError):
        raise InvalidNameFactoryError("Invalid name provided")


def test_invalid_name_factory_error_can_be_caught_as_factory_error() -> None:
    """Test that InvalidNameFactoryError can be caught as FactoryError."""
    with pytest.raises(FactoryError):
        raise InvalidNameFactoryError("Invalid name provided")


def test_abstract_factory_type_error_inherits_from_factory_error() -> None:
    """Test that AbstractFactoryTypeError inherits from FactoryError."""
    assert issubclass(AbstractFactoryTypeError, FactoryError)


def test_abstract_factory_type_error_can_be_raised() -> None:
    """Test that AbstractFactoryTypeError can be raised."""
    with pytest.raises(AbstractFactoryTypeError):
        raise AbstractFactoryTypeError("Object is not AbstractFactory type")


def test_abstract_factory_type_error_can_be_caught_as_factory_error() -> None:
    """Test that AbstractFactoryTypeError can be caught as FactoryError."""
    with pytest.raises(FactoryError):
        raise AbstractFactoryTypeError("Object is not AbstractFactory type")


def test_invalid_attribute_registry_error_inherits_from_factory_error() -> None:
    """Test that InvalidAttributeRegistryError inherits from FactoryError."""
    assert issubclass(InvalidAttributeRegistryError, FactoryError)


def test_invalid_attribute_registry_error_can_be_raised() -> None:
    """Test that InvalidAttributeRegistryError can be raised."""
    with pytest.raises(InvalidAttributeRegistryError):
        raise InvalidAttributeRegistryError("Invalid attribute access")


def test_invalid_attribute_registry_error_can_be_caught_as_factory_error() -> None:
    """Test that InvalidAttributeRegistryError can be caught as FactoryError."""
    with pytest.raises(FactoryError):
        raise InvalidAttributeRegistryError("Invalid attribute access")


def test_all_factory_errors_inherit_from_factory_error() -> None:
    """Test that all specific factory errors inherit from FactoryError."""
    error_types = [
        UnregisteredObjectFactoryError,
        IncorrectObjectFactoryError,
        AbstractClassFactoryError,
        InvalidNameFactoryError,
        AbstractFactoryTypeError,
        InvalidAttributeRegistryError,
    ]
    for error_type in error_types:
        assert issubclass(error_type, FactoryError)
        assert issubclass(error_type, Exception)
