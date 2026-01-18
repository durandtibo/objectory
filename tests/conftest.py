"""Pytest configuration and test style guide for the objectory test suite.

This file serves as both pytest configuration and documentation for the
testing conventions used throughout the objectory project.

================================================================================
TEST STYLE GUIDE
================================================================================

This guide defines the consistent style for all test files in the objectory
test suite. Following these conventions ensures maintainability and readability.

1. FILE STRUCTURE
-----------------
Every test file should follow this structure:

    ```python
    '''\"\"\"Module-level docstring describing what is being tested.\"\"\"
    
    from __future__ import annotations
    
    # Standard library imports (alphabetical)
    import logging
    from abc import ABC, abstractmethod
    from collections import Counter
    
    # Third-party imports (alphabetical)
    import pytest
    
    # Local imports (alphabetical)
    from objectory import Registry, factory
    from objectory.errors import IncorrectObjectFactoryError
    
    
    # Test fixtures and helper classes/functions
    class FakeClass:
        \"\"\"Helper class for testing.\"\"\"
        pass
    
    
    @pytest.fixture
    def fixture_name():
        \"\"\"Fixture docstring.\"\"\"
        return value
    
    
    ####################################
    #     Tests for functionality      #
    ####################################
    
    
    def test_something() -> None:
        \"\"\"Test that something works as expected.\"\"\"
        assert True
    ```

2. SECTION HEADERS
------------------
Use consistent section headers with exactly 36 '#' characters:

    ####################################
    #     Tests for functionality      #
    ####################################

The text should be padded with spaces to fit nicely. Common sections:
- Tests for factory
- Tests for register
- Tests for unregister
- Tests for import_object
- Tests for instantiate_object

3. TEST FUNCTION NAMING
-----------------------
Follow the pattern: test_<functionality>_<specific_case>

Examples:
- test_factory_with_valid_object
- test_factory_raises_error_for_invalid_target
- test_register_object_with_custom_name
- test_is_object_config_returns_false_for_missing_target

Guidelines:
- Use descriptive names that explain WHAT is being tested
- Be specific about the scenario (e.g., "with_kwargs", "raises_error", "returns_false")
- Don't abbreviate excessively - clarity over brevity

4. DOCSTRINGS
-------------
ALL test functions MUST have docstrings that explain:
- WHAT is being tested
- WHY it matters (if not obvious)

Format:
    def test_something() -> None:
        \"\"\"Test that factory creates objects from valid targets.
        
        This ensures the factory can handle both built-in and custom classes.
        \"\"\"

For simple tests, a single-line docstring is sufficient:
    def test_factory_with_counter() -> None:
        \"\"\"Test factory with Counter class.\"\"\"

5. ASSERTIONS
-------------
Use clear, specific assertions:

Good:
    assert obj.arg1 == 42
    assert isinstance(obj, FakeClass)
    assert "expected_key" in registry.registered_names()

For exceptions:
    with pytest.raises(
        IncorrectObjectFactoryError,
        match=r"Unable to create.*not registered"
    ):
        factory("non_existent")

6. PARAMETRIZATION
------------------
Use pytest.mark.parametrize for multiple similar tests:

Preferred format (tuple of parameters):
    @pytest.mark.parametrize(
        ("arg1", "arg2"),
        [
            (1, "a"),
            (10, "z"),
            (-5, "test"),
        ],
    )
    def test_with_parameters(arg1: int, arg2: str) -> None:
        \"\"\"Test with various parameter combinations.\"\"\"

For single parameter:
    @pytest.mark.parametrize("value", [1, 2, 3])
    def test_with_value(value: int) -> None:
        \"\"\"Test with different values.\"\"\"

7. FIXTURES
-----------
Use pytest fixtures for:
- Commonly used test objects
- Setup/teardown operations
- Shared test data

Example:
    @pytest.fixture
    def registry() -> Registry:
        \"\"\"Provide a fresh registry for each test.\"\"\"
        reg = Registry()
        reg.register_object(FakeClass)
        return reg
    
    
    def test_with_fixture(registry: Registry) -> None:
        \"\"\"Test using the registry fixture.\"\"\"
        assert len(registry) >= 1

Use autouse=True for fixtures that should run for all tests:
    @pytest.fixture(autouse=True)
    def reset_state() -> None:
        \"\"\"Reset global state before each test.\"\"\"
        GlobalState.reset()

8. HELPER CLASSES AND FUNCTIONS
--------------------------------
Define test helpers at module level (before test functions):

    class FakeClass:
        \"\"\"Fake class used for testing factory functionality.\"\"\"
        
        def __init__(self, arg1: int) -> None:
            self.arg1 = arg1
    
    
    def create_test_object() -> FakeClass:
        \"\"\"Helper function to create test objects.\"\"\"
        return FakeClass(42)

9. IMPORTS
----------
Follow PEP 8 import ordering:

1. `from __future__ import annotations` (always first)
2. Standard library imports (alphabetical, grouped)
3. Third-party imports (alphabetical, grouped)
4. Local imports (alphabetical, grouped)

Use TYPE_CHECKING for type-only imports:
    from typing import TYPE_CHECKING
    
    if TYPE_CHECKING:
        from collections.abc import Callable

10. TYPE HINTS
--------------
All test functions should have return type annotations:
    def test_something() -> None:
        \"\"\"Test something.\"\"\"

Parametrized test parameters should have type hints:
    def test_with_arg(arg1: int, arg2: str) -> None:
        \"\"\"Test with arguments.\"\"\"

11. ERROR TESTING
-----------------
When testing exceptions, always use pytest.raises with match:

    with pytest.raises(ValueError, match=r"Invalid value: .*"):
        function_that_raises()

Use raw strings (r"...") for regex patterns.

12. ASSERTIONS STYLE
--------------------
Prefer multiple simple assertions over complex ones:

Good:
    obj = factory("collections.Counter", [1, 2, 1])
    assert isinstance(obj, Counter)
    assert obj[1] == 2
    assert obj[2] == 1

Avoid:
    assert isinstance(obj, Counter) and obj[1] == 2 and obj[2] == 1

13. TEST ORGANIZATION
---------------------
Within a section, organize tests by:
1. Happy path tests (normal usage)
2. Parametrized tests
3. Edge cases
4. Error cases

14. COMMENTS
------------
Use comments sparingly in tests - prefer descriptive names and docstrings.

Use comments for:
- Explaining WHY a test exists (if not obvious)
- Clarifying complex setup
- Noting important edge cases

Don't use comments for:
- Explaining WHAT the code does (use better names)
- Restating obvious logic

15. BEST PRACTICES
------------------
- Keep tests focused - one logical assertion per test
- Test behavior, not implementation
- Make tests independent - no reliance on test execution order
- Use fixtures for common setup
- Avoid hardcoded paths - use pathlib or fixtures
- Don't test private methods directly
- Test edge cases and error conditions
- Use descriptive variable names in tests

================================================================================
PYTEST CONFIGURATION
================================================================================

The pytest configuration is defined in pyproject.toml.
This conftest.py file can be used for shared fixtures and plugins.

"""

from __future__ import annotations

# Add any shared fixtures here if needed in the future
