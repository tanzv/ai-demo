from setuptools import setup, find_packages

setup(
    name="ai-demo",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==3.0.2",
        "Flask-SQLAlchemy==3.1.1",
        "Flask-Migrate==4.0.5",
        "Flask-Login==0.6.3",
        "Flask-WTF==1.2.1",
        "Flask-CORS==4.0.0",
        "python-dotenv==1.0.1",
        "SQLAlchemy==2.0.27",
        "Werkzeug==3.0.1",
        "pytest==8.0.2",
        "requests==2.31.0",
        "psycopg2-binary==2.9.9",
        "pydantic==2.5.2",
        "pydantic-settings==2.1.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
        "email-validator==2.1.0.post1",
        "pyyaml==6.0.1",
        "click==8.1.8"
    ],
    entry_points={
        "console_scripts": [
            "ai-demo=backend.cli:cli"
        ]
    }
) 