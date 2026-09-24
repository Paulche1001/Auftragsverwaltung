from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
import models

TEST_DATABASE_URL = "sqlite:///./test_database.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()