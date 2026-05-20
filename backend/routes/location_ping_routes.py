from typing import Optional
from fastapi import APIRouter, Depends, Query
from db.db import get_connection
from handlers.location_ping_handler import LocationPingHandler
from schemas.location_ping_schema import LocationPingCreate, LocationPingUpdate

location_ping_router = APIRouter(
    prefix="/api/v1/location-pings",
    tags=["location-pings"]
)

vehicle_ping_router = APIRouter(
    prefix="/api/v1/vehicles",
    tags=["vehicle-pings"]
)


def get_handler():
    conn = get_connection()
    try:
        yield LocationPingHandler(conn)
    finally:
        conn.close()



@location_ping_router.post("", status_code=201)
def create_location_ping(
    payload: LocationPingCreate,
    handler: LocationPingHandler = Depends(get_handler)
):
    return handler.create_location_ping(payload.model_dump())


@location_ping_router.get("")
def get_location_pings(
    limit: int = Query(100, ge=0),
    offset: int = Query(0, ge=0),
    vehicle_id: Optional[int] = None,
    from_ts: Optional[str] = None,
    to_ts: Optional[str] = None,
    bbox: Optional[str] = Query(None),
    handler: LocationPingHandler = Depends(get_handler)
):
    return handler.get_location_pings(
        limit,
        offset,
        vehicle_id,
        from_ts,
        to_ts,
        bbox
    )


@location_ping_router.get("/latest")
def get_latest_vehicle_pings(
    limit: int = Query(100, ge=0),
    offset: int = Query(0, ge=0),
    bbox: Optional[str] = Query(None),
    handler: LocationPingHandler = Depends(get_handler)
):
    return handler.get_latest_vehicle_pings(limit, offset, bbox)


@location_ping_router.get("/breadcrumb")
def get_breadcrumb(
    vehicle_id: int,
    start_ts: str,
    end_ts: str,
    handler: LocationPingHandler = Depends(get_handler)
):
    return handler.get_breadcrumb(vehicle_id, start_ts, end_ts)


@location_ping_router.get("/pings-per-day")
def get_pings_per_day(
    handler: LocationPingHandler = Depends(get_handler)
):
    return handler.get_pings_per_day()


@location_ping_router.get("/{ping_id}")
def get_location_ping_by_id(
    ping_id: int,
    handler: LocationPingHandler = Depends(get_handler)
):
    return handler.get_location_ping_by_id(ping_id)


@location_ping_router.put("/{ping_id}")
def update_location_ping(
    ping_id: int,
    payload: LocationPingUpdate,
    handler: LocationPingHandler = Depends(get_handler)
):
    data = payload.model_dump(exclude_unset=True)
    return handler.update_location_ping(ping_id, data)


@location_ping_router.delete("/{ping_id}")
def delete_location_ping(
    ping_id: int,
    handler: LocationPingHandler = Depends(get_handler)
):
    return handler.delete_location_ping(ping_id)



@vehicle_ping_router.get("/{vehicle_id}/pings")
def get_vehicle_pings(
    vehicle_id: int,
    limit: int = Query(100, ge=0),
    offset: int = Query(0, ge=0),
    from_ts: Optional[str] = None,
    to_ts: Optional[str] = None,
    bbox: Optional[str] = Query(None),
    handler: LocationPingHandler = Depends(get_handler)
):
    return handler.get_vehicle_pings(
        vehicle_id,
        limit,
        offset,
        from_ts,
        to_ts,
        bbox
    )