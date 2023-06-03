import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi.testclient import TestClient
from app.models import Base

from app.main import app
from app.db.session import get_db


@pytest.fixture(scope="module")
def test_db():
    try:
        engine = create_engine("sqlite:///:memory:")
        SessionLocal = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        session = SessionLocal()
        yield session
    finally:
        session.close()


@pytest.fixture(scope="session")
def test_client():
    app.dependency_overrides[get_db] = test_db
    client = TestClient(app=app)
    yield client
