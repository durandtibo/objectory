# Home

<p align="center">
   <a href="https://github.com/durandtibo/objectory/actions">
      <img alt="CI" src="https://github.com/durandtibo/objectory/workflows/CI/badge.svg?event=push&branch=main">
   </a>
    <a href="https://pypi.org/project/objectory/">
      <img alt="PYPI version" src="https://img.shields.io/pypi/v/objectory">
    </a>
   <a href="https://pypi.org/project/objectory/">
      <img alt="Python" src="https://img.shields.io/pypi/pyversions/objectory.svg">
   </a>
   <a href="https://opensource.org/licenses/BSD-3-Clause">
      <img alt="BSD-3-Clause" src="https://img.shields.io/pypi/l/objectory">
   </a>
   <a href="https://codecov.io/gh/durandtibo/objectory">
      <img alt="Codecov" src="https://codecov.io/gh/durandtibo/objectory/branch/main/graph/badge.svg">
   </a>
   <a href="https://github.com/psf/black">
     <img  alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
   </a>
   <a href="https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings">
     <img  alt="Doc style: google" src="https://img.shields.io/badge/%20style-google-3666d6.svg">
   </a>
   <br/>
</p>

## Overview

A light Python library for general purpose object factories.
In particular, it focuses on dynamic object factory implementations where objects can be registered
dynamically without changing the code of the factory.
An object factory can be used to instantiate an object from its configuration.
The current implementation contains both abstract factory and registry approaches.

**abstract factory**

```python
from objectory import AbstractFactory


class BaseClass(metaclass=AbstractFactory):
    pass


class MyClass(BaseClass):
    pass


obj = BaseClass.factory("MyClass")
print(obj)
```

*Output*:

```textmate
<__main__.MyClass object at 0x123456789>
```

**[registry](registry.md)**

```python
from objectory import Registry

registry = Registry()


@registry.register()
class MyClass:
    pass


obj = registry.factory("MyClass")
print(obj)
```

```textmate
<__main__.MyClass object at 0x123456789>
```

## API stability

:warning: While `objectory` is in development stage, no API is guaranteed to be stable from one
release to the next.
In fact, it is very likely that the API will change multiple times before a stable 1.0.0 release.
In practice, this means that upgrading `objectory` to a new version will possibly break any code
that
was using the old version of `objectory`.

## License

`objectory` is licensed under BSD 3-Clause "New" or "Revised" license available
in [LICENSE](https://github.com/durandtibo/objectory/blob/main/LICENSE) file.
