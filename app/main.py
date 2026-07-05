from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="Python Backend API",
    description="A simple backend server with Docker",
    version="1.0.0"
)

# Request/Response models
class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    environment: str

# In-memory database (just for demo)
items_db = {}

# Health check endpoint (important for Docker health checks)
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Docker"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
        environment=os.getenv("ENVIRONMENT", "development")
    )

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Python Backend API",
        "docs": "/docs",
        "health": "/health"
    }

# CRUD endpoints
@app.post("/items/")
async def create_item(item: Item):
    """Create a new item"""
    item_id = len(items_db) + 1
    items_db[item_id] = item.model_dump()  # Changed from .dict()
    return {"id": item_id, **item.model_dump()}  # Changed from .dict()

@app.get("/items/")
async def get_items():
    """Get all items"""
    return items_db

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """Get a specific item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items_db[item_id]}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """Update an item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item.model_dump()  # Changed from .dict()
    return {"id": item_id, **item.model_dump()}  # Changed from .dict()

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )