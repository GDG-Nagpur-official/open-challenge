# Contributing to API Management System

Thank you for your interest in contributing to the API Management System! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/api-management-system.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit your changes: `git commit -m "Add your commit message"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python app.py
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your configuration
npm start
```

## Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript/React**: Use ES6+ syntax, functional components with hooks
- Write clear, descriptive commit messages
- Add comments for complex logic
- Keep functions small and focused

## Testing

Before submitting a PR:
- Test all functionality manually
- Ensure no console errors
- Test with different browsers (Chrome, Firefox, Safari)
- Verify mobile responsiveness

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include screenshots for UI changes
- Update documentation if needed
- Ensure your code passes all checks

## Code of Conduct

Be respectful and inclusive. We're all here to learn and improve together.

## Questions?

Feel free to open an issue for any questions or concerns.
