from typing import Optional, List
from pydantic import BaseModel, field_validator


class PointGeometry(BaseModel):
    type: str
    coordinates: List[float]

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str):
        if value != "Point":
            raise ValueError("Geometry type must be 'Point'.")
        return value

    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, value: List[float]):
        if len(value) != 2:
            raise ValueError("Point coordinates must have exactly 2 values.")
        lon, lat = value
        if lon < -180 or lon > 180:
            raise ValueError("Longitude must be between -180 and 180.")
        if lat < -90 or lat > 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return value


class TripCreate(BaseModel):
    vehicle_id: int
    start_ts: str
    end_ts: str
    start_geom: PointGeometry
    end_geom: PointGeometry
    distance_km: float

    @field_validator("distance_km")
    @classmethod
    def validate_distance(cls, value):
        if value < 0:
            raise ValueError("distance_km must be >= 0.")
        return value


class TripUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    start_ts: Optional[str] = None
    end_ts: Optional[str] = None
    start_geom: Optional[PointGeometry] = None
    end_geom: Optional[PointGeometry] = None
    distance_km: Optional[float] = None

    @field_validator("distance_km")
    @classmethod
    def validate_distance(cls, value):
        if value is None:
            return value
        if value < 0:
            raise ValueError("distance_km must be >= 0.")
        return value