from fastapi import FastAPI
from routes.vehicle_routes import router as vehicle_router
from routes.location_ping_routes import location_ping_router, vehicle_ping_router

app = FastAPI(title="Car Tracking API", version="1.0.0")

app.include_router(vehicle_router)
app.include_router(location_ping_router)
app.include_router(vehicle_ping_router)


@app.get("/")
def root():
    return {"message": "Car Tracking API is running."}