# Contributing to GHOST PASS

Thank you for your interest in contributing to GHOST PASS! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **🐛 Bug Reports**: Report bugs and issues
- **✨ Feature Requests**: Suggest new features
- **📝 Documentation**: Improve documentation
- **🔧 Code Contributions**: Submit code changes
- **🧪 Testing**: Help with testing and quality assurance
- **🌐 Translations**: Help translate the application
- **📢 Community**: Help with community management

### Before You Start

1. **Check Existing Issues**: Search existing issues to avoid duplicates
2. **Read Documentation**: Familiarize yourself with the project structure
3. **Set Up Development Environment**: Follow the setup instructions below

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- TOR service (for testing)

### Local Development Setup

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/your-username/ghostpass.git
cd ghostpass

# 3. Create virtual environment
python3 -m venv ghostpass_env
source ghostpass_env/bin/activate  # Linux/macOS
# or
ghostpass_env\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install in development mode
pip install -e .

# 6. Run tests
python test_ghostpass.py
```

### Project Structure

```
ghostpass/
├── core/                 # Core functionality
│   ├── tor_controller.py # TOR connection management
│   ├── encryption.py     # Multi-layer encryption
│   └── ip_rotator.py     # IP rotation system
├── ui/                   # User interface
│   └── dashboard.py      # Textual-based dashboard
├── cli/                  # Command-line interface
│   └── main.py          # Click-based CLI
├── config/              # Configuration management
│   └── settings.py      # YAML/JSON config handling
├── utils/               # Utilities
│   ├── network.py       # Network testing & diagnostics
│   ├── security.py      # Security utilities
│   └── system.py        # System utilities
└── __main__.py          # Entry point
```

## 📝 Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

### Example Code Style

```python
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)


def encrypt_data(data: bytes, key: bytes) -> Optional[bytes]:
    """
    Encrypt data using AES-256-GCM.
    
    Args:
        data: Data to encrypt
        key: Encryption key
        
    Returns:
        Encrypted data or None if encryption fails
        
    Raises:
        ValueError: If data or key is invalid
    """
    try:
        # Implementation here
        return encrypted_data
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        return None
```

### Commit Message Guidelines

Use conventional commit messages:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

Examples:
```
feat(encryption): add ChaCha20-Poly1305 support
fix(tor): resolve connection timeout issues
docs(readme): update installation instructions
test(ui): add dashboard component tests
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python test_ghostpass.py

# Run specific test modules
python -m pytest tests/test_core.py
python -m pytest tests/test_ui.py

# Run with coverage
python -m pytest --cov=ghostpass tests/
```

### Writing Tests

- Write tests for new features
- Ensure tests cover edge cases
- Use descriptive test names
- Mock external dependencies

Example test:

```python
import pytest
from ghostpass.core.encryption import EncryptionManager


class TestEncryptionManager:
    """Test encryption manager functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.encryption = EncryptionManager()
    
    def test_encrypt_decrypt_cycle(self):
        """Test that encryption and decryption work correctly."""
        test_data = b"Hello, GHOST PASS!"
        key = self.encryption.generate_key()
        
        encrypted = self.encryption.encrypt(test_data, key)
        decrypted = self.encryption.decrypt(encrypted, key)
        
        assert decrypted == test_data
    
    def test_invalid_key_raises_error(self):
        """Test that invalid keys raise appropriate errors."""
        with pytest.raises(ValueError):
            self.encryption.encrypt(b"test", b"invalid_key")
```

## 🔄 Pull Request Process

### Before Submitting

1. **Update Documentation**: Update relevant documentation
2. **Add Tests**: Include tests for new functionality
3. **Run Tests**: Ensure all tests pass
4. **Check Style**: Verify code follows style guidelines
5. **Update CHANGELOG**: Add entry to CHANGELOG.md if applicable

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Test addition/update

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
- [ ] CHANGELOG updated (if applicable)

## Screenshots (if applicable)
Add screenshots for UI changes
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and style checks
2. **Code Review**: Maintainers review the code
3. **Testing**: Changes are tested on multiple platforms
4. **Approval**: Changes are approved and merged

## 🐛 Bug Reports

### Before Reporting

1. Check existing issues
2. Try to reproduce the issue
3. Check if it's a configuration issue

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, Ubuntu 20.04, macOS 12]
- Python Version: [e.g., 3.9.7]
- GHOST PASS Version: [e.g., 0.1.0]
- TOR Version: [e.g., 0.4.7.13]

## Additional Information
- Error messages
- Screenshots
- Configuration files
```

## ✨ Feature Requests

### Feature Request Template

```markdown
## Feature Description
Clear description of the requested feature

## Use Case
Why this feature is needed

## Proposed Implementation
How the feature could be implemented

## Alternatives Considered
Other approaches that were considered

## Additional Information
Any other relevant information
```

## 📚 Documentation

### Documentation Guidelines

- Write clear, concise documentation
- Include examples where appropriate
- Keep documentation up to date
- Use consistent formatting

### Documentation Structure

```
docs/
├── installation.md      # Installation guide
├── configuration.md     # Configuration guide
├── cli.md              # CLI reference
├── api.md              # API documentation
├── security.md         # Security features
└── troubleshooting.md  # Troubleshooting guide
```

## 🔐 Security

### Security Guidelines

- Never commit sensitive information
- Report security issues privately
- Follow secure coding practices
- Validate all inputs

### Reporting Security Issues

For security issues, please email security@ghostpass.org instead of creating a public issue.

## 🌐 Internationalization

### Translation Guidelines

- Use English as the base language
- Provide context for translators
- Test translations thoroughly
- Maintain consistent terminology

## 📊 Performance

### Performance Guidelines

- Profile code for bottlenecks
- Optimize critical paths
- Use appropriate data structures
- Consider memory usage

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Help others learn
- Provide constructive feedback
- Follow project guidelines

### Getting Help

- Check documentation first
- Search existing issues
- Ask in discussions
- Join community channels

## 💙 Support the Project

If you find GHOST PASS useful, consider supporting its development:

- **Ko-fi**: [https://coff.ee/draknight](https://coff.ee/draknight)
- **Buy Me a Coffee**: [https://buymeacoffee.com/draknight](https://buymeacoffee.com/draknight)

Your support helps us maintain and improve GHOST PASS for everyone!

## 📄 License

By contributing to GHOST PASS, you agree that your contributions will be licensed under the MIT License.

## 🙏 Acknowledgments

Thank you for contributing to GHOST PASS! Your contributions help make the internet a more private and secure place.

---

**Happy Contributing! 🚀** 