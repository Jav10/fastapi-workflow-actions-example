from fastapi.testclient import TestClient
from app.main import app, items_db, item_id_counter

client = TestClient(app)


def setup_function():
    """Reinicia la base de datos en memoria antes de cada test."""
    global item_id_counter
    items_db.clear()
    # Resetear el contador accediendo al módulo directamente
    import app.main as main_module
    main_module.item_id_counter = 1


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "¡Hola desde FastAPI + GitHub Actions!"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_items_empty():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item():
    item_data = {
        "name": "Laptop",
        "description": "Una laptop gamer",
        "price": 1500.00,
        "is_offer": True
    }
    response = client.post("/items", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Laptop"
    assert data["price"] == 1500.00


def test_get_item():
    # Crear un item primero
    item_data = {"name": "Mouse", "price": 25.00}
    client.post("/items", json=item_data)
    
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Mouse"


def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item no encontrado"


def test_delete_item():
    # Crear un item primero
    item_data = {"name": "Teclado", "price": 50.00}
    client.post("/items", json=item_data)
    
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Item 1 eliminado"}


def test_delete_item_not_found():
    response = client.delete("/items/999")
    assert response.status_code == 404