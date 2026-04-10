from typing import Optional
from fastapi import APIRouter, Depends, Query
from db.db import get_connection
from handlers.trip_handler import TripHandler
from schemas.trip_schema import TripCreate, TripUpdate

trip_router = APIRouter(prefix="/api/v1/trips", tags=["trips"])
vehicle_trip_router = APIRouter(prefix="/api/v1/vehicles", tags=["vehicle-trips"])


def get_handler():
    conn = get_connection()
    try:
        yield TripHandler(conn)
    finally:
        conn.close()


@trip_router.post("", status_code=201)
def create_trip(payload: TripCreate, handler: TripHandler = Depends(get_handler)):
    return handler.create_trip(payload.model_dump())


@trip_router.get("")
def get_trips(
    limit: int = Query(100, ge=0),
    offset: int = Query(0, ge=0),
    vehicle_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    handler: TripHandler = Depends(get_handler)
):
    return handler.get_trips(limit, offset, vehicle_id, start_date, end_date)


@trip_router.get("/{trip_id}")
def get_trip_by_id(trip_id: int, handler: TripHandler = Depends(get_handler)):
    return handler.get_trip_by_id(trip_id)


@trip_router.put("/{trip_id}")
def update_trip(
    trip_id: int,
    payload: TripUpdate,
    handler: TripHandler = Depends(get_handler)
):
    data = payload.model_dump(exclude_unset=True)
    return handler.update_trip(trip_id, data)


@trip_router.delete("/{trip_id}")
def delete_trip(trip_id: int, handler: TripHandler = Depends(get_handler)):
    return handler.delete_trip(trip_id)


@vehicle_trip_router.get("/{vehicle_id}/trips")
def get_vehicle_trips(
    vehicle_id: int,
    limit: int = Query(100, ge=0),
    offset: int = Query(0, ge=0),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    handler: TripHandler = Depends(get_handler)
):
    return handler.get_vehicle_trips(vehicle_id, limit, offset, start_date, end_date)