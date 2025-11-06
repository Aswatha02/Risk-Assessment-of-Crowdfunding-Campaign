# Contributing to CrowdRisk

Thank you for your interest in contributing to CrowdRisk! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating a new issue
3. **Include details**:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Error messages and logs

### Suggesting Features

1. **Check existing feature requests** first
2. **Describe the feature** clearly
3. **Explain the use case** and benefits
4. **Consider implementation** complexity

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Make your changes**
4. **Write/update tests**
5. **Update documentation**
6. **Commit with clear messages**
7. **Push to your fork**
8. **Open a Pull Request**

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Risk-Assessment-of-Crowdfunding-Campaign.git
cd Risk-Assessment-of-Crowdfunding-Campaign

# Run setup script
python setup.py

# Or manual setup:
pip install -r requirements.txt
cd frontend && npm install
```

### Running Tests

```bash
# Backend tests
cd tests
python test_api.py
python test_models.py

# Frontend tests
cd frontend
npm test
```

### Code Style

**Python:**
- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for functions/classes
- Maximum line length: 100 characters

**JavaScript/React:**
- Use ES6+ syntax
- Follow React best practices
- Use functional components with hooks
- Proper component naming (PascalCase)

**General:**
- Write clear, self-documenting code
- Add comments for complex logic
- Keep functions small and focused

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(api): add batch prediction endpoint

Add new endpoint to predict multiple campaigns at once.
Improves performance for bulk operations.

Closes #123
```

```
fix(frontend): correct probability display formatting

Fixed issue where probabilities over 100% were displayed.
Now properly formats as percentage with 2 decimal places.
```

## 🧪 Testing Guidelines

### Writing Tests

- **Test coverage**: Aim for >80% coverage
- **Test naming**: Use descriptive names
- **Test isolation**: Each test should be independent
- **Mock external dependencies**: Don't rely on external services

### Test Structure

```python
def test_feature_name():
    # Arrange
    input_data = {...}
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    assert result == expected_value
```

## 📚 Documentation

### Code Documentation

- Add docstrings to all public functions/classes
- Include parameter types and return types
- Provide usage examples for complex functions

### README Updates

- Update README.md for new features
- Add examples for new functionality
- Update installation instructions if needed

## 🔍 Code Review Process

1. **Automated checks** must pass (tests, linting)
2. **At least one approval** from maintainers
3. **Address feedback** promptly
4. **Keep PR focused** on single feature/fix
5. **Rebase if needed** to keep history clean

## 🎯 Priority Areas

We especially welcome contributions in:

- **Model improvements**: Better algorithms, feature engineering
- **UI/UX enhancements**: Better visualizations, user experience
- **Performance optimization**: Faster predictions, caching
- **Documentation**: Tutorials, examples, API docs
- **Testing**: More comprehensive test coverage
- **Accessibility**: Making the app more accessible

## ❓ Questions?

- Open a discussion in GitHub Discussions
- Tag maintainers in issues
- Check existing documentation first

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CrowdRisk! 🎉
