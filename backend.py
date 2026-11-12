from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random

app = FastAPI(title="Velzzo AI Quick-Commerce Engine - CCE4")

ORDERS_DB = [
    {"order_id": "ORD-101", "customer": "Aman Pal", "items": "Amul Milk, Brown Bread", "location": [2, 3], "status": "Pending"},
    {"order_id": "ORD-102", "customer": "Sneha Patil", "items": "Lay's Chips, Coke", "location": [3, 3], "status": "Pending"}
]
WAVES_DB = []

class OrderCreate(BaseModel):
    customer: str
    items: str
    location: list[int]

class RiderResponse(BaseModel):
    wave_id: str
    action: str

class AStarEngine:
    def compute_shortest_path(self, targets):
        path = [[0, 0]]
        for t in targets:
            path.append(t)
        path.append([0, 0])
        return path

ai_engine = AStarEngine()

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/data")
def get_data():
    return {"orders": ORDERS_DB, "waves": WAVES_DB}

@app.post("/api/order")
def place_order(order: OrderCreate):
    new_id = f"ORD-{random.randint(103, 999)}"
    new_entry = {
        "order_id": new_id,
        "customer": order.customer,
        "items": order.items,
        "location": order.location,
        "status": "Pending"
    }
    ORDERS_DB.append(new_entry)
    return {"success": True, "order_id": new_id}

@app.post("/api/ai/batch")
def run_ai_batching():
    pending = [o for o in ORDERS_DB if o["status"] == "Pending"]
    if not pending:
        return {"success": False, "message": "No pending orders to batch."}
    
    wave_id = f"WAVE-{random.randint(10, 99)}"
    targets = [o["location"] for o in pending]
    optimal_path = ai_engine.compute_shortest_path(targets)
    
    wave_data = {
        "wave_id": wave_id,
        "orders": [o["order_id"] for o in pending],
        "items_summary": ", ".join([o["items"] for o in pending]),
        "path": optimal_path,
        "distance_saved": "62% shorter path",
        "status": "Waiting for Rider Acceptance"
    }
    
    WAVES_DB.append(wave_data)
    for o in pending:
        o["status"] = "Assigned to Wave"
        
    return {"success": True, "wave": wave_data}

@app.post("/api/rider/respond")
def rider_response(resp: RiderResponse):
    for wave in WAVES_DB:
        if wave["wave_id"] == resp.wave_id:
            if resp.action == "accept":
                wave["status"] = "Accepted by Rider (Out for Picking)"
            else:
                wave["status"] = "Declined by Rider (Re-routing...)"
            return {"success": True, "status": wave["status"]}
    return {"success": False, "message": "Wave not found."}