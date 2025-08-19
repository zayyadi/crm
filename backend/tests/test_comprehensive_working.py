import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

def test_health_check():
    """Test that the API is running and responding"""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "CRM MVP is running"

def test_invalid_endpoint():
    """Test that invalid endpoints return 404"""
    with TestClient(app) as client:
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404

def test_user_registration():
    """Test user registration endpoint"""
    with TestClient(app) as client:
        # Generate unique email for testing
        unique_email = f"test_{uuid.uuid4()}@example.com"
        user_data = {
            "email": unique_email,
            "password": "testpassword123",
            "full_name": "Test User"
        }
        
        response = client.post("/api/v1/register", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data
        assert "is_active" in data
        assert data["is_active"] == True

def test_user_login():
    """Test user login endpoint"""
    with TestClient(app) as client:
        # First register a user
        unique_email = f"login_test_{uuid.uuid4()}@example.com"
        user_data = {
            "email": unique_email,
            "password": "testpassword123",
            "full_name": "Login Test User"
        }
        
        # Register the user
        register_response = client.post("/api/v1/register", json=user_data)
        assert register_response.status_code == 201
        
        # Try to login
        login_data = {
            "username": unique_email,
            "password": "testpassword123"
        }
        login_response = client.post("/api/v1/login", data=login_data)
        assert login_response.status_code == 200
        
        login_result = login_response.json()
        assert "access_token" in login_result
        assert "token_type" in login_result
        assert login_result["token_type"] == "Bearer"

def test_failed_login():
    """Test that invalid credentials return proper error"""
    with TestClient(app) as client:
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/login", data=login_data)
        assert response.status_code == 401

def test_protected_endpoint_without_auth():
    """Test that protected endpoints require authentication"""
    with TestClient(app) as client:
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
