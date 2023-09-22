from datetime import datetime

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.middleware.authenticate import authenticate
from main import app
from app.db.database import Base, get_db
from app.models import user_models, organization_models
from decouple import config

# Setup test database
password = config("DB_PASSWORD")
db_name = config("DB_NAME")
DATABASE_URL = f"postgresql://postgres:{password}@localhost/{db_name}"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False)

mock_user = user_models.User(
    id=1,
    org_id=1,
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    password_hash="mockhashedpassword123456",
    phone="123-456-7890",
    is_admin=True,
    lunch_credit_balance=100,
    bank_number="1234567890",
    bank_code="TEST01",
    bank_name="Test Bank",
    bank_region="Test Region",
    currency="US Dollar",
    currency_code="USD",
    created_at=datetime.now(),
    updated_at=datetime.now(),
    is_deleted=False
)


# Mock dependencies
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user():
    # return a mock user object
    return mock_user


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)



def test_withdraw_request(session, client):
    app.dependency_overrides[authenticate] = override_get_current_user

    # Mock data
    mock_org = organization_models.Organization(
        name="Test Organization",
        lunch_price=10.50,
        currency_code="USD"
    )
    session.add(mock_org)
    session.commit()

    mock_user = user_models.User(
        org_id=mock_org.id,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password_hash="mockhashedpassword123456",
        phone="123-456-7890",
        is_admin=True,
        lunch_credit_balance=100, 
        bank_number="1234567890",
        bank_code="TEST01",
        bank_name="Test Bank",
        bank_region="Test Region",
        currency="US Dollar",
        currency_code="USD"
    )

    session.add(mock_user)
    session.commit()

    withdraw_data = {
        "bank_number": "9037209772",
        "bank_code": "234",
        "bank_name": "Opay",
        "amount": 10
    }
    response = client.post("api/v1/withdrawal/request", json=withdraw_data)
    print(response)
    print(response.json())
    assert response.json()["amount"] == 105.0

    session.close()
