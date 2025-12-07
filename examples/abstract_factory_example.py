"""Using the AbstractFactory metaclass.

This example demonstrates how to use the AbstractFactory metaclass
to create a factory pattern with automatic registration through inheritance.
"""

from __future__ import annotations

from objectory import AbstractFactory


# Define base class with AbstractFactory metaclass
class DataProcessor(metaclass=AbstractFactory):
    """Base class for data processors."""

    def process(self, data: list) -> list:
        """Process data."""
        raise NotImplementedError


# Child classes are automatically registered
class UppercaseProcessor(DataProcessor):
    """Convert strings to uppercase."""

    def process(self, data: list) -> list:
        """Process data by converting to uppercase."""
        return [item.upper() if isinstance(item, str) else item for item in data]


class LowercaseProcessor(DataProcessor):
    """Convert strings to lowercase."""

    def process(self, data: list) -> list:
        """Process data by converting to lowercase."""
        return [item.lower() if isinstance(item, str) else item for item in data]


class FilterProcessor(DataProcessor):
    """Filter data based on a condition."""

    def __init__(self, min_length: int = 0) -> None:
        """Initialize with minimum length filter."""
        self.min_length = min_length

    def process(self, data: list) -> list:
        """Process data by filtering strings shorter than min_length."""
        return [item for item in data if isinstance(item, str) and len(item) >= self.min_length]


class ReverseProcessor(DataProcessor):
    """Reverse strings in the data."""

    def process(self, data: list) -> list:
        """Process data by reversing strings."""
        return [item[::-1] if isinstance(item, str) else item for item in data]


def main() -> None:
    """Demonstrate AbstractFactory usage."""
    print("=" * 60)
    print("AbstractFactory Usage Examples")
    print("=" * 60)

    # Sample data
    data = ["Hello", "World", "Python", "AI"]

    # Example 1: View registered classes
    print("\n1. Registered processors:")
    for name in sorted(DataProcessor.inheritors.keys()):
        print(f"   - {name}")

    # Example 2: Create processor using short name
    print("\n2. Using UppercaseProcessor:")
    processor = DataProcessor.factory("UppercaseProcessor")
    result = processor.process(data)
    print(f"   Input:  {data}")
    print(f"   Output: {result}")

    # Example 3: Create processor using full name
    print("\n3. Using LowercaseProcessor with full name:")
    processor = DataProcessor.factory(
        "__main__.LowercaseProcessor"
        if __name__ == "__main__"
        else "examples.abstract_factory_example.LowercaseProcessor"
    )
    result = processor.process(data)
    print(f"   Input:  {data}")
    print(f"   Output: {result}")

    # Example 4: Create processor with arguments
    print("\n4. Using FilterProcessor with min_length=6:")
    processor = DataProcessor.factory("FilterProcessor", min_length=6)
    result = processor.process(data)
    print(f"   Input:  {data}")
    print(f"   Output: {result}")

    # Example 5: Chain processors
    print("\n5. Chaining processors (uppercase then reverse):")
    uppercase_proc = DataProcessor.factory("UppercaseProcessor")
    reverse_proc = DataProcessor.factory("ReverseProcessor")
    result = uppercase_proc.process(data)
    result = reverse_proc.process(result)
    print(f"   Input:  {data}")
    print(f"   Output: {result}")

    # Example 6: Create from child class
    print("\n6. Factory can be called from any child class:")
    processor = UppercaseProcessor.factory("LowercaseProcessor")
    result = processor.process(data)
    print("   Created LowercaseProcessor from UppercaseProcessor.factory()")
    print(f"   Output: {result}")

    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
