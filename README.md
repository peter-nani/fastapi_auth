# 🔐 FastAPI JWT Authentication Module

A production-ready, pluggable JWT authentication system for FastAPI applications. Designed with clean architecture and easy integration in mind.

## ✨ Features

- **✅ Pluggable Design** - Use as a standalone module or integrate into existing projects
- **✅ JWT Authentication** - Secure token-based authentication with expiration
- **✅ Multiple Login Methods** - Username/Password & Email/Password login
- **✅ SQLAlchemy ORM** - Supports SQLite, PostgreSQL, MySQL, and more
- **✅ Pydantic V2** - Modern data validation and serialization
- **✅ Route Protection** - Easy dependency injection for protected endpoints
- **✅ Environment Configuration** - Configurable via `.env` files
- **✅ Health Checks** - Built-in monitoring endpoints
- **✅ Comprehensive Logging** - Detailed debug information

## 📦 Installation

### Option 1: Direct Integration
Copy the `auth/` directory to your project:

```bash
# Copy the auth module to your project
cp -r /path/to/auth-module/auth/ ./your-project/

Option 2: Package Installation
Create a setup.py for package installation:
```

# setup.py in auth directory
from setuptools import setup, find_packages

```
setup(
    name="fastapi-auth-module",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "sqlalchemy>=2.0.0",
        "passlib[bcrypt]>=1.7.4",
        "python-jose[cryptography]>=3.3.0",
        "python-multipart>=0.0.6",
    ],
)
```

# Install dependencies:
`pip install fastapi sqlalchemy passlib[bcrypt] python-jose[cryptography] python-multipart`

# Configuration

## Environment Variables
## Create a .env file in your project root:

# JWT Settings
SECRET_KEY="your-super-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL="sqlite:///./auth.db"  # SQLite for development
# DATABASE_URL="postgresql://user:password@localhost/dbname"  # PostgreSQL

## Quick Configuration

# Import and use in your main application:

```
# main.py
from fastapi import FastAPI
from auth.exports import setup_auth

app = FastAPI(title="My Application")

# Setup authentication with custom database
setup_auth(
    app,
    database_url="sqlite:///./myapp.db"
)

# Your other routes
@app.get("/")
async def root():
    return {"message": "Welcome to My Application"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

# 2. Using in Another Application

# app2.py - Another FastAPI app using the same auth module
```
from fastapi import FastAPI
from auth.exports import setup_auth

app2 = FastAPI(title="Second Application")

# Reuse the same auth module
setup_auth(app2, database_url="sqlite:///./app2.db")

@app2.get("/app2/")
async def app2_home():
    return {"message": "This is app2 with the same auth system"}
```

# 🔒 Protecting Routes

# Method 1: Required Authentication

```
from typing import Annotated
from fastapi import Depends
from auth.dependencies import get_current_active_user
import models

@app.get("/protected-endpoint")
async def protected_route(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    return {
        "message": f"Hello {current_user.username}",
        "user_id": current_user.id
    }
```

# 🏗️ Project Structure

```
fastapi_auth/
├── auth/                      # Authentication Module
│   ├── __init__.py           # Package exports
│   ├── auth_main.py          # Main router definition
│   ├── config.py             # Configuration settings
│   ├── db.py                 # Database setup
│   ├── dependencies.py       # FastAPI dependencies
│   ├── exports.py            # Public API exports
│   ├── models.py             # SQLAlchemy models
│   ├── password.py           # Password & JWT utilities
│   ├── protected_routes.py   # Protected endpoints
│   └── schema.py             # Pydantic schemas
├── main.py                   # Main application
├── .env                      # Environment variables
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Happy Coding! 🚀