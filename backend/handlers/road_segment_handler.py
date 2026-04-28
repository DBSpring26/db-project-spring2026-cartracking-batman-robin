from fastapi import HTTPException
from dao.road_segment_dao import RoadSegmentDAO
from utils.pagination import validate_limit_offset
from utils.bbox import parse_bbox


class RoadSegmentHandler:
    def __init__(self, conn):
        self.dao = RoadSegmentDAO(conn)

    def create_road_segment(self, data: dict):
        return self.dao.create_road_segment(data)

    def get_road_segments(
        self,
        limit: int,
        offset: int,
        is_oneway=None,
        direction=None,
        name=None,
        speed_limit_kph=None,
        bbox=None
    ):
        try:
            validate_limit_offset(limit, offset)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        bbox_values = None

        if bbox:
            try:
                bbox_values = parse_bbox(bbox)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

        return self.dao.get_road_segments(
            limit,
            offset,
            is_oneway,
            direction,
            name,
            speed_limit_kph,
            bbox_values
        )

    def get_road_segment_by_id(self, road_id: int):
        if road_id <= 0:
            raise HTTPException(status_code=400, detail="road_id must be a positive integer.")

        row = self.dao.get_road_segment_by_id(road_id)

        if not row:
            raise HTTPException(status_code=404, detail="road_id does not exist.")

        return row

    def update_road_segment(self, road_id: int, data: dict):
        if road_id <= 0:
            raise HTTPException(status_code=400, detail="road_id must be a positive integer.")

        existing = self.dao.get_road_segment_by_id(road_id)

        if not existing:
            raise HTTPException(status_code=404, detail="road_id does not exist.")

        if not data:
            raise HTTPException(status_code=400, detail="At least one updatable field must be present.")

        return self.dao.update_road_segment(road_id, data)

    def delete_road_segment(self, road_id: int):
        if road_id <= 0:
            raise HTTPException(status_code=400, detail="road_id must be a positive integer.")

        existing = self.dao.get_road_segment_by_id(road_id)

        if not existing:
            raise HTTPException(status_code=404, detail="road_id does not exist.")

        deleted = self.dao.delete_road_segment(road_id)

        return {
            "message": "Road segment deleted successfully.",
            "road_id": deleted["road_id"]
        }