from fastapi import HTTPException
from dao.parking_area_dao import ParkingAreaDAO
from utils.pagination import validate_limit_offset
from utils.bbox import parse_bbox


class ParkingAreaHandler:

    def __init__(self, conn):

        self.dao = ParkingAreaDAO(conn)


    def create_parking_area(self, data):

        return self.dao.create_parking_area(data)


    def get_parking_areas(self, limit, offset, bbox=None):

        try:
            validate_limit_offset(limit, offset)
        except ValueError as e:
            raise HTTPException(400, str(e))

        bbox_values = None

        if bbox:
            try:
                bbox_values = parse_bbox(bbox)
            except ValueError as e:
                raise HTTPException(400, str(e))

        return self.dao.get_parking_areas(limit, offset, bbox_values)


    def get_parking_area_by_id(self, parking_area_id):

        if parking_area_id <= 0:

            raise HTTPException(400, "parking_area_id must be positive")
        row = self.dao.get_parking_area_by_id(parking_area_id)

        if not row:

            raise HTTPException(404, "parking_area_id does not exist")

        return row


    def update_parking_area(self, parking_area_id, data):

        existing = self.dao.get_parking_area_by_id(parking_area_id)

        if not existing:

            raise HTTPException(404, "parking_area_id does not exist")

        return self.dao.update_parking_area(parking_area_id, data)


    def delete_parking_area(self, parking_area_id):

        existing = self.dao.get_parking_area_by_id(parking_area_id)

        if not existing:

            raise HTTPException(404, "parking_area_id does not exist")

        return {
            "message": "Parking area deleted successfully",
            "parking_area_id": self.dao.delete_parking_area(parking_area_id)["parking_area_id"]
        }