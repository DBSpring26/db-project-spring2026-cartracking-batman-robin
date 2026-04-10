from fastapi import HTTPException
from dao.trip_dao import TripDAO
from dao.vehicle_dao import VehicleDAO
from utils.pagination import validate_limit_offset


class TripHandler:
    def __init__(self, conn):
        self.dao = TripDAO(conn)
        self.vehicle_dao = VehicleDAO(conn)

    def create_trip(self, data: dict):
        if not self.dao.vehicle_exists(data["vehicle_id"]):
            raise HTTPException(status_code=404, detail="vehicle_id does not exist.")
        return self.dao.create_trip(data)

    def get_trips(self, limit: int, offset: int, vehicle_id=None, start_date=None, end_date=None):
        try:
            validate_limit_offset(limit, offset)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return self.dao.get_trips(limit, offset, vehicle_id, start_date, end_date)

    def get_trip_by_id(self, trip_id: int):
        if trip_id <= 0:
            raise HTTPException(status_code=400, detail="trip_id must be a positive integer.")

        row = self.dao.get_trip_by_id(trip_id)
        if not row:
            raise HTTPException(status_code=404, detail="trip_id does not exist.")
        return row

    def update_trip(self, trip_id: int, data: dict):
        if trip_id <= 0:
            raise HTTPException(status_code=400, detail="trip_id must be a positive integer.")

        existing = self.dao.get_trip_by_id(trip_id)
        if not existing:
            raise HTTPException(status_code=404, detail="trip_id does not exist.")

        if not data:
            raise HTTPException(status_code=400, detail="At least one updatable field must be present.")

        if "vehicle_id" in data and not self.dao.vehicle_exists(data["vehicle_id"]):
            raise HTTPException(status_code=404, detail="vehicle_id does not exist.")

        return self.dao.update_trip(trip_id, data)

    def delete_trip(self, trip_id: int):
        if trip_id <= 0:
            raise HTTPException(status_code=400, detail="trip_id must be a positive integer.")

        existing = self.dao.get_trip_by_id(trip_id)
        if not existing:
            raise HTTPException(status_code=404, detail="trip_id does not exist.")

        deleted = self.dao.delete_trip(trip_id)
        return {
            "message": "Trip deleted successfully.",
            "trip_id": deleted["trip_id"]
        }

    def get_vehicle_trips(self, vehicle_id: int, limit: int, offset: int, start_date=None, end_date=None):
        if vehicle_id <= 0:
            raise HTTPException(status_code=400, detail="vehicle_id must be a positive integer.")

        vehicle = self.vehicle_dao.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="vehicle_id does not exist.")

        try:
            validate_limit_offset(limit, offset)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return self.dao.get_vehicle_trips(vehicle_id, limit, offset, start_date, end_date)