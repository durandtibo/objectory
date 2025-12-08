"""Integration tests for examples to ensure they work correctly."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _run_example(example_name: str) -> subprocess.CompletedProcess:
    """Run an example script with proper PYTHONPATH."""
    example_path = Path(__file__).parent.parent.parent / "examples" / example_name
    repo_root = Path(__file__).parent.parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    return subprocess.run(
        [sys.executable, str(example_path)],
        capture_output=True,
        text=True,
        timeout=10,
        env=env,
    )


def test_basic_factory_example() -> None:
    """Test that basic_factory.py example runs successfully."""
    result = _run_example("basic_factory.py")
    assert result.returncode == 0, f"Example failed with error: {result.stderr}"
    assert "Counter({1: 3, 2: 2, 3: 1})" in result.stdout
    assert "All examples completed successfully!" in result.stdout


def test_abstract_factory_example() -> None:
    """Test that abstract_factory_example.py runs successfully."""
    result = _run_example("abstract_factory_example.py")
    assert result.returncode == 0, f"Example failed with error: {result.stderr}"
    assert "AbstractFactory Usage Examples" in result.stdout
    assert "All examples completed successfully!" in result.stdout


def test_registry_example() -> None:
    """Test that registry_example.py runs successfully."""
    result = _run_example("registry_example.py")
    assert result.returncode == 0, f"Example failed with error: {result.stderr}"
    assert "Registry Usage Examples" in result.stdout
    assert "All examples completed successfully!" in result.stdout


def test_plugin_system_example() -> None:
    """Test that plugin_system.py runs successfully."""
    result = _run_example("plugin_system.py")
    assert result.returncode == 0, f"Example failed with error: {result.stderr}"
    assert "Plugin System Example" in result.stdout
    assert "All examples completed successfully!" in result.stdout


def test_configuration_loader_example() -> None:
    """Test that configuration_loader.py runs successfully."""
    result = _run_example("configuration_loader.py")
    assert result.returncode == 0, f"Example failed with error: {result.stderr}"
    assert "Configuration Loader Example" in result.stdout
    assert "All examples completed successfully!" in result.stdout
