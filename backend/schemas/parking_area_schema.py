from typing import Optional, List
from pydantic import BaseModel, field_validator


class PolygonGeometry(BaseModel):
    type: str
    coordinates: List[List[List[float]]]

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str):
        if value != "Polygon":
            raise ValueError("geom.type must be 'Polygon'.")
        return value

    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, value):

        if len(value) == 0:
            raise ValueError("Polygon must contain at least one ring.")

        ring = value[0]

        if len(ring) < 4:
            raise ValueError("Polygon must have at least 4 coordinate pairs.")

        if ring[0] != ring[-1]:
            raise ValueError("Polygon must be closed (first point = last point).")

        for lon, lat in ring:
            if lon < -180 or lon > 180:
                raise ValueError("Longitude must be between -180 and 180.")
            if lat < -90 or lat > 90:
                raise ValueError("Latitude must be between -90 and 90.")

        return value


class ParkingAreaCreate(BaseModel):
    name: str
    capacity: int
    geom: PolygonGeometry

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("name must be non-empty.")
        return value

    @field_validator("capacity")
    @classmethod
    def validate_capacity(cls, value: int):
        if value < 0:
            raise ValueError("capacity must be >= 0.")
        return value


class ParkingAreaUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None
    geom: Optional[PolygonGeometry] = None