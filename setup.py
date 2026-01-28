from setuptools import setup, find_packages

setup(
    name="fastapi-jwt-auth",
    version="1.0.0",
    packages=find_packages(),
    # Adding pydantic-settings which is required for our config.py logic
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "passlib[bcrypt]",
        "python-jose[cryptography]",
        "python-multipart",
        "pydantic-settings", 
        "pydantic[email]"
    ],
    python_requires=">=3.8",
    description="Pluggable JWT Authentication for FastAPI applications",
    author="Your Name",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "Topic :: Security",
    ],
)