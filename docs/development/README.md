# Development Guide

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Docker and Docker Compose
- PostgreSQL 15
- Git

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-demo.git
cd ai-demo
```

2. Set up environment:
```bash
make setup
```

3. Start services:
```bash
make start
```

## Development Workflow

### Branch Naming Convention

- Feature: `feature/description`
- Bugfix: `bugfix/description`
- Hotfix: `hotfix/description`
- Release: `release/version`

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Tests
- chore: Maintenance

### Code Style Guidelines

#### Python
- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters
- Use docstrings for functions and classes

#### TypeScript/React
- Follow Airbnb Style Guide
- Use functional components
- Use TypeScript interfaces
- Use ESLint and Prettier

### Testing

#### Backend Tests
```bash
cd backend
pytest
```

#### Frontend Tests
```bash
cd frontend
npm test
```

### Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Troubleshooting

### Common Issues

1. Database Connection
```bash
# Check PostgreSQL status
docker-compose ps
# View logs
docker-compose logs db
```

2. Backend Issues
```bash
# Check logs
docker-compose logs backend
```

3. Frontend Issues
```bash
# Check logs
docker-compose logs frontend
```

## IDE Setup

### VSCode Extensions
- Python
- ESLint
- Prettier
- Docker
- EditorConfig
- GitLens

### PyCharm Setup
- Enable Python type hints
- Set up black formatter
- Configure pytest

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Ant Design Documentation](https://ant.design/) 