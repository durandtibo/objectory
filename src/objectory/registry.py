r"""This module implements a registry class."""

__all__ = ["Registry"]

import inspect
import logging
from typing import Any, Callable, Optional

from objectory.errors import (
    IncorrectObjectFactoryError,
    InvalidAttributeRegistryError,
    InvalidNameFactoryError,
    UnregisteredObjectFactoryError,
)
from objectory.utils import (
    all_child_classes,
    full_object_name,
    import_object,
    instantiate_object,
    is_lambda_function,
    resolve_name,
)

logger = logging.getLogger(__name__)


class Registry:
    r"""Implementation of the registry class.

    This class can be used to register some objects and instantiate an
    object from its configuration.
    """

    _CLASS_FILTER = "class_filter"

    def __init__(self):
        self._state = {}
        self._filters = {}

    def __getattr__(self, key):
        if key not in self._state:
            self._state[key] = Registry()
        if self._is_registry(key):
            return self._state[key]
        raise InvalidAttributeRegistryError(
            f"The attribute {key} is not a registry. You can use this function only to access "
            "a Registry object."
        )

    def __len__(self) -> int:
        r"""Returns the number of registered objects.

        Returns:
            int: The number of registered objects.
        """
        return len(self._state)

    def clear(self, nested: bool = False) -> None:
        r"""Clears the registry.

        This functions removes all the registered objects in the
        registry.

        Args:
            nested (bool): Indicates if the sub-registries should
                be cleared or not. Default: ``False``.

        Example usage:

        .. code-block:: python

            >>> from objectory import Registry
            >>> registry = Registry()
            # Clear the main registry.
            >>> registry.clear()
            # Clear only the sub-registry other.
            >>> registry.other.clear()
            # Clear the main registry and its sub-registries.
            >>> registry.clear(nested=True)
        """
        if nested:  # If True, clear all the sub-registries.
            for value in self._state.values():
                if isinstance(value, Registry):
                    value.clear(nested)
        self._state.clear()

    def clear_filters(self, nested: bool = False) -> None:
        r"""Clears all the filters of the registry.

        Args:
            nested (bool): Indicates if the filters of all the
                sub-registries should be cleared or not.
                Default: ``False``.

        Example usage:

        .. code-block:: python

            >>> from objectory import Registry
            >>> registry = Registry()
            # Clear the filters of the main registry.
            >>> registry.clear_filters()
            # Clear the filters of the sub-registry other.
            >>> registry.other.clear_filters()
            # Clear the filters of the main registry and all its sub-registries.
            >>> registry.clear_filters(nested=True)
        """
        if nested:  # If True, clear all the sub-registries.
            for value in self._state.values():
                if isinstance(value, Registry):
                    value.clear_filters(nested)
        self._filters.clear()

    def factory(self, _target_: str, *args, _init_: str = "__init__", **kwargs) -> Any:
        r"""Creates dynamically an object given its configuration.

        Please read the documentation for more information.

        Args:
            _target_ (str): Specifies the name of the object
                (class or function) to instantiate.
                It can be the class name or the full class name.
            *args: Variable length argument list.
            _init_ (str): Specifies the function to use to create
                the object. If ``"__init__"``, the object is
                created by calling the constructor.
                Default: ``"__init__"``.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The instantiated object with the given parameters.

        Raises:
            ``AbstractClassAbstractFactoryError``: if you try to
                instantiate an abstract class.
            ``UnregisteredClassAbstractFactoryError``: if the target
                name is not found.

        Example usage:

        .. code-block:: python

            >>> from objectory import Registry
            >>> registry = Registry()
            >>> @registry.register()
            ... class MyClass:
            ...     ...
            >>> registry.factory("MyClass")
            <__main__.MyClass object at 0x123456789>
        """
        return instantiate_object(
            self._get_target_from_name(_target_), *args, _init_=_init_, **kwargs
        )

    def register(self, name: Optional[str] = None) -> Callable:
        r"""Defines a decorator to add a class or a function to the registry.

        Args:
            name (str, optional): Specifies the name to use to
                register the object. If ``None``, the full name of
                the object is used as name. Default: ``None``.

        Returns:
            The decorated object.

        Example usage:

        .. code-block:: python

            >>> from objectory import Registry
            >>> registry = Registry()
            >>> @registry.register()
            ... class ClassToRegister:
            ...     ...
            >>> registry.registered_names()
            {'__main__.ClassToRegister'}
            >>> @registry.register()
            ... def function_to_register(*args, **kwargs):
            ...     ...
            >>> registry.registered_names()
            {'__main__.ClassToRegister', '__main__.function_to_register'}
        """

        def function_wrapper(obj):
            self.register_object(obj=obj, name=name)
            return obj

        return function_wrapper

    def register_child_classes(self, cls, ignore_abstract_class: bool = True) -> None:
        r"""Registers a given class and its child classes of a given class.

        This function registers all the child classes including the
        child classes of the child classes, etc. If you use this
        function, you cannot choose the names used to register the
        objects. It will use the full name of each object.

        Args:
            cls: Specifies the class to register its child classes.
            ignore_abstract_class (bool): Indicate if the abstract
                class should be ignored or not. Be default, the
                abstract classes are not registered because they
                cannot be instantiated.

        Example usage:

        .. code-block:: python

            >>> from objectory import Registry
            >>> registry = Registry()
            >>> registry.register_child_classes(dict)
            >>> registry.registered_names()
            {'collections.defaultdict', 'enum._EnumDict', 'tornado.util.ObjectDict',
             'collections.Counter', 'builtins.dict', 'collections.OrderedDict'}
        """
        for class_to_register in [cls] + list(all_child_classes(cls)):
            if ignore_abstract_class and inspect.isabstract(class_to_register):
                continue
            self.register_object(class_to_register)

    def register_object(self, obj, name: Optional[str] = None) -> None:
        r"""Registers an object.

        Please read the documentation for more information.

        Args:
            obj: Specifies the object to register. The object is
                expected to be a class or a function.
            name (str, optional): Specifies the name to use to
                register the object. If ``None``, the full name of
                the object is used as name. Default: ``None``.

        Example usage:

        .. code-block:: python

            >>> from objectory import Registry
            >>> registry = Registry()
            >>> class ClassToRegister:
            ...     ...
            >>> registry.registered_names()
            {'__main__.ClassToRegister'}
            >>> registry.register_object(ClassToRegister)
            >>> def function_to_register(*args, **kwargs):
            ...     ...
            >>> registry.register_object(function_to_register)
            >>> registry.registered_names()
            {'__main__.ClassToRegister', '__main__.function_to_register'}
        """
        self._check_object(obj)
        if name is None:
            name = full_object_name(obj)
        elif not isinstance(name, str):
            raise TypeError(f"The name has to be a string (received: {name})")

        if name in self._state:
            if self._is_registry(name):
                raise InvalidNameFactoryError(f"The name {name} is already used by a sub-registry")
            if self._state[name] != obj:
                logger.warning(
                    f"The name {name} already exists and its value will be replaced by {obj}"
                )

        self._state[name] = obj

    def registered_names(self, include_registry: bool = True) -> set[str]:
        r"""Gets the names of all the registered objects.

        Args:
            include_registry (bool): Specifies if the other
                (sub-)registries should be included in the set.
                By default, the other (sub-)registries are included.
                Default: ``True``.

        Returns:
            set: The names of the registered objects.

        Example usage:

        .. code-block:: python

            >>> from objectory import Registry
            >>> registry = Registry()
            >>> registry.registered_names()
            # Show name of all the registered objects except the sub-registries.
            >>> registry.registered_names(include_registry=False)
        """
        if include_registry:
            return set(self._state.keys())

        names = set()
        for key, value in self._state.items():
            if not isinstance(value, Registry):
                names.add(key)
        return names

    def unregister(self, name: str) -> None:
        r"""Removes a registered object.

        Args:
            name (string): Specifies the name of the object to remove.
                This function uses the name resolution mechanism to
                find the full name if only the short name is given.

        Raises:
            ``UnregisteredObjectFactoryError`` if the name does not
                exist in the registry.

        Example usage:

        .. code-block:: python

            >>> from objectory import Registry
            >>> registry = Registry()
            >>> registry.unregister('my_package.my_module.ClassToUnregister')
        """
        resolved_name = self._resolve_name(name)
        if resolved_name is None or not self._is_name_registered(resolved_name):
            raise UnregisteredObjectFactoryError(
                f"It is not possible to remove an object which is not registered (received: {name})"
            )
        self._state.pop(resolved_name)

    def set_class_filter(self, cls: Optional[type]) -> None:
        r"""Sets the class filter so only the child classes of this class can be
        registered.

        If you set this filter, you cannot register functions.
        To unset this filter, you can use ``set_class_filter(None)``.

        Args:
            cls (class or ``None``): Specifies the class to use as
                filter. Only the child classes of this class
                can be registered.

        Raises:
            TypeError if the input is not a class or ``None``.

        Example usage:

        .. code-block:: python

            >>> from collections import Counter, OrderedDict
            >>> from objectory import Registry
            >>> registry = Registry()
            >>> registry.mapping.set_class_filter(dict)
            >>> registry.mapping.register_object(OrderedDict)
            >>> registry.mapping.register_object(int)
            objectory.errors.IncorrectObjectFactoryError: All the registered objects
            should inherit builtins.dict class (received <class 'int'>)
            >>> registry.mapping.registered_names()
            {'collections.OrderedDict'}
        """
        if cls is None:
            self._filters.pop(self._CLASS_FILTER, None)
            return

        if not inspect.isclass(cls):
            raise TypeError(f"The class filter has to be a class (received: {cls})")
        self._filters[self._CLASS_FILTER] = cls

    def _check_object(self, obj) -> None:
        r"""Checks if the object is valid for this registry before to register
        it.

        This function will raise an exception if the object is not
        valid.

        Args:
            obj: Specifies the object to check.

        Raises:
            ``IncorrectObjectFactoryError`` if it is an invalid
                object for this factory.
        """
        if is_lambda_function(obj):
            raise IncorrectObjectFactoryError(
                "It is not possible to register a lambda function. "
                "Please use a regular function instead"
            )

        filter_class = self._filters.get(self._CLASS_FILTER, None)
        if filter_class is not None and not issubclass(obj, filter_class):
            class_name = full_object_name(filter_class)
            raise IncorrectObjectFactoryError(
                f"All the registered objects should inherit {class_name} class (received {obj})"
            )

    def _get_target_from_name(self, name: str) -> Any:
        r"""Gets the class or function to used given its name.

        Args:
            name (str): Specifies the name of the class or function.

        Returns:
            The class or function.

        Raises:
            ``UnregisteredObjectFactoryError`` if it is not possible
                to find the target.
        """
        resolved_name = self._resolve_name(name)
        if resolved_name is None:
            raise UnregisteredObjectFactoryError(
                f"Unable to create the object {name}. Registered objects of {self.__name__} are "
                f"{self.registered_names(include_registry=False)}."
            )
        if not self._is_name_registered(resolved_name):
            self.register_object(import_object(resolved_name))
        return self._state[resolved_name]

    def _is_name_registered(self, name: str) -> bool:
        r"""Indicates if the name exists or not in the registry .

        Args:
            name (string): Specifies the name to check.

        Returns:
            bool: ``True`` if the name exists, otherwise ``False``.
        """
        return name in self._state

    def _is_registry(self, name: str) -> bool:
        r"""Indicates if the given is used as sub-registry.

        Args:
            name (string): Specifies the name to check.

        Returns:
            bool: ``True`` if the name is used as sub-registry, otherwise ``False``.
        """
        return isinstance(self._state[name], Registry)

    def _resolve_name(self, name: str) -> Optional[str]:
        r"""Tries to resolve the name.

        This function will look at if it can find an object which
        match with the given name. It is quite useful because there
        are several ways to load an object but only one can be
        registered. If you specify a full name (module path +
        class/function name), it will try to import the module
        and registered it if it is not registered yet.

        Args:
            name (str):

        Returns:
            ``str`` or ``None``: It returns the name to use to get the
                object if the resolution was successful,
                otherwise ``None``.
        """
        return resolve_name(name, self.registered_names(include_registry=False))
