# Agent Instructions - Calculus-Core

This document defines the technical standards and workflows that must be followed by any AI agent working on the `calculus-core` codebase.

## Python Development Standards

All Python code must adhere to current community best practices:

*   **PEP 8 Compatibility**: Follow standard Python style guidelines (naming conventions, line length, etc.). Use Ruff for formatting and linting as configured in `pyproject.toml`.
*   **Architecture**: Follow the project's modular architecture (Cosmic Python principles). Keep domain logic isolated from infrastructure and entrypoints.
*   **Clean Code**:
    *   Functions should be small and do one thing.
    *   Variable and function names should be descriptive and in Portuguese (as currently used in domain models) or English (for infrastructure/system parts), maintaining the established pattern.
    *   Avoid complex nested logic.
*   **Type Hinting**: Use Python type hints (Type Annotations) for all function arguments and return values. Ensure compatibility with Python 3.13+.
*   **Documentation**: Document public APIs and complex domain logic using Docstrings.

## Commit Message Guidelines

All commits must follow the **Conventional Commits** specification (v1.0.0):

### Format
`<type>[optional scope]: <description>`

### Types
*   **feat**: A new feature for the user.
*   **fix**: A bug fix for the user.
*   **docs**: Changes to documentation only.
*   **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
*   **refactor**: A code change that neither fixes a bug nor adds a feature.
*   **perf**: A code change that improves performance.
*   **test**: Adding missing tests or correcting existing tests.
*   **chore**: Updating grunt tasks etc; no production code change.
*   **build**: Changes that affect the build system or external dependencies.
*   **ci**: Changes to our CI configuration files and scripts.

### Examples
*   `feat(soil): add SPT CSV import functionality`
*   `fix(frontend): adjust depth selector value clamping`
*   `refactor(domain): improve Aoki-Velloso method modularity`
*   `chore(ci): update coverage badge path`
