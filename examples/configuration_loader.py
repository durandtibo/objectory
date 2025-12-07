"""Loading objects from configuration files.

This example demonstrates how to use objectory to instantiate
objects from configuration dictionaries, useful for YAML/JSON configs.
"""

from __future__ import annotations

from typing import Any

from objectory import factory


# Simulated configuration data (typically loaded from YAML/JSON)
CONFIGS = {
    "database": {
        "_target_": "collections.OrderedDict",
        "host": "localhost",
        "port": 5432,
        "database": "myapp",
        "username": "admin",
    },
    "cache": {"_target_": "collections.defaultdict", "default_factory": int},
    "data_structures": {
        "counter": {"_target_": "collections.Counter"},
        "deque": {"_target_": "collections.deque", "maxlen": 5},
        "ordered_dict": {
            "_target_": "collections.OrderedDict",
            "a": 1,
            "b": 2,
            "c": 3,
        },
    },
}


def load_object_from_config(config: dict[str, Any]) -> Any:
    """Load an object from a configuration dictionary.

    Args:
        config: Configuration dictionary with '_target_' key

    Returns:
        Instantiated object
    """
    if not isinstance(config, dict) or "_target_" not in config:
        return config

    # Extract target and remove it from config
    target = config.pop("_target_")

    # Handle positional arguments (stored with empty string key)
    args = []
    if "" in config:
        args_value = config.pop("")
        args = args_value if isinstance(args_value, list) else [args_value]

    # Handle special case for default_factory (needs to be a callable)
    if "default_factory" in config:
        factory_obj = config.pop("default_factory")
        if isinstance(factory_obj, str):
            # Import the callable and add it as first argument for defaultdict
            if factory_obj == "int":
                args.insert(0, int)
            elif factory_obj == "list":
                args.insert(0, list)
            elif factory_obj == "dict":
                args.insert(0, dict)
        elif callable(factory_obj):
            # If it's already a callable, use it directly
            args.insert(0, factory_obj)

    # Create the object
    return factory(target, *args, **config)


def load_nested_config(config: dict[str, Any]) -> dict[str, Any]:
    """Load objects from a nested configuration dictionary.

    Args:
        config: Nested configuration dictionary

    Returns:
        Dictionary with instantiated objects
    """
    result = {}
    for key, value in config.items():
        if isinstance(value, dict):
            if "_target_" in value:
                result[key] = load_object_from_config(value)
            else:
                result[key] = load_nested_config(value)
        else:
            result[key] = value
    return result


def main() -> None:
    """Demonstrate configuration-based object loading."""
    print("=" * 60)
    print("Configuration Loader Example")
    print("=" * 60)

    # Example 1: Load a single object
    print("\n1. Loading database configuration as OrderedDict:")
    db_config = CONFIGS["database"].copy()
    db_obj = load_object_from_config(db_config)
    print(f"   Type: {type(db_obj).__name__}")
    print(f"   Contents: {db_obj}")

    # Example 2: Load cache with default factory
    print("\n2. Loading cache configuration as defaultdict:")
    cache_config = CONFIGS["cache"].copy()
    cache_obj = load_object_from_config(cache_config)
    # Access keys to demonstrate default factory behavior
    _ = cache_obj["hits"]  # This will create entry with default value 0
    _ = cache_obj["misses"]  # This will create entry with default value 0
    cache_obj["hits"] += 5
    cache_obj["misses"] += 2
    print(f"   Type: {type(cache_obj).__name__}")
    print(f"   Contents: {dict(cache_obj)}")

    # Example 3: Load nested configurations
    print("\n3. Loading nested data structures:")
    data_config = CONFIGS["data_structures"].copy()
    data_objects = load_nested_config(data_config)
    for name, obj in data_objects.items():
        print(f"   {name}: {type(obj).__name__} = {obj}")

    # Example 4: Configuration from "YAML-like" structure
    print("\n4. Simulating YAML-style configuration:")
    yaml_like_config = """
    Database Config:
        _target_: collections.OrderedDict
        host: db.example.com
        port: 5432

    Cache Config:
        _target_: collections.defaultdict
        default_factory: int
    """
    print(yaml_like_config)
    print("   (In practice, you would use yaml.safe_load() here)")

    # Example 5: Building complex objects
    print("\n5. Building complex nested structure:")
    complex_config = {
        "services": {
            "api": {
                "_target_": "collections.OrderedDict",
                "url": "https://api.example.com",
                "timeout": 30,
            },
            "cache": {"_target_": "collections.defaultdict", "default_factory": list},
        }
    }
    services = load_nested_config(complex_config)
    print(f"   Services: {services}")

    # Example 6: Using with path objects
    print("\n6. Creating Path objects from config:")
    path_config = {"_target_": "pathlib.Path", "": ["/tmp/myapp/data"]}
    path_obj = load_object_from_config(path_config)
    print(f"   Type: {type(path_obj).__name__}")
    print(f"   Path: {path_obj}")
    print(f"   Parent: {path_obj.parent}")

    # Example 7: Error handling
    print("\n7. Handling invalid configuration:")
    try:
        invalid_config = {"_target_": "non.existent.Module"}
        load_object_from_config(invalid_config)
    except RuntimeError as e:
        print(f"   Caught expected error: {e}")

    print("\n" + "=" * 60)
    print("Configuration Loading Best Practices:")
    print("=" * 60)
    print(
        """
1. Always validate configurations before loading
2. Use '_target_' key to specify the fully qualified name
3. Store positional args with empty string key: "": [arg1, arg2]
4. Handle special cases (like callables) explicitly
5. Consider using a schema validator (e.g., Pydantic)
6. Log loaded configurations for debugging
7. Use try-except blocks for error handling
    """
    )

    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
