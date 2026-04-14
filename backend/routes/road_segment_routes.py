from typing import Optional
from fastapi import APIRouter, Depends, Query
from db.db import get_connection
from handlers.road_segment_handler import RoadSegmentHandler
from schemas.road_segment_schema import RoadSegmentCreate, RoadSegmentUpdate

road_segment_router = APIRouter(prefix="/api/v1/road-segments", tags=["road-segments"])


def get_handler():
    conn = get_connection()
    try:
        yield RoadSegmentHandler(conn)
    finally:
        conn.close()


@road_segment_router.post("", status_code=201)
def create_road_segment(payload: RoadSegmentCreate, handler: RoadSegmentHandler = Depends(get_handler)):
    return handler.create_road_segment(payload.model_dump())


@road_segment_router.get("")
def get_road_segments(
    limit: int = Query(100, ge=0),
    offset: int = Query(0, ge=0),
    is_oneway: Optional[bool] = None,
    direction: Optional[str] = None,
    bbox: Optional[str] = Query(None),
    handler: RoadSegmentHandler = Depends(get_handler)
):
    return handler.get_road_segments(limit, offset, is_oneway, direction, bbox)


@road_segment_router.get("/{road_id}")
def get_road_segment_by_id(road_id: int, handler: RoadSegmentHandler = Depends(get_handler)):
    return handler.get_road_segment_by_id(road_id)


@road_segment_router.put("/{road_id}")
def update_road_segment(
    road_id: int,
    payload: RoadSegmentUpdate,
    handler: RoadSegmentHandler = Depends(get_handler)
):
    data = payload.model_dump(exclude_unset=True)
    return handler.update_road_segment(road_id, data)


@road_segment_router.delete("/{road_id}")
def delete_road_segment(road_id: int, handler: RoadSegmentHandler = Depends(get_handler)):
    return handler.delete_road_segment(road_id)