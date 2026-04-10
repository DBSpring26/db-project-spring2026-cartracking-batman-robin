from fastapi import HTTPException
from dao.location_ping_dao import LocationPingDAO
from dao.vehicle_dao import VehicleDAO
from utils.pagination import validate_limit_offset


class LocationPingHandler:
    def __init__(self, conn):
        self.dao = LocationPingDAO(conn)
        self.vehicle_dao = VehicleDAO(conn)

    def create_location_ping(self, data: dict):
        if not self.dao.vehicle_exists(data["vehicle_id"]):
            raise HTTPException(status_code=404, detail="vehicle_id does not exist.")
        return self.dao.create_location_ping(data)

    def get_location_pings(self, limit: int, offset: int, vehicle_id=None, from_ts=None, to_ts=None):
        try:
            validate_limit_offset(limit, offset)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return self.dao.get_location_pings(limit, offset, vehicle_id, from_ts, to_ts)

    def get_location_ping_by_id(self, ping_id: int):
        if ping_id <= 0:
            raise HTTPException(status_code=400, detail="ping_id must be a positive integer.")

        row = self.dao.get_location_ping_by_id(ping_id)
        if not row:
            raise HTTPException(status_code=404, detail="ping_id does not exist.")
        return row

    def update_location_ping(self, ping_id: int, data: dict):
        if ping_id <= 0:
            raise HTTPException(status_code=400, detail="ping_id must be a positive integer.")

        existing = self.dao.get_location_ping_by_id(ping_id)
        if not existing:
            raise HTTPException(status_code=404, detail="ping_id does not exist.")

        if not data:
            raise HTTPException(status_code=400, detail="At least one updatable field must be present.")

        if "vehicle_id" in data and not self.dao.vehicle_exists(data["vehicle_id"]):
            raise HTTPException(status_code=404, detail="vehicle_id does not exist.")

        return self.dao.update_location_ping(ping_id, data)

    def delete_location_ping(self, ping_id: int):
        if ping_id <= 0:
            raise HTTPException(status_code=400, detail="ping_id must be a positive integer.")

        existing = self.dao.get_location_ping_by_id(ping_id)
        if not existing:
            raise HTTPException(status_code=404, detail="ping_id does not exist.")

        deleted = self.dao.delete_location_ping(ping_id)
        return {
            "message": "Location ping deleted successfully.",
            "ping_id": deleted["ping_id"]
        }

    def get_vehicle_pings(self, vehicle_id: int, limit: int, offset: int, from_ts=None, to_ts=None):
        if vehicle_id <= 0:
            raise HTTPException(status_code=400, detail="vehicle_id must be a positive integer.")

        vehicle = self.vehicle_dao.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="vehicle_id does not exist.")

        try:
            validate_limit_offset(limit, offset)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return self.dao.get_vehicle_pings(vehicle_id, limit, offset, from_ts, to_ts)