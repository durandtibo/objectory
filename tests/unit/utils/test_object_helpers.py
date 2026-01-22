from __future__ import annotations

from abc import ABC, abstractmethod

from objectory.utils import all_child_classes

####################################
#     Tests for all_child_classes  #
####################################


def test_all_child_classes() -> None:
    """Test all_child_classes with a simple hierarchy."""

    class Foo: ...

    assert all_child_classes(Foo) == set()

    class Bar(Foo): ...

    assert all_child_classes(Foo) == {Bar}

    class Baz(Foo): ...

    assert all_child_classes(Foo) == {Bar, Baz}

    class Bing(Bar): ...

    assert all_child_classes(Foo) == {Bar, Baz, Bing}


def test_all_child_classes_empty_hierarchy() -> None:
    """Test all_child_classes with a class that has no children."""

    class Standalone: ...

    assert all_child_classes(Standalone) == set()


def test_all_child_classes_single_child() -> None:
    """Test all_child_classes with a single child class."""

    class Parent: ...

    class Child(Parent): ...

    result = all_child_classes(Parent)
    assert result == {Child}
    assert len(result) == 1


def test_all_child_classes_multiple_levels() -> None:
    """Test all_child_classes with multiple inheritance levels."""

    class Level0: ...

    class Level1A(Level0): ...

    class Level1B(Level0): ...

    class Level2A(Level1A): ...

    class Level2B(Level1A): ...

    class Level2C(Level1B): ...

    result = all_child_classes(Level0)
    expected = {Level1A, Level1B, Level2A, Level2B, Level2C}
    assert result == expected


def test_all_child_classes_multiple_inheritance() -> None:
    """Test all_child_classes with multiple inheritance (diamond
    pattern)."""

    class Base: ...

    class Left(Base): ...

    class Right(Base): ...

    class Diamond(Left, Right): ...

    result = all_child_classes(Base)
    assert result == {Left, Right, Diamond}


def test_all_child_classes_with_abstract_base_class() -> None:
    """Test all_child_classes with abstract base classes."""

    class AbstractBase(ABC):
        @abstractmethod
        def method(self) -> None:
            pass

    class ConcreteChild(AbstractBase):
        def method(self) -> None:
            pass

    result = all_child_classes(AbstractBase)
    assert result == {ConcreteChild}


def test_all_child_classes_returns_set_type() -> None:
    """Test that all_child_classes always returns a set."""

    class Parent: ...

    class Child(Parent): ...

    result = all_child_classes(Parent)
    assert isinstance(result, set)


def test_all_child_classes_deep_hierarchy() -> None:
    """Test all_child_classes with a deep inheritance hierarchy."""

    class Level0: ...

    class Level1(Level0): ...

    class Level2(Level1): ...

    class Level3(Level2): ...

    class Level4(Level3): ...

    result = all_child_classes(Level0)
    assert result == {Level1, Level2, Level3, Level4}


def test_all_child_classes_siblings() -> None:
    """Test all_child_classes with sibling classes."""

    class Parent: ...

    class Sibling1(Parent): ...

    class Sibling2(Parent): ...

    class Sibling3(Parent): ...

    result = all_child_classes(Parent)
    assert result == {Sibling1, Sibling2, Sibling3}


def test_all_child_classes_grandchildren_only() -> None:
    """Test that grandchildren are included in results."""

    class GrandParent: ...

    class Parent(GrandParent): ...

    class Child(Parent): ...

    result = all_child_classes(GrandParent)
    assert Child in result
    assert Parent in result


def test_all_child_classes_mixed_inheritance() -> None:
    """Test all_child_classes with mixed single and multiple
    inheritance."""

    class Base: ...

    class Mixin: ...

    class Child1(Base): ...

    class Child2(Base, Mixin): ...

    # Child2 should be a child of Base even though it has multiple parents
    result = all_child_classes(Base)
    assert result == {Child1, Child2}


def test_all_child_classes_no_duplicate_classes() -> None:
    """Test that all_child_classes returns unique classes (no
    duplicates)."""

    class Parent: ...

    class Child(Parent): ...

    result = all_child_classes(Parent)
    # Sets naturally don't have duplicates, but verify the count
    assert len(result) == len(set(result))
    assert len(result) == 1
