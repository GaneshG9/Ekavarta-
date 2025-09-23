# Contributing to Ekavarta

Thank you for considering contributing to Ekavarta! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch from `main`
4. Make your changes
5. Test your changes thoroughly
6. Submit a pull request

## Development Setup

1. **Prerequisites**
   - Node.js (v16 or higher)
   - MongoDB (v5 or higher)
   - npm or yarn

2. **Installation**
   ```bash
   git clone https://github.com/your-username/Ekavarta-.git
   cd Ekavarta-
   npm install
   npm run install-client
   ```

3. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start Development**
   ```bash
   npm run dev
   ```

## Code Style

- Use ES6+ features
- Follow React hooks patterns
- Use consistent naming conventions
- Add comments for complex logic
- Ensure responsive design

## Testing

- Write unit tests for new features
- Test API endpoints with Postman/curl
- Verify UI components across different screen sizes
- Test authentication flows

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update README.md if applicable
5. Describe your changes in the PR

## Reporting Issues

When reporting issues, please include:
- Operating system and version
- Node.js version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

## Feature Requests

For feature requests, please:
- Check existing issues first
- Describe the use case
- Explain why it would be valuable
- Consider backward compatibility

## License

By contributing, you agree that your contributions will be licensed under the MIT License.