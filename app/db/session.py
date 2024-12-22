from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Налаштування бази даних
def get_database_url():
    from app.core.config import settings  # Імпортуйте settings тут, щоб уникнути циклічного імпорту
    return f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@db/{settings.POSTGRES_DB}"

SQLALCHEMY_DATABASE_URL = get_database_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Створення SessionLocal та Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Функція для отримання сесії
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()