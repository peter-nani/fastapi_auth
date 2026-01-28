from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Internal relative import
from .config import auth_settings

# Create the engine using the URL from your config
engine = create_engine(
    auth_settings.DATABASE_URL, 
    # connect_args is only needed for SQLite
    connect_args={"check_same_thread": False} if "sqlite" in auth_settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()