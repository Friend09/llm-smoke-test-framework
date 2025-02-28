# Contributing to LLM-Enhanced Smoke Test Generator

Thank you for considering contributing to this project! Here's how you can help.

## Code of Conduct

This project follows a Code of Conduct that all contributors are expected to adhere to. Please read the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) file to understand what behaviors are expected.

## How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in the Issues section
- Use the bug report template when creating a new issue
- Provide as much detail as possible, including steps to reproduce, expected behavior, and actual behavior
- Include screenshots or logs if possible

### Suggesting Enhancements

- Check if the enhancement has already been suggested in the Issues section
- Use the feature request template when creating a new issue
- Clearly describe the problem and solution
- Explain why this enhancement would be useful to most users

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Add or update tests as necessary
5. Ensure all tests pass
6. Update documentation if needed
7. Submit a pull request

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```
4. Setup your `.env` file based on `.env.example`

## Testing

Before submitting a pull request, ensure all tests pass:

```bash
pytest
```

For code style checks:

```bash
flake8
```

## Coding Conventions

- Follow PEP 8 style guide for Python code
- Write descriptive commit messages
- Include docstrings for all functions, classes, and modules
- Add type hints where applicable
- Keep functions small and focused on a single responsibility
- Write unit tests for new functionality

## Documentation

- Update the README.md with details of changes to the interface
- Update the documentation when changing core functionality
- Comment your code where necessary to explain complex logic

## Version Control Practices

- Create feature branches from `develop` branch
- Use descriptive branch names (e.g., `feature/improved-url-extraction`, `fix/auth-handler-crash`)
- Make focused commits that address a single concern
- Rebase your branch before submitting a pull request

## Questions?

If you have any questions about contributing, please open an issue with your question.

Thank you for contributing to this project!
