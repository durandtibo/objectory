# Frequently Asked Questions (FAQ)

## General Questions

### What is objectory?

objectory is a Python library that provides general-purpose object factories. It allows you to instantiate objects dynamically without hardcoding class names, making your code more flexible and maintainable. It supports three main approaches: universal factory, abstract factory, and registry patterns.

### When should I use objectory?

objectory is useful when you need to:

- Load objects dynamically from configuration files
- Build plugin systems
- Create flexible application architectures
- Avoid tight coupling between classes
- Support multiple implementations that can be switched at runtime

### What are the differences between the three factory approaches?

- **Universal Factory** (`factory()`): No registration needed, works with any importable object
- **AbstractFactory**: Automatic registration through inheritance, best for related object families
- **Registry**: Manual registration with decorators or methods, provides fine-grained control

## Installation

### What Python versions are supported?

objectory supports Python 3.10 and later. See the [get_started](get_started.md) page for the compatibility matrix.

### How do I install objectory?

Using `uv`:
```shell
uv pip install objectory
```

Using `pip`:
```shell
pip install objectory
```

For more installation options, see the [get_started](get_started.md) page.

### Can I use objectory without installing it?

For development or testing, you can clone the repository and install it in editable mode:

```shell
git clone https://github.com/durandtibo/objectory.git
cd objectory
pip install -e .
```

## Usage Questions

### How do I instantiate an object using the universal factory?

```python
from objectory import factory

# Using full module path with positional arguments
obj = factory("collections.Counter", [1, 2, 3])

# Using a single positional argument
obj = factory("pathlib.Path", "/tmp/example")

# With keyword arguments
obj = factory("collections.OrderedDict", a=1, b=2)
```

### Can I use custom class methods for initialization?

Yes! Use the `_init_` parameter:

```python
class MyClass:
    def __init__(self, value):
        self.value = value
    
    @classmethod
    def from_string(cls, s):
        return cls(int(s))

# Using custom initializer
obj = BaseClass.factory(_target_="MyClass", _init_="from_string", s="42")
```

### How do I resolve ambiguous class names?

If multiple classes have the same name, use the full qualified name:

```python
# Ambiguous - will raise an error if multiple "Linear" classes exist
obj = BaseClass.factory("Linear")

# Unambiguous - specifies exact class
obj = BaseClass.factory("torch.nn.modules.linear.Linear")
```

### Can I register third-party library classes?

Yes! Use `register_object()`:

```python
import torch
from objectory import AbstractFactory

class BaseModule(torch.nn.Module, metaclass=AbstractFactory):
    pass

# Register PyTorch's Linear
BaseModule.register_object(torch.nn.Linear)

# Now you can use it
linear = BaseModule.factory("torch.nn.Linear", in_features=10, out_features=5)
```

### How do I see what's registered in a factory?

For `AbstractFactory`:

```python
print(BaseClass.inheritors)
```

For `Registry`:

```python
print(registry.registered_names())
```

### Can I use objectory with configuration files?

Yes! objectory works great with YAML/JSON configs:

```python
import yaml
from objectory import factory

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Instantiate from config
obj = factory(**config)
```

