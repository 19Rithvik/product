from fastapi.testclient import TestClient
import sqlite3
from app.main import app
import random

clint = TestClient(app)

def fetch_id():
    conn = sqlite3.connect("app/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users")
    id = [row[0] for row in cursor.fetchall()]
    conn.close()
    return id


ids = fetch_id()

def test_get_prdt():
    prd = random.choice(ids)
    response = clint.get(f"/product/{prd}")
    assert response.status_code == 200
    assert response.jsom()["id"] == prd

    response = clint.get(f"/product/999")
    assert response.status_code == 404  
    assert response.json()["detail"] == "no data found"

def test_update_prdt():
    prd = random.choice(ids)
    updated_data = {
        "name": "Updated Product",
        "price": 30.0,
        "quantity": 20,
        "description": "Updated description",
        "category": "Updated category"
    }
    response = clint.put(f"/product/{prd}", json= updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]


    response = clint.put(f"/product/999", json= updated_data)
    assert response.status_code == 404  
    assert response.json()["detail"] == "no product found"

def test_delete_prdt():
    prd = random.choice(ids)
    response = clint.delete(f"/product/{prd}")
    assert response.status_code == 200
    assert response.json()["detail"] == "product deleted"

    response = clint.get(f"/product/{prd}")
    assert response.status_code == 404 

    response = clint.delete("/products/999")  
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_list_prdt():
    response = clint.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()["count"] > 0

def test_create_product():
    new_product = {
        "name": "Test Product",
        "price": 10.0,
        "quantity": 5,
        "description": "A test product",
        "category": "Test Category"
    }
    response = clint.post("/products/", json=new_product)
    assert response.status_code == 200 
    assert "id" in response.json()  

    invalid_product = {"price": 10.0}  
    response = clint.post("/products/", json=invalid_product)
    assert response.status_code == 422