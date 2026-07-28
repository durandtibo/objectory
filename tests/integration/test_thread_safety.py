from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor

from objectory import AbstractFactory, Registry

##############################################
#     Integration tests for thread safety     #
##############################################


def test_registry_concurrent_register_and_factory() -> None:
    r"""Register objects and instantiate them concurrently through the
    public API, mixing writers and readers on the same registry."""
    registry = Registry()
    n_classes = 200

    classes = [type(f"IntegrationClass{i}", (), {}) for i in range(n_classes)]
    for cls in classes:
        registry.register_object(cls, name=cls.__name__)

    errors: list[BaseException] = []
    lock = threading.Lock()

    def register_more(i: int) -> None:
        try:
            cls = type(f"IntegrationExtraClass{i}", (), {})
            registry.register_object(cls, name=cls.__name__)
        except Exception as exc:  # noqa: BLE001
            with lock:
                errors.append(exc)

    def instantiate(i: int) -> None:
        try:
            cls = classes[i % n_classes]
            obj = registry.factory(cls.__name__)
            assert isinstance(obj, cls)
        except Exception as exc:  # noqa: BLE001
            with lock:
                errors.append(exc)

    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(register_more, i) for i in range(100)]
        futures += [executor.submit(instantiate, i) for i in range(200)]
        for future in futures:
            future.result()

    assert not errors
    assert len(registry) == n_classes + 100


def test_registry_concurrent_get_or_create_sub_registries() -> None:
    r"""Concurrently create the same sub-registries from multiple
    threads and check that a single sub-registry instance is created per
    key."""
    registry = Registry()
    n_keys = 20
    n_workers_per_key = 25

    def create_sub_registry(key: str) -> Registry:
        return registry.get_or_create(key)

    with ThreadPoolExecutor(max_workers=64) as executor:
        futures = {
            key: [executor.submit(create_sub_registry, key) for _ in range(n_workers_per_key)]
            for key in (f"key{i}" for i in range(n_keys))
        }
        results = {key: [f.result() for f in fs] for key, fs in futures.items()}

    for key, sub_registries in results.items():
        assert all(sub_registry is sub_registries[0] for sub_registry in sub_registries)
        assert registry.get_or_create(key) is sub_registries[0]
    assert len(registry) == n_keys


def test_abstract_factory_concurrent_subclassing_and_factory() -> None:
    r"""Create subclasses of an ``AbstractFactory`` base class from
    multiple threads and instantiate them concurrently through the
    public API."""

    class IntegrationBaseClass(metaclass=AbstractFactory):
        pass

    n_subclasses = 100
    errors: list[BaseException] = []
    lock = threading.Lock()
    created: list[type] = []

    def create_subclass(i: int) -> None:
        try:
            new_cls = type(
                f"IntegrationSubClass{i}",
                (IntegrationBaseClass,),
                {},
            )
            with lock:
                created.append(new_cls)
        except Exception as exc:  # noqa: BLE001
            with lock:
                errors.append(exc)

    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(create_subclass, i) for i in range(n_subclasses)]
        for future in futures:
            future.result()

    assert not errors
    assert len(created) == n_subclasses

    def instantiate(cls: type) -> None:
        try:
            obj = IntegrationBaseClass.factory(cls.__qualname__)
            assert isinstance(obj, cls)
        except Exception as exc:  # noqa: BLE001
            with lock:
                errors.append(exc)

    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(instantiate, cls) for cls in created]
        for future in futures:
            future.result()

    assert not errors
    # +1 for IntegrationBaseClass itself, which is auto-registered.
    assert len(IntegrationBaseClass.inheritors) == n_subclasses + 1
