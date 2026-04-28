from fastapi import HTTPException
from dao.parking_area_dao import ParkingAreaDAO
from utils.pagination import validate_limit_offset
from utils.bbox import parse_bbox


class ParkingAreaHandler:

    def __init__(self, conn):
        self.dao = ParkingAreaDAO(conn)

    def create_parking_area(self, data):
        return self.dao.create_parking_area(data)

    def get_parking_areas(self, limit, offset, name=None, capacity=None, bbox=None):
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

        return self.dao.get_parking_areas(
            limit,
            offset,
            name,
            capacity,
            bbox_values
        )

    def get_parking_area_by_id(self, parking_area_id):
        if parking_area_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="parking_area_id must be positive"
            )

        row = self.dao.get_parking_area_by_id(parking_area_id)

        if not row:
            raise HTTPException(
                status_code=404,
                detail="parking_area_id does not exist"
            )

        return row

    def update_parking_area(self, parking_area_id, data):
        if parking_area_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="parking_area_id must be positive"
            )

        existing = self.dao.get_parking_area_by_id(parking_area_id)

        if not existing:
            raise HTTPException(
                status_code=404,
                detail="parking_area_id does not exist"
            )

        if not data:
            raise HTTPException(
                status_code=400,
                detail="At least one updatable field must be present."
            )

        return self.dao.update_parking_area(parking_area_id, data)

    def delete_parking_area(self, parking_area_id):
        if parking_area_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="parking_area_id must be positive"
            )

        existing = self.dao.get_parking_area_by_id(parking_area_id)

        if not existing:
            raise HTTPException(
                status_code=404,
                detail="parking_area_id does not exist"
            )

        deleted = self.dao.delete_parking_area(parking_area_id)

        return {
            "message": "Parking area deleted successfully",
            "parking_area_id": deleted["parking_area_id"]
        }