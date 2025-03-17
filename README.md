# AI Demo Project

A full-stack AI demonstration system based on Flask + React.

## Project Structure

```
ai-demo/
├── backend/                # Backend directory
│   ├── api/               # API interfaces
│   │   └── v1/           # API version
│   │       └── endpoints/ # API endpoints
│   ├── config/           # Configuration files
│   ├── core/             # Core functionality
│   ├── models/           # Database models
│   ├── schemas/          # Data validation schemas
│   ├── services/         # Business service layer
│   ├── utils/            # Utility functions
│   └── tests/            # Backend tests
├── frontend/             # Frontend directory
│   ├── public/          # Static resources
│   ├── src/             # Source code
│   │   ├── api/         # API interfaces
│   │   ├── assets/      # Resource files
│   │   ├── components/  # Components
│   │   ├── hooks/       # Custom Hooks
│   │   ├── layouts/     # Layout components
│   │   ├── pages/       # Pages
│   │   ├── services/    # Services
│   │   ├── store/       # State management
│   │   ├── styles/      # Style files
│   │   └── utils/       # Utility functions
│   └── tests/           # Frontend tests
├── scripts/             # Script files
└── docs/               # Project documentation

## Tech Stack

### Backend
- Python 3.9+
- Flask
- SQLAlchemy
- PostgreSQL
- JWT Authentication

### Frontend
- React 18
- TypeScript
- Ant Design
- React Router
- Axios

## Quick Start

### Backend Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start development server
./scripts/run.sh
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## Features
- 🔐 JWT Authentication
- 🎨 Beautiful UI Interface
- 📱 Responsive Design
- 🔄 State Management
- 📝 Complete CRUD Operations
- 🌐 RESTful API

## Contributing
Issues and Pull Requests are welcome

## License
MIT License
