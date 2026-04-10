from typing import Optional
from fastapi import APIRouter, Depends, Query, Response
from db.db import get_connection
from handlers.vehicle_handler import VehicleHandler
from schemas.vehicle_schema import VehicleCreate, VehicleUpdate

router = APIRouter(prefix="/api/v1/vehicles", tags=["vehicles"])


def get_handler():
    conn = get_connection()
    try:
        yield VehicleHandler(conn)
    finally:
        conn.close()


@router.post("", status_code=201)
def create_vehicle(payload: VehicleCreate, handler: VehicleHandler = Depends(get_handler)):
    return handler.create_vehicle(payload.model_dump())


@router.get("")
def get_vehicles(
    limit: int = Query(20, ge=0),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None,
    plate_number: Optional[str] = None,
    handler: VehicleHandler = Depends(get_handler)
):
    return handler.get_vehicles(limit, offset, status, plate_number)


@router.get("/{vehicle_id}")
def get_vehicle_by_id(vehicle_id: int, handler: VehicleHandler = Depends(get_handler)):
    return handler.get_vehicle_by_id(vehicle_id)


@router.put("/{vehicle_id}")
def update_vehicle(
    vehicle_id: int,
    payload: VehicleUpdate,
    handler: VehicleHandler = Depends(get_handler)
):
    data = payload.model_dump(exclude_unset=True)
    return handler.update_vehicle(vehicle_id, data)


@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, handler: VehicleHandler = Depends(get_handler)):
    return handler.delete_vehicle(vehicle_id)


@router.get("/{vehicle_id}/current-location")
def get_current_location(
    vehicle_id: int,
    response: Response,
    handler: VehicleHandler = Depends(get_handler)
):
    result = handler.get_current_location(vehicle_id)
    if result is None:
        response.status_code = 204
        return
    return result