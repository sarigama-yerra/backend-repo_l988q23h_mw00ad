import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import MenuItem, Order

app = FastAPI(title="RTU Kota Canteen API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "RTU Kota Canteen API is running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


# ----- Menu Endpoints -----

@app.post("/api/menu", response_model=dict)
def add_menu_item(item: MenuItem):
    try:
        item_id = create_document("menuitem", item)
        return {"id": item_id, "message": "Menu item added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/menu", response_model=List[dict])
def list_menu(category: Optional[str] = None):
    try:
        filter_q = {"category": category} if category else {}
        items = get_documents("menuitem", filter_q)
        # Convert ObjectId to str
        for it in items:
            it["id"] = str(it.pop("_id"))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----- Order Endpoints -----

@app.post("/api/orders", response_model=dict)
def create_order(order: Order):
    try:
        order_id = create_document("order", order)
        return {"id": order_id, "message": "Order placed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/orders", response_model=List[dict])
def get_orders(phone: Optional[str] = None):
    try:
        filter_q = {"phone": phone} if phone else {}
        orders = get_documents("order", filter_q)
        for od in orders:
            od["id"] = str(od.pop("_id"))
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/hello")
def hello():
    return {"message": "Hello from RTU canteen backend!"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
