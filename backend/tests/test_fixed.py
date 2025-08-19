import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Test data
test_user = {
    "email": "test@example.com",
    "password": "testpassword",
    "full_name": "Test User"
}

test_customer = {
    "name": "Test Customer",
    "email": "customer@example.com",
    "phone": "1234567890",
    "address": "123 Test Street"
}

@pytest.fixture
def client():
    # Create a test database engine
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Override the database dependency
    def override_db():
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        try:
            db_session = TestingSessionLocal()
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[db] = override_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

def test_create_user(client):
    response = client.post("/api/v1/register", json=test_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]
    assert "id" in data
    assert "is_active" in data

def test_login_user(client):
    # First create a user
    response = client.post("/api/v1/register", json=test_user)
    assert response.status_code == 201
    
    # Then login
    login_response = client.post(
        "/api/v1/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_create_customer(client):
    # First create a user to authenticate
    user_data = {
        "email": "customer_test@example.com",
        "password": "testpassword",
        "full_name": "Customer Test User"
    }
    response = client.post("/api/v1/register", json=user_data)
    assert response.status_code == 201
    
    # Login to get token
    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    auth_headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    
    # Create customer
    response = client.post("/api/v1/customers/", json=test_customer, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_customer["name"]
    assert data["email"] == test_customer["email"]
    assert "id" in data

def test_get_customers(client):
    # First create a user to authenticate
    user_data = {
        "email": "customers_test@example.com",
        "password": "testpassword",
        "full_name": "Customers Test User"
    }
    response = client.post("/api/v1/register", json=user_data)
    assert response.status_code == 201
    
    # Login to get token
    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    auth_headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    
    # Get all customers
    response = client.get("/api/v1/customers/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "CRM MVP is running"
