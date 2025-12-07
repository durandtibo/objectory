"""Building a plugin system with objectory.

This example demonstrates how to use objectory to build a flexible
plugin system where plugins can be loaded dynamically.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from objectory import AbstractFactory


class Plugin(ABC, metaclass=AbstractFactory):
    """Base class for all plugins."""

    @abstractmethod
    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute the plugin logic.

        Args:
            context: Input context dictionary

        Returns:
            Updated context dictionary
        """


class LoggingPlugin(Plugin):
    """Plugin that logs messages."""

    def __init__(self, prefix: str = "[LOG]") -> None:
        """Initialize logging plugin."""
        self.prefix = prefix

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Log a message from the context."""
        message = context.get("message", "No message")
        print(f"{self.prefix} {message}")
        context["logged"] = True
        return context


class ValidationPlugin(Plugin):
    """Plugin that validates data."""

    def __init__(self, required_keys: list[str] | None = None) -> None:
        """Initialize validation plugin."""
        self.required_keys = required_keys or []

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Validate that required keys are present."""
        missing_keys = [key for key in self.required_keys if key not in context]
        if missing_keys:
            context["valid"] = False
            context["errors"] = f"Missing keys: {missing_keys}"
        else:
            context["valid"] = True
        return context


class TransformPlugin(Plugin):
    """Plugin that transforms data."""

    def __init__(self, operation: str = "uppercase") -> None:
        """Initialize transform plugin."""
        self.operation = operation

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Transform the message in the context."""
        message = context.get("message", "")
        if self.operation == "uppercase":
            context["message"] = message.upper()
        elif self.operation == "lowercase":
            context["message"] = message.lower()
        elif self.operation == "reverse":
            context["message"] = message[::-1]
        return context


class FilterPlugin(Plugin):
    """Plugin that filters data."""

    def __init__(self, min_length: int = 0) -> None:
        """Initialize filter plugin."""
        self.min_length = min_length

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Filter messages that are too short."""
        message = context.get("message", "")
        if len(message) < self.min_length:
            context["filtered"] = True
            context["message"] = ""
        else:
            context["filtered"] = False
        return context


class PluginManager:
    """Manager for loading and executing plugins."""

    def __init__(self) -> None:
        """Initialize plugin manager."""
        self.plugins: list[Plugin] = []

    def load_plugin(self, plugin_config: dict[str, Any]) -> None:
        """Load a plugin from configuration.

        Args:
            plugin_config: Dictionary with '_target_' and plugin arguments
        """
        plugin = Plugin.factory(**plugin_config)
        self.plugins.append(plugin)
        print(f"Loaded plugin: {plugin.__class__.__name__}")

    def execute_pipeline(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute all plugins in sequence.

        Args:
            context: Initial context

        Returns:
            Final context after all plugins
        """
        for plugin in self.plugins:
            context = plugin.execute(context)
        return context

    def clear_plugins(self) -> None:
        """Clear all loaded plugins."""
        self.plugins.clear()


def main() -> None:
    """Demonstrate plugin system usage."""
    print("=" * 60)
    print("Plugin System Example")
    print("=" * 60)

    # Example 1: Simple pipeline
    print("\n1. Simple logging and transformation pipeline:")
    manager = PluginManager()

    # Load plugins from configuration
    manager.load_plugin({"_target_": "LoggingPlugin", "prefix": "[BEFORE]"})
    manager.load_plugin({"_target_": "TransformPlugin", "operation": "uppercase"})
    manager.load_plugin({"_target_": "LoggingPlugin", "prefix": "[AFTER]"})

    # Execute pipeline
    context = {"message": "hello world"}
    print(f"Initial context: {context}")
    result = manager.execute_pipeline(context)
    print(f"Final context: {result}")

    # Example 2: Validation and filtering pipeline
    print("\n2. Validation and filtering pipeline:")
    manager.clear_plugins()

    manager.load_plugin(
        {"_target_": "ValidationPlugin", "required_keys": ["message", "user"]}
    )
    manager.load_plugin({"_target_": "FilterPlugin", "min_length": 5})
    manager.load_plugin({"_target_": "LoggingPlugin"})

    # Test with valid data
    context = {"message": "Hello, World!", "user": "Alice"}
    print(f"Valid data: {context}")
    result = manager.execute_pipeline(context)
    print(f"Result: {result}")

    # Test with invalid data
    manager.clear_plugins()
    manager.load_plugin(
        {"_target_": "ValidationPlugin", "required_keys": ["message", "user"]}
    )
    context = {"message": "Hi"}
    print(f"\nInvalid data: {context}")
    result = manager.execute_pipeline(context)
    print(f"Result: {result}")

    # Example 3: Complex transformation pipeline
    print("\n3. Complex transformation pipeline:")
    manager.clear_plugins()

    manager.load_plugin({"_target_": "TransformPlugin", "operation": "lowercase"})
    manager.load_plugin({"_target_": "FilterPlugin", "min_length": 3})
    manager.load_plugin({"_target_": "TransformPlugin", "operation": "uppercase"})
    manager.load_plugin({"_target_": "TransformPlugin", "operation": "reverse"})

    context = {"message": "Python Programming"}
    print(f"Input: {context}")
    result = manager.execute_pipeline(context)
    print(f"Output: {result}")

    # Example 4: Available plugins
    print("\n4. Available plugins:")
    for name in sorted(Plugin.inheritors.keys()):
        print(f"   - {name}")

    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
