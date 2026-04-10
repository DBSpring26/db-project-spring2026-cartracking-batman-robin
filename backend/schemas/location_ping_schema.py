from typing import Optional, List
from pydantic import BaseModel, field_validator


class PointGeometry(BaseModel):
    type: str
    coordinates: List[float]

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str):
        if value != "Point":
            raise ValueError("geom.type must be 'Point'.")
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


class LocationPingCreate(BaseModel):
    vehicle_id: int
    ts: str
    geom: PointGeometry
    speed_kph: Optional[float] = None
    heading_deg: Optional[float] = None

    @field_validator("speed_kph")
    @classmethod
    def validate_speed(cls, value):
        if value is None:
            return value
        if value < 0:
            raise ValueError("speed_kph must be >= 0.")
        return value

    @field_validator("heading_deg")
    @classmethod
    def validate_heading(cls, value):
        if value is None:
            return value
        if value < 0 or value >= 360:
            raise ValueError("heading_deg must be >= 0 and < 360.")
        return value


class LocationPingUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    ts: Optional[str] = None
    geom: Optional[PointGeometry] = None
    speed_kph: Optional[float] = None
    heading_deg: Optional[float] = None

    @field_validator("speed_kph")
    @classmethod
    def validate_speed(cls, value):
        if value is None:
            return value
        if value < 0:
            raise ValueError("speed_kph must be >= 0.")
        return value

    @field_validator("heading_deg")
    @classmethod
    def validate_heading(cls, value):
        if value is None:
            return value
        if value < 0 or value >= 360:
            raise ValueError("heading_deg must be >= 0 and < 360.")
        return value