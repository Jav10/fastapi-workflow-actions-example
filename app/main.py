from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="FastAPI + GitHub Actions Demo")

# Base de datos en memoria
items_db = []
item_id_counter = 1


class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    is_offer: Optional[bool] = False


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_offer: Optional[bool] = False


@app.get("/")
def read_root():
    return {"message": "¡Hola desde FastAPI + GitHub Actions!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/items", response_model=List[Item])
def get_items():
    return items_db


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item no encontrado")


@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate):
    global item_id_counter
    new_item = {
        "id": item_id_counter,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "is_offer": item.is_offer,
    }
    items_db.append(new_item)
    item_id_counter += 1
    return new_item


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global items_db
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            del items_db[i]
            return {"message": f"Item {item_id} eliminado"}
    raise HTTPException(status_code=404, detail="Item no encontrado")