from fastapi import APIRouter, Depends, Query
from db.db import get_connection
from handlers.parking_area_handler import ParkingAreaHandler
from schemas.parking_area_schema import ParkingAreaCreate, ParkingAreaUpdate


parking_area_router = APIRouter(
    prefix="/api/v1/parking-areas",
    tags=["parking-areas"]
)


def get_handler():

    conn = get_connection()

    try:

        yield ParkingAreaHandler(conn)

    finally:

        conn.close()


@parking_area_router.post("")
def create_parking_area(
    payload: ParkingAreaCreate,
    handler: ParkingAreaHandler = Depends(get_handler)
):

    return handler.create_parking_area(payload.model_dump())


@parking_area_router.get("")
def get_parking_areas(
    limit: int = Query(100),
    offset: int = Query(0),
    handler: ParkingAreaHandler = Depends(get_handler)
):

    return handler.get_parking_areas(limit, offset)


@parking_area_router.get("/{parking_area_id}")
def get_parking_area_by_id(
    parking_area_id: int,
    handler: ParkingAreaHandler = Depends(get_handler)
):

    return handler.get_parking_area_by_id(parking_area_id)


@parking_area_router.put("/{parking_area_id}")
def update_parking_area(
    parking_area_id: int,
    payload: ParkingAreaUpdate,
    handler: ParkingAreaHandler = Depends(get_handler)
):

    return handler.update_parking_area(
        parking_area_id,
        payload.model_dump(exclude_unset=True)
    )


@parking_area_router.delete("/{parking_area_id}")
def delete_parking_area(
    parking_area_id: int,
    handler: ParkingAreaHandler = Depends(get_handler)
):

    return handler.delete_parking_area(parking_area_id)