See the [configuration_loader.py](https://github.com/durandtibo/objectory/blob/main/examples/configuration_loader.py) example for more details.

## Advanced Questions

### How does name resolution work?

The name resolution mechanism tries to find objects in this order:

1. Exact match in registered objects
2. Single match by class name only
3. Import and register the object dynamically

See the [name resolution](name_resolution.md) documentation for details.

### Can I use objectory in a multithreaded environment?

Be careful with registration. Register objects before starting threads to avoid race conditions. Factory calls themselves are thread-safe as they only read from the registry.

### How do I create a plugin system with objectory?

Check out the [plugin_system.py](https://github.com/durandtibo/objectory/blob/main/examples/plugin_system.py) example, which shows a complete plugin architecture.

### Can I register functions, not just classes?

Yes! Both `AbstractFactory` and `Registry` support function registration:

```python
from objectory import Registry

registry = Registry()

@registry.register()
def my_function(x, y):
    return x + y

result = registry.factory(_target_="my_function", x=1, y=2)
```

### How do I unregister objects?

For `AbstractFactory`:

```python
BaseClass.unregister("MyClass")
```

For `Registry`:

```python
registry.unregister("MyClass")
```

### Can I clear all registered objects?

For `Registry`:

```python
# Clear current registry
registry.clear()

# Clear including sub-registries
registry.clear(nested=True)
```

For `AbstractFactory`, objects are registered permanently and cannot be cleared (this is by design).

### How do I handle circular dependencies?

Avoid circular imports by:

1. Registering objects in `__init__.py` files
2. Using lazy imports
3. Structuring your code to avoid circular dependencies

### Can I use objectory with type hints?

Yes! For better IDE support:

```python
from typing import TypeVar
from objectory import AbstractFactory

T = TypeVar('T', bound='BaseClass')

class BaseClass(metaclass=AbstractFactory):
    @classmethod
    def factory(cls, _target_: str, *args, **kwargs) -> 'BaseClass':
        return super().factory(_target_, *args, **kwargs)
```

## Troubleshooting

### I get "UnregisteredObjectFactoryError"

This means the object hasn't been registered. Solutions:

1. Make sure the module containing the class has been imported
2. Check the class inherits from the base factory class
3. Use `register_object()` to manually register it
4. Verify the class name spelling

### My object isn't showing up in `inheritors`

The object must be imported at least once to be registered. Solutions:

1. Import the module in your `__init__.py`
2. Use the `register_child_classes()` function
3. Call `register_object()` explicitly

### I get a "RuntimeError: The target object does not exist"

The universal factory cannot find the object. Check:

1. Is the module path correct?
2. Is the package installed?
3. Can you import it manually with `from x import y`?

### Performance concerns with large numbers of registered objects

The registry lookup is O(1) for exact matches and O(n) for name resolution. For better performance:

1. Use full qualified names when possible
2. Avoid having many objects with the same class name
3. Consider using multiple registries to partition objects

## Security

### Is it safe to use user input with factory functions?

⚠️ **No!** Never pass untrusted user input directly to factory functions. The factory can instantiate any Python object, which could be a security risk.

Always validate and sanitize input:

```python
# BAD - Don't do this!
user_class = request.get("class_name")
obj = factory(user_class)

# GOOD - Validate against allowlist
ALLOWED_CLASSES = {"collections.Counter", "collections.defaultdict"}
user_class = request.get("class_name")
if user_class not in ALLOWED_CLASSES:
    raise ValueError("Class not allowed")
obj = factory(user_class)
```

See [SECURITY.md](https://github.com/durandtibo/objectory/blob/main/SECURITY.md) for more security guidelines.

## Contributing

### How can I contribute to objectory?

We welcome contributions! See [CONTRIBUTING.md](https://github.com/durandtibo/objectory/blob/main/.github/CONTRIBUTING.md) for guidelines.

### I found a bug, what should I do?

Please [open an issue](https://github.com/durandtibo/objectory/issues) on GitHub with:

- A clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your Python version and objectory version

### Can I request a feature?

Yes! Open a [feature request issue](https://github.com/durandtibo/objectory/issues) on GitHub. Please describe:

- The use case
- Why existing features don't work
- Proposed API (if applicable)

## Getting Help

### Where can I ask questions?

- Open a [discussion](https://github.com/durandtibo/objectory/discussions) on GitHub
- Open an [issue](https://github.com/durandtibo/objectory/issues) for bugs or feature requests
- Check existing documentation and examples

### Are there more examples?

Yes! Check the [examples directory](https://github.com/durandtibo/objectory/tree/main/examples) for practical examples covering various use cases.
