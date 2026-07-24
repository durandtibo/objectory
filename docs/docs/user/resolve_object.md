# Resolve Object

`resolve_object` is a small helper built on top of the [universal factory](universal_factory.md).
It is meant for the common case where a value can be *either* an already-configured instance
*or* an objectory configuration dictionary describing how to build one, and you want a single
line of code that returns a real instance either way.

## Basic Usage

```python
from datetime import date
from objectory import resolve_object

# From an existing instance: returned as-is.
d1 = resolve_object(date(2020, 1, 1), cls=date)

# From a configuration dictionary: built with `factory`.
d2 = resolve_object(
    {"_target_": "datetime.date", "year": 2020, "month": 1, "day": 1},
    cls=date,
)
```

Both `d1` and `d2` are `date` instances. This is typically used to normalize a constructor or
function argument that users may pass either as a ready-made object or as a config dict, for
example when loading settings from YAML/JSON.

```python
from objectory import resolve_object


class Optimizer:
    pass


class SGD(Optimizer):
    def __init__(self, lr: float = 0.01) -> None:
        self.lr = lr


class Trainer:
    def __init__(self, optimizer: Optimizer | dict):
        # Accepts either an Optimizer instance or an objectory config dict.
        self.optimizer = resolve_object(optimizer, cls=Optimizer)


trainer1 = Trainer(SGD(lr=0.1))
trainer2 = Trainer({"_target_": "__main__.SGD", "lr": 0.1})
```

## Function Signature

```python notest
def resolve_object(obj: T | dict[str, Any], cls: type[T] = object) -> T
```

### Parameters

- **obj**: Either a fully configured instance of `cls`, or a `dict` containing an objectory
  factory specification (must include a `"_target_"` key pointing to the fully qualified class
  name).
- **cls** (optional): The expected type, used to validate the resolved object whether `obj` was
  already an instance or was built from a configuration dictionary. Defaults to `object`, which
  accepts any resolved value without validation.

### Returns

A configured instance of `cls`.

### Raises

- **IncorrectTypeFactoryError**: if `obj` is a `dict` missing the `"_target_"` key, or if the
  resolved object is not an instance of `cls`.

## Dict Subclasses Are Always Treated as Configuration

`resolve_object` decides whether `obj` needs to be built by checking `isinstance(obj, dict)`.
This means **any** `dict` subclass — including `Counter`, `OrderedDict`, or your own
`dict` subclass — is always treated as a factory configuration, even if it is already a valid
instance of `cls`:

```python
from collections import OrderedDict
from objectory import resolve_object

# OrderedDict IS a dict subclass, so it is (incorrectly) treated as a config
# and objectory looks for a "_target_" key in it, raising an error here.
od = OrderedDict(a=1)
resolve_object(od, cls=OrderedDict)  # raises IncorrectTypeFactoryError
```

Do not use `resolve_object` for values whose expected type is itself a `dict` subclass.

## When to Use `resolve_object`

Use `resolve_object` when:

- A field or argument may be provided either as a real object or as an objectory config dict.
- You want type validation as part of the resolution (via `cls`).
- The expected type is not a `dict` subclass.

If you always have a config dict and never a pre-built instance, use [`factory`](universal_factory.md)
directly instead.

## See Also

- [Universal Factory](universal_factory.md) - The lower-level function `resolve_object` uses to
  build objects from configuration dictionaries.
