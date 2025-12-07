"""Basic usage of the universal factory function.

This example demonstrates how to use the universal factory function
to instantiate objects dynamically without prior registration.
"""

from __future__ import annotations

from objectory import factory


def main() -> None:
    """Demonstrate basic factory usage."""
    print("=" * 60)
    print("Basic Factory Usage Examples")
    print("=" * 60)

    # Example 1: Create standard library objects
    print("\n1. Creating a Counter from collections:")
    counter = factory("collections.Counter", [1, 2, 1, 3, 2, 1])
    print(f"   Result: {counter}")

    # Example 2: Create a defaultdict
    print("\n2. Creating a defaultdict:")
    default_dict = factory("collections.defaultdict", int)
    default_dict["a"] += 1
    default_dict["b"] += 2
    print(f"   Result: {dict(default_dict)}")

    # Example 3: Create a deque
    print("\n3. Creating a deque:")
    deque = factory("collections.deque", [1, 2, 3], maxlen=3)
    print(f"   Result: {deque}")

    # Example 4: Instantiate with keyword arguments
    print("\n4. Creating an OrderedDict:")
    ordered_dict = factory("collections.OrderedDict", [("a", 1), ("b", 2), ("c", 3)])
    print(f"   Result: {ordered_dict}")

    # Example 5: Using built-in types
    print("\n5. Creating a list:")
    my_list = factory("builtins.list", [4, 5, 6])
    print(f"   Result: {my_list}")

    # Example 6: Creating a set
    print("\n6. Creating a set:")
    my_set = factory("builtins.set", [1, 2, 2, 3, 3, 3])
    print(f"   Result: {my_set}")

    # Example 7: Using pathlib
    print("\n7. Creating a Path object:")
    path = factory("pathlib.Path", "/tmp/example")
    print(f"   Result: {path}")
    print(f"   Type: {type(path)}")

    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
