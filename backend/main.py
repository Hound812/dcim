from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import (
    clients,
    contracts,
    rooms,
    racks,
    equipment,
    placement,
    history,
)

app = FastAPI(
    title="DCIM API",
    description="Data Center Infrastructure Management",
    version="1.0.0",
)

STATIC_DIR = "/opt/inventory/backend/static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(f"{STATIC_DIR}/index.html")

@app.get("/equipment/add", include_in_schema=False)
def equipment_add_page():
    return FileResponse(f"{STATIC_DIR}/add_equipment.html")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(clients.router)
app.include_router(contracts.router)
app.include_router(rooms.router)
app.include_router(racks.router)
app.include_router(equipment.router)
app.include_router(placement.router)
app.include_router(history.router)
