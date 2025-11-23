from __future__ import annotations

from objectory.utils import all_child_classes

#############################
#     all_child_classes     #
#############################


def test_all_child_classes() -> None:
    class Foo: ...

    assert all_child_classes(Foo) == set()

    class Bar(Foo): ...

    assert all_child_classes(Foo) == {Bar}

    class Baz(Foo): ...

    assert all_child_classes(Foo) == {Bar, Baz}

    class Bing(Bar): ...

    assert all_child_classes(Foo) == {Bar, Baz, Bing}
