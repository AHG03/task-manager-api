import pytest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.models import Base
from app.dependencies import get_db


TEST_DATABASE_PATH = Path(__file__).parent.parent / "test_tasks.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DATABASE_PATH}"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def override_get_db():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def remove_test_db(test_db: Path):
    test_engine.dispose()

    if test_db.exists():
        test_db.unlink()


@pytest.fixture
def client():
    remove_test_db(TEST_DATABASE_PATH)

    Base.metadata.create_all(bind=test_engine)

    yield TestClient(app)

    remove_test_db(TEST_DATABASE_PATH)
