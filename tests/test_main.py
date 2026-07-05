import sys
import os
# Add the parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to Python Backend API"
    assert "/docs" in data["docs"]

def test_create_item():
    """Test creating an item"""
    response = client.post(
        "/items/",
        json={
            "name": "Test Item",
            "price": 99.99,
            "description": "This is a test item"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 99.99
    assert "id" in data

def test_get_items():
    """Test getting all items"""
    # First create an item
    client.post("/items/", json={"name": "Item 1", "price": 10.0})
    
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_single_item():
    """Test getting a single item"""
    # Create item
    create_response = client.post(
        "/items/",
        json={"name": "Single Item", "price": 5.0}
    )
    item_id = create_response.json()["id"]
    
    # Get it
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Single Item"

def test_update_item():
    """Test updating an item"""
    # Create item
    create_response = client.post(
        "/items/",
        json={"name": "Old Name", "price": 10.0}
    )
    item_id = create_response.json()["id"]
    
    # Update it
    response = client.put(
        f"/items/{item_id}",
        json={"name": "New Name", "price": 20.0, "description": "Updated"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["price"] == 20.0

def test_delete_item():
    """Test deleting an item"""
    # Create item
    create_response = client.post(
        "/items/",
        json={"name": "To Delete", "price": 1.0}
    )
    item_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    
    # Try to get it (should fail)
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404