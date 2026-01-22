from __future__ import annotations

from objectory.constants import OBJECT_INIT, OBJECT_TARGET

####################################
#     Tests for Constants          #
####################################


def test_object_target_constant_value() -> None:
    """Test that OBJECT_TARGET has the expected value."""
    assert OBJECT_TARGET == "_target_"


def test_object_init_constant_value() -> None:
    """Test that OBJECT_INIT has the expected value."""
    assert OBJECT_INIT == "_init_"


def test_object_target_is_string() -> None:
    """Test that OBJECT_TARGET is a string type."""
    assert isinstance(OBJECT_TARGET, str)


def test_object_init_is_string() -> None:
    """Test that OBJECT_INIT is a string type."""
    assert isinstance(OBJECT_INIT, str)


def test_constants_are_different() -> None:
    """Test that OBJECT_TARGET and OBJECT_INIT have different values."""
    assert OBJECT_TARGET != OBJECT_INIT


def test_object_target_starts_with_underscore() -> None:
    """Test that OBJECT_TARGET starts with underscore (private
    convention)."""
    assert OBJECT_TARGET.startswith("_")


def test_object_init_starts_with_underscore() -> None:
    """Test that OBJECT_INIT starts with underscore (private
    convention)."""
    assert OBJECT_INIT.startswith("_")
