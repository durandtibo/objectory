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

############################
#     Tests for Errors     #
############################


def test_factory_error_is_exception() -> None:
    """Test that FactoryError inherits from Exception."""
    assert issubclass(FactoryError, Exception)


def test_factory_error_can_be_raised() -> None:
    """Test that FactoryError can be instantiated and raised."""
    msg = "Test error message"
    with pytest.raises(FactoryError, match=msg):
        raise FactoryError(msg)


def test_factory_error_message() -> None:
    """Test that FactoryError preserves error messages."""
    msg = "Custom error message"
    error = FactoryError(msg)
    assert str(error) == msg


def test_unregistered_object_factory_error_inherits_from_factory_error() -> None:
    """Test that UnregisteredObjectFactoryError inherits from
    FactoryError."""
    assert issubclass(UnregisteredObjectFactoryError, FactoryError)


def test_unregistered_object_factory_error_can_be_raised() -> None:
    """Test that UnregisteredObjectFactoryError can be raised."""
    msg = "Object not registered"
    with pytest.raises(UnregisteredObjectFactoryError, match=msg):
        raise UnregisteredObjectFactoryError(msg)


def test_unregistered_object_factory_error_can_be_caught_as_factory_error() -> None:
    """Test that UnregisteredObjectFactoryError can be caught as
    FactoryError."""
    msg = "Object not registered"
    with pytest.raises(FactoryError, match=msg):
        raise UnregisteredObjectFactoryError(msg)


def test_incorrect_object_factory_error_inherits_from_factory_error() -> None:
    """Test that IncorrectObjectFactoryError inherits from
    FactoryError."""
    assert issubclass(IncorrectObjectFactoryError, FactoryError)


def test_incorrect_object_factory_error_can_be_raised() -> None:
    """Test that IncorrectObjectFactoryError can be raised."""
    msg = "Invalid object type"
    with pytest.raises(IncorrectObjectFactoryError, match=msg):
        raise IncorrectObjectFactoryError(msg)


def test_incorrect_object_factory_error_can_be_caught_as_factory_error() -> None:
    """Test that IncorrectObjectFactoryError can be caught as
    FactoryError."""
    msg = "Invalid object type"
    with pytest.raises(FactoryError, match=msg):
        raise IncorrectObjectFactoryError(msg)


def test_abstract_class_factory_error_inherits_from_factory_error() -> None:
    """Test that AbstractClassFactoryError inherits from
    FactoryError."""
    assert issubclass(AbstractClassFactoryError, FactoryError)


def test_abstract_class_factory_error_can_be_raised() -> None:
    """Test that AbstractClassFactoryError can be raised."""
    msg = "Cannot instantiate abstract class"
    with pytest.raises(AbstractClassFactoryError, match=msg):
        raise AbstractClassFactoryError(msg)


def test_abstract_class_factory_error_can_be_caught_as_factory_error() -> None:
    """Test that AbstractClassFactoryError can be caught as
    FactoryError."""
    msg = "Cannot instantiate abstract class"
    with pytest.raises(FactoryError, match=msg):
        raise AbstractClassFactoryError(msg)


def test_invalid_name_factory_error_inherits_from_factory_error() -> None:
    """Test that InvalidNameFactoryError inherits from FactoryError."""
    assert issubclass(InvalidNameFactoryError, FactoryError)


def test_invalid_name_factory_error_can_be_raised() -> None:
    """Test that InvalidNameFactoryError can be raised."""
    msg = "Invalid name provided"
    with pytest.raises(InvalidNameFactoryError, match=msg):
        raise InvalidNameFactoryError(msg)


def test_invalid_name_factory_error_can_be_caught_as_factory_error() -> None:
    """Test that InvalidNameFactoryError can be caught as
    FactoryError."""
    msg = "Invalid name provided"
    with pytest.raises(FactoryError, match=msg):
        raise InvalidNameFactoryError(msg)


def test_abstract_factory_type_error_inherits_from_factory_error() -> None:
    """Test that AbstractFactoryTypeError inherits from FactoryError."""
    assert issubclass(AbstractFactoryTypeError, FactoryError)


def test_abstract_factory_type_error_can_be_raised() -> None:
    """Test that AbstractFactoryTypeError can be raised."""
    msg = "Object is not AbstractFactory type"
    with pytest.raises(AbstractFactoryTypeError):
        raise AbstractFactoryTypeError(msg)


def test_abstract_factory_type_error_can_be_caught_as_factory_error() -> None:
    """Test that AbstractFactoryTypeError can be caught as
    FactoryError."""
    msg = "Object is not AbstractFactory type"
    with pytest.raises(FactoryError, match=msg):
        raise AbstractFactoryTypeError(msg)


def test_invalid_attribute_registry_error_inherits_from_factory_error() -> None:
    """Test that InvalidAttributeRegistryError inherits from
    FactoryError."""
    assert issubclass(InvalidAttributeRegistryError, FactoryError)


def test_invalid_attribute_registry_error_can_be_raised() -> None:
    """Test that InvalidAttributeRegistryError can be raised."""
    msg = "Invalid attribute access"
    with pytest.raises(InvalidAttributeRegistryError):
        raise InvalidAttributeRegistryError(msg)


def test_invalid_attribute_registry_error_can_be_caught_as_factory_error() -> None:
    """Test that InvalidAttributeRegistryError can be caught as
    FactoryError."""
    msg = "Invalid attribute access"
    with pytest.raises(FactoryError, match=msg):
        raise InvalidAttributeRegistryError(msg)


def test_all_factory_errors_inherit_from_factory_error() -> None:
    """Test that all specific factory errors inherit from
    FactoryError."""
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
