import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timezone

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

test_contact = {
    "name": "Test Contact",
    "email": "contact@example.com",
    "phone": "0987654321"
}

test_lead = {
    "name": "Test Lead",
    "status": "new",
    "score": 50
}

test_opportunity = {
    "name": "Test Opportunity",
    "value": 10000,
    "stage": "proposal"
}

test_invoice = {
    "amount": 10000,  # $100.00 in cents
    "currency": "USD",
    "status": "draft",
    "due_date": "2023-12-31T23:59:59",
    "description": "Test invoice"
}

test_payment = {
    "amount": 10000,  # $100.00 in cents
    "currency": "USD",
    "payment_method": "credit_card",
    "status": "pending"
}

test_subscription = {
    "plan_name": "Basic Plan",
    "amount": 2999,  # $29.99 in cents
    "currency": "USD",
    "status": "active",
    "billing_cycle": "monthly"
}

test_chat_message = {
    "message": "Hello, how can I help you?",
    "sender": "user"
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

@pytest.fixture(scope="module")
def auth_token(test_client):
    # Register a user
    response = test_client.post("/api/v1/register", json=test_user)
    assert response.status_code == 201
    
    # Login to get token
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    return token_data["access_token"]

@pytest.fixture(scope="module")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

# Authentication Tests
def test_register_user(test_client):
    response = test_client.post("/api/v1/register", json=test_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]
    assert "id" in data
    assert "is_active" in data

def test_login_user(test_client):
    response = test_client.post(
        "/api/v1/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_invalid_login(test_client):
    response = test_client.post(
        "/api/v1/login",
        data={
            "username": "wrong@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

# Customer Tests
def test_create_customer(test_client, auth_headers):
    response = test_client.post("/api/v1/customers/", json=test_customer, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_customer["name"]
    assert data["email"] == test_customer["email"]
    assert "id" in data
    return data["id"]  # Return customer ID for other tests

def test_get_customers(test_client, auth_headers):
    response = test_client.get("/api/v1/customers/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_customer_by_id(test_client, auth_headers):
    # First create a customer
    customer_id = test_create_customer(test_client, auth_headers)
    
    # Then retrieve it
    response = test_client.get(f"/api/v1/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == customer_id
    assert data["name"] == test_customer["name"]

def test_update_customer(test_client, auth_headers):
    # First create a customer
    customer_id = test_create_customer(test_client, auth_headers)
    
    # Update the customer
    updated_customer = {
        "name": "Updated Customer",
        "email": "updated@example.com",
        "phone": "1111111111",
        "address": "456 Updated Street"
    }
    
    response = test_client.put(f"/api/v1/customers/{customer_id}", json=updated_customer, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_customer["name"]
    assert data["email"] == updated_customer["email"]

def test_delete_customer(test_client, auth_headers):
    # First create a customer
    customer_id = test_create_customer(test_client, auth_headers)
    
    # Delete the customer
    response = test_client.delete(f"/api/v1/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 204

# Contact Tests
def test_create_contact(test_client, auth_headers):
    # First create a customer
    customer_id = test_create_customer(test_client, auth_headers)
    
    # Create a contact
    contact_data = test_contact.copy()
    contact_data["customer_id"] = customer_id
    
    response = test_client.post("/api/v1/contacts/", json=contact_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_contact["name"]
    assert data["email"] == test_contact["email"]
    assert "id" in data

def test_get_contacts(test_client, auth_headers):
    response = test_client.get("/api/v1/contacts/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Lead Tests
def test_create_lead(test_client, auth_headers):
    # First create a customer
    customer_id = test_create_customer(test_client, auth_headers)
    
    # Create a lead
    lead_data = test_lead.copy()
    lead_data["customer_id"] = customer_id
    
    response = test_client.post("/api/v1/leads/", json=lead_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_lead["name"]
    assert data["status"] == test_lead["status"]
    assert "id" in data

def test_get_leads(test_client, auth_headers):
    response = test_client.get("/api/v1/leads/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Opportunity Tests
def test_create_opportunity(test_client, auth_headers):
    # First create a customer
    customer_id = test_create_customer(test_client, auth_headers)
    
    # Create an opportunity
    opportunity_data = test_opportunity.copy()
    opportunity_data["customer_id"] = customer_id
    
    response = test_client.post("/api/v1/opportunities/", json=opportunity_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_opportunity["name"]
    assert data["value"] == test_opportunity["value"]
    assert "id" in data

def test_get_opportunities(test_client, auth_headers):
    response = test_client.get("/api/v1/opportunities/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Billing Tests
def test_create_invoice(test_client, auth_headers):
    # First create a customer
    customer_id = test_create_customer(test_client, auth_headers)
    
    # Create an invoice
    invoice_data = test_invoice.copy()
    invoice_data["customer_id"] = customer_id
    invoice_data["due_date"] = datetime.now(timezone.utc).isoformat()
    
    response = test_client.post("/api/v1/billing/invoices/", json=invoice_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == test_invoice["amount"]
    assert data["status"] == test_invoice["status"]
    assert "id" in data

def test_get_invoices(test_client, auth_headers):
    response = test_client.get("/api/v1/billing/invoices/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_payment(test_client, auth_headers):
    # First create a customer
    customer_id = test_create_customer(test_client, auth_headers)
    
    # Create an invoice
    invoice_data = test_invoice.copy()
    invoice_data["customer_id"] = customer_id
    invoice_data["due_date"] = datetime.now(timezone.utc).isoformat()
    
    invoice_response = test_client.post("/api/v1/billing/invoices/", json=invoice_data, headers=auth_headers)
    assert invoice_response.status_code == 201
    invoice_id = invoice_response.json()["id"]
    
    # Create a payment
    payment_data = test_payment.copy()
    payment_data["invoice_id"] = invoice_id
    
    response = test_client.post("/api/v1/billing/payments/", json=payment_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == test_payment["amount"]
    assert data["status"] == test_payment["status"]
    assert "id" in data

def test_get_payments(test_client, auth_headers):
    response = test_client.get("/api/v1/billing/payments/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_subscription(test_client, auth_headers):
    # First create a customer
    customer_id = test_create_customer(test_client, auth_headers)
    
    # Create a subscription
    subscription_data = test_subscription.copy()
    subscription_data["customer_id"] = customer_id
    subscription_data["end_date"] = datetime.now(timezone.utc).isoformat()
    
    response = test_client.post("/api/v1/billing/subscriptions/", json=subscription_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["plan_name"] == test_subscription["plan_name"]
    assert data["status"] == test_subscription["status"]
    assert "id" in data

def test_get_subscriptions(test_client, auth_headers):
    response = test_client.get("/api/v1/billing/subscriptions/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Chatbot Tests
def test_create_chat_session(test_client, auth_headers):
    response = test_client.post("/api/v1/chatbot/sessions/", json={}, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_send_chat_message(test_client, auth_headers):
    # First create a chat session
    session_response = test_client.post("/api/v1/chatbot/sessions/", json={}, headers=auth_headers)
    assert session_response.status_code == 201
    session_id = session_response.json()["id"]
    
    # Send a message
    response = test_client.post(
        f"/api/v1/chatbot/sessions/{session_id}/messages", 
        json=test_chat_message, 
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "suggestions" in data

def test_get_chat_sessions(test_client, auth_headers):
    response = test_client.get("/api/v1/chatbot/sessions/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_chat_session_by_id(test_client, auth_headers):
    # First create a chat session
    session_response = test_client.post("/api/v1/chatbot/sessions/", json={}, headers=auth_headers)
    assert session_response.status_code == 201
    session_id = session_response.json()["id"]
    
    # Retrieve the session
    response = test_client.get(f"/api/v1/chatbot/sessions/{session_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == session_id

def test_delete_chat_session(test_client, auth_headers):
    # First create a chat session
    session_response = test_client.post("/api/v1/chatbot/sessions/", json={}, headers=auth_headers)
    assert session_response.status_code == 201
    session_id = session_response.json()["id"]
    
    # Delete the session
    response = test_client.delete(f"/api/v1/chatbot/sessions/{session_id}", headers=auth_headers)
    assert response.status_code == 204

# Error Handling Tests
def test_unauthorized_access(test_client):
    response = test_client.get("/api/v1/customers/")
    assert response.status_code == 401

def test_not_found(test_client, auth_headers):
    response = test_client.get("/api/v1/customers/99999", headers=auth_headers)
    assert response.status_code == 404

# Health Check Test
def test_health_check(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "CRM MVP is running"
