# Development Scripts

This directory contains development and validation scripts for the `objectory` package.

## Overview

The scripts in this directory are used for:
- Testing code examples in markdown documentation
- Validating package builds and metadata
- Checking type annotations
- Verifying dependency trees
- Generating configuration for dependency testing

## Directory Structure

```
dev/
├── check_markdown.sh           # Validates code examples in markdown files
├── generate_versions.py        # Generates package version configurations
├── config/                     # Configuration files
│   └── package_versions.json   # Package version configurations for testing
└── package/                    # Package validation scripts
    ├── check_metadata.sh       # Validates package metadata
    ├── check_type.sh          # Validates type annotations
    ├── check_dependency_tree.sh # Validates dependency tree
    └── custom_checks.sh        # Custom package validation checks
```

## Scripts

### `check_markdown.sh`

Validates code examples in markdown files using Python's doctest module.

**Usage:**
```bash
./dev/check_markdown.sh
```

**Purpose:** Ensures documentation examples are accurate and up-to-date.

**Requirements:**
- Python with doctest module
- Markdown files with Python code blocks

---

### `generate_versions.py`

Generates package version configurations for dependency compatibility testing.

**Usage:**
```bash
python dev/generate_versions.py
```

**Purpose:** Creates configuration file for testing different dependency versions.

**Output:** `dev/config/package_versions.json`

---

### Package Validation Scripts (`package/` directory)

These scripts validate the built package before publishing:

#### `check_metadata.sh`

Verifies package metadata is correct.

**Usage:**
```bash
./dev/package/check_metadata.sh
```

**Checks:**
- Package name is correct
- Required dependencies are listed

---

#### `check_type.sh`

Validates that the package is properly typed.

**Usage:**
```bash
./dev/package/check_type.sh
```

**Checks:**
- Package includes py.typed marker
- Pyright recognizes the package as typed
- Type annotations are valid

---

#### `check_dependency_tree.sh`

Validates the dependency tree structure.

**Usage:**
```bash
./dev/package/check_dependency_tree.sh
```

**Checks:**
- No unexpected dependencies
- Dependency tree matches expected patterns

**Note:** Update the `PATTERNS` array in the script if dependencies change.

---

#### `custom_checks.sh`

Runs project-specific validation checks.

**Usage:**
```bash
./dev/package/custom_checks.sh
```

**Checks:** Executes tests defined in `tests/package_checks.py`

---

## Usage in CI/CD

These scripts are used in GitHub Actions workflows:

- **`build.yaml`**: Uses package validation scripts to verify builds
- **`generate-package-versions.yaml`**: Uses `generate_versions.py` to update configs
- **CI workflow**: Uses `check_markdown.sh` for documentation validation

## Requirements

All scripts require:
- Bash 4.0 or later
- Python 3.10 or later
- `uv` package manager (for package validation scripts)
- Package installed in the current environment (for package validation)

## Error Handling

All scripts use `set -euo pipefail` for strict error handling:
- `set -e`: Exit on any command failure
- `set -u`: Exit on undefined variable usage
- `set -o pipefail`: Propagate errors through pipes

## Development

When adding new validation scripts:

1. Use the same error handling settings (`set -euo pipefail`)
2. Add comprehensive header documentation (see existing scripts)
3. Include clear exit codes and requirements
4. Update this README with script information
5. Add the script to relevant CI workflows

## Troubleshooting

### Script fails with "command not found"

Ensure required tools are installed:
```bash
# Install uv
pip install uv

# Install pyright (for type checking)
pip install pyright
```

### Package validation scripts fail

Ensure the package is installed:
```bash
# Install in development mode
uv pip install -e .
```

### check_markdown.sh reports doctest failures

The markdown files contain code examples that are executed. Fix the code examples or update the documentation to match the current API.
