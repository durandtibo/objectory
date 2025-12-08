# Universal Factory

The universal factory is the simplest way to use objectory. It provides a single `factory()` function that can instantiate any Python object by its fully qualified name, without requiring prior registration.

## Basic Usage

The `factory()` function takes a target string and optional arguments:

```python
from objectory import factory

# Create a Counter from collections
counter = factory("collections.Counter", [1, 2, 1, 3])
print(counter)  # Counter({1: 2, 2: 1, 3: 1})

# Create a Path object
path = factory("pathlib.Path", "/tmp/data")
print(path)  # /tmp/data
```

## Function Signature

```python
def factory(
    _target_: str,
    *args: Any,
    _init_: str = "__init__",
    **kwargs: Any
) -> Any
```

### Parameters

- **_target_** (str): The fully qualified name of the object (class or function) to instantiate
  - Examples: `"collections.Counter"`, `"pathlib.Path"`, `"builtins.list"`
- **\*args**: Positional arguments to pass to the constructor or function
- **_init_** (str, optional): The initialization method to use (default: `"__init__"`)
  - Can be `"__init__"`, `"__new__"`, or the name of a class method
- **\*\*kwargs**: Keyword arguments to pass to the constructor or function

### Returns

The instantiated object with the given parameters.

### Raises

- **RuntimeError**: If the target cannot be found or imported

## Examples

### Creating Standard Library Objects

```python
from objectory import factory

# Lists and collections
my_list = factory("builtins.list", [1, 2, 3])
my_set = factory("builtins.set", [1, 2, 2, 3])
deque = factory("collections.deque", [1, 2, 3], maxlen=5)

# Dictionaries
counter = factory("collections.Counter", [1, 2, 1])
ordered_dict = factory("collections.OrderedDict", [("a", 1), ("b", 2)])
default_dict = factory("collections.defaultdict", list)

# Path objects
path = factory("pathlib.Path", "/tmp/example")
```

### Using Keyword Arguments

```python
from objectory import factory

# Create objects with keyword arguments
ordered_dict = factory("collections.OrderedDict", a=1, b=2, c=3)

# Mix positional and keyword arguments
deque = factory("collections.deque", [1, 2, 3], maxlen=5)
```

### Using Custom Initialization Methods

You can specify a different initialization method using the `_init_` parameter:

```python
from objectory import factory

class MyClass:
    def __init__(self, value: int):
        self.value = value
    
    @classmethod
    def from_string(cls, s: str):
        return cls(int(s))
    
    @classmethod
    def default(cls):
        return cls(0)

# Register the class (for this example, we'll use it directly)
# In practice, you'd have it in a module

# Using default constructor
obj1 = factory("__main__.MyClass", 42)

# Using class method
obj2 = factory("__main__.MyClass", "42", _init_="from_string")

# Using default factory method
obj3 = factory("__main__.MyClass", _init_="default")
```

## Comparison with Other Approaches

### Universal Factory vs AbstractFactory

**Universal Factory:**
- ✅ No registration needed
- ✅ Works with any importable object
- ✅ Simple to use
- ❌ No inheritance-based organization
- ❌ No automatic discovery

**AbstractFactory:**
- ✅ Automatic registration through inheritance
- ✅ Organized object families
- ✅ Supports short names
- ❌ Requires metaclass
- ❌ More setup required

### Universal Factory vs Registry

**Universal Factory:**
- ✅ No registration needed
- ✅ Works immediately
- ✅ Simple API
- ❌ No filters or validation
- ❌ No sub-registries

**Registry:**
- ✅ Fine-grained control
- ✅ Sub-registries for organization
- ✅ Class filters
- ❌ Manual registration required
- ❌ More complex

## When to Use Universal Factory

Use the universal factory when:

- You need to instantiate objects from configuration files
- You want a simple, no-setup solution
- You're working with third-party libraries
- You don't need object organization or validation
- You have fully qualified names available

## Configuration File Integration

The universal factory works great with YAML/JSON configuration files:

**config.yaml:**
```yaml
database:
  _target_: collections.OrderedDict
  host: localhost
  port: 5432
  database: myapp

cache:
  _target_: collections.defaultdict
  default_factory: int
```

**Loading configuration:**
```python
import yaml
from objectory import factory

with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Create database config
db = factory(**config["database"])
print(db)  # OrderedDict([('host', 'localhost'), ('port', 5432), ...])

# Create cache
cache = factory(**config["cache"])
print(type(cache))  # <class 'collections.defaultdict'>
```

## Best Practices

### 1. Use Full Qualified Names

Always use the full module path to avoid ambiguity:

```python
# Good
factory("collections.Counter")

# Avoid (may not work)
factory("Counter")
```

### 2. Validate Input for Security

Never use untrusted user input directly with the factory:

```python
# BAD - Security risk!
user_input = request.get("class")
obj = factory(user_input)

# GOOD - Validate against allowlist
ALLOWED_CLASSES = {"collections.Counter", "collections.defaultdict"}
user_input = request.get("class")
if user_input not in ALLOWED_CLASSES:
    raise ValueError("Class not allowed")
obj = factory(user_input)
```

### 3. Handle Errors Gracefully

The factory raises `RuntimeError` if the target cannot be found:

```python
from objectory import factory

try:
    obj = factory("non.existent.Module")
except RuntimeError as e:
    print(f"Failed to create object: {e}")
```

### 4. Document Configuration Schema

When using with configuration files, document the expected structure:

```python
"""
Configuration schema:

database:
  _target_: str          # Fully qualified class name
  host: str              # Database host
  port: int              # Database port
  database: str          # Database name
"""
```

## Advanced Usage

### Creating Custom Factory Wrappers

You can create type-safe wrappers around the universal factory:

```python
from typing import Any
from objectory import factory
from pathlib import Path

def create_path(path_str: str, **kwargs: Any) -> Path:
    """Create a Path object."""
    return factory("pathlib.Path", path_str, **kwargs)

def create_counter(items: list, **kwargs: Any):
    """Create a Counter object."""
    return factory("collections.Counter", items, **kwargs)

# Usage
path = create_path("/tmp/data")
counter = create_counter([1, 2, 1, 3])
```

### Lazy Object Creation

Create a factory function that delays instantiation:

```python
from typing import Any, Callable
from objectory import factory

def lazy_factory(target: str, *args: Any, **kwargs: Any) -> Callable:
    """Return a function that creates the object when called."""
    def create():
        return factory(target, *args, **kwargs)
    return create

# Create lazy constructors
create_counter = lazy_factory("collections.Counter", [1, 2, 3])
create_path = lazy_factory("pathlib.Path", "/tmp")

# Instantiate when needed
counter = create_counter()
path = create_path()
```

## Limitations

1. **No object discovery**: The factory cannot list available objects
2. **No validation**: The factory doesn't validate if objects are compatible
3. **Requires full names**: Short names are not supported (use AbstractFactory or Registry for that)
4. **No caching**: Each call creates a new object instance

## See Also

- [AbstractFactory](abstract_factory.md) - For inheritance-based factories
- [Registry](registry.md) - For manual registration with more control
- [Name Resolution](name_resolution.md) - Understanding how names are resolved
