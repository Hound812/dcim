from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routers import (
    clients,
    contracts,
    rooms,
    racks,
    equipment,
    placement,
    history
)

app = FastAPI(
    title="DCIM API",
    description="Data Center Infrastructure Management",
    version="1.0.0"
)

# Подключаем папку со статическими файлами
app.mount("/static", StaticFiles(directory="/opt/inventory/backend/static"), name="static")


# Главная страница
@app.get("/", include_in_schema=False)
def root():
    return FileResponse("/opt/inventory/backend/static/index.html")


# Проверка работоспособности API
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Подключение роутеров
app.include_router(clients.router)
app.include_router(contracts.router)
app.include_router(rooms.router)
app.include_router(racks.router)
app.include_router(equipment.router)
app.include_router(placement.router)
app.include_router(history.router)
