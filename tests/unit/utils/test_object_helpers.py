from abc import ABC, abstractmethod
from collections import Counter
from math import isclose
from typing import Any
from unittest.mock import Mock

from pytest import mark, raises

from objectory.errors import AbstractClassFactoryError, IncorrectObjectFactoryError
from objectory.utils import (
    all_child_classes,
    full_object_name,
    import_object,
    instantiate_object,
    is_lambda_function,
)


class FakeClass:
    """Fake class to tests some functions."""

    def __init__(self, arg1: int, arg2: str = "abc"):
        self.arg1 = arg1
        self.arg2 = arg2

    def method(self):
        """Do nothing."""

    @staticmethod
    def static_method() -> "FakeClass":
        return FakeClass(1, "qwerty")

    @classmethod
    def class_method(cls) -> "FakeClass":
        return cls(arg1=35, arg2="bac")

    @classmethod
    def class_method_with_arg(cls, arg2: str):
        return cls(arg1=333, arg2=arg2)


def fake_function(arg1: int, arg2: str = "abc"):
    """Fake function to tests some functions."""
    return FakeClass(arg1=arg1, arg2=arg2)


#############################
#     all_child_classes     #
#############################


def test_all_child_classes():
    class Foo:
        ...

    assert all_child_classes(Foo) == set()

    class Bar(Foo):
        ...

    assert all_child_classes(Foo) == {Bar}

    class Baz(Foo):
        ...

    assert all_child_classes(Foo) == {Bar, Baz}

    class Bing(Bar):
        ...

    assert all_child_classes(Foo) == {Bar, Baz, Bing}


############################
#     full_object_name     #
############################


def test_full_object_name_builtin():
    assert full_object_name(int) == "builtins.int"


def test_full_object_name_class():
    assert full_object_name(FakeClass) == "unit.utils.test_object_helpers.FakeClass"


def test_full_object_name_local_class():
    class FakeClass:
        ...

    assert (
        full_object_name(FakeClass)
        == "unit.utils.test_object_helpers.test_full_object_name_local_class.<locals>.FakeClass"
    )


def test_full_object_name_function():
    assert full_object_name(fake_function) == "unit.utils.test_object_helpers.fake_function"


def test_full_object_name_builtin_module():
    assert (
        full_object_name(Mock(spec=type, __qualname__="name", __module__="__builtin__")) == "name"
    )


def test_full_object_name_incorrect_type():
    with raises(TypeError):
        full_object_name(1)


#########################
#     import_object     #
#########################


def test_import_object_class():
    assert import_object("collections.Counter") == Counter


def test_import_object_function():
    assert import_object("math.isclose") == isclose


def test_import_object_incorrect():
    assert import_object("collections.NotACounter") is None


def test_import_object_incorrect_type():
    with raises(TypeError):
        import_object(1)


##############################
#     instantiate_object     #
##############################


@mark.parametrize("arg1", (-1, 1))
@mark.parametrize("arg2", ("arg2", "cba"))
def test_instantiate_object_class_args(arg1, arg2):
    obj = instantiate_object(FakeClass, arg1, arg2)
    assert isinstance(obj, FakeClass)
    assert obj.arg1 == arg1
    assert obj.arg2 == arg2


@mark.parametrize("arg1", (-1, 1))
@mark.parametrize("arg2", ("arg2", "cba"))
def test_instantiate_object_class_kwargs(arg1: int, arg2: str):
    obj = instantiate_object(FakeClass, arg1=arg1, arg2=arg2)
    assert isinstance(obj, FakeClass)
    assert obj.arg1 == arg1
    assert obj.arg2 == arg2


def test_instantiate_object_class_init_classmethod():
    obj = instantiate_object(FakeClass, _init_="class_method")
    assert isinstance(obj, FakeClass)
    assert obj.arg1 == 35
    assert obj.arg2 == "bac"


def test_instantiate_object_class_init_classmethod_with_arg():
    obj = instantiate_object(
        FakeClass,
        "meow",
        _init_="class_method_with_arg",
    )
    assert isinstance(obj, FakeClass)
    assert obj.arg1 == 333
    assert obj.arg2 == "meow"


def test_instantiate_object_class_init_classmethod_with_kwarg():
    obj = instantiate_object(
        FakeClass,
        _init_="class_method_with_arg",
        arg2="meow",
    )
    assert isinstance(obj, FakeClass)
    assert obj.arg1 == 333
    assert obj.arg2 == "meow"


def test_instantiate_object_class_init_new():
    assert isinstance(instantiate_object(FakeClass, _init_="__new__"), FakeClass)


def test_instantiate_object_class_init_static_method():
    obj = instantiate_object(FakeClass, _init_="static_method")
    assert isinstance(obj, FakeClass)
    assert obj.arg1 == 1
    assert obj.arg2 == "qwerty"


def test_instantiate_object_init_not_exist():
    with raises(IncorrectObjectFactoryError):
        # Should fail because the init function does not exist.
        instantiate_object(FakeClass, _init_="incorrect_init_function")


def test_instantiate_object_init_regular_method():
    with raises(TypeError):
        # Should fail because self is not defined.
        instantiate_object(FakeClass, _init_="method")


def test_instantiate_object_init_not_method():
    with raises(IncorrectObjectFactoryError):
        FakeClass.not_a_method = None
        # Should fail because the attribute not_a_method is not a method.
        instantiate_object(FakeClass, _init_="not_a_method")


def test_instantiate_object_abstract_class():
    class FakeAbstractClass(ABC):
        @abstractmethod
        def my_method(self):
            """Abstract method."""

    with raises(AbstractClassFactoryError):
        instantiate_object(FakeAbstractClass, 42)


def test_instantiate_object_function():
    obj = instantiate_object(fake_function, 42)
    assert isinstance(obj, FakeClass)
    assert obj.arg1 == 42
    assert obj.arg2 == "abc"


def test_instantiate_object_function_init():
    obj = instantiate_object(fake_function, 42, _init_="my_init_function")
    assert isinstance(obj, FakeClass)
    assert obj.arg1 == 42
    assert obj.arg2 == "abc"


@mark.parametrize("arg1", (-1, 1))
@mark.parametrize("arg2", ("arg2", "cba"))
def test_instantiate_object_function_args(arg1: int, arg2: str):
    obj = instantiate_object(fake_function, arg1, arg2)
    assert isinstance(obj, FakeClass)
    assert obj.arg1 == arg1
    assert obj.arg2 == arg2


@mark.parametrize("arg1", (-1, 1))
@mark.parametrize("arg2", ("arg2", "cba"))
def test_instantiate_object_function_kwargs(arg1: int, arg2: str):
    obj = instantiate_object(fake_function, arg1=arg1, arg2=arg2)
    assert isinstance(obj, FakeClass)
    assert obj.arg1 == arg1
    assert obj.arg2 == arg2


def test_instantiate_object_incorrect_type():
    with raises(TypeError):
        instantiate_object(FakeClass(12))


########################################
#     Tests for is_lambda_function     #
########################################


def test_is_lambda_function_lambda():
    assert is_lambda_function(lambda x: x)


def test_is_lambda_function_regular_function():
    assert not is_lambda_function(fake_function)


@mark.parametrize("obj", (-1, "abc", FakeClass))
def test_is_lambda_function_non_function(obj: Any):
    assert not is_lambda_function(obj)
