# Contributing to data-export-approver

Thank you for your interest in this project!

## Project Status

This is a **personal open-source project**, currently maintained solely by
[PerryLink](https://github.com/PerryLink). Active development happens in focused
bursts rather than on a regular schedule. External contributions are welcome but
may take time to review.

---

## Reporting Issues

If you encounter a bug or have a feature request, please
[open an issue](https://github.com/PerryLink/data-export-approver/issues) and include:

- A clear, descriptive title
- Steps to reproduce the problem
- Expected behavior vs. actual behavior
- Your environment (OS, Python version, Pandas version, package version)
- Minimal code snippet that demonstrates the issue

---

## Development Setup

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) (recommended) or pip

### Clone and Install

```bash
git clone https://github.com/PerryLink/data-export-approver.git
cd data-export-approver

# Install all dependencies (including dev extras)
poetry install
```

### Run Tests

```bash
poetry run pytest tests/ -v --cov=data_export_approver
```

### Verify the Patch Works

```bash
poetry run python -m data_export_approver test
```

---

## Code Standards

This project follows [PEP 8](https://pep8.org/). Please ensure your changes comply:

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters
- Use descriptive variable and function names
- Add docstrings to public functions and classes
- Keep functions small and focused on a single responsibility

You can check compliance locally with:

```bash
poetry run flake8 src/ tests/
```

---

## Pull Request Process

1. Fork the repository and create a feature branch from `main`:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Write or update tests to cover your changes.

3. Ensure all tests pass before submitting:

   ```bash
   poetry run pytest tests/ -v
   ```

4. Keep commits focused — one logical change per commit. Write clear commit
   messages in the imperative mood (e.g., `Add support for Polars exports`).

5. Open a Pull Request against the `main` branch. In the PR description:
   - Explain *what* you changed and *why*
   - Reference any related issues (e.g., `Closes #42`)
   - List any manual testing you performed

6. Be patient — this is a solo-maintained project and reviews may not be
   immediate.

---

## Questions

Feel free to reach out via email: **novelnexusai@outlook.com**
