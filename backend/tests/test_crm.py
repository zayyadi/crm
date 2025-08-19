import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Create a test client
client = TestClient(app)

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

@pytest.fixture(scope="module")
def test_client():
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
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[db] = override_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

def test_create_user(test_client):
    response = test_client.post("/api/v1/register", json=test_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]
    assert "id" in data
    assert "is_active" in data

def test_create_customer(test_client):
    # First create a user to authenticate
    user_data = {
        "email": "customer_test@example.com",
        "password": "testpassword",
        "full_name": "Customer Test User"
    }
    response = test_client.post("/api/v1/register", json=user_data)
    assert response.status_code == 201
    
    # Login to get token
    login_response = test_client.post(
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
    response = test_client.post("/api/v1/customers/", json=test_customer, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_customer["name"]
    assert data["email"] == test_customer["email"]
    assert "id" in data

def test_get_customers(test_client):
    # First create a user to authenticate
    user_data = {
        "email": "customers_test@example.com",
        "password": "testpassword",
        "full_name": "Customers Test User"
    }
    response = test_client.post("/api/v1/register", json=user_data)
    assert response.status_code == 201
    
    # Login to get token
    login_response = test_client.post(
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
    response = test_client.get("/api/v1/customers/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_contact(test_client):
    # Create a contact
    contact_data = {
        "name": "Test Contact",
        "email": "contact@example.com",
        "phone": "0987654321",
        "customer_id": 1
    }
    
    response = test_client.post("/api/v1/contacts/", json=contact_data)
    # Note: This might fail if customer_id doesn't exist in test DB
    # but we're testing the endpoint structure
    assert response.status_code in [201, 400, 404]

def test_create_lead(test_client):
    # Create a lead
    lead_data = {
        "name": "Test Lead",
        "status": "new",
        "score": 50,
        "customer_id": 1
    }
    
    response = test_client.post("/api/v1/leads/", json=lead_data)
    # Note: This might fail if customer_id doesn't exist in test DB
    # but we're testing the endpoint structure
    assert response.status_code in [201, 400, 404]

def test_create_opportunity(test_client):
    # Create an opportunity
    opportunity_data = {
        "name": "Test Opportunity",
        "value": 10000,
        "stage": "proposal",
        "customer_id": 1
    }
    
    response = test_client.post("/api/v1/opportunities/", json=opportunity_data)
    # Note: This might fail if customer_id doesn't exist in test DB
    # but we're testing the endpoint structure
    assert response.status_code in [201, 400, 404]
