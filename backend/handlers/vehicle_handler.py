from fastapi import HTTPException
from dao.vehicle_dao import VehicleDAO
from utils.pagination import validate_limit_offset


class VehicleHandler:
    def __init__(self, conn):
        self.dao = VehicleDAO(conn)

    def create_vehicle(self, data: dict):
        if not self.dao.vehicle_type_exists(data["vehicle_type_id"]):
            raise HTTPException(status_code=404, detail="Referenced vehicle_type_id does not exist.")

        if not self.dao.vehicle_status_exists(data["vehicle_status_id"]):
            raise HTTPException(status_code=404, detail="Referenced vehicle_status_id does not exist.")

        if self.dao.plate_number_exists(data["plate_number"]):
            raise HTTPException(status_code=409, detail="plate_number already exists.")

        return self.dao.create_vehicle(data)

    def get_vehicles(self, limit: int, offset: int, status=None, plate_number=None):
        try:
            validate_limit_offset(limit, offset)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return self.dao.get_vehicles(limit, offset, status, plate_number)

    def get_vehicle_by_id(self, vehicle_id: int):
        if vehicle_id <= 0:
            raise HTTPException(status_code=400, detail="vehicle_id must be a positive integer.")

        row = self.dao.get_vehicle_by_id(vehicle_id)
        if not row:
            raise HTTPException(status_code=404, detail="vehicle_id does not exist.")
        return row

    def update_vehicle(self, vehicle_id: int, data: dict):
        if vehicle_id <= 0:
            raise HTTPException(status_code=400, detail="vehicle_id must be a positive integer.")

        existing = self.dao.get_vehicle_by_id(vehicle_id)
        if not existing:
            raise HTTPException(status_code=404, detail="vehicle_id does not exist.")

        if not data:
            raise HTTPException(status_code=400, detail="At least one updatable field must be supplied.")

        if "vehicle_type_id" in data and not self.dao.vehicle_type_exists(data["vehicle_type_id"]):
            raise HTTPException(status_code=404, detail="Referenced vehicle_type_id does not exist.")

        if "vehicle_status_id" in data and not self.dao.vehicle_status_exists(data["vehicle_status_id"]):
            raise HTTPException(status_code=404, detail="Referenced vehicle_status_id does not exist.")

        if "plate_number" in data and self.dao.plate_number_exists(data["plate_number"], exclude_vehicle_id=vehicle_id):
            raise HTTPException(status_code=409, detail="Updated plate_number conflicts with another vehicle.")

        return self.dao.update_vehicle(vehicle_id, data)

    def delete_vehicle(self, vehicle_id: int):
        if vehicle_id <= 0:
            raise HTTPException(status_code=400, detail="vehicle_id must be a positive integer.")

        existing = self.dao.get_vehicle_by_id(vehicle_id)
        if not existing:
            raise HTTPException(status_code=404, detail="vehicle_id does not exist.")

        deleted = self.dao.delete_vehicle(vehicle_id)
        if not deleted:
            raise HTTPException(status_code=409, detail="Vehicle deletion failed.")

        return {
            "message": "Vehicle deleted successfully.",
            "vehicle_id": deleted["vehicle_id"]
        }

    def get_current_location(self, vehicle_id: int):
        if vehicle_id <= 0:
            raise HTTPException(status_code=400, detail="vehicle_id must be a positive integer.")

        existing = self.dao.get_vehicle_by_id(vehicle_id)
        if not existing:
            raise HTTPException(status_code=404, detail="vehicle_id does not exist.")

        row = self.dao.get_vehicle_current_location(vehicle_id)
        if not row:
            return None
        return row