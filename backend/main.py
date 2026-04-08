from fastapi import FastAPI
from routes.vehicle_routes import router as vehicle_router

app = FastAPI(title="Car Tracking API", version="1.0.0")

app.include_router(vehicle_router)


@app.get("/")
def root():
    return {"message": "Car Tracking API is running."}