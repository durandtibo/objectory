# Security Policy

## Supported Versions

We provide security updates for the following versions of objectory:

| Version | Supported          |
|---------|--------------------|
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :x:                |
| < 0.1.0 | :x:                |

## Reporting a Vulnerability

The objectory team takes security vulnerabilities seriously. We appreciate your efforts to
responsibly disclose your findings.

### How to Report

If you discover a security vulnerability, please follow these steps:

1. **Do NOT** open a public GitHub issue for the vulnerability
2. Email the maintainer directly at: durand.tibo+gh@gmail.com
3. Include the following information in your report:
    - Description of the vulnerability
    - Steps to reproduce the issue
    - Potential impact
    - Suggested fix (if available)

### What to Expect

After you submit a vulnerability report, you can expect:

- **Initial Response**: Within 48 hours, you will receive an acknowledgment of your report
- **Status Updates**: We will keep you informed about the progress of addressing the vulnerability
- **Resolution Timeline**: We aim to release a fix within 30 days of the initial report, depending
  on the complexity
- **Credit**: If you desire, we will publicly acknowledge your contribution to the security of
  objectory

### Security Best Practices

When using objectory, please follow these security best practices:

1. **Dynamic Imports**: Be cautious when using the factory functions with user-provided input. The
   factory can instantiate any Python object by name, which could be a security risk if not properly
   validated.

2. **Input Validation**: Always validate and sanitize user input before passing it to factory
   functions, especially the `_target_` parameter.

3. **Restricted Imports**: Consider implementing allowlists of permitted classes/functions when
   using objectory in security-sensitive contexts.

4. **Dependency Updates**: Keep objectory and its dependencies up to date to benefit from the latest
   security patches.

### Example of Safe Usage

```python
from objectory import factory

# Define an allowlist of safe classes
ALLOWED_CLASSES = {
    "collections.Counter",
    "collections.defaultdict",
    # Add your safe classes here
}


def safe_factory(target: str, *args, **kwargs):
    if target not in ALLOWED_CLASSES:
        raise ValueError(f"Class {target} is not allowed")
    return factory(target, *args, **kwargs)


# Use the safe wrapper instead of factory directly
obj = safe_factory("collections.Counter", [1, 2, 3])
```

## Scope

This security policy applies to:

- The objectory library code (src/objectory)
- Documentation and examples
- GitHub Actions workflows and automation

This policy does not apply to:

- Third-party dependencies (please report issues to their respective maintainers)
- Forks or unofficial distributions of objectory

## Security Updates

Security updates will be released as patch versions and announced via:

- GitHub Security Advisories
- Release notes

Thank you for helping keep objectory and its users safe!
