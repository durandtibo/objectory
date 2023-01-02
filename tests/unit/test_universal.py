from abc import ABC, abstractmethod
from collections import Counter

from pytest import raises

from objectory import factory
from objectory.errors import AbstractClassFactoryError


class BaseFakeClass(ABC):
    @abstractmethod
    def method(self):
        """Abstract method."""


#############################
#     Tests for factory     #
#############################


def test_factory_valid_object():
    counter = factory("collections.Counter", [1, 2, 1, 3])
    assert isinstance(counter, Counter)
    assert counter.most_common(5) == [(1, 2), (2, 1), (3, 1)]


def test_factory_abstract_object():
    with raises(AbstractClassFactoryError):
        factory("unit.test_universal.BaseFakeClass")


def test_factory_non_existing_object():
    with raises(RuntimeError):
        factory("collections.NotACounter")
